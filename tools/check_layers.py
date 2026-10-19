#!/usr/bin/env python3
"""Check the skill layers of this repo.

Rules (see README, "구조"):
  1. Every skill declares `principle:` in its front matter.
  2. `principle: self` (a principle skill) lives only in ugot-mindset.
  3. A domain skill names a principle skill that exists in this repo.
  4. A binding chain ends at a principle skill and never loops.

Prints a one-line summary and exits 1 on any violation:

    python3 tools/check_layers.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRINCIPLE_PLUGIN = "ugot-mindset"


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError("no front matter")
    return m.group(1)


def main():
    skills = {}
    errors = []
    for path in sorted(ROOT.glob("plugins/*/skills/*/SKILL.md")):
        plugin, name = path.parts[-4], path.parts[-2]
        try:
            fm = front_matter(path)
        except ValueError as exc:
            errors.append(f"{plugin}/{name}: {exc}")
            continue
        m = re.search(r"(?m)^principle:\s*(\S+)\s*$", fm)
        skills[name] = (plugin, m.group(1) if m else None)

    principles = {n for n, (plugin, p) in skills.items() if p == "self"}
    unbound = []
    for name, (plugin, principle) in sorted(skills.items()):
        if principle is None:
            unbound.append(f"{plugin}/{name}")
        elif principle == "self" and plugin != PRINCIPLE_PLUGIN:
            errors.append(f"{plugin}/{name}: principle skills belong in {PRINCIPLE_PLUGIN}")
        elif principle != "self" and principle not in skills:
            errors.append(f"{plugin}/{name}: bound to missing principle '{principle}'")
        elif principle != "self" and principle not in principles:
            # Bound to a skill that is itself bound: follow the chain, it must end at a principle.
            seen, cur = {name}, principle
            while cur in skills and skills[cur][1] not in (None, "self"):
                if cur in seen:
                    errors.append(f"{plugin}/{name}: principle chain loops at '{cur}'")
                    break
                seen.add(cur)
                cur = skills[cur][1]

    bound = len(skills) - len(unbound)
    print(f"skills {len(skills)} · principles {len(principles)} · bound {bound}/{len(skills)}"
          + (f" · unbound: {', '.join(unbound)}" if unbound else "")
          + f" · errors {len(errors)}")
    for line in errors:
        print("  " + line)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
