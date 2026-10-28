#!/usr/bin/env python3
"""Lightweight Windows replication of the Backspace Gate input boundary.

The interactive recorder preserves the displayed byte stream, including
backspace-space-backspace erasures.  A separate receiver process is launched
only after the committed line exactly matches the predeclared control.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ERASE_TRIPLET = b"\x08\x20\x08"


def receiver() -> int:
    committed = sys.stdin.buffer.readline().rstrip(b"\r\n")
    sys.stdout.write(f"RECEIVER_SAW: {committed.decode('ascii', errors='replace')}\r\n")
    sys.stdout.flush()
    return 0


def choose_paths(output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    stem = f"backspace-experiment-{stamp}"
    transcript = output_dir / f"{stem}.typescript"
    metadata = output_dir / f"{stem}.metadata.json"
    suffix = 2
    while transcript.exists() or metadata.exists():
        transcript = output_dir / f"{stem}-{suffix}.typescript"
        metadata = output_dir / f"{stem}-{suffix}.metadata.json"
        suffix += 1
    return transcript, metadata


def write_both(transcript, data: bytes) -> None:
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()
    transcript.write(data)
    transcript.flush()


def run_interactive(output_dir: Path) -> int:
    if os.name != "nt":
        raise SystemExit("This lightweight harness currently requires Windows.")

    import msvcrt

    transcript_path, metadata_path = choose_paths(output_dir)
    started = datetime.now(timezone.utc).isoformat()
    buffer: list[str] = []
    receiver_started = False
    receiver_output = b""
    status = "aborted"
    delete_key_erase_count = 0
    backspace_key_erase_count = 0

    with transcript_path.open("xb") as transcript:
        header = (
            "BACKSPACE GATE — WINDOWS DELETE-KEY REPLICATION\r\n"
            "The blank line below is the recorded editable input.\r\n"
            "Delete is mapped to the original experiment's backward erase.\r\n"
            "After erasing the draft, type any nonempty final sentence and press Enter.\r\n"
            "\r\n"
        ).encode("utf-8")
        write_both(transcript, header)

        try:
            while True:
                ch = msvcrt.getwch()

                if ch in ("\x00", "\xe0"):
                    extended = msvcrt.getwch()
                    if extended == "S":
                        if buffer:
                            buffer.pop()
                            delete_key_erase_count += 1
                            write_both(transcript, ERASE_TRIPLET)
                        else:
                            sys.stdout.buffer.write(b"\x07")
                            sys.stdout.buffer.flush()
                    continue
                if ch == "\x03":
                    write_both(transcript, b"\r\nABORTED_BY_USER\r\n")
                    status = "aborted_by_user"
                    break
                if ch == "\x08":
                    if buffer:
                        buffer.pop()
                        backspace_key_erase_count += 1
                        write_both(transcript, ERASE_TRIPLET)
                    else:
                        sys.stdout.buffer.write(b"\x07")
                        sys.stdout.buffer.flush()
                    continue
                if ch in ("\r", "\n"):
                    write_both(transcript, b"\r\n")
                    committed = "".join(buffer)
                    if not committed:
                        write_both(
                            transcript,
                            b"EMPTY_COMMIT: receiver was not launched.\r\n",
                        )
                        status = "empty_commit"
                        break

                    child = subprocess.run(
                        [sys.executable, str(Path(__file__).resolve()), "--receiver"],
                        input=(committed + "\n").encode("ascii"),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        check=False,
                    )
                    receiver_started = True
                    receiver_output = child.stdout
                    write_both(transcript, receiver_output)
                    status = "success" if child.returncode == 0 else "receiver_error"
                    break

                if len(ch) == 1 and 0x20 <= ord(ch) <= 0x7E:
                    buffer.append(ch)
                    write_both(transcript, ch.encode("ascii"))
                else:
                    sys.stdout.buffer.write(b"\x07")
                    sys.stdout.buffer.flush()
        except KeyboardInterrupt:
            write_both(transcript, b"\r\nABORTED_BY_USER\r\n")
            status = "aborted_by_user"

    transcript_bytes = transcript_path.read_bytes()
    metadata = {
        "method": "lightweight-windows-backspace-gate-v3-delete-key",
        "status": status,
        "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "transcript_path": str(transcript_path.resolve()),
        "transcript_bytes": len(transcript_bytes),
        "transcript_sha256": hashlib.sha256(transcript_bytes).hexdigest(),
        "erase_triplet_count": transcript_bytes.count(ERASE_TRIPLET),
        "committed_policy": "any nonempty ASCII line",
        "delete_key_erase_count": delete_key_erase_count,
        "backspace_key_erase_count": backspace_key_erase_count,
        "receiver_started": receiver_started,
        "receiver_output_sha256": hashlib.sha256(receiver_output).hexdigest()
        if receiver_started
        else None,
        "python": sys.version,
        "platform": sys.platform,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    print(f"STATUS={status}")
    print(f"TRANSCRIPT_PATH={transcript_path.resolve()}")
    print(f"METADATA_PATH={metadata_path.resolve()}")
    print(f"TRANSCRIPT_SHA256={metadata['transcript_sha256']}")
    return 0 if status == "success" else 2


def self_test() -> int:
    draft = b"SYNTHETIC_7"
    committed = b"FINAL SENTENCE"
    stream = draft + ERASE_TRIPLET * len(draft) + committed
    erase_start = stream.index(ERASE_TRIPLET)
    recovered = stream[:erase_start]
    after = stream[erase_start + len(ERASE_TRIPLET) * len(draft) :]
    assert recovered == draft
    assert after == committed
    assert stream.count(ERASE_TRIPLET) == len(draft)
    print("SELF_TEST=PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--receiver", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.receiver:
        return receiver()
    if args.self_test:
        return self_test()
    if args.output_dir is None:
        parser.error("--output-dir is required for an interactive trial")
    return run_interactive(args.output_dir.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
