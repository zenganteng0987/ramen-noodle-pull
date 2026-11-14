#!/usr/bin/env python3
"""food-picture-01 entry: write the bundled food picture to the output dir.

The picture ships inside this repository as entry.png (JPEG data — the
brief keeps the name entry.png for PNG and JPEG alike, told apart by their
first bytes). Before copying, the program validates the asset with the
standard library only: JPEG signature and end marker, the 1 MiB size limit,
and the frame dimensions from the SOF segment (at most 1024x1024). It then
writes the bytes unchanged, so repeated runs produce identical output.
"""
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, "entry.png")
MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Return (width, height) from the first SOF0/SOF2 segment."""
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG: missing SOI marker")
    i = 2
    while i + 4 <= len(data):
        if data[i] != 0xFF:
            raise ValueError("corrupt JPEG: expected marker")
        marker = data[i + 1]
        if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        (length,) = struct.unpack(">H", data[i + 2 : i + 4])
        if marker in (0xC0, 0xC2):  # SOF0 / SOF2
            height, width = struct.unpack(">HH", data[i + 5 : i + 9])
            return width, height
        if marker == 0xDA:  # SOS: image data starts, no SOF seen
            break
        i += 2 + length
    raise ValueError("corrupt JPEG: no SOF segment found")


def validate(data: bytes) -> None:
    if len(data) > MAX_BYTES:
        raise ValueError(f"asset too large: {len(data)} bytes > {MAX_BYTES}")
    if not data.endswith(b"\xff\xd9"):
        raise ValueError("corrupt JPEG: missing EOI marker")
    width, height = jpeg_dimensions(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"asset too big: {width}x{height} > {MAX_SIDE}x{MAX_SIDE}")


def main() -> None:
    with open(ASSET, "rb") as fh:
        data = fh.read()
    validate(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()
