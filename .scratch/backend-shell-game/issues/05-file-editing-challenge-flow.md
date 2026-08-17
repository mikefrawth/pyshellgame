# 05 — File-editing challenge flow

**What to build:** The second challenge mode. A challenge can specify a target Python file the player edits directly (e.g. to write a route handler). The game loads that file as a module, invokes a designated entry point against the live Flask app/DB, and grades it via the same `check_state()` mechanism as REPL-only challenges. Demonstrated with one concrete example in the HTTP chapter.

**Blocked by:** 02

**Status:** ready-for-agent

- [ ] A challenge type exists that names a target file and an expected entry point (e.g. a function the game calls after loading the module)
- [ ] The game loads the player-edited file and invokes that entry point against the real, live Flask app (and DB, if relevant) owned by `GameSession`
- [ ] Grading reuses `check_state()` — no separate/parallel grading path for file-editing challenges
- [ ] One concrete file-editing challenge is implemented and playable end-to-end (edit file → submit → graded)
- [ ] A passing-path and a failing-path test exist, both driven through `GameSession.run_command()` plus loading a fixture file standing in for player-edited code
