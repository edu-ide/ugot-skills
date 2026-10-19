#!/usr/bin/env python3
"""Snapshot selected skills; verify preservation, never task completion."""

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from zoneinfo import ZoneInfo


IGNORED_DIRS = {".git", "__pycache__"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    files = []
    for base, directories, names in os.walk(root, followlinks=False):
        directories[:] = sorted(d for d in directories if d not in IGNORED_DIRS)
        for name in directories + sorted(names):
            path = Path(base) / name
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise ValueError(f"Internal symlink requires an explicit snapshot: {path}")
            if stat.S_ISREG(mode):
                files.append(path.relative_to(root))
            elif not stat.S_ISDIR(mode):
                raise ValueError(f"Unsupported special file: {path}")
    return sorted(files)


def create_run(skills, workdir, session_uri, timezone=None):
    roots = []
    workdir = Path(workdir).resolve()
    for value in skills:
        path = Path(value).resolve(strict=True)
        root = path.parent if path.name == "SKILL.md" else path
        if not (root / "SKILL.md").is_file():
            raise ValueError(f"Missing SKILL.md: {root}")
        if workdir == root or root in workdir.parents:
            raise ValueError("Work directory must not be inside a copied skill")
        if root.name in {p.name for p in roots}:
            raise ValueError(f"Duplicate skill folder name: {root.name}")
        roots.append(root)
    if not roots:
        raise ValueError("At least one skill is required")
    now = datetime.now(ZoneInfo(timezone)) if timezone else datetime.now().astimezone()
    workdir.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".skill-run-", dir=workdir))
    target = workdir / now.strftime("%Y-%m-%d_%H-%M-%S_%f%z")
    manifest = {"version": 1, "created_at": now.isoformat(), "session_uri": session_uri,
                "skills": [], "verification_scope": "snapshot_integrity_only"}
    try:
        for root in roots:
            record = {"name": root.name, "original": str(root), "files": {}}
            for relative in inventory(root):
                source = root / relative
                data = source.read_bytes()
                record["files"][relative.as_posix()] = {"sha256": digest(data), "bytes": len(data)}
                for kind in ("source", "working"):
                    destination = staging / kind / root.name / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(data)
                    destination.chmod(stat.S_IMODE(source.stat().st_mode))
            manifest["skills"].append(record)
        (staging / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if target.exists():
            raise ValueError(f"Run already exists: {target}")
        staging.rename(target)
        return {"run": str(target), "skills": [r.name for r in roots],
                "verification_scope": "snapshot_integrity_only"}
    except BaseException:
        shutil.rmtree(staging)
        raise


def verify_run(run):
    run = Path(run).resolve(strict=True)
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("version") != 1 or not manifest.get("skills"):
        raise ValueError("Unsupported or empty manifest")
    count = 0
    for skill in manifest["skills"]:
        name = skill["name"]
        if Path(name).name != name or name in (".", ".."):
            raise ValueError("Invalid skill name in manifest")
        root = run / "source" / name
        if root.is_symlink() or not root.is_dir():
            raise ValueError(f"Missing or linked snapshot: {root}")
        actual = {p.as_posix() for p in inventory(root)}
        if actual != set(skill["files"]):
            raise ValueError(f"Snapshot file set changed: {name}")
        for relative, expected in skill["files"].items():
            data = (root / relative).read_bytes()
            if len(data) != expected["bytes"] or digest(data) != expected["sha256"]:
                raise ValueError(f"Snapshot content changed: {name}/{relative}")
            count += 1
    return {"run": str(run), "verified_files": count,
            "verification_scope": "snapshot_integrity_only"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create")
    create.add_argument("--skill", action="append", required=True)
    create.add_argument("--workdir", required=True)
    create.add_argument("--timezone")
    create.add_argument("--session-uri", required=True)
    verify = commands.add_parser("verify")
    verify.add_argument("--run", required=True)
    args = parser.parse_args()
    try:
        result = (create_run(args.skill, args.workdir, args.session_uri, args.timezone)
                  if args.command == "create" else verify_run(args.run))
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f"skill-run: {error}\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
