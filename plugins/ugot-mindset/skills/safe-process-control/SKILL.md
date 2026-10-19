---
name: safe-process-control
description: 프로세스는 PID로만 — pkill -f·killall·kill -9·pgrep 패턴 일괄 종료 금지(자기 자신·남의 프로세스·건강한 런을 죽인 사고가 6회 이상 재발). 종료 전 PID·명령줄·시작 시각으로 "내 것이고 낡은 것"임을 확인하고, SIGKILL·exit 137은 OOM이 아니라 "누가 죽였나"부터 본다.
contract:
  trigger: "프로세스를 종료·재시작하려는 순간, 죽은 런(SIGKILL·exit 137)의 원인을 적으려는 순간"
  trigger_when: ["tool_use:Bash~(^|\\\\n|[;&|]\\s*)\\s*(kill|killall)\\s+(?!-0\\b)(-[A-Za-z0-9]+\\s+)*(\\d|\\$)"]
  procedure: "ps -o pid,lstart,cmd -p <pid>로 명령줄·시작 시각 확인 → 내 것이고 낡은 것일 때만 kill <pid>(SIGTERM 먼저) → 패턴 일괄 종료 금지 → SIGKILL은 '누가 죽였나'부터"
  exit_check: "kill마다 그 PID의 ps 확인이 먼저 있고 패턴으로 고른 일괄 종료(pkill -f·killall)가 없다"
  evidence: "ps -p 출력과 kill <pid>가 든 Bash 호출"
  failure_modes: [19]
  validator: ["tool_use:Bash~(ps (-[a-z]+ )*-p|ps -o|/proc/[0-9]+)"]
principle: self
---

# 프로세스를 죽이기 전에

- **패턴 일괄 종료 금지**: `pkill -f`, `killall`, `pgrep -f … | xargs kill`, `kill -9`. 패턴은 내 셸·감시 루프·같은 이름의 건강한 런까지 맞는다(2026-06-30 수 시간 손실, 2026-07-21 6회차, 2026-10-08 2회).
- **PID 지정만**: `ps -o pid,lstart,cmd -p <pid>`로 명령줄·시작 시각을 확인한 뒤 `kill <pid>`(먼저 SIGTERM). 내가 띄운 것인지·낡은 것인지 둘 다 확인.
- **죽은 런의 원인**: traceback 없고 "CUDA out of memory" 없는 SIGKILL/exit 137 = 외부·자기 종료를 먼저 의심. 메모리 최고치가 용량보다 한참 낮으면 OOM이 아니다.
- **공유 장비(unified memory 등)**: 종료가 메모리를 돌려주지 않는 장비에서는 한 번 띄운 것을 끝까지 둔다. 설정을 바꾸려면 재시작이 아니라 깨끗한 상태에서 한 번만.
