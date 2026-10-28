#!/usr/bin/env python3
"""Generate the 1200 x 630 social card using only the Python standard library.

Typography is a small vector pixel alphabet. The SVG is the source image;
the PNG renderer supports its integer, solid-color rectangles only. No fonts,
image libraries, browser, or operating-system render cache are required.
"""

from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zlib

ASSETS = Path(__file__).resolve().parent / "assets"
WIDTH, HEIGHT = 1200, 630
GLYPHS = {
    "A": "01110 10001 10001 11111 10001 10001 10001",
    "B": "11110 10001 10001 11110 10001 10001 11110",
    "C": "01111 10000 10000 10000 10000 10000 01111",
    "D": "11110 10001 10001 10001 10001 10001 11110",
    "E": "11111 10000 10000 11110 10000 10000 11111",
    "F": "11111 10000 10000 11110 10000 10000 10000",
    "G": "01111 10000 10000 10111 10001 10001 01111",
    "H": "10001 10001 10001 11111 10001 10001 10001",
    "I": "11111 00100 00100 00100 00100 00100 11111",
    "J": "00111 00010 00010 00010 10010 10010 01100",
    "K": "10001 10010 10100 11000 10100 10010 10001",
    "L": "10000 10000 10000 10000 10000 10000 11111",
    "M": "10001 11011 10101 10101 10001 10001 10001",
    "N": "10001 11001 10101 10011 10001 10001 10001",
    "O": "01110 10001 10001 10001 10001 10001 01110",
    "P": "11110 10001 10001 11110 10000 10000 10000",
    "Q": "01110 10001 10001 10001 10101 10010 01101",
    "R": "11110 10001 10001 11110 10100 10010 10001",
    "S": "01111 10000 10000 01110 00001 00001 11110",
    "T": "11111 00100 00100 00100 00100 00100 00100",
    "U": "10001 10001 10001 10001 10001 10001 01110",
    "V": "10001 10001 10001 10001 10001 01010 00100",
    "W": "10001 10001 10001 10101 10101 10101 01010",
    "X": "10001 10001 01010 00100 01010 10001 10001",
    "Y": "10001 10001 01010 00100 00100 00100 00100",
    "Z": "11111 00001 00010 00100 01000 10000 11111",
    "0": "01110 10001 10011 10101 11001 10001 01110",
    "2": "01110 10001 00001 00010 00100 01000 11111",
    "-": "00000 00000 00000 11111 00000 00000 00000",
    ".": "00000 00000 00000 00000 00000 00110 00110",
    "/": "00001 00001 00010 00100 01000 10000 10000",
    " ": "00000 00000 00000 00000 00000 00000 00000",
}


def main():
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg",
                     width=str(WIDTH), height=str(HEIGHT), viewBox="0 0 1200 630")
    ET.SubElement(svg, "title").text = "job-agent-kit — AI job search. You approve."

    def rect(x, y, width, height, color):
        ET.SubElement(svg, "rect", x=str(x), y=str(y), width=str(width),
                      height=str(height), fill=color)

    def label(text, x, y, scale, color):
        for index, char in enumerate(text):
            for row, bits in enumerate(GLYPHS[char].split()):
                for column, bit in enumerate(bits):
                    if bit == "1":
                        rect(x + (index * 6 + column) * scale,
                             y + row * scale, scale, scale, color)

    rect(0, 0, WIDTH, HEIGHT, "#f0eee6")
    rect(0, 0, 18, HEIGHT, "#a8502e")
    rect(80, 82, 12, 12, "#a8502e")
    label("OPEN SOURCE / MIT / V0.2.0", 112, 78, 3, "#a8502e")
    label("JOB-AGENT-KIT", 80, 182, 12, "#141413")
    label("AI JOB SEARCH. YOU APPROVE.", 80, 314, 5, "#a8502e")
    rect(80, 399, 1040, 2, "#d8d3c4")
    label("CLAUDE CODE / CODEX", 80, 440, 3, "#5e5d59")
    label("SCOUT / TRACK / REVIEW", 80, 506, 3, "#5e5d59")
    ET.indent(svg)
    source = ASSETS / "og.svg"
    ET.ElementTree(svg).write(source, encoding="utf-8", xml_declaration=True)

    # Render the saved SVG, so the bitmap always comes from the vector source.
    pixels = bytearray(WIDTH * HEIGHT * 3)
    root = ET.parse(source).getroot()
    for node in root:
        if node.tag.rsplit("}", 1)[-1] != "rect":
            continue
        x, y, width, height = (int(node.attrib[key]) for key in ("x", "y", "width", "height"))
        assert 0 <= x < x + width <= WIDTH and 0 <= y < y + height <= HEIGHT
        color = bytes.fromhex(node.attrib["fill"].removeprefix("#"))
        scanline = color * width
        for row in range(y, y + height):
            start = (row * WIDTH + x) * 3
            pixels[start:start + width * 3] = scanline
    raw = b"".join(b"\0" + pixels[row * WIDTH * 3:(row + 1) * WIDTH * 3] for row in range(HEIGHT))

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    (ASSETS / "og.png").write_bytes(png)
    print(f"Generated site/assets/og.svg → og.png ({WIDTH}×{HEIGHT}, {len(png):,} bytes)")


if __name__ == "__main__":
    main()
