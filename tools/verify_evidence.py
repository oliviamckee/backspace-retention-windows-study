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


def verify_matrix() -> None:
    matrix_dir = ROOT / "evidence" / "matrix"
    specs = [
        ("conpty-matrix-col0-bs7f-20261027-233628", 0, "0x7f", 4, 1),
        ("conpty-matrix-col0-bs08-20261027-233629", 0, "0x08", 4, 1),
        ("conpty-matrix-col4-bs7f-20261027-233631", 4, "0x7f", 5, 0),
        ("conpty-matrix-col4-bs08-20261027-233632", 4, "0x08", 5, 0),
    ]
    streams: dict[tuple[int, str], bytes] = {}

    for stem, start_column, backspace_byte, erase_count, edge_count in specs:
        data = (matrix_dir / f"{stem}.typescript").read_bytes()
        draft_end = data.index(b"alpha") + len(b"alpha")
        final_start = data.index(b"omega", draft_end)
        edit_region = data[draft_end:final_start]
        require(
            edit_region.count(ERASE) == erase_count,
            f"{stem} 08 20 08 count changed",
        )
        require(
            edit_region.count(EDGE_ERASE) == edge_count,
            f"{stem} edge erase count changed",
        )
        require(
            len(edit_region) == 15,
            f"{stem} edit region is not exactly five three-byte erasures",
        )
        require(b"CHILD_RECEIVED: omega" in data, f"{stem} child output missing")
        require(
            b"CHILD_RECEIVED: alpha" not in data,
            f"{stem} child received the abandoned string",
        )

        metadata = json.loads((matrix_dir / f"{stem}.metadata.json").read_text(encoding="utf-8"))
        require(metadata["status"] == "success", f"{stem} status is not success")
        require(metadata["matrix_case_passed"] is True, f"{stem} matrix check failed")
        require(metadata["matrix_start_column"] == start_column, f"{stem} column changed")
        require(
            metadata["serialized_backspace_byte"] == backspace_byte,
            f"{stem} serialized Backspace changed",
        )
        require(metadata["scripted_backspace_count"] == 5, f"{stem} erase input count changed")
        require(metadata["scripted_key_delay_ms"] == 75, f"{stem} key pacing changed")
        require(metadata["child_exit_code"] == 0, f"{stem} child exit code changed")
        streams[(start_column, backspace_byte)] = data

    for start_column in (0, 4):
        delete_stream = streams[(start_column, "0x7f")].replace(b"0x7f", b"0x08")
        backspace_stream = streams[(start_column, "0x08")]
        require(
            delete_stream == backspace_stream,
            f"column {start_column} output differs beyond the self-label",
        )


def verify_powershell_screen_copy() -> None:
    path = ROOT / "evidence" / "screen-copies" / "backspacetextretention2.txt"
    data = path.read_bytes()
    require(len(data) == 1579, "O1 screen-copy byte length changed")
    require(data.startswith(b"Windows PowerShell\r\n"), "O1 PowerShell banner missing")
    require(
        b"PS C:\\Users\\12149> phoebe is sleeping\r\n" in data,
        "O1 visible phoebe entry missing",
    )
    require(
        b"CommandNotFoundException" in data,
        "O1 PowerShell error record missing",
    )
    require(data.endswith(b"fwd-i-search: _\r\n"), "O1 exact ending changed")
    require(data.count(b"\r\n") == 27, "O1 CRLF count is not 27")
    require(b"\x08" not in data, "O1 unexpectedly contains Backspace bytes")
    require(b"\x7f" not in data, "O1 unexpectedly contains Delete bytes")
    require(b"\x1b" not in data, "O1 unexpectedly contains escape bytes")
    require(
        b"**********************\r\nWindows PowerShell transcript start" not in data,
        "O1 unexpectedly contains a PowerShell transcript header",
    )

    metadata_path = ROOT / "evidence" / "metadata" / "powershell-screen-copy-20261028.metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    require(metadata["byte_length"] == len(data), "O1 metadata byte length changed")
    require(
        metadata["sha256"] == hashlib.sha256(data).hexdigest(),
        "O1 metadata hash changed",
    )
    require(metadata["byte_counts"]["backspace_0x08"] == 0, "O1 metadata Backspace count changed")
    require(metadata["byte_counts"]["delete_0x7f"] == 0, "O1 metadata Delete count changed")
    require(metadata["byte_counts"]["escape_0x1b"] == 0, "O1 metadata escape count changed")


def main() -> int:
    try:
        file_count = verify_manifest()
        verify_structures()
        verify_matrix()
        verify_powershell_screen_copy()
    except (AssertionError, OSError, ValueError, KeyError) as error:
        print(f"VERIFY=FAIL: {error}", file=sys.stderr)
        return 1
    print(f"VERIFY=PASS: {file_count} evidence files and all declared byte structures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
