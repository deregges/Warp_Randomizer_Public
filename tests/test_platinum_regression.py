from concurrent.futures import ProcessPoolExecutor, as_completed
import difflib
import os
from pathlib import Path
import shutil
import traceback
from unittest import TestCase

from tests.platinum_regression_utils import (
    EXPECTED_FIXTURE_DIR,
    REGRESSION_OUTPUT_FILES,
    fixture_directories,
    read_fixture_seed,
    write_platinum_expected_data,
)


ACTUAL_FIXTURE_DIR = Path(__file__).resolve().parent / "actual" / "platinum_seed_matrix"


def _compare_files(expected_path: Path, actual_path: Path, diff_path: Path):
    expected = expected_path.read_text(encoding="utf-8").splitlines(keepends=True)
    actual = actual_path.read_text(encoding="utf-8").splitlines(keepends=True)

    if expected == actual:
        return None

    diff_path.write_text(
        "".join(
            difflib.unified_diff(
                expected,
                actual,
                fromfile=str(expected_path),
                tofile=str(actual_path),
            )
        ),
        encoding="utf-8",
    )

    for line_number, (expected_line, actual_line) in enumerate(zip(expected, actual), start=1):
        if expected_line != actual_line:
            return (
                f"{expected_path.name} differs at line {line_number}\n"
                f"expected: {expected_line!r}\n"
                f"actual:   {actual_line!r}\n"
                f"diff:     {diff_path}"
            )

    return (
        f"{expected_path.name} has different line counts: "
        f"expected {len(expected)}, actual {len(actual)}\n"
        f"diff:     {diff_path}"
    )


def _artifact_summary(actual_dir: Path):
    artifacts = sorted(path.name for path in actual_dir.iterdir() if path.is_file())
    return ", ".join(artifacts) if artifacts else "(none)"


def _validation_failure_message(fixture_dir: Path, actual_dir: Path, details: str):
    return (
        f"{fixture_dir.name} failed Platinum regression validation\n"
        f"expected output: {fixture_dir}\n"
        f"actual output:   {actual_dir}\n"
        f"actual artifacts: {_artifact_summary(actual_dir)}\n"
        f"{details}"
    )


def _validate_fixture_worker(fixture_dir_text: str, actual_root_text: str):
    fixture_dir = Path(fixture_dir_text)
    actual_dir = Path(actual_root_text) / fixture_dir.name
    if actual_dir.exists():
        shutil.rmtree(actual_dir)
    actual_dir.mkdir(parents=True, exist_ok=True)

    seed = read_fixture_seed(fixture_dir)
    (actual_dir / "seed.txt").write_text(str(seed), encoding="utf-8")

    for filename in REGRESSION_OUTPUT_FILES:
        if not (fixture_dir / filename).is_file():
            return seed, _validation_failure_message(
                fixture_dir,
                actual_dir,
                f"Missing expected fixture file: {fixture_dir / filename}",
            )

    try:
        write_platinum_expected_data(seed, actual_dir)
    except BaseException:
        error_path = actual_dir / "ERROR.txt"
        error_path.write_text(traceback.format_exc(), encoding="utf-8")
        return seed, _validation_failure_message(
            fixture_dir,
            actual_dir,
            f"Exception while generating actual output. Traceback: {error_path}",
        )

    for filename in ("warps.txt", "routes.txt"):
        actual_path = actual_dir / filename
        if not actual_path.is_file():
            return seed, _validation_failure_message(
                fixture_dir,
                actual_dir,
                f"Missing actual output file: {actual_path}",
            )
        try:
            mismatch = _compare_files(fixture_dir / filename, actual_path, actual_dir / f"{filename}.diff")
        except BaseException:
            error_path = actual_dir / f"COMPARE_{filename}.ERROR.txt"
            error_path.write_text(traceback.format_exc(), encoding="utf-8")
            return seed, _validation_failure_message(
                fixture_dir,
                actual_dir,
                f"Exception while comparing {filename}. Traceback: {error_path}",
            )
        if mismatch is not None:
            return seed, _validation_failure_message(fixture_dir, actual_dir, mismatch)

    return seed, None


class TestPlatinumSeedRegression(TestCase):
    def test_platinum_seed_matrix_matches_expected_data(self):
        fixtures = fixture_directories()
        self.assertEqual(
            100,
            len(fixtures),
            f"Expected 100 Platinum regression fixtures under {EXPECTED_FIXTURE_DIR}",
        )

        if ACTUAL_FIXTURE_DIR.exists():
            shutil.rmtree(ACTUAL_FIXTURE_DIR)
        ACTUAL_FIXTURE_DIR.mkdir(parents=True)

        # 1-indexed list of (case_number, fixture_dir) for ordered fail-fast.
        cases = [(i + 1, d) for i, d in enumerate(fixtures)]

        max_workers = os.cpu_count() or 1
        future_to_case = {}  # future -> case_number
        results = {}  # case_number -> (seed, mismatch_or_None)
        first_failing_case = None
        next_to_submit = 0  # index into cases

        executor = ProcessPoolExecutor(max_workers=max_workers)
        try:
            # Submit initial batch.
            while next_to_submit < min(max_workers, len(cases)):
                case_num, fixture_dir = cases[next_to_submit]
                next_to_submit += 1
                future = executor.submit(
                    _validate_fixture_worker, str(fixture_dir), str(ACTUAL_FIXTURE_DIR)
                )
                future_to_case[future] = case_num

            while future_to_case:
                future = next(as_completed(future_to_case))
                case_num = future_to_case.pop(future)

                # Discard results from cases we already know are past the first failure.
                if first_failing_case is not None and case_num > first_failing_case:
                    continue

                seed, mismatch = future.result()
                results[case_num] = (seed, mismatch)

                if mismatch is not None:
                    # Shrink the first-failure boundary if this is an earlier case.
                    if first_failing_case is None or case_num < first_failing_case:
                        first_failing_case = case_num
                        # Cancel every future for a case beyond the new boundary.
                        for f, cn in list(future_to_case.items()):
                            if cn > first_failing_case:
                                f.cancel()

                if first_failing_case is not None:
                    # Confirm: every case before the first failure has completed and passed.
                    all_prior_pass = all(
                        i in results and results[i][1] is None
                        for i in range(1, first_failing_case)
                    )
                    no_prior_in_flight = not any(
                        cn < first_failing_case for cn in future_to_case.values()
                    )
                    if all_prior_pass and no_prior_in_flight:
                        break
                else:
                    # No failure yet — keep the pipeline full.
                    if next_to_submit < len(cases):
                        case_num, fixture_dir = cases[next_to_submit]
                        next_to_submit += 1
                        future = executor.submit(
                            _validate_fixture_worker,
                            str(fixture_dir),
                            str(ACTUAL_FIXTURE_DIR),
                        )
                        future_to_case[future] = case_num
        finally:
            for future in future_to_case:
                future.cancel()
            executor.shutdown(wait=True, cancel_futures=True)

        if first_failing_case is not None:
            seed, mismatch = results[first_failing_case]
            fixture_dir = cases[first_failing_case - 1][1]
            with self.subTest(seed=seed, fixture=fixture_dir.name):
                self.assertIsNone(mismatch, mismatch)

