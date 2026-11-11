# Codex engineering progress

## Landing Camp verification and QA

- Replayed the exact ROM built at `f5815a20cb63959ad2999e6c51052124ed84e5ad` by the [original-art integration run](https://github.com/carter3994-sketch/Pokemon_Meridian/actions/runs/42923734899).
- Reached the camp through character setup at (12,23). Walked through HQ, research, medical, supply and living quarters, then verified each interior and return coordinate. The moved medical, supply and quarters doors return to (18,17), (34,14) and (38,23). Confirmed both tile banks and all 13 field palettes after returning outdoors. [Runtime evidence](../verification/landing_camp_f5815a20.json).
- Traced the [Town Design failure](https://github.com/carter3994-sketch/Pokemon_Meridian/actions/runs/42923734907) to the placeholder map being passed into the quality checks. The QA branch runs the current art conversion and asset validation before rendering, retains both repetition gates, and checks relevant PR changes. The local workflow steps passed using previously staged tileset inputs. The generated map and tile banks matched the published ROM build inputs byte for byte. [QA commit](https://github.com/carter3994-sketch/Pokemon_Meridian/commit/cf8411aeff836bc1419bf57276b77e6a211f097d).

## Engine audit

The repository contains Emerald expansion source. `src/main_menu.c` already routes the Meridian opening text after appearance and name selection. The checked-in `src/new_game.c` keeps the baseline spawn, and `scripts/register_landing_camp_prototype.py` supplies Landing Camp arrival in the integration build. The five current interiors are temporary layouts.

The replay covered one successful character setup path. Separate tests are needed for both appearance choices, name rejection, and save/load across opening events. The approved ship-to-medic beats should be implemented after the scene handoff, with the existing arrival check kept available for map QA.
