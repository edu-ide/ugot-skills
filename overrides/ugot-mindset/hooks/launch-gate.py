#!/usr/bin/env python3
"""PreToolUse(Bash) hook: a training/pretraining launch needs a DESIGN CARD first (multi-axis design before work).
0.7.3: a card must also hold the 8th axis "통념 밖" (lever level / 3 nearest priors / one property none has + its ruler / identity equation) — otherwise it is a reassembly and the launch is refused.
0.7.1: the launch test looks at the SCRIPT NAME / step flags, not at any path fragment (a weights path containing "ft_" is not a launch); eval/compose/ruler/diag scripts pass.
A launch = a background python run that trains (nohup/&, with train|pretrain|diffusion|ft|steps). It passes only when the
command carries DESIGN=<path> and that file exists and holds the seven axes and the pre-registered rulers. Smoke tests,
eval-only runs and non-training commands pass untouched. Exit 2 = block with the message."""
import json, os, re, sys
try:
    cmd = (json.load(sys.stdin).get("tool_input") or {}).get("command", "")
except Exception:
    sys.exit(0)
is_bg = bool(re.search(r"\bnohup\b|&\s*$|&\s*\n|&\s*;|setsid", cmd))
script = re.search(r"python[\w./-]*\s+(?:-m\s+)?([\w./-]+\.py|[\w.]+)", cmd)
name = script.group(1) if script else ""
is_eval = bool(re.search(r"eval|compose|ruler|diag|score|probe|test_", name, re.I))
is_train = (not is_eval) and bool(re.search(r"train|pretrain|diffusion|finetune|_ft\b|ft_", name, re.I) or re.search(r"--ft-steps|--steps|--mlm-steps|MLM_STEPS=|FT_STEPS=|\bSTEPS=\d", cmd))
if not (is_bg and is_train): sys.exit(0)
if re.search(r"--smoke|SMOKE=1|--eval-only|eval_only|--resume-from", cmd): sys.exit(0)
m = re.search(r"DESIGN=([^\s;&]+)", cmd)
ok = False
if m:
    path = os.path.expanduser(m.group(1))
    if os.path.isfile(path):
        txt = open(path, errors="ignore").read()
        axes = sum(1 for k in ("목표", "원리", "증거", "선행", "대안", "반증", "비용") if k in txt)
        beyond = ("통념 밖" in txt) and ("정체성 등식" in txt or "identity equation" in txt.lower()) and ("없는 성질" in txt or "property none" in txt.lower()) and ("레버의 수준" in txt or "lever level" in txt.lower())
        ok = axes >= 7 and beyond and ("사전 등록" in txt or "pre-regist" in txt.lower()) and ("자" in txt or "ruler" in txt.lower())
if not ok:
    sys.stderr.write("[설계 먼저 게이트] 학습 발사에는 설계 카드가 필요하다. 카드 = 일곱 축(목표·원리·증거·선행·대안·반증·비용) + 다섯 자(읽기·생성·구성적 성질·비용·추세) 사전 등록 + **8번째 축 '통념 밖' 절**(①바꾸는 레버의 수준: 학습 규칙/계산 모델/연산자/표현 ②최근접 선행 3편(최근 18개월) ③그 전부에 없는 성질 1개와 그것을 재는 자 ④정체성 등식). '통념 밖' 절이 없는 카드는 이미 연구된 부품의 재조립이므로 발사 거부(2026-10-10). 발사 명령 앞에 DESIGN=<카드 경로>. 연기 시험(--smoke)·평가만(--eval-only)·재개(--resume-from)는 통과.\n")
    sys.exit(2)
