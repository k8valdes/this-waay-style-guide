#!/usr/bin/env python3
"""
resolve_tokens.py — the Phase 3b resolver. Flattens the tiered DTCG-2025.10
tokens.json into a resolved token set that every emitter reads. Standard
library only.

The resolver is the single source the emitters share, so they cannot disagree.
It follows {group.token} aliases transitively (component -> semantic ->
primitive), detects cycles / dangling refs, resolves colors to the object form,
dimensions to {value,unit}, typography composites (fontFamily stack +
fontWeight, never synthesizing bold), and gradients to stops + resolved angle.

Production-only filter (load-bearing): resolve(select="production") exposes
only status:production tokens to emitters; select="all" exposes everything for
inspection. Emitters always run production.

CLI:
    python3 scripts/resolve_tokens.py                 # summary
    python3 scripts/resolve_tokens.py --select all --dump   # full JSON dump
"""

import argparse
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOKENS = REPO / "product-design-studio" / "tokens.json"
REF_RE = re.compile(r"^\{(.+)\}$")


class ResolveError(Exception):
    pass


class Resolver:
    def __init__(self, tokens_path=TOKENS):
        self.doc = json.loads(Path(tokens_path).read_text())
        # namespace single-sourced from meta, never hardcoded
        self.ns = self.doc.get("meta", {}).get("extensionsNamespace")
        if not self.ns:
            raise ResolveError("meta.extensionsNamespace missing")
        self.version = self.doc.get("meta", {}).get("version")

    # ---- token lookup + effective type / status -------------------------
    def _node(self, dotted):
        node = self.doc
        for seg in dotted.split("."):
            if not isinstance(node, dict) or seg not in node:
                return None
            node = node[seg]
        return node

    def token_at(self, dotted):
        n = self._node(dotted)
        return n if isinstance(n, dict) and "$value" in n else None

    def effective_type(self, dotted):
        """Nearest $type walking from the token up its group ancestors."""
        parts = dotted.split(".")
        for i in range(len(parts), 0, -1):
            n = self._node(".".join(parts[:i]))
            if isinstance(n, dict) and "$type" in n:
                return n["$type"]
        return None

    def status(self, dotted):
        """Nearest status walking from the token up its group ancestors — a
        component's status sits on the component GROUP (card.skewed-accent),
        and its leaf children (.radius/.title) must inherit it, or the
        production-only filter would leak deprecated tokens through the leaves."""
        parts = dotted.split(".")
        for i in range(len(parts), 0, -1):
            n = self._node(".".join(parts[:i]))
            if isinstance(n, dict):
                st = ((n.get("$extensions", {}) or {}).get(self.ns, {}) or {}).get("status")
                if st:
                    return st
        return "production"  # tokens without any status ancestor are production

    def ext(self, dotted):
        tok = self.token_at(dotted)
        return ((tok.get("$extensions", {}) or {}).get(self.ns, {}) or {}) if tok else {}

    # ---- reference resolution ------------------------------------------
    def _resolve_ref_str(self, s, seen):
        m = REF_RE.match(s.strip())
        if not m:
            return None
        target = m.group(1)
        if target in seen:
            raise ResolveError(f"reference cycle: {' -> '.join(list(seen) + [target])}")
        if self.token_at(target) is None:
            raise ResolveError(f"dangling reference: {{{target}}}")
        return self._resolve_token(target, seen | {target})

    def _resolve_token(self, dotted, seen=None):
        seen = seen or {dotted}
        tok = self.token_at(dotted)
        if tok is None:
            raise ResolveError(f"no token at {dotted}")
        typ = self.effective_type(dotted)
        val = tok["$value"]

        # a whole-value alias
        if isinstance(val, str):
            r = self._resolve_ref_str(val, seen)
            if r is not None:
                return r
            raise ResolveError(f"{dotted}: string $value that is not a reference: {val!r}")

        if typ == "color":
            return {"colorSpace": val["colorSpace"], "components": val["components"],
                    "hex": val["hex"], **({"alpha": val["alpha"]} if "alpha" in val else {})}
        if typ == "dimension":
            return {"value": val["value"], "unit": val["unit"]}
        if typ == "number":
            return val
        if typ == "fontFamily":
            return list(val)
        if typ == "typography":
            out = OrderedDict()
            fam = val["fontFamily"]
            out["fontFamily"] = self._resolve_ref_str(fam, seen) if isinstance(fam, str) and REF_RE.match(fam) else fam
            out["fontWeight"] = val["fontWeight"]  # emitted verbatim — never synthesized
            out["fontSize"] = val.get("fontSize")
            lh = val.get("lineHeight")
            out["lineHeight"] = self._resolve_ref_str(lh, seen) if isinstance(lh, str) and REF_RE.match(str(lh)) else lh
            if "letterSpacing" in val:
                out["letterSpacing"] = val["letterSpacing"]
            return out
        if typ == "gradient":
            stops = []
            for stop in val:
                c = stop["color"]
                stops.append({"color": self._resolve_ref_str(c, seen) if isinstance(c, str) else c,
                              "position": stop["position"]})
            angle_ref = self.ext(dotted).get("angle")
            angle = self._resolve_ref_str(angle_ref, seen) if isinstance(angle_ref, str) and REF_RE.match(angle_ref) else angle_ref
            return {"stops": stops, "angle": angle}
        if typ == "shadow":
            out = OrderedDict()
            for k, v in val.items():
                if isinstance(v, dict) and "colorSpace" in v:
                    out[k] = dict(v)
                elif isinstance(v, str) and REF_RE.match(v):
                    out[k] = self._resolve_ref_str(v, seen)
                else:
                    out[k] = v
            return out
        # unknown type: pass through
        return val

    # ---- public: the resolved set --------------------------------------
    def resolve(self, select="production"):
        """Return OrderedDict path -> {type,status,value,description,ext}."""
        out = OrderedDict()
        for path in self._all_token_paths():
            st = self.status(path)
            if select == "production" and st != "production":
                continue
            tok = self.token_at(path)
            value = self._resolve_token(path)
            out[path] = {
                "type": self.effective_type(path) or self._infer_type(value),
                "status": st,
                "value": value,
                "description": tok.get("$description"),
                "ext": self.ext(path),
            }
        return out

    @staticmethod
    def _infer_type(value):
        """Untyped component tokens (button.primary.label) inherit no $type;
        infer from the resolved value shape so emitters know how to format."""
        if isinstance(value, dict):
            if "colorSpace" in value:
                return "color"
            if "value" in value and "unit" in value:
                return "dimension"
            if "fontFamily" in value:
                return "typography"
            if "stops" in value:
                return "gradient"
        if isinstance(value, list):
            return "fontFamily"
        if isinstance(value, (int, float)):
            return "number"
        return None

    def _all_token_paths(self):
        paths = []

        def walk(node, prefix):
            if isinstance(node, dict):
                if "$value" in node:
                    paths.append(".".join(prefix))
                    return
                for k, v in node.items():
                    if k.startswith("$") or k == "meta":
                        continue
                    walk(v, prefix + [k])
        walk(self.doc, [])
        return paths

    def counts(self):
        allset = self.resolve("all")
        prod = self.resolve("production")
        withheld = {p: e["status"] for p, e in allset.items() if p not in prod}
        return len(allset), len(prod), withheld


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--select", choices=["production", "all"], default="production")
    ap.add_argument("--dump", action="store_true", help="print the resolved set as JSON")
    args = ap.parse_args()
    r = Resolver()
    resolved = r.resolve(args.select)
    if args.dump:
        print(json.dumps(resolved, indent=2, ensure_ascii=False))
        return
    total, prod, withheld = r.counts()
    print(f"resolver — tokens.json v{r.version}  (namespace: {r.ns})")
    print(f"  total tokens: {total}   production (emittable): {prod}   withheld: {len(withheld)}")
    print(f"  selected ({args.select}): {len(resolved)}")
    if withheld:
        print("  withheld (never emitted):")
        for p, st in sorted(withheld.items()):
            print(f"    [{st}] {p}")


if __name__ == "__main__":
    main()
