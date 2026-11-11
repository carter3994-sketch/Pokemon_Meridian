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
