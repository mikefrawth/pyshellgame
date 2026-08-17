# 05 — File-editing challenge flow

**What to build:** The second challenge mode. A challenge can specify a target Python file the player edits directly (e.g. to write a route handler). The game loads that file as a module, invokes a designated entry point against the live Flask app/DB, and grades it via the same `check_state()` mechanism as REPL-only challenges. Demonstrated with one concrete example in the HTTP chapter.

**Blocked by:** 02

**Status:** done

- [x] A challenge type exists that names a target file and an expected entry point (e.g. a function the game calls after loading the module)
- [x] The game loads the player-edited file and invokes that entry point against the real, live Flask app (and DB, if relevant) owned by `GameSession`
- [x] Grading reuses `check_state()` — no separate/parallel grading path for file-editing challenges
- [x] One concrete file-editing challenge is implemented and playable end-to-end (edit file → submit → graded)
- [x] A passing-path and a failing-path test exist, both driven through `GameSession.run_command()` plus loading a fixture file standing in for player-edited code

## Comments

Implemented as `FileEditingChallenge` (`src/pyshellgame/challenge.py`) with `target_filename`/`entry_point`, plus `GameSession.workspace_dir`, `write_workspace_file()`, `load_player_module()`, and a `submit` verb in `run_command()` (`src/pyshellgame/session.py`). `submit` only runs the player's `register_routes(session)`-style entry point against the real `session.app`; grading still happens via the existing post-command `check_state()` call, same as every other command. Concrete example: `WhoAmIChallenge` in `src/pyshellgame/challenges/http.py`, which has the player register a `/whoami` route. `help` tells the player where their workspace file lives when the active challenge is file-editing. Tests: `tests/test_challenges_file_editing.py` (passing path, failing path, broken player code, submit on a non-file-editing challenge, setup() not clobbering an in-progress edit, `help` surfacing the file path).

Scope note: `GameSession` still defaults `self.challenge` to `HealthCheckChallenge` — there's no campaign/chapter sequencing yet to hand the player off to `WhoAmIChallenge` after chapter 1's first challenge. That's issue 06 (chapter1-completion)'s job; wiring multi-challenge progression here would preempt that design. `WhoAmIChallenge` is fully playable end-to-end (setup → edit → submit → curl → graded) once selected as `session.challenge`, exactly as `HealthCheckChallenge` was when issue 02 shipped it as the only active challenge.
