# 03 — Save/progress persistence

**What to build:** Progress survives closing and reopening the game. Completing the Chapter 1 challenge from ticket 02 is recorded to a local save file; relaunching the game loads that save and reflects the challenge as already completed rather than replayable from scratch.

**Blocked by:** 02

**Status:** done

- [x] A local JSON save file (under a user dotfile/profile location) records completed chapters/challenges
- [x] Completing a challenge updates the save file
- [x] Launching the game loads the save file if present and reflects prior completion state
- [x] A fresh save (no file present) starts the player at the beginning without erroring
- [x] A test verifies save/load round-trips correctly through `GameSession`, without asserting on raw file contents as the primary behavior under test
