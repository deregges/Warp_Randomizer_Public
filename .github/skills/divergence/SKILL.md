---
description: 'Diagnose and fix Platinum warp-randomizer regression divergences between the zone-accessibility model and the reference (main) flat-accessibility model. Use when a Platinum regression fixture fails, when randomize() returns False for a seed, or when zones-model output must be made byte-identical to main. Provides tooling under scripts/divergence/.'
---

# Warp Randomizer — Regression Divergence Analysis

Use this skill when the Platinum regression test (`../../../tests/test_platinum_regression.py`)
fails, when `randomize()` returns `False` for a seed, or when you must make the
**zone-accessibility** refactor reproduce the **reference `main`** (flat
`map_warp_accessibility`) output byte-for-byte.

The tooling lives in `../../../scripts/divergence`. Prefer it over ad-hoc scripts.

## Approval guard

YOU ARE ONLY ALLOWED TO MAKE UNSUPERVISED CHANGES ON PlatonumWarpMapInfo#zone_accessibility or PlatonumMapResources.json.  
ANY OTHER CHANGE NEEDS INTERACTIVE APPROVAL WITH DESCRIPTIVE USE-CASE AND EXPLANATION OF WHY IT CANNOT BE DONE IN 
PlatonumWarpMapInfo#zone_accessibility OR PlatonumMapResources.json.

---

## 1. The system (what you're debugging)

**Goal of the refactor.** `main` describes map reachability with flat tables
(`map_warp_accessibility`, `map_to_map_warp_accessibility`,
`non_navigable_connections`, `connection_to_connection_rules`, and per-map HM
lists like `surf_needed`). The `zones-model` branch replaces these with a single
`zone_accessibility` table per map. The refactor is meant to be **behaviour
preserving**: given the same seed it must consume the PRNG identically and emit
identical `warps.txt`/`routes.txt`. Any reachability difference changes the PRNG
stream and the output.

**Pipeline** (`../../../RandomizerUtils/Randomizer.py`):
1. `load_map_data()` reads warps/connections from the ROM (identical in both
   models — only the *accessibility metadata* differs).
2. `build_available_warps` → the pool of warps to randomize; `remove_pair_warps`
   collapses adjacent "paired doors".
3. `map_warp_divide` classifies every warp as an **end** (dead end) or a
   **connect** (leads onward). `select_random_warp` uses these lists.
4. Main loop: `build_warps_to_randomize` walks reachability from the start map to
   produce `warps_to_randomize` (the reachable, still-unassigned "pool"), then
   `select_random_warp` picks a **start** from the pool and an **end** from
   `available_warps`, pairs them, and repeats until the pool empties.

**The PRNG** (`../../../RandomizerUtils/RandomGenerator.py`) is a tiny LCG. Each
`random()` advances state once and is appended to `rng.created`, so
`len(rng.created)` is the *true* number of state advances. `choice(seq)` returns
`seq[randint() % len(seq)]` — **one** advance, and the index depends on
`len(seq)`. Identical PRNG state + identical list ⇒ identical pick. So a
divergence means either the list differed (reachability) or the state already
drifted (a previous step consumed a different number of draws).

**Zone model** (`../../../nds/gen4/PlatinumWarpMapInfo.py`, `USES_ZONE_ACCESSIBILITY = True`):
- `zone_accessibility[map] = {'zones': [...], 'rules': {...}}`.
- A **zone** is a list of members that are mutually reachable. A member is a warp
  id (`int`) or a connection's destination map name (`str`).
- `rules[from_zone] = [ZT(to_zone, flag)]` allow crossing between zones, gated by
  a flag bitmask (`fl(SURF_FLAG)` etc.; `0` = ungated). `reachable_zone_ids`
  BFS-follows rules whose flags are currently satisfied.
- Unlisted connection members default to **warp 0's zone** and are freely
  traversable — a frequent source of missing gates.

---

## 2. The tooling

All commands are run from the repo root. The reference recording uses a
throwaway `git worktree`, so a clean working tree helps.

```bash
# Main tool: record current tree + reference ref, classify the FIRST divergence.
python scripts/divergence/analyze.py compare --seed 1
python scripts/divergence/analyze.py compare --seed 1 --ref main --show-pool

# Inspect WHY a map is / isn't reachable at a step. Run in BOTH checkouts and
# compare the "neighbour_reachable" flags to find the edge one model traverses
# and the other blocks.
python scripts/divergence/inspect_reach.py replay 1 37 Map_Celestic_Town_00 Map_Route_210_05

# Dump a map's warp data + zone/rules/pair structure (or flat accessibility on main).
python scripts/divergence/inspect_reach.py dumpmap Map_Route_210_05

# Lower level: record a single tree to JSON, or diff two recordings.
python scripts/divergence/analyze.py record --seed 1 --out cur.json
python scripts/divergence/analyze.py diff --ref-json main.json --cur-json cur.json
```

`compare` prints, in order: run summaries, any `map_warp_divide` ends/connects
difference, the first PRNG-advance divergence (true drift origin), and the first
**output** divergence classified into one of the kinds below, with a recommended
`inspect_reach` probe. `../../../scripts/divergence/record_seed.py` and `../../../scripts/divergence/inspect_reach.py` are self-contained
so `../../../scripts/divergence/analyze.py` can copy the recorder into the reference worktree.

To run the reference in a worktree yourself:
`git worktree add ../ref main` then run `../../../scripts/divergence/inspect_reach.py` inside `../ref`;
remove with `git worktree remove --force ../ref`.

---

## 3. Workflow

1. **Reproduce**: `python -m pytest tests/test_platinum_regression.py -x -q`.
   A failing fixture writes `tests/actual/platinum_seed_matrix/case_XXX/` with
   `ERROR.txt` / `randomization_status.txt` (a `randomize_returned: False` means
   the seed got *stuck* — an unassignable pocket of warps).
2. **Classify**: `analyze.py compare --seed <seed>` (the fixture's `seed.txt`).
3. **Probe** the maps named in the report with `inspect_reach.py replay ... `
   in **both** checkouts; the differing `neighbour_reachable` edge is the bug.
4. **Fix** the zone data (or predicate) — see §5. Never reintroduce the `*_needed`
   lists; express gates as zones + rules. If the fix would add any new zone-model
   fact or mechanism, stop and get explicit approval first (see approval guard
   above), even if the addition would live outside `zone_accessibility`.
5. **Re-run** `compare`; the first divergence should move to a *later* step.
   Iterate. When `compare` reports "identical pairings", the seed matches.
6. Repeat for other failing seeds (fixes usually generalize across seeds).

Progress is measured by how deep the first divergence is (e.g. step 18 → 37 →
115). A fix that moves it later is real progress even if the seed isn't done.

---

## 4. Divergence kinds (what the classifier reports)

- **REACHABILITY-CONTENT** — the reachable pools differ. `OVER-reach` = a warp
  reachable in the zone model but not main (a gate main enforces is **missing**
  in the zone data). `UNDER-reach` = reachable in main but not zones (the zone
  data **over-gates**). Most actionable; the report lists the extra/missing warps
  and a probe command. Start here.
- **POOL-ORDERING** — same warps, different order. `build_warps_to_randomize`
  traversal order differs. Rare; usually a symptom of an earlier content fix
  needed elsewhere.
- **END-SELECTION** — same start, different end; the end-selection loop rejected a
  different number of candidates (see the `REF/CUR draws` counts). Caused by
  accept/reject predicates differing: usually the `map_warp_divide` ends/connects
  classification (printed above the step) or `is_map_progressable` /
  flag-event predicates for a candidate.
- **RNG-DRIFT** — identical pool but different start; the PRNG already drifted in
  an earlier step. Use the "first PRNG-advance divergence" line to find the true
  origin step, then analyze THAT step (it will be an END-SELECTION there).

---

## 5. Common root causes and their zone-native fixes

### A. Orphan warp — zone lists a warp id that doesn't exist / omits the real one
**Signature:** seed gets *stuck* (`randomize` returns False); the stranded warp is
`in_zones=True` but `get_member_zone(...) is None`. A map with only warp 0 whose
`zones` reference `[2]` or `[1]`.
**Cause:** a typo in `zone_accessibility` — the real warp is left out of every
zone, so it's "undefined" for randomization, is never paired, and pollutes the
pool.
**Fix:** put the real warp id into a zone.
```python
# Map_Mount_Coronet_Floor09_00 has only warp 0:
'zones': [[0], ['Map_Mount_Coronet_Floor09_01']],   # was [[2], [...]]
```

### B. Missing per-map HM gate (fully-HM route) — OVER-reach
**Signature:** OVER-reach into a water/forest/rock-climb cluster; `dumpmap` shows
one merged zone `[[connA, connB]]` with `rules: {}`.
**Cause:** in main the map is in `surf_needed`/`cut_needed`/etc.
(`is_map_progressable` blocks traversal without the HM). The conversion merged the
connections into one free zone.
**Fix:** split each connection into its own zone linked by the HM flag.
```python
'Map_Route_219_00': {
    'zones': [['Map_Sandgem_Town_00'], ['Map_Route_220_00']],
    'rules': {0: [ZT(1, fl(SURF_FLAG))], 1: [ZT(0, fl(SURF_FLAG))]},
},
```

### C. HM-gated map that ALSO has warps — UNDER-reach if over-gated
**Signature:** after fixing B, an UNDER-reach appears: the gated map's *warp* is in
main's pool but not the zone pool.
**Cause:** the flat model adds a gated map's warps to the pool *before* blocking
its exits, so warps are standable without the HM; only connection→connection is
gated. Putting the warp in a gated zone is too strict.
**Fix:** connections reach the standable warp for **free**; leaving the warp to any
connection needs the HM (connection↔connection then routes through the warp).
```python
'Map_Route_210_05': {            # rock-climb terrain, warp 0 + 3 connections
    'zones': [[0], ['Map_Route_210_00'], ['Map_Route_210_04'], ['Map_Route_210_01']],
    'rules': {
        0: [ZT(1, fl(ROCKCLIMB_FLAG)), ZT(2, fl(ROCKCLIMB_FLAG)),
            ZT(3, fl(PSYDUCK_FLAG) | fl(ROCKCLIMB_FLAG))],
        1: [ZT(0, 0)], 2: [ZT(0, 0)], 3: [ZT(0, 0)],   # conn -> warp is free
    },
},
```

### D. Non-navigable connection — OVER-reach
**Signature:** OVER-reach where the entered map is reached via a connection main
lists in `non_navigable_connections`; `inspect_reach replay` shows
`neighbour_reachable=True` in zones, `False` in main for that edge.
**Cause:** the zone model ignores `non_navigable_connections`; an unlisted
connection member defaults to warp 0's zone and is freely traversable.
**Fix:** add the blocked connection as an **isolated zone** (no rules) on both
sides so it can never be traversed.
```python
'Map_Canalave_City_01': { 'zones': [[0, 1, 3, 4], [2, 5], ['Map_Route_218_00']] },
'Map_Route_218_00':      { 'zones': [[0, 1], ['Map_Route_218_01'], ['Map_Canalave_City_01']],
                           'rules': {0: [ZT(1, fl(SURF_FLAG))], 1: [ZT(0, fl(SURF_FLAG))]} },
```

### E. `is_map_progressable` doesn't honor gates — END-SELECTION
**Signature:** END-SELECTION divergence where the wrongly-accepted end is a warp on
an HM-gated map (e.g. `Route_207_01` when BIKE isn't held).
**Cause:** the zone `is_map_progressable` only checked `get_member_zone(...) is not
None`, ignoring flag gates. main rejects a candidate on a not-yet-progressable map.
**Fix (already applied):** `is_map_progressable(map, accessible, warp_id)` returns
True only if, from `warp_id`'s zone, some *other* member is reachable under the
currently-satisfied flags (via `reachable_zone_ids`). Dead-end warps behind an
unmet gate are not progressable — no `*_needed` list needed.

### F. `map_warp_divide` classification mismatch — END-SELECTION
**Signature:** `compare` prints an ends/connects difference; END-SELECTION
divergences whose accepted end sits on a map in the ends/connects diff.
**Cause:** the zone-access branch of `map_warp_divide` filters by
`available_warp_ids` (post-pair-removal) and keys off `zone_member_has_accessible_exit`,
while the flat branch iterates all warps and keys off `map_warp_accessibility`
rule-emptiness. The two partitions differ, changing `select_random_warp`'s phase
logic. This lives in shared `../../../RandomizerUtils/Randomizer.py`, not the zone data —
reconciling it is a design decision; confirm with the maintainer before changing
shared logic.

---

## 6. Key files

- `../../../RandomizerUtils/Randomizer.py` — `randomize`, `build_warps_to_randomize`,
  `select_random_warp`, `map_warp_divide`, the zone wrappers
  (`is_member_to_member_valid`, `zone_member_has_accessible_exit`, ...).
- `../../../RandomizerUtils/RandomGenerator.py` — the LCG PRNG.
- `../../../nds/gen4/PlatinumWarpMapInfo.py` — `zone_accessibility`, `ZT`/`fl`, the zone
  helpers (`get_member_zone`, `reachable_zone_ids`, `is_map_progressable`, ...).
- `../../../tests/test_platinum_regression.py`, `../../../tests/platinum_regression_utils.py` — the
  regression harness and its expected fixtures.
- `../../../scripts/divergence` — this skill's tooling.

## 7. Rules of thumb

- Express every gate as **zones + rules**; never reintroduce `*_needed`.
- Do not implement additions to the zone model without explicit approval,
  regardless of whether they are added to `zone_accessibility` or elsewhere.
- Fix **REACHABILITY-CONTENT** (over/under-reach) before END-SELECTION/RNG-DRIFT;
  content fixes usually resolve the later kinds too.
- Warps of a gated map are standable without the HM; only its **exits** are gated
  (case C vs B).
- Validate every zone edit with `dumpmap`, then re-run `compare` and confirm the
  first divergence moved later.
- A `randomize_returned: False` fixture is a *stuck* seed — look for orphan warps
  (case A) or an over-gate that strands a cluster.




