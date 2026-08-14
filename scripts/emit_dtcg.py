#!/usr/bin/env python3
"""
emit_dtcg.py — flat DTCG-2025.10 export from the resolved token set.

A resolved, single-tier DTCG file (every {reference} followed to a literal) for
clients whose tooling wants standard tokens without the tier indirection. Keeps
the natural group structure and the DTCG object forms (color object,
{value,unit} dimension), so it is itself valid 2025.10 and re-resolves to the
same values. A pure function of the resolver's production-only output.

    python3 scripts/emit_dtcg.py   # writes product-design-studio/build/tokens.flat.dtcg.json
"""
import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resolve_tokens import Resolver  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "product-design-studio" / "build" / "tokens.flat.dtcg.json"
SCHEMA_URL = "https://www.designtokens.org/schemas/2025.10/format.json"


def dtcg_value(t, v):
    if t == "gradient":
        # DTCG gradient $value is the stop array; the angle is a documented extension
        return [{"color": s["color"], "position": s["position"]} for s in v["stops"]]
    return v


def emit(resolved, version=None, ns="x.brandkit"):
    doc = OrderedDict()
    doc["$schema"] = SCHEMA_URL
    doc["$description"] = (f"Flat resolved DTCG 2025.10 export of This Waay tokens.json v{version}. "
                           "GENERATED — do not hand-edit. Every reference is resolved to a literal; "
                           "production-only (deprecated/proposed tokens excluded).")
    for path, e in resolved.items():
        node = doc
        parts = path.split(".")
        for seg in parts[:-1]:
            node = node.setdefault(seg, OrderedDict())
        tok = OrderedDict([("$type", e["type"]), ("$value", dtcg_value(e["type"], e["value"]))])
        if e["type"] == "gradient" and e["value"].get("angle") is not None:
            tok["$extensions"] = {ns: {"angle": e["value"]["angle"]}}  # resolved number
        if e["description"]:
            tok["$description"] = e["description"]
        node[parts[-1]] = tok
    return doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()
    r = Resolver()
    data = emit(r.resolve("production"), r.version, r.ns)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if args.stdout:
        sys.stdout.write(text)
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(text)
        n = sum(1 for _ in r.resolve("production"))
        print(f"wrote {OUT}  ({n} resolved tokens, flat DTCG 2025.10)")


if __name__ == "__main__":
    main()
