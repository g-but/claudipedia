# AGENTS.md

> Universal guide for AI coding agents. Works with Claude Code, Cursor, GitHub Copilot, OpenAI Codex, Gemini, and other AI tools.

---

## Project Overview

<!-- CUSTOMIZE: Add 1-2 sentences describing your project -->

---

## Quick Start

```bash
npm install
npm run dev
```

<!-- CUSTOMIZE: Update commands for your project -->

---

## Code Style

<!-- Don't add style rules here - use linters instead -->
<!-- LLMs should follow existing code patterns in the codebase -->

**Principles:**
- Follow existing patterns in the codebase
- Run linters before committing
- Keep changes minimal and focused

---

## Testing

```bash
npm test
```

**Before committing:** Ensure tests pass.

---

## Project Structure

<!-- CUSTOMIZE: Add your project structure -->

```
project/
├── src/           # Source code
├── tests/         # Test files
├── docs/          # Documentation
└── package.json
```

---

## Key Files

| File | Purpose |
|------|---------|
| `.claude/CLAUDE.md` | Claude Code instructions |
| `.cursor/rules/` | Cursor IDE rules |
| `docs/BEST_PRACTICES.md` | Coding principles |

---

## Security

- Never commit `.env` files
- Validate all inputs
- Use environment variables for secrets

---

**Last Updated:** <!-- DATE -->
