from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from pathlib import Path
import tempfile
from unittest import TestCase

from tests.platinum_regression_utils import (
    EXPECTED_FIXTURE_DIR,
    REGRESSION_OUTPUT_FILES,
    fixture_directories,
    read_fixture_seed,
    write_platinum_expected_data,
)


def _compare_files(expected_path: Path, actual_path: Path):
    expected = expected_path.read_text(encoding="utf-8").splitlines(keepends=True)
    actual = actual_path.read_text(encoding="utf-8").splitlines(keepends=True)

    if expected == actual:
        return None

    for line_number, (expected_line, actual_line) in enumerate(zip(expected, actual), start=1):
        if expected_line != actual_line:
            return (
                f"{expected_path.name} differs at line {line_number}\n"
                f"expected: {expected_line!r}\n"
                f"actual:   {actual_line!r}"
            )

    return (
        f"{expected_path.name} has different line counts: "
        f"expected {len(expected)}, actual {len(actual)}"
    )


def _validate_fixture_worker(fixture_dir_text: str):
    fixture_dir = Path(fixture_dir_text)
    seed = read_fixture_seed(fixture_dir)

    for filename in REGRESSION_OUTPUT_FILES:
        if not (fixture_dir / filename).is_file():
            return seed, f"Missing {filename}"

    with tempfile.TemporaryDirectory() as temp_dir:
        actual_dir = Path(temp_dir)
        write_platinum_expected_data(seed, actual_dir)

        for filename in ("warps.txt", "routes.txt"):
            mismatch = _compare_files(fixture_dir / filename, actual_dir / filename)
            if mismatch is not None:
                return seed, mismatch

    return seed, None


class TestPlatinumSeedRegression(TestCase):
    def test_platinum_seed_matrix_matches_expected_data(self):
        fixtures = fixture_directories()
        self.assertEqual(
            100,
            len(fixtures),
            f"Expected 100 Platinum regression fixtures under {EXPECTED_FIXTURE_DIR}",
        )

        max_workers = min(4, os.cpu_count() or 1)
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_fixture = {
                executor.submit(_validate_fixture_worker, str(fixture_dir)): fixture_dir
                for fixture_dir in fixtures
            }

            for future in as_completed(future_to_fixture):
                fixture_dir = future_to_fixture[future]
                seed, mismatch = future.result()
                with self.subTest(seed=seed, fixture=fixture_dir.name):
                    self.assertIsNone(mismatch, mismatch)

