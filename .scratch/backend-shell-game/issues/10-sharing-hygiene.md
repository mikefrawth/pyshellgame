# 10 — Sharing hygiene: git init, .gitignore, README notes

**What to build:** The repo is safe and clear to share publicly. Git is initialized, secrets/env files are ignored, and the README documents how to configure the AI helper's API key and flags any intentionally-broken/vulnerable challenge code as deliberate teaching content rather than a reference implementation.

**Blocked by:** 01, 09

**Status:** ready-for-agent

- [ ] Git is initialized for the repo
- [ ] `.gitignore` excludes local env files (e.g. `.env`) and any local save-file paths that shouldn't be committed
- [ ] README documents setting `ANTHROPIC_API_KEY` to enable the AI helper, and that the game runs fully without it
- [ ] README includes a clear note that some challenge code is intentionally broken/vulnerable by design, for teaching purposes, and should not be copied into real projects
- [ ] A check (manual or scripted) confirms no secrets are present in any committed file before the first commit
