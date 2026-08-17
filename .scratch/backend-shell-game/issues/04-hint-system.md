# 04 — Hint system

**What to build:** A `hint` REPL command that gives the player a progressive nudge on the currently active challenge. Each `hint` invocation advances one level (up to that challenge's max, 2-3 levels), with no scoring or completion penalty.

**Blocked by:** 02

**Status:** ready-for-agent

- [ ] `Challenge` supports defining 2-3 progressive hint strings
- [ ] The `hint` command returns the next hint level for the currently active challenge on each invocation
- [ ] Requesting a hint beyond the last level returns the final hint again (or an appropriate "no more hints" message) rather than erroring
- [ ] Using `hint` has no effect on challenge completion/scoring state
- [ ] A test drives `hint` through `GameSession.run_command()` and asserts on returned hint content/progression
