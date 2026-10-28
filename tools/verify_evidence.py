#!/usr/bin/env python3
"""Verify preserved evidence hashes and declared byte structures read-only."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
ERASE = b"\x08\x20\x08"
EDGE_ERASE = b"\x0d\x20\x0d"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_manifest() -> int:
    count = 0
    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split("  ", 1)
        path = ROOT / relative
        require(path.is_file(), f"Missing evidence file: {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected, f"SHA-256 mismatch: {relative}")
        count += 1
    return count


def transcript(name: str) -> bytes:
    return (ROOT / "evidence" / "transcripts" / name).read_bytes()


def verify_structures() -> None:
    a0 = transcript("backspace-experiment-20261027-215112.typescript")
    require(b"ABORTED_BY_USER" in a0, "A0 abort marker missing")
    require(ERASE not in a0, "A0 unexpectedly contains an erase triplet")

    p1 = transcript("backspace-experiment-20261027-215309.typescript")
    p1_expected = (
        b"i had macaroni for dinner"
        + ERASE * 25
        + b"i had pizza for dinner"
    )
    require(p1_expected in p1, "P1 declared draft/edit/final structure missing")
    require(p1.count(ERASE) == 25, "P1 erase count is not 25")
    require(b"receiver was not launched" in p1, "P1 receiver status missing")

    p2 = transcript("backspace-experiment-20261027-220503.typescript")
    p2_expected = (
        b"i'm drinking water"
        + ERASE
        + b"r"
        + ERASE * 18
        + b"i'm drinking juice"
    )
    require(p2_expected in p2, "P2 correction/edit/final structure missing")
    require(p2.count(ERASE) == 19, "P2 erase count is not 19")
    require(b"receiver was not launched" in p2, "P2 receiver status missing")

    p3 = transcript("backspace-experiment-20261027-220922.typescript")
    p3_expected = (
        b"my cat's name is mischa"
        + ERASE * 23
        + b"my cats name is phoebe"
    )
    require(p3_expected in p3, "P3 declared draft/edit/final structure missing")
    require(p3.count(ERASE) == 23, "P3 erase count is not 23")
    require(
        b"RECEIVER_SAW: my cats name is phoebe" in p3,
        "P3 receiver output missing",
    )

    n1 = transcript("conpty-experiment-20261027-223358.typescript")
    draft = b"i hate architecture"
    final = b"i like architecture"
    draft_start = n1.index(draft)
    edit_start = draft_start + len(draft)
    final_start = n1.index(final, edit_start)
    edit_region = n1[edit_start:final_start]
    require(draft_start == 394, f"N1 draft offset changed: {draft_start}")
    require(final_start == 470, f"N1 final offset changed: {final_start}")
    require(edit_region.count(ERASE) == 18, "N1 08 20 08 count is not 18")
    require(edit_region.count(EDGE_ERASE) == 1, "N1 edge erase count is not 1")
    require(
        b"CHILD_RECEIVED: i like architecture" in n1,
        "N1 child output missing",
    )
    require(
        b"CHILD_RECEIVED: i hate architecture" not in n1,
        "N1 child output unexpectedly contains the abandoned draft",
    )

    n0 = (ROOT / "evidence" / "self-tests" / "conpty-self-test-20261027-223338.typescript").read_bytes()
    require(b"alpha" in n0, "N0 abandoned string missing")
    require(b"CHILD_RECEIVED: omega" in n0, "N0 committed child output missing")
    require(b"CHILD_RECEIVED: alpha" not in n0, "N0 child received abandoned string")

    metadata_path = ROOT / "evidence" / "metadata" / "conpty-experiment-20261027-223358.metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    require(metadata["status"] == "success", "N1 metadata status is not success")
    require(metadata["backspace_key_count"] == 19, "N1 Backspace count is not 19")
    require(metadata["home_key_count"] == 0, "N1 Home count is not 0")
    require(metadata["delete_key_count"] == 0, "N1 Del count is not 0")
    require(metadata["child_exit_code"] == 0, "N1 child exit code is not 0")


def main() -> int:
    try:
        file_count = verify_manifest()
        verify_structures()
    except (AssertionError, OSError, ValueError, KeyError) as error:
        print(f"VERIFY=FAIL: {error}", file=sys.stderr)
        return 1
    print(f"VERIFY=PASS: {file_count} evidence files and all declared byte structures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
