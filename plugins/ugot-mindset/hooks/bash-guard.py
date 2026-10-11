#!/usr/bin/env python3
"""PreToolUse(Bash) hook: refuse pattern-based process killing (mistake pattern 19). Exit 2 = block + message."""
import json, re, sys
try:
    cmd = (json.load(sys.stdin).get("tool_input") or {}).get("command", "")
except Exception:
    sys.exit(0)
BAD = [
    (r"\bpkill\b", "pkill (패턴 종료)"),
    (r"\bkillall\b", "killall"),
    (r"\bkill\s+(-9|-KILL|-s\s*KILL)\b", "kill -9"),
    (r"\bpgrep\b[^|\n]*\|\s*(xargs\s+)?kill\b", "pgrep | kill"),
    (r"\bpgrep\b[^\n]*\bwhile\b[^\n]*\bkill\b", "pgrep … while … kill"),
]
for pat, name in BAD:
    if re.search(pat, cmd):
        sys.stderr.write(f"[프로세스 가드] '{name}' 은 금지다(자기 자신·남의 프로세스·건강한 런을 죽인 사고 6회 이상). ps -o pid,lstart,cmd -p <pid> 로 명령줄·시작 시각을 확인한 뒤 PID를 지정해 kill <pid> (SIGTERM) 하라. 스킬 safe-process-control.\n")
        sys.exit(2)
