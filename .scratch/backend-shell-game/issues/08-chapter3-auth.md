# 08 — Chapter 3: Auth

**What to build:** The third and final core campaign chapter. Main-line challenges cover sessions, tokens, and permissions, building on the real Flask app and SQLite DB from prior chapters. One optional stretch side-challenge (e.g. async or queues) is included.

**Blocked by:** 07

**Status:** ready-for-agent

- [ ] Main-line challenges cover session handling, token-based auth, and permissions/authorization checks
- [ ] At least one main-line challenge uses the file-editing flow (e.g. player writes/fixes an auth check function)
- [ ] Auth-related state (sessions, tokens, permissions) is real and inspectable — grading via `check_state()` on that real state, not simulated flags
- [ ] One optional stretch side-challenge is implemented (e.g. async or queues), clearly optional
- [ ] Chapter 3 challenges integrate with save/hint systems from prior tickets
- [ ] Passing- and failing-path tests exist for each new challenge, driven through `GameSession.run_command()`
