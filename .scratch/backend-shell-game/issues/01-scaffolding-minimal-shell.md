# 01 — Project scaffolding & minimal playable shell

**What to build:** An installable Python package with a console-script entry point that launches a minimal but real interactive shell. Running the game starts a `GameSession`, accepts a typed command, dispatches it through `GameSession.run_command()`, and prints the resulting `CommandResult`. At least one trivial command (e.g. `help` or `look`) works end-to-end. This is the foundation every later ticket builds on — no chapters, no Flask/SQLite backend, no persistence yet.

**Blocked by:** None — can start immediately

**Status:** done

- [x] `pyproject.toml` defines the package and a console-script entry point (e.g. `pyshellgame`)
- [x] Installing the package (`pip install -e .`) and running the entry point launches an interactive REPL loop
- [x] `GameSession.run_command(text: str) -> CommandResult` exists and is the sole dispatch path the REPL calls — no game logic lives directly in the REPL's input loop
- [x] At least one working command demonstrates the full loop: input → `run_command` → `CommandResult` → printed output
- [x] No `input()`/`print()` or other terminal-specific calls exist inside `GameSession` or command-handling logic — only in the CLI presentation layer
- [x] A basic test exercises the shell purely through `GameSession.run_command()`, with no REPL I/O captured as the source of truth
