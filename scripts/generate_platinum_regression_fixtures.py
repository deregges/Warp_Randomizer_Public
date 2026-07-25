"""Generate Platinum seed regression fixtures.

The generator writes progress to tests/expected/platinum_seed_matrix/generation_status.txt
so long-running fixture generation can be monitored without relying on console output.
"""

from __future__ import annotations

import shutil
import sys
import time
from multiprocessing import get_context
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.platinum_regression_utils import EXPECTED_FIXTURE_DIR, write_platinum_expected_data


FIXTURE_COUNT = 100
SEED_TIMEOUT_SECONDS = 45


def _generate_case(seed: int, temp_case_dir: str, result_queue) -> None:
    try:
        write_platinum_expected_data(seed, Path(temp_case_dir))
    except BaseException as exc:
        result_queue.put((False, repr(exc)))
    else:
        result_queue.put((True, ""))


def _append_status(status_path: Path, message: str) -> None:
    status_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with status_path.open("a", encoding="utf-8", newline="\n") as status_file:
        status_file.write(f"[{timestamp}] {message}\n")
        status_file.flush()


def main() -> int:
    if EXPECTED_FIXTURE_DIR.exists():
        shutil.rmtree(EXPECTED_FIXTURE_DIR)
    EXPECTED_FIXTURE_DIR.mkdir(parents=True)

    status_path = EXPECTED_FIXTURE_DIR / "generation_status.txt"
    _append_status(status_path, f"Starting generation of {FIXTURE_COUNT} Platinum regression fixtures")

    process_context = get_context("spawn")
    accepted = []
    seed = 1
    while len(accepted) < FIXTURE_COUNT:
        case_number = len(accepted) + 1
        final_case_dir = EXPECTED_FIXTURE_DIR / f"case_{case_number:03d}"
        temp_case_dir = EXPECTED_FIXTURE_DIR / f".case_{case_number:03d}.tmp"

        if temp_case_dir.exists():
            shutil.rmtree(temp_case_dir)
        _append_status(status_path, f"Trying seed {seed} for case_{case_number:03d}")

        result_queue = process_context.Queue()
        process = process_context.Process(target=_generate_case, args=(seed, str(temp_case_dir), result_queue))
        process.start()
        process.join(SEED_TIMEOUT_SECONDS)

        if process.is_alive():
            process.terminate()
            process.join(5)
            if process.is_alive():
                process.kill()
                process.join()
            shutil.rmtree(temp_case_dir, ignore_errors=True)
            _append_status(status_path, f"Rejected seed {seed}: timed out after {SEED_TIMEOUT_SECONDS}s")
            seed += 1
            continue

        if process.exitcode != 0:
            shutil.rmtree(temp_case_dir, ignore_errors=True)
            _append_status(status_path, f"Rejected seed {seed}: worker exit code {process.exitcode}")
            seed += 1
            continue

        ok, error = result_queue.get() if not result_queue.empty() else (False, "worker produced no result")
        if not ok:
            shutil.rmtree(temp_case_dir, ignore_errors=True)
            _append_status(status_path, f"Rejected seed {seed}: {error}")
            seed += 1
            continue

        if final_case_dir.exists():
            shutil.rmtree(final_case_dir)
        temp_case_dir.rename(final_case_dir)
        accepted.append(seed)
        _append_status(status_path, f"Accepted seed {seed} as case_{case_number:03d} ({len(accepted)}/{FIXTURE_COUNT})")
        seed += 1

    _append_status(status_path, f"Completed {len(accepted)} fixtures. Seeds: {', '.join(str(s) for s in accepted)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

