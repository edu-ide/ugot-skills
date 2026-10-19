#!/usr/bin/env python3
"""Rebuild this public repo's plugins from the private UGOT marketplace.

Only skills named in tools/public-allowlist.json are copied. The private
marketplace stays the single source; edit skills there, then run:

    python3 tools/sync_from_private.py /path/to/ugot-claude-plugins [--local-skills ~/.claude/skills] [--check]

Skills listed under a plugin's "local_skills" come from --local-skills (skills
not yet in the private marketplace). Files named in "exclude_files" (for example
references/local.md, a skill's private profile) are never copied. Folders named
in a plugin's "keep" (for example hooks that depend on private tools) are left
as they are in this repo. With "strip_criticmarkup", Markdown files lose their
CriticMarkup evidence comments, which point at private sources.

Every copied file is scanned before anything is written. A hit on a private
pattern (personal data, local paths, unpublished research names) stops the
sync, so a leak has to be fixed in the private source or listed in
`replace` with a reviewed public wording.
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALLOW = json.loads((ROOT / "tools" / "public-allowlist.json").read_text(encoding="utf-8"))
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")

# Anything matching these must not reach the public repo.
BLOCK = re.compile(
    r"/mnt/|/home/[a-z]|~/\.ilhae|\b01[016789]-?\d{3,4}-?\d{4}\b"
    r"|192\.168\.|\.svc\.cluster"
    r"|GOCSPX-|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|PRIVATE KEY",
    re.IGNORECASE,
)
# Personal identifiers (names, account ids) stay out of this public file:
# one regex per line in ~/.config/ugot-skills/private-patterns.txt.
_private = Path.home() / ".config" / "ugot-skills" / "private-patterns.txt"
if not _private.is_file():
    raise SystemExit(f"missing {_private}: list personal patterns there before syncing")
if not _private.with_name("private-patterns-cs.txt").is_file():
    raise SystemExit("missing private-patterns-cs.txt next to private-patterns.txt")
PRIVATE = re.compile("|".join(l.strip() for l in _private.read_text(encoding="utf-8").splitlines() if l.strip()), re.IGNORECASE)
# Case-sensitive private tokens (internal code names) live next to it.
_private_cs = _private.with_name("private-patterns-cs.txt")
BLOCK_CS = re.compile("|".join(l.strip() for l in _private_cs.read_text(encoding="utf-8").splitlines() if l.strip()) or r"(?!x)x")


def strip_criticmarkup(text):
    """Drop CriticMarkup evidence comments and their [cm-*] link definitions.

    The private skills carry per-rule evidence notes that point at private
    repositories and local transcripts. The public cut keeps the rules only.
    """
    text = re.sub(r"[ \t]*\{>>.*?<<\}", "", text, flags=re.S)
    text = re.sub(r"(?m)^\[cm-[^\]]*\]:.*\n?", "", text)
    # Links into local transcripts and files mean nothing outside this machine.
    text = re.sub(r"(?m)^\[[^\]]+\]:\s*(?:claude|codex|file)://.*\n?", "", text)
    text = re.sub(r"\[([^\]]+)\]\((?:claude|codex|file)://[^)]*\)", r"\1", text)
    return re.sub(r"\n{3,}", "\n\n", text)


def text_files(folder):
    for path in sorted(folder.rglob("*")):
        if path.is_file():
            try:
                yield path, path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue


def stage(source_root, local_root):
    staged = {}
    for plugin, spec in ALLOW["plugins"].items():
        src_plugin = source_root / "plugins" / spec["from"]
        out = {}
        for name in spec["skills"]:
            src = src_plugin / "skills" / name
            if not (src / "SKILL.md").is_file():
                raise SystemExit(f"{plugin}/{name}: no SKILL.md in {src}")
            out[f"skills/{name}"] = src
        for name in spec.get("local_skills", []):
            if local_root is None:
                raise SystemExit(f"{plugin}/{name}: needs --local-skills")
            src = local_root / name
            if not (src / "SKILL.md").is_file():
                raise SystemExit(f"{plugin}/{name}: no SKILL.md in {src}")
            out[f"skills/{name}"] = src
        for extra in spec.get("extra", []):
            src = src_plugin / extra
            if not src.exists():
                raise SystemExit(f"{plugin}: missing {src}")
            out[extra] = src
        staged[plugin] = out
    return staged


def scan_and_copy(staged, dry_run):
    replace = ALLOW.get("replace", {})
    hits = []
    plan = []
    for plugin, entries in staged.items():
        for rel, src in entries.items():
            files = [(src, src.read_text(encoding="utf-8"))] if src.is_file() else list(text_files(src))
            excluded = set(ALLOW.get("exclude_files", []))
            files = [(p, t) for p, t in files if src.is_file() or (str(p.relative_to(src)) not in excluded
                     and f"{plugin}/{rel}/{p.relative_to(src)}" not in excluded
                     and not p.name.endswith((".bak", ".orig")) and ".bak-" not in p.name)]
            for path, text in files:
                key = f"{plugin}/{rel}/{path.relative_to(src)}" if src.is_dir() else f"{plugin}/{rel}"
                override = ALLOW.get("overrides", {}).get(key)
                if override is not None:
                    now = hashlib.sha256(path.read_bytes()).hexdigest()
                    if now != override:
                        raise SystemExit(f"{key}: private source changed since its public override was reviewed "
                                         f"(was {override[:12]}, now {now[:12]}). Re-review overrides/{key}.")
                    text = (ROOT / "overrides" / key).read_text(encoding="utf-8")
                elif ALLOW.get("strip_criticmarkup") and path.suffix == ".md":
                    text = strip_criticmarkup(text)
                for old, new in replace.get(key, []):
                    if old not in text:
                        raise SystemExit(f"{key}: reviewed replacement no longer matches: {old[:60]}")
                    text = text.replace(old, new)
                for n, line in enumerate(text.splitlines(), 1):
                    if BLOCK.search(line) or BLOCK_CS.search(line) or PRIVATE.search(line):
                        hits.append(f"{key}:{n}: {line.strip()[:120]}")
                plan.append((plugin, rel, src, path, text))
    if hits:
        print("Blocked: private patterns found. Fix the private source or add a reviewed replacement.")
        print("\n".join(hits))
        raise SystemExit(1)
    if dry_run:
        print(f"clean: {len(plan)} files")
        return
    for plugin in staged:
        target = ROOT / "plugins" / plugin
        keep = set(ALLOW["plugins"][plugin].get("keep", []))
        for sub in ("skills", "hooks", "agents"):
            if sub not in keep and (target / sub).exists():
                shutil.rmtree(target / sub)
    for plugin, rel, src, path, text in plan:
        dest = ROOT / "plugins" / plugin / rel
        if src.is_dir():
            dest = dest / path.relative_to(src)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        dest.chmod(path.stat().st_mode & 0o777)
    print(f"copied {len(plan)} files")


def write_manifests():
    market = {
        "name": ALLOW["marketplace"]["name"],
        "description": ALLOW["marketplace"]["description"],
        "owner": {"name": "UGOT"},
        "plugins": [],
    }
    for plugin, spec in ALLOW["plugins"].items():
        meta = ROOT / "plugins" / plugin / ".claude-plugin"
        meta.mkdir(parents=True, exist_ok=True)
        manifest = {
            "name": plugin,
            "displayName": spec["displayName"],
            "version": spec["version"],
            "description": spec["description"],
            "author": {"name": "UGOT"},
            "license": "MIT",
            "homepage": "https://github.com/edu-ide/ugot-skills",
        }
        (meta / "plugin.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        market["plugins"].append({"name": plugin, "source": f"./plugins/{plugin}", "description": spec["description"]})
    out = ROOT / ".claude-plugin"
    out.mkdir(exist_ok=True)
    (out / "marketplace.json").write_text(json.dumps(market, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    argv = sys.argv[1:]
    local_root = None
    if "--local-skills" in argv:
        i = argv.index("--local-skills")
        local_root = Path(argv[i + 1]).expanduser().resolve()
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        raise SystemExit(__doc__)
    staged = stage(Path(args[0]).resolve(), local_root)
    scan_and_copy(staged, dry_run="--check" in sys.argv)
    if "--check" not in sys.argv:
        write_manifests()
