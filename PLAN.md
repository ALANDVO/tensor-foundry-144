# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

core-skeleton

## Roadmap

### core-skeleton — Core FastAPI/React skeleton with one end-to-end workflow

Status: in_progress

Acceptance:
- FastAPI backend runs and serves API
- React frontend builds and loads
- Single end-to-end workflow works (e.g., health check or simple API call)
- Install instructions documented
- Basic tests pass

Implementation: `backend/main.py`, `backend/requirements.txt`, `frontend/package.json`, `frontend/src/App.tsx`, `frontend/src/main.tsx`, `frontend/index.html`, `frontend/vite.config.ts`, `README.md`, `PLAN.md`

Tests: `backend/tests/test_health.py`, `frontend/src/App.test.tsx`

### ponytail-config — Ponytail configuration system (modes, settings, persistence)

Status: planned

Acceptance:
- Configuration file read/write
- Mode switching (lite, standard, ultra, off)
- Environment variable overrides
- Settings persisted across sessions

### hooks-system — Hooks system for AI agent integration

Status: planned

Acceptance:
- SessionStart hook injects context
- UserPromptSubmit hook tracks prompts
- PreToolUse/PostToolUse hooks for tool tracking
- Hook output format compatible with Claude Code, Copilot, etc.

### band-statusline — Band statusline UI (compact/detailed modes)

Status: planned

Acceptance:
- Compact single-line display
- Detailed multi-line display
- Mode indicator, cost, time, review/audit/board buttons
- Desktop app layout fix (no unwanted wrapping)

### codebase-map — Codebase map injection at session start

Status: planned

Acceptance:
- Generates repository map on SessionStart
- Configurable size via PONYTAIL_MAP_CHARS
- Can be disabled via PONYTAIL_MAP=0
- Works with Claude Code, Codex, Copilot CLI, Cursor

### gitattributes-ci — Git attributes and cross-platform CI

Status: planned

Acceptance:
- .gitattributes with LF enforcement
- CI matrix for ubuntu-latest and windows-latest
- Tests pass on both platforms

