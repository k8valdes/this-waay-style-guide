#!/usr/bin/env python3
"""
emit_figma.py — Figma-import variable JSON from the resolved token set.

DTCG-shaped, grouped into three collections by tier (Primitives / Semantic /
Component) so a client's designers import the same tokens the generators use.
A pure function of the resolver's production-only output.

    python3 scripts/emit_figma.py   # writes product-design-studio/build/figma-variables.json
"""
import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resolve_tokens import Resolver  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "product-design-studio" / "build" / "figma-variables.json"

SEMANTIC_COLOR = ("surface", "fill", "text", "border")
COMPONENT_GROUPS = ("button", "card", "badge")


def tier_of(path):
    head = path.split(".")
    if head[0] in COMPONENT_GROUPS:
        return "Component"
    if head[0] == "color" and len(head) > 1 and head[1] in SEMANTIC_COLOR:
        return "Semantic"
    if head[0] in ("gradient", "typography"):
        return "Semantic"
    return "Primitives"


def dtcg_value(t, v):
    if t == "gradient":
        return {"stops": [{"color": s["color"], "position": s["position"]} for s in v["stops"]]}
    return v  # color object / {value,unit} / number / array / typography composite already DTCG-shaped


def emit(resolved, version=None):
    collections = OrderedDict([("Primitives", OrderedDict()),
                               ("Semantic", OrderedDict()),
                               ("Component", OrderedDict())])
    for path, e in resolved.items():
        col = collections[tier_of(path)]
        node = col
        parts = path.split(".")
        for seg in parts[:-1]:
            node = node.setdefault(seg, OrderedDict())
        tok = OrderedDict([("$type", e["type"]), ("$value", dtcg_value(e["type"], e["value"]))])
        if e["type"] == "gradient" and e["value"].get("angle") is not None:
            tok["$extensions"] = {"angle": e["value"]["angle"]}  # resolved number
        if e["description"]:
            tok["$description"] = e["description"]
        node[parts[-1]] = tok
    return OrderedDict([
        ("$meta", {"generatedFrom": f"tokens.json v{version}", "note": "GENERATED — do not hand-edit"}),
        ("collections", collections),
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()
    r = Resolver()
    data = emit(r.resolve("production"), r.version)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if args.stdout:
        sys.stdout.write(text)
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(text)
        n = sum(1 for _ in r.resolve("production"))
        print(f"wrote {OUT}  ({n} variables across 3 tier collections)")


if __name__ == "__main__":
    main()
