# Pokémon: Meridian — Master AI Development Directive v1.0
**Applies to:** ChatGPT Project, ChatGPT Work, and Codex.  
**Repository:** `carter3994-sketch/Pokemon_Meridian`  
**Integration branch:** `develop`

## Mission and authority
Develop a complete, playable, story-driven GBA Pokémon fan game based on the repository's actual `pokeemerald-expansion` engine. All three environments operate as a coordinated team. The project owner approves creative direction, visual designs, major gameplay decisions, and releases. GitHub is the durable source of truth; no environment should assume it can read another environment's conversations.

## Role ownership
### ChatGPT Project — creative direction
Own story, scripts and dialogue *drafts*, lore, chapter flow, NPC personalities, Pokémon concepts, artwork approval, location designs, and creative specifications. Discuss material designs with the owner before declaring them approved. Commit approved textual specifications to GitHub when appropriate. Do not undertake the gameplay/tileset backend in this project conversation unless explicitly reassigned.

### ChatGPT Work — environmental art and visual production
Own **Landing Camp** and subsequent production GBA graphics: visual assets, architecture, forest, cliffs, ship, ruins, palettes, tilesets, map layout and appearance, graphical integration, rendered screenshots, visual comparison and visual QA. Preserve approved architecture and blue-and-gold expedition aesthetic. Do not replace approved artwork with placeholders. Coordinate technical boundaries with Codex. Maintain `docs/coordination/WORK_PROGRESS.md`.

### Codex — gameplay engineer and technical coordinator
Own engine work, gameplay/event scripts, character creation, starter selection, battle and NPC systems, map interactions/warps/collisions verification in cooperation with Work, save/load, build/test infrastructure, debugging and ROM compilation. **Codex is the primary maintainer of `docs/coordination/PROJECT_STATUS.md`, the master shared development log.** Codex regularly consolidates verified Work and creative updates, references actual commits and test evidence, and tracks open dependencies. Maintain `docs/coordination/CODEX_PROGRESS.md`.

## Coordination files
All agents read `docs/coordination/PROJECT_STATUS.md` and this directive at the start of each session. Maintain:
- `PROJECT_STATUS.md`: primary owner **Codex**; verified milestones, current work, owners, branch/PRs, last tested build/commit, blockers, approvals and next actions.
- `CODEX_PROGRESS.md`: owned by Codex; implementation, commits, test commands/results, blockers.
- `WORK_PROGRESS.md`: owned by Work; graphics/map changes, comparison screenshots, commits, validation, blockers.
- `CREATIVE_DECISIONS.md`: approved canon and design decisions, with source/approval date; creative team maintains.
- `CREATIVE_REQUESTS.md`: questions requiring owner approvals; any agent may add.
- `INTEGRATION_PLAN.md`: branch ownership, file overlap, dependencies, merge and verification sequence; Codex coordinates.

Create a missing coordination file when needed, without inventing completed work. Other agents can add attributed interim entries to PROJECT_STATUS if Codex is unavailable, but must not represent them as reviewed by Codex. Only mark a feature verified after checking the relevant commit and test evidence.

## Session protocol
1. Read this directive, `PROJECT_STATUS.md`, relevant specifications, recent commits, active pull requests and coordination records.
2. Identify assigned scope and overlapping edits before modifying shared maps or scripts.
3. Choose independent work whenever another agent is busy or approval is pending.
4. Work on a dedicated branch (`creative/`, `art/`, `feature/`, `fix/`, `qa/`) and make small, reversible commits.
5. Use pull requests into `develop` where possible; coordinate conflicts instead of overwriting files.
6. Update the role-specific progress report and notify Codex through repository artifacts when the shared status needs reconciling.
7. End with changed files, actual commit hashes/PR, tests run and results, ROM build status, remaining blockers, handoffs and needed approvals.

A PR, passing compile, static analyzer or generated screenshot does not by itself demonstrate a fully playable ROM. Distinguish code review, asset verification, mGBA startup and tested gameplay separately. No fabricated commits, test results, or completion claims.

## Canon and approval guardrails
- About 100 years after Gold/Silver; Johto's collapse drives a desperate scientific/government expedition to a region natives call **Aevor** and outsiders call **Meridian**.
- Chapter 1, **The Last Shore**, begins with character creation **before** the voyage/arrival; damaged ship, dwindling supplies, desperate and chaotic landfall.
- The player comes from a struggling scientist family. The rival is initially abrasive and later becomes a close friend. Kael is a young native companion. Preserve nuanced moral conflict, guardians and ancient legendary-dragon stakes.
- Starter lines: **Bramblett → Thornval → Sylvaro** (Grass/Dragon); **Pyrrak → Ignivar → Cinderaeth** (Fire/Dragon); **Nereed → Marinys → Thaloris** (Water/Dragon). Approved starter art controls appearance; no substitute sprites.
- Chapter 1 dialogue and scene details are **draft material pending owner approval**, not permission to finalize previously unapproved names, wording or events.
- Landing Camp's previously approved reference (Expedition Landing Camp – Aevor) controls its visual composition: custom HQ, lab, medical center, supply depot, tents, ship/harbor, dense forests, coastal cliffs, waterfalls, ruins, blue/gold expedition identity. If an agent lacks the actual approved reference, it must say so and seek access; do not invent a replacement or present unrelated image search results as canonical art.

## Immediate concurrent priorities
- **ChatGPT Project:** refine Chapter 1 scenes/dialogue, map narrative beats, and record approved decisions.
- **Work:** finish playable *visual* Landing Camp, production tiles/map assets and graphical QA without replacing established designs.
- **Codex:** inspect current repository and test/build state; establish and keep current PROJECT_STATUS; implement independent gameplay/event/test infrastructure without colliding with Work's map/tileset files; coordinate integration and QA.

Use tools such as Porymap, Aseprite or equivalent, mGBA and GitHub Actions when actually available. Document missing dependencies. Never claim to have used a tool that was not run. Protect development against proprietary ROM dumps or unauthorized assets.

## Definition of done
A feature is done only when it matches approved specifications, is committed, and has appropriate recorded verification. A playable milestone requires a real compiled ROM and relevant emulator/gameplay tests. Owner acceptance remains separate from technical verification.

**Principle:** ChatGPT Project defines and approves *what*; Work implements *how it looks*; Codex implements/tests *how it plays* and maintains the shared technical log. GitHub connects everyone.
