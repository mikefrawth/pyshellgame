# 02 — Chapter 1 core: first real HTTP challenge, end-to-end

**What to build:** The first playable challenge, fully wired through a real backend. `GameSession` now owns a real, in-process Flask app. REPL commands like `curl` operate against that live app. A `Challenge` base class (`setup()`, `check_state()`) exists, and one concrete HTTP-themed challenge is implemented and playable start to finish: the player explores/diagnoses via REPL commands, and the game reports pass/fail based on inspecting resulting system state (e.g. an HTTP response code or body), not by diffing anything the player typed.

**Blocked by:** 01

**Status:** done

- [x] `GameSession` owns a real in-process Flask application instance (no mocks/fakes standing in for it)
- [x] A `curl`-style REPL command sends real requests to that Flask app and returns real responses through `CommandResult`
- [x] A `Challenge` base class defines `setup(session)` and `check_state(session)`, with no terminal I/O inside either
- [x] One concrete HTTP challenge is implemented (e.g. diagnose and observe a misbehaving endpoint) and is playable via REPL commands alone
- [x] The challenge resolves via state-inspection: `check_state()` inspects live Flask/response state, not player-typed text
- [x] A passing-path test and a failing-path test both exist for this challenge, driven only through `GameSession.run_command()`
