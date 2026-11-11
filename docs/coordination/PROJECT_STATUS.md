# Pokémon: Meridian — Shared Project Status

**Primary maintainer:** Codex
**Updated:** 2026-11-10
**Authority:** [MASTER_DIRECTIVE.md](MASTER_DIRECTIVE.md)

## Current milestone
Landing Camp production environment and Chapter 1 engineering remain in progress. The camp still uses debug arrival and temporary interiors. Final playability and visual acceptance are incomplete.

## Verified engineering state
- `develop` inspected at `d43921da9f5dbb2effef8707508758069c31da57`.
- PR #12, `fix/map-registry-null-connections`: `bd8ac6dc` fixes a reproduced null-connections crash; `b612a675` validates static warp destination maps and indexes, while explicitly counting dynamic warps as requiring runtime verification.
- Seven regression tests pass locally. Source audit: 935 maps, 785 layouts, 266 connections, 2,607 warps; 64 dynamic warps excluded from static destination resolution; zero errors.
- Fresh generated Landing Camp audit in an isolated checkout at `b612a675`: 941 maps, 791 layouts, 2,622 warps, zero errors. Existing static collision/reachable-door/paired-return checks pass. This generated map uses `develop` artwork, not Work's newer waterfront branch.
- Source CI compiled a ROM successfully at `65514db8` ([run](https://github.com/carter3994-sketch/Pokemon_Meridian/actions/runs/42952413364)). This workflow does not register playable Landing Camp. Local compilation was not performed.

## Latest Landing Camp ROM evidence
Work's integration CI succeeded at `f966f929efce985e98e155249ed213887d8b6bd8` ([run](https://github.com/carter3994-sketch/Pokemon_Meridian/actions/runs/42948669070)). Codex downloaded artifact `13824840223`, checked the GBA header and SHA-256 `0d5285a706aabb8a673ec9778d8dd10304e90755ed7bc52d6cf32f5c2fdcdd00`, and ran bundled mGBA to first VBlank with exit code 0. Startup produced emulator diagnostics documented in the evidence record; these are not claimed resolved.

Work reports dock/collision and five building round trips on that ROM. Those gameplay tests were not repeated by Codex this session. Later art head `49136383` has not been replayed here. See [fresh audit/startup evidence](../verification/codex_registry_b612a675.json) and attributed prior tests in CODEX_PROGRESS.md.

## Owners and active PRs
| Owner | Active work | Branch / PR |
| --- | --- | --- |
| ChatGPT Work | Landing Camp art, waterfront and visual QA | `art/landing-camp-waterfront`, draft #10 |
| Codex / earlier QA session | Town Design QA and prior coordination records | `qa/landing-camp-coordination`, #8 |
| Codex / this session | Registry/warp validation and consolidated status | `fix/map-registry-null-connections`, #12 |
| ChatGPT Project | Approved Guardian/city canon | `creative/approved-guardian-city-lore`, #7 |
| ChatGPT Project | Approved father legacy and mentor arc | `creative/approved-father-legacy`, #9 |
| ChatGPT Project | Approved Scene 4 / journal gate specification | `creative/approved-medical-awakening-scene`, #11 |

No PR merged in this session. Coordination content overlapping #8 and full creative records on #7/#9/#11 need reconciliation; preserve their evidence and approvals. All six coordination paths exist on this branch.

## Blockers and next priorities
- **Work:** provide permanent medical interior and event positions for Scene 4; maintain current rendered/gameplay evidence and obtain final visual approval.
- **Codex:** integrate/reconcile QA and coordination records; test exact new ROM after any map integration, including doors, collisions and save/load. Implement approved Scene 4 after the environment handoff. Keep debug camp entry available for QA.
- **ChatGPT Project / owner:** approve Scene 5 and remaining dialogue as needed; preserve precise approved specifications. No creative approval is required for the registry audit changes.
- The generated camp source audit and startup smoke are limited checks, not a completed gameplay or visual test. Save/load, final camp appearance, permanent interiors, provision-store/cave entrances and full opening remain unfinished.
