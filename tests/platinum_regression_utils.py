"""Utilities for Platinum randomizer regression fixtures."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

from nds.gen4 import PlatinumWarpRandomizer
from RandomizerUtils import Randomizer
from RandomizerUtils.RandomGenerator import Random


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FIXTURE_DIR = PROJECT_ROOT / "tests" / "expected" / "platinum_seed_matrix"
REGRESSION_OUTPUT_FILES = ("seed.txt", "warps.txt", "routes.txt")


def _platinum_context():
    """Load fresh Platinum map data for one regression run."""
    gen_functions = PlatinumWarpRandomizer.PlatinumRandomizerFunctions()
    with contextlib.redirect_stdout(io.StringIO()):
        map_warps = gen_functions.load_map_data()
        _starting_node, map_nodes, _valid_warps = Randomizer.build_map(map_warps, gen_functions)
        unreachable_maps = gen_functions.determine_unreachable_maps(map_nodes, map_warps)
        all_maps = [*map_nodes.keys(), *unreachable_maps]
    return gen_functions, map_warps, all_maps


def fixture_directories():
    """Return all seed fixture directories in deterministic matrix order."""
    if not EXPECTED_FIXTURE_DIR.exists():
        return []
    return sorted(path for path in EXPECTED_FIXTURE_DIR.iterdir() if path.is_dir() and path.name.startswith("case_"))


def read_fixture_seed(fixture_dir: Path) -> int:
    return int((fixture_dir / "seed.txt").read_text(encoding="utf-8").strip())


def randomize_platinum_seed(seed: int):
    """Run Platinum randomization for seed and return randomized map warps."""
    gen_functions, map_warps, all_maps = _platinum_context()
    randomized_map_warps = Randomizer.clean_up_map_warps(map_warps)
    rng = Random(seed)

    with contextlib.redirect_stdout(io.StringIO()):
        randomized = Randomizer.randomize(all_maps, map_warps, gen_functions, rng, randomized_map_warps)
        checked = randomized and Randomizer.check_randomized_map_warps(
            randomized_map_warps, map_warps, gen_functions, all_maps
        )

    if not checked:
        raise RuntimeError(f"Seed {seed} did not produce a valid Platinum randomization")

    return randomized_map_warps


def write_platinum_expected_data(seed: int, output_dir: Path) -> None:
    """Write seed.txt, warps.txt and routes.txt for a Platinum seed."""
    gen_functions, _map_warps, _all_maps = _platinum_context()
    randomized_map_warps = randomize_platinum_seed(seed)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "seed.txt").write_text(str(seed), encoding="utf-8")
    Randomizer.write_warp_pairs_file(str(output_dir / "warps.txt"), randomized_map_warps)
    Randomizer.write_route_file(
        str(output_dir / "routes.txt"),
        randomized_map_warps,
        gen_functions,
        gen_functions.define_starting_map_id(),
    )



