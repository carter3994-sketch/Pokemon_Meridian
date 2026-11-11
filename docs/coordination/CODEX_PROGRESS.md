<!-- Preserved from PR #8 head 0613c38b77c2bdd5c3e1f1f515c5aa1ec1986961; prior testing is attributed to that session. -->
# Codex engineering progress

## Landing Camp verification and QA

- Replayed the exact ROM built at `f5815a20cb63959ad2999e6c51052124ed84e5ad` by the [original-art integration run](https://github.com/carter3994-sketch/Pokemon_Meridian/actions/runs/42923734899).
- Reached the camp through character setup at (12,23). Walked through HQ, research, medical, supply and living quarters, then verified each interior and return coordinate. The moved medical, supply and quarters doors return to (18,17), (34,14) and (38,23). Confirmed both tile banks and all 13 field palettes after returning outdoors. [Runtime evidence](../verification/landing_camp_f5815a20.json).
- Traced the [Town Design failure](https://github.com/carter3994-sketch/Pokemon_Meridian/actions/runs/42923734907) to the placeholder map being passed into the quality checks. The QA branch runs the current art conversion and asset validation before rendering, retains both repetition gates, and checks relevant PR changes. The local workflow steps passed using previously staged tileset inputs. The generated map and tile banks matched the published ROM build inputs byte for byte. [QA commit](https://github.com/carter3994-sketch/Pokemon_Meridian/commit/cf8411aeff836bc1419bf57276b77e6a211f097d).

## Engine audit

The repository contains Emerald expansion source. `src/main_menu.c` already routes the Meridian opening text after appearance and name selection. The checked-in `src/new_game.c` keeps the baseline spawn, and `scripts/register_landing_camp_prototype.py` supplies Landing Camp arrival in the integration build. The five current interiors are temporary layouts.

The replay covered one successful character setup path. Separate tests are needed for both appearance choices, name rejection, and save/load across opening events. The approved ship-to-medic beats should be implemented after the scene handoff, with the existing arrival check kept available for map QA.

## 2026-11-10 — Codex repository audit and registry repair

Base: `d43921da9f5dbb2effef8707508758069c31da57`; engineering commit: `bd8ac6dc`; branch: `fix/map-registry-null-connections`.

Fresh local audit reproduced a TypeError on valid Porymap `connections: null`. Fixed the null handling and replaced the no-op connection loop with registered map-ID lookup. CI now runs three isolated CLI regression cases (null, valid reference, invalid reference).

Executed `python3 -m unittest discover -s tests -v`: 3 passed. Executed `python3 tools/meridian_map_audit.py`: 935 maps, 785 layouts, zero errors. No Landing Camp maps are checked into this registry; the integration workflow generates them. This is source registry validation, not collision, warp, or emulator verification.

No ROM compiled or emulator launched this session. No ARM compiler found. A make dry run stopped on missing generated `tools/mapjson/mapjson`; it was not a compilation attempt. Work's PR #10 reports newer ROM verification separately; that report has not been replayed here. No map, art, gameplay script or creative design changed.

## Continued audit — warp validation and fresh ROM startup

Engineering commit `b612a675` extends PR #12 with static warp destination/index checks and explicit MAP_DYNAMIC exclusions. Seven tests pass; the 935-map source registry has 2,607 warps (64 dynamic) and no errors. Generated the current develop-based camp in a detached worktree, ran the existing engine asset validator successfully, then audited 941 maps / 2,622 warps with no errors. No generated art or map files committed.

Inspected successful source compilation CI at `65514db8`, run `42952413364`. Downloaded Work's successful integration ROM artifact `13824840223` from run `42948669070`, source `f966f929`; header and SHA-256 match. Bundled mGBA `-S 5` returned 0 within 30 seconds. Emulator diagnostics remain documented; this tests startup to first VBlank only. No local compilation, traversal, save/load or final visual verification claimed.

Full commands, counts, source distinctions and limitations: [evidence](../verification/codex_registry_b612a675.json). Next: run the registry CI on this update, reconcile open handoffs and preserve Work's map ownership.
