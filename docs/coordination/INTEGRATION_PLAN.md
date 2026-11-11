<!-- Preserved from PR #8 head 0613c38b77c2bdd5c3e1f1f515c5aa1ec1986961; prior testing is attributed to that session. -->
# Integration plan

`develop` is the integration branch. Use `creative/` for canon and design, `art/` for environment assets, and `feature/`, `fix/` or `qa/` for engineering. Use PRs for substantial changes. Check the status log, recent commits and active PRs before modifying shared files.

| Handoff | Owner | Dependency and review |
| --- | --- | --- |
| Approved story and worldbuilding | ChatGPT Project | PR #7 owns `CREATIVE_DECISIONS.md`. Keep that file on the creative PR to avoid a conflict. |
| Landing Camp art and layout | ChatGPT Work | Use approved references. Provide map IDs, door tiles, rendered evidence and asset checks. Coordinate shared map files with Codex before editing. |
| Gameplay and technical integration | Codex | Review warps and collisions against the current map. Record source commit, ROM build and actual emulator tests. |
| Releases and major creative choices | Project owner | Review the proposed creative changes or release candidate. |

The original-art integration workflow produces the current Landing Camp ROM and native asset artifacts. Town Design provides a separate map quality check. Rebuild and rerun the relevant checks whenever an integrated map, tileset or warp revision changes.

PR #7 is open. The coordination and Town Design changes are prepared separately on `qa/landing-camp-coordination`. Both target `develop`.

## Reconciliation after 2026-11-10 audit

- PR #8 already owns QA workflow and coordination updates. This branch preserves its CODEX_PROGRESS and INTEGRATION_PLAN content as the basis for additions; reconcile overlapping documentation when integrating either PR. Do not drop prior evidence.
- PR #10 owns art and integration workflow. This registry fix edits neither.
- PRs #7, #9 and #11 own creative handoffs. Their full CREATIVE_DECISIONS content must replace/reconcile the temporary index here during integration, retaining each approved record.
- This branch owns `tools/meridian_map_audit.py`, its regression tests, and registry-audit CI only. Integrate the registry fix independently; it does not require artwork approval.
- After map/art integration, run the original-art workflow and repeat actual camp traversal/door/return tests on the exact newly built ROM. Source registry success alone is insufficient.
