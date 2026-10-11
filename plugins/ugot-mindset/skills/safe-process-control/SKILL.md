---
name: safe-process-control
description: 프로세스는 PID로만 — pkill -f·killall·kill -9·pgrep 패턴 일괄 종료 금지(자기 자신·남의 프로세스·건강한 런을 죽인 사고가 6회 이상 재발). 종료 전 PID·명령줄·시작 시각으로 "내 것이고 낡은 것"임을 확인하고, SIGKILL·exit 137은 OOM이 아니라 "누가 죽였나"부터 본다.
---

# 프로세스를 죽이기 전에

- **패턴 일괄 종료 금지**: `pkill -f`, `killall`, `pgrep -f … | xargs kill`, `kill -9`. 패턴은 내 셸·감시 루프·같은 이름의 건강한 런까지 맞는다(2026-06-30 수 시간 손실, 2026-07-21 6회차, 2026-10-08 2회).
- **PID 지정만**: `ps -o pid,lstart,cmd -p <pid>`로 명령줄·시작 시각을 확인한 뒤 `kill <pid>`(먼저 SIGTERM). 내가 띄운 것인지·낡은 것인지 둘 다 확인.
- **죽은 런의 원인**: traceback 없고 "CUDA out of memory" 없는 SIGKILL/exit 137 = 외부·자기 종료를 먼저 의심. 메모리 최고치가 용량보다 한참 낮으면 OOM이 아니다.
- **공유 장비(unified memory 등)**: 종료가 메모리를 돌려주지 않는 장비에서는 한 번 띄운 것을 끝까지 둔다. 설정을 바꾸려면 재시작이 아니라 깨끗한 상태에서 한 번만.
