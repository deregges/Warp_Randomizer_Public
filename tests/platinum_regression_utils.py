"""Utilities for Platinum randomizer regression fixtures."""

from __future__ import annotations

import contextlib
import io
from collections.abc import Iterable
from pathlib import Path
from typing import cast

from nds.gen4 import PlatinumWarpRandomizer
from RandomizerUtils import Randomizer
from RandomizerUtils.RandomGenerator import Random


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FIXTURE_DIR = PROJECT_ROOT / "tests" / "expected" / "platinum_seed_matrix"
REGRESSION_OUTPUT_FILES = ("seed.txt", "warps.txt", "routes.txt")


class PlatinumRandomizationError(RuntimeError):
    """Raised when a seed produces inspectable but invalid Platinum output."""

    def __init__(self, seed: int, randomized: bool, checked: bool, randomized_map_warps, debug_output: str):
        super().__init__(f"Seed {seed} did not produce a valid Platinum randomization")
        self.seed = seed
        self.randomized = randomized
        self.checked = checked
        self.randomized_map_warps = randomized_map_warps
        self.debug_output = debug_output


def _platinum_context():
    """Load fresh Platinum map data for one regression run."""
    gen_functions = PlatinumWarpRandomizer.PlatinumRandomizerFunctions()
    with contextlib.redirect_stdout(io.StringIO()):
        map_warps = gen_functions.load_map_data()
        _starting_node, map_nodes, _valid_warps = Randomizer.build_map(map_warps, gen_functions)
        all_maps = list(map_nodes.keys())
        unreachable_maps = cast(Iterable[str], cast(object, gen_functions.determine_unreachable_maps(map_nodes, map_warps)))
        all_maps.extend(unreachable_maps)
    return gen_functions, map_warps, all_maps


def fixture_directories():
    """Return all seed fixture directories in deterministic matrix order."""
    if not EXPECTED_FIXTURE_DIR.exists():
        return []
    return sorted(path for path in EXPECTED_FIXTURE_DIR.iterdir() if path.is_dir() and path.name.startswith("case_"))


def read_fixture_seed(fixture_dir: Path) -> int:
    return int((fixture_dir / "seed.txt").read_text(encoding="utf-8").strip())


def _write_raw_warp_dump(raw_warps_path: Path, randomized_map_warps) -> None:
    """Write every actual warp destination, including unassigned/incomplete warps."""
    lines = []
    for map_name in sorted(randomized_map_warps):
        warps, _connections = randomized_map_warps[map_name]
        for warp in warps:
            dest_map = warp.dest_map or "<unassigned>"
            dest_warp_id = warp.dest_warp_id
            sekii_id = getattr(warp, "sekii_id", None)
            suffix = f" ({sekii_id})" if sekii_id else ""
            lines.append(f"{map_name}[{warp.warp_id}]{suffix} -> {dest_map}[{dest_warp_id}]")

    raw_warps_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8", newline="\n")


def _write_randomization_status(status_path: Path, error: PlatinumRandomizationError) -> None:
    status_path.write_text(
        "\n".join(
            (
                f"seed: {error.seed}",
                f"randomize_returned: {error.randomized}",
                f"check_randomized_map_warps_returned: {error.checked}",
            )
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_platinum_output_files(seed: int, output_dir: Path, gen_functions, randomized_map_warps) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "seed.txt").write_text(str(seed), encoding="utf-8")
    Randomizer.write_warp_pairs_file(str(output_dir / "warps.txt"), randomized_map_warps)
    _write_raw_warp_dump(output_dir / "warps_raw.txt", randomized_map_warps)
    Randomizer.write_route_file(
        str(output_dir / "routes.txt"),
        randomized_map_warps,
        gen_functions,
        gen_functions.define_starting_map_id(),
    )


def _write_best_effort_invalid_output(seed: int, output_dir: Path, gen_functions, error: PlatinumRandomizationError) -> None:
    """Preserve as much actual output as possible without hiding the original failure."""
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "seed.txt").write_text(str(seed), encoding="utf-8")
    _write_randomization_status(output_dir / "randomization_status.txt", error)
    if error.debug_output:
        (output_dir / "debug_stdout.txt").write_text(error.debug_output, encoding="utf-8", newline="\n")

    artifact_errors = []
    if error.randomized_map_warps is not None:
        writers = (
            ("warps.txt", lambda: Randomizer.write_warp_pairs_file(str(output_dir / "warps.txt"), error.randomized_map_warps)),
            ("warps_raw.txt", lambda: _write_raw_warp_dump(output_dir / "warps_raw.txt", error.randomized_map_warps)),
            (
                "routes.txt",
                lambda: Randomizer.write_route_file(
                    str(output_dir / "routes.txt"),
                    error.randomized_map_warps,
                    gen_functions,
                    gen_functions.define_starting_map_id(),
                ),
            ),
        )
        for artifact_name, writer in writers:
            try:
                writer()
            except Exception as exc:
                artifact_errors.append(f"{artifact_name}: {exc!r}")

    if artifact_errors:
        (output_dir / "ARTIFACT_ERRORS.txt").write_text(
            "\n".join(artifact_errors) + "\n",
            encoding="utf-8",
            newline="\n",
        )


def randomize_platinum_seed(seed: int):
    """Run Platinum randomization for seed and return randomized map warps."""
    gen_functions, map_warps, all_maps = _platinum_context()
    randomized_map_warps = Randomizer.clean_up_map_warps(map_warps)
    rng = Random(seed)

    debug_output = io.StringIO()
    randomized = False
    checked = False
    try:
        with contextlib.redirect_stdout(debug_output):
            randomized = Randomizer.randomize(all_maps, map_warps, gen_functions, rng, randomized_map_warps)
            if randomized:
                checked = Randomizer.check_randomized_map_warps(
                    randomized_map_warps, map_warps, gen_functions, all_maps
                )
    except Exception as exc:
        raise PlatinumRandomizationError(seed, randomized, checked, randomized_map_warps, debug_output.getvalue()) from exc

    if not checked:
        raise PlatinumRandomizationError(seed, randomized, checked, randomized_map_warps, debug_output.getvalue())

    return randomized_map_warps


def write_platinum_expected_data(seed: int, output_dir: Path) -> None:
    """Write seed.txt, warps.txt and routes.txt for a Platinum seed."""
    gen_functions, _map_warps, _all_maps = _platinum_context()
    try:
        randomized_map_warps = randomize_platinum_seed(seed)
    except PlatinumRandomizationError as exc:
        _write_best_effort_invalid_output(seed, output_dir, gen_functions, exc)
        raise

    _write_platinum_output_files(seed, output_dir, gen_functions, randomized_map_warps)



