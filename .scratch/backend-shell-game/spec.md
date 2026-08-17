Status: ready-for-agent

# Backend Shell Game — Spec

## Problem Statement

The user knows Python syntax but wants to learn backend engineering concepts (HTTP/APIs, databases/persistence, auth) hands-on rather than by reading. Existing tutorials are either passive (articles, videos) or disconnected exercises with no narrative or system to explore. The user wants something that feels like actually operating a backend system — diagnosing and fixing it — from a terminal, without committing to building a full web frontend right now.

## Solution

A personal, shell-based single-player game. The player is a newly-hired backend engineer who has just inherited an undocumented, half-broken system. They interact with it through a custom in-game REPL (a fictional shell) that runs game commands (`curl`, SQL-style queries, `cat /var/log/...`, `ps`, etc.) against a **real, in-process backend** — an actual small Flask app and an actual SQLite database, not a simulation. Some challenges instead drop the player into editing a real `.py` file (e.g. write a route handler, a query, an auth check), which the game then loads and runs.

Challenges are organized into a linear campaign of three chapters — HTTP/APIs, Databases/persistence, Auth — each with optional side-challenges drawing from a stretch list (async, caching, queues, rate-limiting, observability). A challenge is solved when the resulting system state matches what's expected (state-inspection grading), not by diffing the player's source code. Progress is saved locally across sessions. An optional AI helper (`ask <question>`), backed by the Claude API, explains concepts and errors in context without giving away solutions; it's fully disabled and free to ignore if no API key is configured.

The core game logic is architected so a future web frontend could reuse it, but building that frontend is explicitly out of scope for this spec.

## User Stories

1. As a learner, I want to launch a persistent in-game shell, so that I can explore a simulated-but-real backend system interactively.
2. As a learner, I want the shell to accept familiar-feeling commands (`curl`, SQL queries, `cat`, `ps`, `ls`), so that the experience maps to real backend/ops muscle memory.
3. As a learner, I want the backend behind the shell to be a real Flask app and real SQLite database, so that what I learn transfers directly to real backend work.
4. As a learner, I want a fictional framing (newly-hired engineer inheriting a broken system), so that exploring and fixing things feels motivated rather than arbitrary.
5. As a learner, I want a linear sequence of chapters (HTTP/APIs → Databases → Auth), so that concepts build on each other in a sensible order.
6. As a learner, I want each chapter to include a couple of optional side-challenges on stretch topics (async, caching, queues, rate-limiting, observability), so that I can go deeper without those topics blocking the main campaign.
7. As a learner, I want most challenges resolved by exploring/diagnosing via the REPL, so that the early game doesn't require me to write code for every single challenge.
8. As a learner, I want some challenges to require editing a real Python file (a route handler, a query, an auth check), so that I actually practice writing backend code, not just typing commands.
9. As a learner, when I submit a file-editing challenge, I want the game to load and execute my code against the real Flask/SQLite backend, so that my code has to actually work, not just look right.
10. As a learner, I want challenges graded by inspecting the resulting system state (DB contents, HTTP response codes, session/auth state), so that grading works consistently across both REPL-only and file-editing challenges, and doesn't require diffing my source code.
11. As a learner, I want my progress (completed chapters/challenges) saved locally between sessions, so that I don't lose progress when I close the terminal.
12. As a learner, I want to resume from where I left off when I relaunch the game, so that I don't have to replay completed challenges.
13. As a learner, I want a `hint` command with 2-3 progressive levels per challenge, so that I can get unstuck without being forced to look outside the game.
14. As a learner, I want hints to be free (no scoring penalty), so that using them doesn't feel like a punished last resort.
15. As a learner, I want an `ask <question>` command backed by an AI helper, so that I can get plain-language explanations of concepts or errors I don't understand.
16. As a learner, I want the AI helper to have context on my current chapter, challenge description, and recent shell output, so that its answers are relevant without me having to re-explain my situation.
17. As a learner, I want the AI helper to explain concepts rather than hand me the literal solution, so that using it doesn't defeat the point of the game (that's what `hint` is for).
18. As a learner, I want the game to work fully with `ask` disabled when no `ANTHROPIC_API_KEY` is configured, so that I (or anyone else) can play the game for free with zero required setup beyond installing it.
19. As a learner, I want a clear message when `ask` is unavailable (e.g. "AI helper not configured — set ANTHROPIC_API_KEY to enable"), so that I understand why the command isn't working rather than assuming it's broken.
20. As the developer of this game, I want to install it as a proper Python package with a console-script entry point, so that running it feels like using a real CLI tool rather than invoking a loose script.
21. As the developer of this game, I want challenges defined as plain Python classes (a `Challenge` base class with `setup()` and `check_state()`), so that challenge definitions are simple to write, extend, and read as reference code.
22. As the developer of this game, I want the game engine (`GameSession`) to expose a single command-dispatch entry point, so that both the REPL and file-editing challenges funnel through identical logic, and so that the whole game is testable through one seam.
23. As the developer of this game, I want the CLI to be the primary and only interface built right now (no forced core/CLI package split), so that early effort goes into making the game itself work rather than into speculative architecture for a web frontend that doesn't exist yet.
24. As the developer of this game, I want the design to avoid CLI-specific assumptions baked into challenge/grading logic (e.g. no `check_state()` implementation should call `input()`/`print()`), so that extracting a reusable core later, if a web frontend is ever built, doesn't require a rewrite.
25. As someone who might share this repo publicly, I want no secrets (API keys) committed to the repository, so that sharing the code doesn't leak credentials.
26. As someone who might share this repo publicly, I want intentionally-broken/vulnerable challenge code clearly documented as intentional teaching content, so that it isn't mistaken for a reference implementation to copy into real projects.

## Implementation Decisions

- **Engine seam**: A `GameSession` object is the single entry point for all player action. It exposes `run_command(text: str) -> CommandResult`. Both the REPL's input loop and the file-editing challenge flow (after loading and executing player-authored code) go through this same call — there is no second code path for "did the player's action count."
- **Backend fidelity**: `GameSession` owns a real, in-process Flask application instance and a real SQLite database (file-backed, scoped per save/profile). REPL commands like `curl`, `psql`-style queries, `cat /var/log/...`, and `ps` are implemented as shell-command handlers that operate against this real Flask app and SQLite DB — not against mock/fake objects.
- **Challenge model**: Challenges are plain Python classes subclassing a `Challenge` base with at minimum `setup(session)` (establishes starting state/scenario) and `check_state(session) -> bool` (or richer result) methods. No `input()`/`print()`/terminal-specific calls inside challenge or engine code — those belong exclusively to the CLI presentation layer.
- **File-editing challenges**: A subset of challenges specify a target file the player edits; the game loads that file as a module and invokes a designated entry point (e.g. a route-registration function, a query function) against the live Flask app/DB before running `check_state()`.
- **Chapter/campaign structure**: Chapters are ordered and linear: 1) HTTP/APIs, 2) Databases/persistence, 3) Auth. Each chapter has a main-line sequence of challenges plus 1-2 optional side-challenges pulled from the stretch list (async, caching, queues, rate-limiting, observability). Side-challenges do not block main-line progression.
- **Save/progress persistence**: A local JSON save file (e.g. under a user dotfile directory) records completed chapters/challenges and unlocks state, loaded on startup and updated as challenges are completed.
- **Hint system**: Each challenge defines 2-3 progressive hint strings, exposed via a `hint` command that advances one level per invocation. No scoring/cost impact.
- **AI helper**: An `AIHelper` interface with a single method, `ask(prompt: str) -> str`, implemented against the Anthropic Claude API by default. The `ask` REPL command builds its prompt from the current chapter/challenge context plus the player's question, with a system-level instruction to explain concepts/errors and redirect to `hint` rather than reveal the literal answer/expected state. If `ANTHROPIC_API_KEY` is not set, `ask` reports it's unavailable and names the env var, rather than erroring or silently failing; the rest of the game is unaffected.
- **Packaging**: Distributed as an installable package (`pyproject.toml`) with a console-script entry point (e.g. `pyshellgame`) rather than a bare `python -m`/script invocation.
- **Architecture posture**: Build CLI-first with no forced `core`/`cli` package split yet. The one hard constraint carried forward from this decision is the engine/challenge-code purity rule above (no terminal I/O outside the CLI layer) — that's what keeps a future extraction cheap without requiring the split now.

## Testing Decisions

- Tests drive the game exclusively through `GameSession.run_command()` — this is the one seam. A test issues one or more command strings (identical in form to what a player would type or what a file-editing challenge flow would produce) and asserts on the returned `CommandResult` and/or `challenge.check_state()` outcome.
- Tests must not assert on REPL text I/O (no capturing `print()` output as the source of truth) and must not reach around `GameSession` to poke the Flask app or SQLite connection directly — if a test needs to verify DB state, it does so by issuing a `run_command()` that reads that state back (matching how the game itself verifies state in `check_state()`), or through a `GameSession`-exposed accessor, not a raw DB connection grabbed out of band.
- Each `Challenge` subclass should have at least one test exercising a passing path (a command sequence that satisfies `check_state()`) and one failing path (a command sequence that does not).
- The `AIHelper` is tested behind its interface: tests use a fake/stub implementation of `ask(prompt) -> str` rather than making real API calls, so the test suite runs with no `ANTHROPIC_API_KEY` and no network access.
- There is no prior art in this codebase (repo is currently empty) — this is the first testing convention established for the project; later specs should follow it rather than introduce new seams.

## Out of Scope

- Building any actual web frontend (HTML templates, JS, a second presentation layer). The architecture should not actively prevent this later, but no web-facing code is part of this spec.
- Multiplayer, leaderboards, or any shared/competitive state — this is a single local player.
- Scoring/points systems beyond binary challenge completion tracking.
- Support for AI providers other than the Claude API (the `AIHelper` interface should make this possible later, but only one implementation ships now).
- Chapters/content beyond HTTP/APIs, Databases/persistence, and Auth, and their stretch-topic side-challenges. Additional chapters are future work.
- Deploying the in-process Flask app as an actual network-reachable service. It runs in-process for local play only.

## Further Notes

- Repo currently has no code, no `CONTEXT.md`, and no ADRs — this spec is the first substantive artifact. Whoever implements it should create `CONTEXT.md` entries for the domain vocabulary introduced here (`GameSession`, `Challenge`, `CommandResult`, chapter/side-challenge, `AIHelper`) as that vocabulary solidifies, per this repo's `docs/agents/domain.md`.
- Before any commit that could include a real API key (e.g. a local `.env` used for manual testing of the AI helper), verify `.gitignore` covers it and check `git status`/diff contents, not just filenames, before pushing — this repo doesn't have git initialized yet, so this should be set up as part of initial project scaffolding.
- Intentionally-broken/vulnerable code used as challenge content (e.g. a deliberately bad auth check to fix) should be flagged in-repo (e.g. a README note) as intentional teaching content, not a pattern to copy elsewhere.
