# UGOT Skills

Claude Code와 Codex에서 쓰는 UGOT의 공개 스킬 묶음입니다. 에이전트가 사용자의 의도를 읽고, 확인한 것만 말하고, 빠뜨린 것을 숨기지 않게 만드는 습관을 스킬과 훅으로 담았습니다.

Open skills from UGOT for Claude Code and Codex: agent mindset gates, reader-first writing and engineering habits. Most skill text is written in Korean.

## 플러그인

| 플러그인 | 내용 |
|---|---|
| `ugot-mindset` | 의도 읽기, 확인 전 주장 금지, 빠뜨린 것 밝히기, 끝까지 하기, 짧은 사람 말 답변. 스킬 19개, 에이전트 2개, 자동 점검 훅 |
| `ugot-writing` | 독자 중심 글쓰기, 문체 편집, 지원서 최종 확인, 노래·가사, 이야기 구성, 짧은 광고 |
| `ugot-engineering-habits` | 근본 원리부터 구현, 최신 문헌 확인, 지름길을 숨기지 않기, 사전 부검, 치명적인 것부터, 장애는 수습과 근본 수정을 나누고 재발을 원인 단위로 확인 |

## 설치

**Claude Code**

```
/plugin marketplace add edu-ide/ugot-skills
/plugin install ugot-mindset@ugot-skills
```

**Codex**

```bash
codex plugin marketplace add https://github.com/edu-ide/ugot-skills.git
codex plugin add ugot-mindset@ugot-skills
```

Codex에서도 스킬이 동작합니다(Codex 0.160 확인). `ugot-mindset`의 훅은 Claude Code 형식이며, Codex에서 실행되는지는 아직 확인하지 않았습니다.

## 만든 곳

UGOT은 AI가 한 일을 믿을 수 있게 기록하고 확인하는 도구를 만듭니다. 문서(Office), 업무 기록(Work), 기억(Brain), 브라우저(Agent Browser), 메일 도구는 [space.ugot.uk](https://space.ugot.uk)에서 볼 수 있습니다.

## 기여와 라이선스

이 저장소는 UGOT 내부 원본에서 공개 허용 목록(`tools/public-allowlist.json`)만 복사해 만듭니다. 고칠 점은 이슈로 알려 주세요.

MIT License. `LICENSE`를 보세요.
