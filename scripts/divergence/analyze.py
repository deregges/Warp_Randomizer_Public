"""Divergence analyzer for the warp randomizer (zone model vs. a reference ref).

This is the entry point. It records a seed's randomization in the current
checkout and in a reference ref (checked out in a temporary ``git worktree``),
then aligns the two step-by-step and classifies the FIRST divergence into one of
the well-known buckets (see ``SKILL.md``), printing concrete evidence and the
recommended next probe.

Subcommands:
    compare   Record current tree + reference ref, diff, classify. (main tool)
    record    Record only the current tree to a JSON file.
    diff      Compare two existing recording JSON files.

Examples:
    python scripts/divergence/analyze.py compare --seed 1
    python scripts/divergence/analyze.py compare --seed 1 --ref main --show-pool
    python scripts/divergence/analyze.py record --seed 1 --out cur.json
    python scripts/divergence/analyze.py diff --ref-json main.json --cur-json cur.json
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(HERE))
RECORDER = os.path.join(HERE, "record_seed.py")


# --------------------------------------------------------------------------- #
# Recording (current tree + reference worktree)
# --------------------------------------------------------------------------- #

def _run_recorder(cwd, out_path, seed, game):
    result = subprocess.run(
        [sys.executable, "-W", "ignore", os.path.join(cwd, "_divergence_record_seed.py"),
         str(seed), out_path, "--game", game],
        cwd=cwd, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"reference recorder failed:\n{result.stderr}")
    print(result.stdout.strip())


def record_current(seed, game, out_path):
    """Record the current checkout by running the recorder in-place."""
    result = subprocess.run(
        [sys.executable, "-W", "ignore", RECORDER, str(seed), out_path, "--game", game],
        cwd=PROJECT_ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"recorder failed:\n{result.stderr}")
    print(result.stdout.strip())
    with open(out_path, encoding="utf-8") as handle:
        return json.load(handle)


def record_reference(seed, game, ref, out_path, keep_worktree=False):
    """Record a reference ref via a throwaway git worktree."""
    worktree = tempfile.mkdtemp(prefix="wr_divergence_ref_")
    try:
        subprocess.run(["git", "worktree", "add", "--force", "--detach", worktree, ref],
                       cwd=PROJECT_ROOT, check=True, capture_output=True, text=True)
        shutil.copy2(RECORDER, os.path.join(worktree, "_divergence_record_seed.py"))
        _run_recorder(worktree, out_path, seed, game)
        with open(out_path, encoding="utf-8") as handle:
            return json.load(handle)
    finally:
        if not keep_worktree:
            subprocess.run(["git", "worktree", "remove", "--force", worktree],
                           cwd=PROJECT_ROOT, capture_output=True, text=True)
            shutil.rmtree(worktree, ignore_errors=True)
        else:
            print(f"[kept reference worktree: {worktree}]")


# --------------------------------------------------------------------------- #
# Classification
# --------------------------------------------------------------------------- #

def _first_output_divergence(ref, cur):
    """Index of the first step whose start/end/assigned differ, or None."""
    n = min(len(ref["pairings"]), len(cur["pairings"]))
    for i in range(n):
        rp, cp = ref["pairings"][i], cur["pairings"][i]
        if (rp["start"], rp["end"], rp["assigned"]) != (cp["start"], cp["end"], cp["assigned"]):
            return i
    if len(ref["pairings"]) != len(cur["pairings"]):
        return n
    return None


def _first_rng_divergence(ref, cur):
    """Index of the first step whose PRNG advance count entering it differs."""
    n = min(len(ref["pairings"]), len(cur["pairings"]))
    for i in range(n):
        if ref["pairings"][i]["rng_before"] != cur["pairings"][i]["rng_before"]:
            return i
    return None


def _classify(ref, cur, index, show_pool):
    rp, cp = ref["pairings"][index], cur["pairings"][index]
    ref_pool, cur_pool = rp["pool"], cp["pool"]
    ref_set, cur_set = set(ref_pool), set(cur_pool)
    over = [w for w in cur_pool if w not in ref_set]   # reachable in CUR, not in REF
    under = [w for w in ref_pool if w not in cur_set]  # reachable in REF, not in CUR

    lines = []
    lines.append(f"Step {index}:")
    lines.append(f"  REF (reference)  start={rp['start']} end={rp['end']} "
                 f"rng={rp['rng_before']}->{rp['rng_after']} pool_len={rp['pool_len']}")
    lines.append(f"  CUR (this tree)  start={cp['start']} end={cp['end']} "
                 f"rng={cp['rng_before']}->{cp['rng_after']} pool_len={cp['pool_len']}")

    if over or under:
        kind = "REACHABILITY-CONTENT"
        lines.append("")
        lines.append("  -> Kind: REACHABILITY divergence (the reachable pools differ).")
        if over:
            lines.append(f"     OVER-reach: {len(over)} warp(s) reachable in CUR but NOT in REF:")
            lines.extend(f"       + {w}" for w in over[:20])
            lines.append("       (a gate/non-navigable rule main enforces is MISSING in the zone data)")
        if under:
            lines.append(f"     UNDER-reach: {len(under)} warp(s) reachable in REF but NOT in CUR:")
            lines.extend(f"       - {w}" for w in under[:20])
            lines.append("       (the zone data OVER-gates: a warp/exit main reaches is blocked)")
        example = (over or under)[0].split("[")[0]
        lines.append("")
        lines.append("  Next probe (run in BOTH checkouts and compare 'neighbour_reachable'):")
        lines.append(f"     python scripts/divergence/inspect_reach.py replay {cur['seed']} {index} "
                     f"{example} <neighbours...> --game {cur['game']}")
    elif ref_pool != cur_pool:
        kind = "POOL-ORDERING"
        first = next(i for i in range(min(len(ref_pool), len(cur_pool))) if ref_pool[i] != cur_pool[i])
        lines.append("")
        lines.append("  -> Kind: POOL ORDERING divergence (same warps, different order).")
        lines.append(f"     first differing index {first}: REF={ref_pool[first]} CUR={cur_pool[first]}")
        lines.append("     The build_warps_to_randomize traversal order differs between models.")
    else:
        # Identical pool (content + order).
        if rp["start"] != cp["start"]:
            kind = "RNG-DRIFT"
            lines.append("")
            lines.append("  -> Kind: RNG DRIFT (identical pool, different start).")
            lines.append("     The PRNG state already diverged in an EARLIER step's end-selection")
            lines.append("     loop (different number of accept/reject draws). See the rng-advance")
            lines.append("     divergence reported above for the true origin step.")
        else:
            kind = "END-SELECTION"
            ref_draws = rp["rng_after"] - rp["rng_before"]
            cur_draws = cp["rng_after"] - cp["rng_before"]
            lines.append("")
            lines.append("  -> Kind: END-SELECTION divergence (same start, different end).")
            lines.append(f"     end-selection PRNG draws: REF={ref_draws} CUR={cur_draws} "
                         f"(a different number of candidates was rejected)")
            lines.append("     select_random_warp's accept/reject predicates evaluate differently.")
            lines.append("     Most common cause: ends/connects classification differs (see below),")
            lines.append("     or is_map_progressable / flag-event predicates differ for a candidate.")

    return kind, lines


def _ends_connects_summary(ref, cur):
    lines = []
    for key in ("ends", "connects"):
        ref_set, cur_set = set(ref[key]), set(cur[key])
        only_ref = sorted(ref_set - cur_set)
        only_cur = sorted(cur_set - ref_set)
        if only_ref or only_cur:
            lines.append(f"  {key}: REF={len(ref[key])} CUR={len(cur[key])} "
                         f"(+{len(only_cur)} only-CUR, -{len(only_ref)} only-REF via map_warp_divide)")
            for w in only_ref[:8]:
                lines.append(f"       only in REF {key}: {w}")
            for w in only_cur[:8]:
                lines.append(f"       only in CUR {key}: {w}")
    return lines


def report(ref, cur, show_pool):
    print("=" * 72)
    print(f"Divergence report  seed={cur['seed']}  game={cur['game']}")
    print(f"  REF returned={ref['returned']} steps={ref['steps']} rng_total={ref['rng_total']}")
    print(f"  CUR returned={cur['returned']} steps={cur['steps']} rng_total={cur['rng_total']}")
    print("=" * 72)

    ec = _ends_connects_summary(ref, cur)
    if ec:
        print("map_warp_divide classification differs (affects end-selection):")
        print("\n".join(ec))
        print("-" * 72)

    out_i = _first_output_divergence(ref, cur)
    rng_i = _first_rng_divergence(ref, cur)
    if rng_i is not None and (out_i is None or rng_i < out_i):
        print(f"First PRNG-advance divergence: step {rng_i} "
              f"(REF rng_before={ref['pairings'][rng_i]['rng_before']} "
              f"CUR={cur['pairings'][rng_i]['rng_before']}) -- the true origin of drift.")
        print("-" * 72)

    if out_i is None:
        print("No output divergence: the two runs produced identical pairings.")
        if ref["steps"] != cur["steps"]:
            print(f"  (but step counts differ: REF={ref['steps']} CUR={cur['steps']})")
        return

    if out_i >= len(ref["pairings"]) or out_i >= len(cur["pairings"]):
        print(f"Runs diverge in length at step {out_i} (one run ended earlier).")
        return

    kind, lines = _classify(ref, cur, out_i, show_pool)
    print("\n".join(lines))
    if show_pool:
        print("\n  REF pool:", cur["pairings"][out_i]["pool"])
    print("=" * 72)
    print(f"CLASSIFICATION: {kind}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def cmd_compare(args):
    with tempfile.TemporaryDirectory(prefix="wr_divergence_") as tmp:
        cur_path = args.cur_json or os.path.join(tmp, "cur.json")
        ref_path = args.ref_json or os.path.join(tmp, "ref.json")
        if not args.cur_json:
            print("Recording current tree...")
            cur = record_current(args.seed, args.game, cur_path)
        else:
            cur = json.load(open(args.cur_json, encoding="utf-8"))
        if not args.ref_json:
            print(f"Recording reference '{args.ref}' via git worktree...")
            ref = record_reference(args.seed, args.game, args.ref, ref_path, args.keep_worktree)
        else:
            ref = json.load(open(args.ref_json, encoding="utf-8"))
        report(ref, cur, args.show_pool)
    return 0


def cmd_record(args):
    record_current(args.seed, args.game, args.out)
    return 0


def cmd_diff(args):
    ref = json.load(open(args.ref_json, encoding="utf-8"))
    cur = json.load(open(args.cur_json, encoding="utf-8"))
    report(ref, cur, args.show_pool)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_cmp = sub.add_parser("compare", help="Record current tree + reference ref, classify first divergence.")
    p_cmp.add_argument("--seed", type=int, required=True)
    p_cmp.add_argument("--ref", default="main", help="Reference git ref (default: main)")
    p_cmp.add_argument("--game", default="platinum")
    p_cmp.add_argument("--show-pool", action="store_true", help="Print the full pool at the divergence step.")
    p_cmp.add_argument("--keep-worktree", action="store_true", help="Keep the reference worktree for reuse.")
    p_cmp.add_argument("--cur-json", help="Use an existing current-tree recording instead of re-recording.")
    p_cmp.add_argument("--ref-json", help="Use an existing reference recording instead of re-recording.")
    p_cmp.set_defaults(func=cmd_compare)

    p_rec = sub.add_parser("record", help="Record only the current tree to a JSON file.")
    p_rec.add_argument("--seed", type=int, required=True)
    p_rec.add_argument("--out", required=True)
    p_rec.add_argument("--game", default="platinum")
    p_rec.set_defaults(func=cmd_record)

    p_diff = sub.add_parser("diff", help="Compare two existing recording JSON files.")
    p_diff.add_argument("--ref-json", required=True)
    p_diff.add_argument("--cur-json", required=True)
    p_diff.add_argument("--show-pool", action="store_true")
    p_diff.set_defaults(func=cmd_diff)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())


