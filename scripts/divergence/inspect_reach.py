"""Standalone reachability inspector for the warp randomizer.

Two modes, both useful when a divergence points at a specific map/cluster:

  replay  -- replay a seed's randomization up to a given step, then report why
             each target map is (or is not) reachable: the members it was reached
             through, its connections and whether each neighbour is reachable, and
             any randomized warps pointing into it. Run this in BOTH checkouts to
             see exactly which connection edge one model traverses and the other
             blocks.

  dumpmap -- print a map's raw warp data plus its zone/rules/pair structure, so
             you can see how it is (or isn't) gated.

Self-contained on purpose (see record_seed.py): ``analyze.py`` may copy it into a
reference worktree, so it only imports the project's own modules.

Usage:
    python inspect_reach.py replay <seed> <stop_step> MAP [MAP ...] [--game platinum]
    python inspect_reach.py dumpmap MAP [MAP ...] [--game platinum]
"""

from __future__ import annotations

import argparse
import contextlib
import io
import os
import sys


def _find_project_root() -> str:
    def ancestors(path: str):
        while True:
            parent = os.path.dirname(path)
            if parent == path:
                return
            yield parent
            path = parent

    here = os.path.dirname(os.path.abspath(__file__))
    for path in [here, *ancestors(here), os.getcwd(), *ancestors(os.getcwd())]:
        if os.path.isdir(os.path.join(path, "nds")) and os.path.isdir(os.path.join(path, "RandomizerUtils")):
            return path
    raise RuntimeError("Could not locate project root (nds/ + RandomizerUtils/)")


PROJECT_ROOT = _find_project_root()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from RandomizerUtils import Randomizer  # noqa: E402
from RandomizerUtils.RandomGenerator import Random  # noqa: E402

GAME_FUNCTIONS = {
    "platinum": ("nds.gen4.PlatinumWarpRandomizer", "PlatinumRandomizerFunctions"),
    "johto": ("nds.gen4.JohtoWarpRandomizer", "JohtoRandomizerFunctions"),
    "white2": ("nds.gen5.White2WarpRandomizer", "White2RandomizerFunctions"),
}


def _make_gen_functions(game):
    module_path, class_name = GAME_FUNCTIONS[game]
    module = __import__(module_path, fromlist=[class_name])
    return getattr(module, class_name)()


def _build_context(gen_functions):
    with contextlib.redirect_stdout(io.StringIO()):
        map_warps = gen_functions.load_map_data()
        _start, map_nodes, _valid = Randomizer.build_map(map_warps, gen_functions)
        all_maps = list(map_nodes.keys())
        all_maps.extend(gen_functions.determine_unreachable_maps(map_nodes, map_warps))
    return map_warps, all_maps


def replay(seed, stop_step, targets, game):
    gen_functions = _make_gen_functions(game)
    map_warps, all_maps = _build_context(gen_functions)

    randomized = Randomizer.clean_up_map_warps(map_warps)
    rng = Random(seed)
    available, ignore = Randomizer.build_available_warps(randomized, map_warps, all_maps, gen_functions)
    Randomizer.remove_pair_warps(available, ignore, randomized, map_warps, all_maps, gen_functions)
    ends, connects = Randomizer.map_warp_divide(all_maps, map_warps, gen_functions, available)

    accessible_maps = {}
    warps_to_randomize = []
    visited = {}

    def rebuild():
        visited.clear()
        Randomizer.build_warps_to_randomize(
            accessible_maps, visited, warps_to_randomize, randomized, available,
            gen_functions.define_starting_map_id(), "", -1, gen_functions, map_warps)

    rebuild()
    steps = 0
    while steps < stop_step:
        with contextlib.redirect_stdout(io.StringIO()):
            ok = Randomizer.select_random_warp(
                warps_to_randomize, available, ignore, randomized,
                accessible_maps, connects, ends, gen_functions, rng)
        if not ok:
            print(f"randomization stuck at step {steps} (before reaching stop={stop_step})")
            break
        steps += 1
        rebuild()

    print(f"Replayed {steps} steps. accessible_maps={len(accessible_maps)} pool={len(warps_to_randomize)}")
    for target in targets:
        print(f"\n=== {target} ===")
        if target not in map_warps:
            print("  NOT IN MAP DATA")
            continue
        warps, connections = map_warps[target]
        print(f"  reachable={target in accessible_maps}  reached_via={accessible_maps.get(target)}")
        incoming = []
        for map_name, (ws, _cs) in randomized.items():
            for w in ws:
                if w.dest_map == target:
                    incoming.append(f"{map_name}[{w.warp_id}]->{target}[{w.dest_warp_id}]")
        print(f"  incoming randomized warps: {incoming or 'none'}")
        for connection in connections:
            print(f"  conn {target} -> {connection.map}: neighbour_reachable={connection.map in accessible_maps}")


def dumpmap(targets, game):
    gen_functions = _make_gen_functions(game)
    with contextlib.redirect_stdout(io.StringIO()):
        map_warps = gen_functions.load_map_data()
    info = gen_functions.info()

    flag_names = {v: n for n, v in vars(info).items()
                  if n.endswith("_FLAG") and isinstance(v, int) and n != "END_FLAG"}

    def decode(mask):
        parts, i = [], 0
        while mask:
            if mask & 1:
                parts.append(flag_names.get(i, f"bit{i}"))
            mask >>= 1
            i += 1
        return "+".join(parts) if parts else "0"

    uses_zones = getattr(info, "USES_ZONE_ACCESSIBILITY", False)
    for target in targets:
        print(f"=== {target} ===")
        if target not in map_warps:
            print("  NOT IN MAP DATA")
            continue
        warps, connections = map_warps[target]
        for w in warps:
            print(f"  warp {w.warp_id}: x={w.x} y={w.y} no_pair={getattr(w, 'no_pair', None)} "
                  f"-> {w.dest_map}[{w.dest_warp_id}] sekii={getattr(w, 'sekii_id', None)}")
        print(f"  connections: {[c.map for c in connections]}")
        print(f"  computed pairs: {Randomizer.compute_pairs_for_map(target, warps, gen_functions)}")
        if uses_zones:
            entry = info.zone_accessibility.get(target, {})
            print(f"  zones: {entry.get('zones')}")
            rules = entry.get("rules") or {}
            pretty = {zid: [f"z{z.zone_id}/{decode(z.flag)}" for z in zts] for zid, zts in rules.items()}
            print(f"  rules: {pretty}")
        else:
            acc = getattr(info, "map_warp_accessibility", {}).get(target)
            print(f"  map_warp_accessibility: {acc}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect randomizer reachability for specific maps.")
    sub = parser.add_subparsers(dest="mode", required=True)

    p_replay = sub.add_parser("replay", help="Replay to a step and inspect target maps.")
    p_replay.add_argument("seed", type=int)
    p_replay.add_argument("stop_step", type=int)
    p_replay.add_argument("targets", nargs="+")
    p_replay.add_argument("--game", default="platinum", choices=sorted(GAME_FUNCTIONS))

    p_dump = sub.add_parser("dumpmap", help="Dump a map's warp/zone/pair structure.")
    p_dump.add_argument("targets", nargs="+")
    p_dump.add_argument("--game", default="platinum", choices=sorted(GAME_FUNCTIONS))

    args = parser.parse_args(argv)
    if args.mode == "replay":
        replay(args.seed, args.stop_step, args.targets, args.game)
    else:
        dumpmap(args.targets, args.game)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


