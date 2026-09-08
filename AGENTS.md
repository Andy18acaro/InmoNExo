# AGENTS.md

Este directorio es **un proyecto independiente**, no la carpeta madre.

- Git: solo aquí. No hagas commit en `E:\DEV`.
- Shipping: sigue el skill `ship` (checklist: corre, README, sin secretos, commit de este repo).
- Si el usuario quiere otro proyecto: `proj new <nombre>`, no anides un segundo producto dentro de este.

CLI-first: WezTerm → PowerShell → `cproj` / `agent`.

## Agent skills

### Issue tracker

Local markdown under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context: root `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.

Engineering flow (mattpocock/skills): `grill-with-docs` → `to-spec` → `to-tickets` → `implement` (`tdd` + `code-review`). Router: `ask-matt`.
