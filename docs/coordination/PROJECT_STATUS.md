# Pokémon: Meridian — Shared Project Status

Codex maintains this log under the [master directive](MASTER_DIRECTIVE.md).

## Current milestone

Landing Camp production and Chapter 1 engineering are in progress. The camp has a playable verification build with five working building entrances. The full approved environment, permanent interiors, provision-store and cave entrances, and Chapter 1 story sequence are still in development.

## Verified build and gameplay

- The latest successful Landing Camp integration ROM came from commit [f5815a20](https://github.com/carter3994-sketch/Pokemon_Meridian/commit/f5815a20cb63959ad2999e6c51052124ed84e5ad). The [original-art integration run](https://github.com/carter3994-sketch/Pokemon_Meridian/actions/runs/42923734899) and [source build](https://github.com/carter3994-sketch/Pokemon_Meridian/actions/runs/42923734904) passed.
- In the compiled integration ROM, mGBA reached arrival after character setup. All five buildings passed entry and return using walking inputs. Both 16 KiB graphics banks and all 13 map palettes matched the build artifacts after the return trips. See the [runtime record](../verification/landing_camp_f5815a20.json).
- The separate [Town Design run](https://github.com/carter3994-sketch/Pokemon_Meridian/actions/runs/42923734907) failed both terrain repetition gates while rendering the placeholder map. The correction in this PR runs those checks on the integrated art and passes locally. GitHub check status is tracked on the PR.

## Ownership and active integration

| Environment | Current responsibility | Next handoff |
| --- | --- | --- |
| ChatGPT Project | Approved canon, Chapter 1 treatment and dialogue | Maintain the approved canon in [PR #7](https://github.com/carter3994-sketch/Pokemon_Meridian/pull/7), then publish the approved ship-to-medic scene specifications. |
| ChatGPT Work | Landing Camp visuals and map integration | Continue the waterfront and ruins arrangement, interior art, and visual comparison to the approved reference. Supply actual render evidence and walkable entrances. |
| Codex | Engine, progression, warps, builds and verification | Maintain the coordination log, review the Town Design check, and prepare reproducible tests for the opening and map transitions. |

`develop` is the integration branch. The inspected base was `d43921da`. Creative PR #7 uses `creative/approved-guardian-city-lore`. The QA and coordination changes use `qa/landing-camp-coordination`. See the [integration plan](INTEGRATION_PLAN.md) for dependencies and ownership boundaries.

## Pending dependencies and decisions

- The owner approved the building placement shown in the `f5815a20` render. The waterfront, ruins, permanent interiors and final map appearance still need visual review. See the [approval register](../AREA_APPROVAL_REGISTER.md).

- The current ROM reaches the outdoor map through the build-time registration script. The ship, storm, blackout, and medical-facility wake-up need authored maps and story events.
- Chapter 1 has owner-approved story beats. Final dialogue, cutscene staging, and the exact Guardian encounter designs need a creative handoff. Track specifics in [creative requests](CREATIVE_REQUESTS.md).
- The current build covers five building round trips. Save/load across story flags, alternative character setup paths, and the complete opening remain unverified.

See [engineering progress](CODEX_PROGRESS.md) and [visual progress](WORK_PROGRESS.md) for test scope and the current map checkpoint.
