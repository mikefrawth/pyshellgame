# 06 — Chapter 1 completion

**What to build:** Chapter 1 (HTTP/APIs) is fleshed out to its full main-line sequence, plus one optional stretch side-challenge (e.g. rate-limiting or observability), using the save, hint, and file-editing infrastructure already in place. Completing the chapter's main line should feel like a coherent arc, not just one isolated challenge.

**Blocked by:** 03, 04, 05

**Status:** ready-for-agent

- [ ] Chapter 1's main-line challenge sequence is implemented beyond the single challenge from ticket 02, forming a coherent progression
- [ ] At least one main-line challenge uses the file-editing flow from ticket 05 (not every challenge needs to)
- [ ] One optional stretch side-challenge is implemented (e.g. rate-limiting), clearly marked optional and non-blocking to main-line progression
- [ ] Completing the chapter's main-line challenges is reflected in save state (builds on ticket 03)
- [ ] `hint` works correctly across all new challenges in this chapter
- [ ] Passing- and failing-path tests exist for each new challenge, driven through `GameSession.run_command()`
