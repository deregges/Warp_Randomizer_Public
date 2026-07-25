"""Standalone divergence recorder for the warp randomizer.

Runs one Platinum (or other gen) randomization for a seed and records, for every
successful ``select_random_warp`` call, the exact PRNG consumption, the chosen
start/end warps and the reachable "pool" (``warps_to_randomize``) at that step.
It also records the one-time ``ends``/``connects`` classification produced by
``map_warp_divide``.

The recording is written as JSON so two checkouts (e.g. a feature branch and a
reference branch checked out in a git worktree) can be compared step-by-step by
``analyze.py``.

IMPORTANT: this file is intentionally self-contained. ``analyze.py`` copies it
into a reference ``git worktree`` and runs it there, so it must NOT import
anything from the ``scripts.divergence`` package -- only the project's own
randomizer modules, which exist in every checkout.

Usage:
    python record_seed.py <seed> <out.json> [--game platinum]
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import sys


def _find_project_root() -> str:
    """Locate the checkout root (the dir containing ``nds`` and ``RandomizerUtils``).

    Searches upward from this file's location first, then from the current working
    directory, so the recorder works whether it is run from ``scripts/divergence``
    in the feature tree or copied to the root of a reference worktree.
    """
    candidates = []
    here = os.path.dirname(os.path.abspath(__file__))
    candidates.append(here)
    candidates.extend(_ancestors(here))
    cwd = os.getcwd()
    candidates.append(cwd)
    candidates.extend(_ancestors(cwd))
    for path in candidates:
        if os.path.isdir(os.path.join(path, "nds")) and os.path.isdir(os.path.join(path, "RandomizerUtils")):
            return path
    raise RuntimeError("Could not locate project root (nds/ + RandomizerUtils/)")


def _ancestors(path: str):
    while True:
        parent = os.path.dirname(path)
        if parent == path:
            return
        yield parent
        path = parent


PROJECT_ROOT = _find_project_root()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from RandomizerUtils import Randomizer  # noqa: E402
from RandomizerUtils.RandomGenerator import Random  # noqa: E402


# Map a --game name to (module import path, gen-functions class name).
GAME_FUNCTIONS = {
    "platinum": ("nds.gen4.PlatinumWarpRandomizer", "PlatinumRandomizerFunctions"),
    "johto": ("nds.gen4.JohtoWarpRandomizer", "JohtoRandomizerFunctions"),
    "white2": ("nds.gen5.White2WarpRandomizer", "White2RandomizerFunctions"),
}


def _make_gen_functions(game: str):
    module_path, class_name = GAME_FUNCTIONS[game]
    module = __import__(module_path, fromlist=[class_name])
    return getattr(module, class_name)()


def _snapshot(randomized_map_warps):
    """Map (map_name, warp_id) -> (dest_map, dest_warp_id) for every assigned warp."""
    snap = {}
    for map_name, (warps, _connections) in randomized_map_warps.items():
        for warp in warps:
            if warp.dest_map != "":
                snap[(map_name, warp.warp_id)] = (warp.dest_map, warp.dest_warp_id)
    return snap


def _member(pair):
    return f"{pair[0]}[{pair[1]}]"


def _build_context(gen_functions):
    with contextlib.redirect_stdout(io.StringIO()):
        map_warps = gen_functions.load_map_data()
        _start, map_nodes, _valid = Randomizer.build_map(map_warps, gen_functions)
        all_maps = list(map_nodes.keys())
        all_maps.extend(gen_functions.determine_unreachable_maps(map_nodes, map_warps))
    return map_warps, all_maps


def _classify_divide(gen_functions, map_warps, all_maps):
    """Return (ends, connects) as sorted lists of 'map[warp]' strings."""
    randomized = Randomizer.clean_up_map_warps(map_warps)
    available, ignore = Randomizer.build_available_warps(randomized, map_warps, all_maps, gen_functions)
    Randomizer.remove_pair_warps(available, ignore, randomized, map_warps, all_maps, gen_functions)
    ends, connects = Randomizer.map_warp_divide(all_maps, map_warps, gen_functions, available)
    return (
        sorted(f"{m}[{w}]" for m, w in ends),
        sorted(f"{m}[{w}]" for m, w in connects),
    )


def record(seed: int, game: str):
    gen_functions = _make_gen_functions(game)
    map_warps, all_maps = _build_context(gen_functions)
    ends, connects = _classify_divide(gen_functions, map_warps, all_maps)

    randomized_map_warps = Randomizer.clean_up_map_warps(map_warps)
    rng = Random(seed)

    pairings = []
    original = Randomizer.select_random_warp

    def wrapper(*args, **kwargs):
        warps_to_randomize = args[0]
        pool = [_member((m, w.warp_id)) for m, w in warps_to_randomize]
        pool_set = {(m, w.warp_id) for m, w in warps_to_randomize}
        before_snap = _snapshot(randomized_map_warps)
        rng_before = len(rng.created)
        result = original(*args, **kwargs)
        if result:
            after_snap = _snapshot(randomized_map_warps)
            added = sorted(set(after_snap) - set(before_snap))
            # select_random_warp assigns exactly one start (from the pool) and its
            # end partner. Identify which is which via pool membership.
            start = next((k for k in added if k in pool_set), None)
            end = next((k for k in added if k != start), None)
            pairings.append({
                "i": len(pairings),
                "rng_before": rng_before,
                "rng_after": len(rng.created),
                "start": _member(start) if start else None,
                "end": _member(end) if end else None,
                "assigned": [_member(k) for k in added],
                "pool_len": len(pool),
                "pool": pool,
            })
        return result

    Randomizer.select_random_warp = wrapper
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            returned = Randomizer.randomize(all_maps, map_warps, gen_functions, rng, randomized_map_warps)
    finally:
        Randomizer.select_random_warp = original

    return {
        "seed": seed,
        "game": game,
        "returned": bool(returned),
        "steps": len(pairings),
        "rng_total": len(rng.created),
        "n_ends": len(ends),
        "n_connects": len(connects),
        "ends": ends,
        "connects": connects,
        "pairings": pairings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Record a randomizer run for divergence analysis.")
    parser.add_argument("seed", type=int)
    parser.add_argument("out", help="Output JSON path")
    parser.add_argument("--game", default="platinum", choices=sorted(GAME_FUNCTIONS))
    args = parser.parse_args(argv)

    recording = record(args.seed, args.game)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(recording, handle)
    print(
        f"seed {args.seed} ({args.game}): returned={recording['returned']} "
        f"steps={recording['steps']} rng_total={recording['rng_total']} "
        f"ends={recording['n_ends']} connects={recording['n_connects']} -> {args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())




