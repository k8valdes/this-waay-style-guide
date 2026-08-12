#!/usr/bin/env python3
"""
validate-spec.py — a linter for the This Waay / Gridmark brand spec itself.

Standard library only. Two checks:

  Check A (default) — internal contradiction.
    Finds the same value or rule asserted differently in two places: either
    within one brand's tokens.json, or between that tokens.json and its
    rendered HTML guide. Exits non-zero on a finding. Two passes:
      A1. Same colour NAME (e.g. "green", "mint") mapped to two different
          hex values anywhere in tokens.json, or a mismatch between a named
          colour's hex in tokens.json and the same-named CSS custom property
          in the HTML guide's :root block. Structured, low-noise, high-confidence.
      A2. Two schema blocks whose PATHS share a rare, specific keyword (e.g.
          both paths mention "measure") but whose associated numeric/hex/
          clamp() values disagree. Deliberately conservative — see the
          "known scope limits" note in Part 3 of the Phase 0 report for what
          this pass does and doesn't catch (it will not catch a contradiction
          that exists ONLY in free-text prose with no shared schema keyword,
          e.g. two blocks that use different key names and never repeat a
          keyword in their paths).

  Check B (--check-output) — off-token colour.
    Given a file of generated output (CSS/HTML/SVG/etc.), flags every hex
    colour not present in the target brand's tokens.json.

Always takes --brand, so Product Design Studio is never cross-checked
against Gridmark (or vice versa) by accident.

Usage:
    python3 validate-spec.py --brand product-design-studio
    python3 validate-spec.py --brand gridmark-partners
    python3 validate-spec.py --brand product-design-studio --check-output path/to/generated.css
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

BRANDS = {
    "product-design-studio": {
        "tokens": REPO_ROOT / "product-design-studio" / "tokens.json",
        "html": REPO_ROOT / "product-design-studio" / "index.html",
    },
    "gridmark-partners": {
        "tokens": REPO_ROOT / "gridmark-partners" / "tokens.json",
        "html": REPO_ROOT / "gridmark-partners" / "gridmark-design-system-v3.html",
    },
}

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")
MEASURE_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*(ch|px|em|rem|deg|vw|vh|:1)\b", re.IGNORECASE)
# A whole "~N unit" or "≈N unit" token is an approximation/unit-conversion
# mentioned in prose (e.g. "2.76px (≈0.23em)") — not an authoritative
# declared value. Stripped out (not just lookbehind-guarded) so the regex
# above can't re-match a substring of it starting mid-number.
APPROX_RE = re.compile(r"[~≈]\s*-?\d+(?:\.\d+)?\s*(?:ch|px|em|rem|deg|vw|vh|:1)\b", re.IGNORECASE)
CLAMP_RE = re.compile(r"clamp\([^)]*\)")
CSS_VAR_RE = re.compile(r"--([\w-]+)\s*:\s*([^;]+);")
ROOT_BLOCK_RE = re.compile(r":root\s*\{(.*?)\}", re.DOTALL)

# Words too generic to be a trustworthy signal that two schema blocks are
# "about the same thing" — brand-status vocabulary, narration verbs, and
# structural/English filler that shows up everywhere in this document.
PATH_STOPWORDS = {
    "value", "use", "note", "status", "decided", "guidance", "rule", "meta",
    "production", "proposed", "true", "false", "note2026", "correction2026",
    # generic structural/English/UI-state words that recur as key names or in
    # prose across unrelated concepts — overloaded, not a reliable "same
    # topic" signal on their own.
    "base", "default", "style", "padding", "clearance", "angled", "real",
    "pressed", "hover", "active", "disabled", "primary", "secondary", "focus",
    "height", "anatomy", "accepted", "variant", "variants", "axes",
}
TOP_LEVEL_EXCLUDE = {"meta"}  # narration about the doc itself, not a brand value


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def load_tokens(path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        die(f"tokens file not found: {path}")
    except json.JSONDecodeError as e:
        die(f"{path} is not valid JSON: {e}")


def walk_leaves(obj, path=()):
    """Yield (path_tuple, value) for every scalar leaf in a JSON tree."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_leaves(v, path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_leaves(v, path + (str(i),))
    else:
        yield path, obj


def split_words(s, min_len=4):
    """camelCase/snake/kebab/space/digit-suffix aware tokenizer -> lowercase word list.
    Splits 'greenPunch' -> [green, punch] and 'green500' / 'green-500' both -> [green, 500]."""
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(s))
    s = re.sub(r"([A-Za-z])(\d)", r"\1 \2", s)
    return [w.lower() for w in re.split(r"[^A-Za-z0-9]+", s) if len(w) >= min_len]


CSS_VENDOR_PREFIXES = ("tw-",)


def color_name_words(s):
    """Same tokenizer, but min_len=2 (colour names like 'ink'/'no' are short —
    exactness, not rarity, is what keeps this matcher safe from noise) and
    with any known CSS vendor prefix stripped first."""
    for prefix in CSS_VENDOR_PREFIXES:
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    return split_words(s, min_len=2)


def path_keywords(path):
    return {w for w in split_words(" ".join(path)) if w not in PATH_STOPWORDS}


def extract_signatures(text):
    """hex colours, unit-measurements, and clamp() expressions found in text."""
    text = str(text)
    hexes = {h.lower() for h in HEX_RE.findall(text)}
    clamps = set(CLAMP_RE.findall(text))
    text_no_approx = APPROX_RE.sub(" ", text)
    measures = {(float(n), u.lower()) for n, u in MEASURE_RE.findall(text_no_approx)}
    return hexes, measures, clamps


def block_key(path, depth=2):
    return path[:depth] if len(path) > depth else path


# ---------------------------------------------------------------------------
# Check A1 — colour-name consistency (structured, near-zero noise)
# ---------------------------------------------------------------------------

def check_a1_color_names(tokens, html_text, brand):
    findings = []
    color_block = tokens.get("color", {})

    # A1a: same colour name -> two different hexes, anywhere in tokens.json
    name_to_hexes = {}
    for name, entry in color_block.items():
        if isinstance(entry, dict) and isinstance(entry.get("value"), str):
            hexes, _, _ = extract_signatures(entry["value"])
            if hexes:
                name_to_hexes.setdefault(name, set()).update(hexes)
    for name, hexes in name_to_hexes.items():
        if len(hexes) > 1:
            findings.append({
                "type": "color-name-multi-hex", "brand": brand,
                "name": name, "hexes": sorted(hexes),
            })

    # A1b: tokens.json named colour vs. same-named CSS custom property in :root
    root_match = ROOT_BLOCK_RE.search(html_text)
    css_vars = {}
    if root_match:
        for var_name, raw in CSS_VAR_RE.findall(root_match.group(1)):
            css_vars[var_name.lower()] = raw.strip()

    for name, entry in color_block.items():
        if not (isinstance(entry, dict) and isinstance(entry.get("value"), str)):
            continue
        hexes, _, _ = extract_signatures(entry["value"])
        if not hexes:
            continue
        json_hex = next(iter(hexes))
        name_words = {w for w in color_name_words(name) if w not in PATH_STOPWORDS}
        if not name_words:
            continue
        for css_name, css_raw in css_vars.items():
            css_words = {w for w in color_name_words(css_name) if w not in PATH_STOPWORDS}
            # exact word-set match, not mere overlap — "navy" must match the var
            # that means exactly "navy", not also fuzzily match "navy-deep"
            if name_words != css_words:
                continue
            css_hexes, _, _ = extract_signatures(css_raw)
            if css_hexes and json_hex not in css_hexes:
                findings.append({
                    "type": "color-json-vs-html", "brand": brand,
                    "token": f"color.{name}.value", "json_hex": json_hex,
                    "css_var": f"--{css_name}", "css_hexes": sorted(css_hexes),
                })
    return findings


# ---------------------------------------------------------------------------
# Check A2 — rare shared schema keyword, disagreeing values (conservative)
# ---------------------------------------------------------------------------

def check_a2_rare_keyword_blocks(tokens, brand):
    """Group leaves into blocks (for keyword document-frequency, so a keyword
    is judged 'rare' at the concept level, not inflated by a block's own
    verbose sub-leaves) — but keep per-LEAF keyword/signature attribution, so
    that when two blocks are compared on a shared keyword, only the specific
    leaves whose own path actually carries that keyword are compared. This is
    what keeps e.g. component.button's padding (unrelated) from being swept
    into a comparison triggered by component.button vs component.card sharing
    the word 'radius'."""
    leaves = [(p, v) for p, v in walk_leaves(tokens)
              if p and p[0] not in TOP_LEVEL_EXCLUDE and isinstance(v, (str, int, float))]

    # per-leaf: its block, its own keywords, its own signatures
    leaf_records = []
    for path, value in leaves:
        kw = path_keywords(path)
        hexes, measures, clamps = extract_signatures(str(value))
        leaf_records.append({"block": block_key(path), "keywords": kw,
                              "hexes": hexes, "measures": measures, "clamps": clamps})

    block_keywords = {}
    for rec in leaf_records:
        block_keywords.setdefault(rec["block"], set()).update(rec["keywords"])

    df = Counter()
    for kws in block_keywords.values():
        for w in kws:
            df[w] += 1
    # a keyword is a trustworthy clustering key only if it is genuinely rare:
    # it identifies exactly the two blocks that share a concept, not a theme
    # that recurs across many unrelated parts of the schema.
    rare_keywords = {w for w, c in df.items() if c == 2}
    if not rare_keywords:
        return []

    # for each rare keyword, the (up to 2) blocks that carry it, and — scoped
    # to just the leaves in that block whose OWN path carries the keyword —
    # the union of their signatures
    keyword_blocks = {}
    for rec in leaf_records:
        for w in rec["keywords"] & rare_keywords:
            entry = keyword_blocks.setdefault(w, {})
            slot = entry.setdefault(rec["block"], {"hexes": set(), "measures": set(), "clamps": set()})
            slot["hexes"] |= rec["hexes"]
            slot["measures"] |= rec["measures"]
            slot["clamps"] |= rec["clamps"]

    findings = []
    seen = set()
    for kw, blocks in keyword_blocks.items():
        block_ids = list(blocks.keys())
        for i in range(len(block_ids)):
            for j in range(i + 1, len(block_ids)):
                a, b = block_ids[i], block_ids[j]
                pair = (kw, tuple(sorted((a, b))))
                if pair in seen:
                    continue
                seen.add(pair)
                ia, ib = blocks[a], blocks[b]
                reasons = []
                if ia["hexes"] and ib["hexes"] and not (ia["hexes"] & ib["hexes"]):
                    reasons.append(f"hex colours disagree: {sorted(ia['hexes'])} vs {sorted(ib['hexes'])}")
                for unit in {u for _, u in ia["measures"]} & {u for _, u in ib["measures"]}:
                    va = {n for n, u in ia["measures"] if u == unit}
                    vb = {n for n, u in ib["measures"] if u == unit}
                    if not (va & vb):
                        reasons.append(f"'{unit}' values disagree: {sorted(va)} vs {sorted(vb)}")
                if ia["clamps"] and ib["clamps"] and not (ia["clamps"] & ib["clamps"]):
                    reasons.append(f"clamp() expressions disagree: {sorted(ia['clamps'])} vs {sorted(ib['clamps'])}")
                if reasons:
                    findings.append({
                        "type": "rare-keyword-block", "brand": brand,
                        "block_a": ".".join(a), "block_b": ".".join(b),
                        "shared_keywords": [kw], "reasons": reasons,
                    })
    return findings


def run_check_a(brand):
    paths = BRANDS[brand]
    tokens = load_tokens(paths["tokens"])
    html_text = paths["html"].read_text() if paths["html"].exists() else ""
    findings = check_a1_color_names(tokens, html_text, brand)
    findings += check_a2_rare_keyword_blocks(tokens, brand)
    return findings


def print_findings_a(findings):
    if not findings:
        print("Check A: no internal contradictions found.")
        return
    print(f"Check A: {len(findings)} possible contradiction(s) found:\n")
    for f in findings:
        if f["type"] == "color-name-multi-hex":
            print(f"  [{f['brand']}] color.{f['name']} maps to multiple hexes: {f['hexes']}")
        elif f["type"] == "color-json-vs-html":
            print(f"  [{f['brand']}] {f['token']} = {f['json_hex']}  <->  "
                  f"HTML {f['css_var']} = {f['css_hexes']}")
        else:
            print(f"  [{f['brand']}] {f['block_a']}  <->  {f['block_b']}")
            print(f"    shared concept: {', '.join(f['shared_keywords'])}")
            for r in f["reasons"]:
                print(f"    - {r}")
        print()


# ---------------------------------------------------------------------------
# Check B — off-token colour in a file of generated output
# ---------------------------------------------------------------------------

def run_check_b(brand, output_path):
    tokens = load_tokens(BRANDS[brand]["tokens"])
    known_hexes = set()
    for path, value in walk_leaves(tokens):
        if isinstance(value, str):
            for h in HEX_RE.findall(value):
                known_hexes.add(h.lower())

    # A "knownTypo" field documents a mistake by mentioning BOTH the wrong
    # hex and (for contrast) the entry's own correct one — e.g. "...always
    # use #54B987." Only the hex that ISN'T this entry's own correct value is
    # the actual typo; that one must be pulled back out of the whitelist, or
    # the linter can never catch the very typo it names.
    known_typos = {}
    for path, value in walk_leaves(tokens):
        if not (isinstance(value, str) and path and path[-1] == "knownTypo"):
            continue
        entry_path = path[:-1]
        correct_hex = None
        node = tokens
        for seg in entry_path:
            node = node[seg] if isinstance(node, dict) else node[int(seg)]
        if isinstance(node, dict) and isinstance(node.get("value"), str):
            m = HEX_RE.findall(node["value"])
            correct_hex = m[0].lower() if m else None
        for h in HEX_RE.findall(value):
            if h.lower() != correct_hex:
                known_typos[h.lower()] = ".".join(entry_path)
    known_hexes -= set(known_typos.keys())

    text = Path(output_path).read_text()
    found = HEX_RE.findall(text)
    offenders = {}
    for h in found:
        if h.lower() not in known_hexes:
            offenders[h] = offenders.get(h, 0) + 1

    if not offenders:
        print(f"Check B: no off-token colours found in {output_path}.")
        return {}

    print(f"Check B: {len(offenders)} off-token colour(s) found in {output_path}:\n")
    for h, count in sorted(offenders.items()):
        typo_of = known_typos.get(h.lower())
        note = f"  (documented known typo — see {typo_of}.knownTypo)" if typo_of else ""
        print(f"  {h}  — {count} occurrence(s){note}")
    print()
    return offenders


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brand", required=True, choices=sorted(BRANDS.keys()))
    ap.add_argument("--check-output", metavar="FILE",
                     help="run Check B on this generated CSS/HTML/SVG file instead of Check A")
    args = ap.parse_args()

    if args.check_output:
        offenders = run_check_b(args.brand, args.check_output)
        sys.exit(1 if offenders else 0)
    else:
        findings = run_check_a(args.brand)
        print_findings_a(findings)
        sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
