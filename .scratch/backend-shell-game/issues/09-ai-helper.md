# 09 — AI helper (`ask` command)

**What to build:** An `ask <question>` REPL command backed by the Claude API. It builds context from the player's current chapter, active challenge description, and recent shell output, and is scoped (via its system instruction) to explain concepts/errors rather than reveal the literal solution — redirecting to `hint` instead. Fully optional: if `ANTHROPIC_API_KEY` isn't set, `ask` reports it's unavailable and names the env var, and the rest of the game is unaffected.

**Blocked by:** 02

**Status:** ready-for-agent

- [ ] An `AIHelper` interface exposes a single `ask(prompt: str) -> str` method
- [ ] A Claude API-backed implementation of `AIHelper` exists behind that interface
- [ ] The `ask` REPL command builds its prompt from current chapter, active challenge description, and recent shell output, plus the player's question
- [ ] The system-level instruction directs the helper to explain concepts/errors and redirect to `hint` rather than reveal the literal expected state/solution
- [ ] With no `ANTHROPIC_API_KEY` set, `ask` returns a clear "AI helper not configured — set ANTHROPIC_API_KEY to enable" message; no other game functionality is affected
- [ ] Tests for `ask` use a fake/stub `AIHelper` implementation — no real API calls, no network access required to run the test suite
