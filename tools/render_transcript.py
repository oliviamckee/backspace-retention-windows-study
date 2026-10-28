#!/usr/bin/env python3
"""Render a raw terminal transcript without modifying it."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def caret_render(data: bytes) -> str:
    output: list[str] = []
    for byte in data:
        if byte == 0x08:
            output.append("^H")
        elif byte == 0x0D:
            output.append("^M")
        elif byte == 0x0A:
            output.append("^J\n")
        elif byte == 0x1B:
            output.append("<ESC>")
        elif byte == 0x07:
            output.append("<BEL>")
        elif 0x20 <= byte <= 0x7E:
            output.append(chr(byte))
        else:
            output.append(f"<0x{byte:02X}>")
    return "".join(output)


def hexdump(data: bytes, width: int = 16) -> str:
    lines: list[str] = []
    for offset in range(0, len(data), width):
        chunk = data[offset : offset + width]
        hex_bytes = " ".join(f"{byte:02x}" for byte in chunk)
        printable = "".join(chr(byte) if 0x20 <= byte <= 0x7E else "." for byte in chunk)
        lines.append(f"{offset:08x}  {hex_bytes:<47}  |{printable}|")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--hex", action="store_true", help="render a full hex view")
    args = parser.parse_args()

    data = args.transcript.read_bytes()
    print(f"FILE: {args.transcript}")
    print(f"BYTES: {len(data)}")
    print(f"SHA-256: {hashlib.sha256(data).hexdigest()}")
    print()
    print(hexdump(data) if args.hex else caret_render(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
