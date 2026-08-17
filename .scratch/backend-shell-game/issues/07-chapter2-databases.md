# 07 — Chapter 2: Databases/persistence

**What to build:** The second campaign chapter. `GameSession` gains a real SQLite database, and REPL commands can query/inspect it (e.g. a `psql`-style query command). Main-line challenges cover schema, queries, and transactions, using both REPL exploration and the file-editing flow (e.g. writing a query function). One optional stretch side-challenge (e.g. caching) is included.

**Blocked by:** 06

**Status:** ready-for-agent

- [ ] `GameSession` owns a real, file-backed SQLite database scoped per save/profile
- [ ] REPL commands exist to query/inspect DB state (real SQL against the real DB, not a fake)
- [ ] Main-line challenges cover schema design/inspection, queries, and transactions
- [ ] At least one main-line challenge uses the file-editing flow (e.g. player writes a query function that's loaded and executed)
- [ ] One optional stretch side-challenge is implemented (e.g. caching), clearly optional
- [ ] Chapter 2 challenges integrate with save/hint systems from prior tickets
- [ ] Passing- and failing-path tests exist for each new challenge, driven through `GameSession.run_command()`
