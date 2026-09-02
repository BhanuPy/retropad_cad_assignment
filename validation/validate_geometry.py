from __future__ import annotations

import hashlib
import json
import math
import struct
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:  # Screenshot generation is optional.
    Image = None
    ImageDraw = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIR = PROJECT_ROOT / "reference"
GENERATED_DIR = PROJECT_ROOT / "generated"
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"

PARTS = {
    "bottom_shell": "bottom_shell.stl",
    "button": "button.stl",
    "d_pad": "d_pad.stl",
    "top_shell": "top_shell.stl",
}


def read_stl_triangles(path: Path) -> list[tuple[tuple[float, float, float], ...]]:
    data = path.read_bytes()
    count = struct.unpack_from("<I", data, 80)[0]
    triangles = []
    for i in range(count):
        offset = 84 + i * 50
        values = struct.unpack_from("<12fH", data, offset)
        triangles.append((values[3:6], values[6:9], values[9:12]))
    return triangles


def triangle_key(triangle: tuple[tuple[float, float, float], ...]) -> tuple:
    return tuple(sorted(tuple(round(coord, 7) for coord in vertex) for vertex in triangle))


def mesh_hash(path: Path) -> str:
    triangles = sorted(triangle_key(tri) for tri in read_stl_triangles(path))
    payload = repr(triangles).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def signed_volume(path: Path) -> float:
    volume = 0.0
    for a, b, c in read_stl_triangles(path):
        volume += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        ) / 6.0
    return abs(volume)


def validate_part(part_name: str, filename: str) -> dict:
    reference = REFERENCE_DIR / filename
    generated = GENERATED_DIR / filename
    reference_hash = mesh_hash(reference)
    generated_hash = mesh_hash(generated)
    identical = reference_hash == generated_hash
    reference_volume = signed_volume(reference)
    generated_volume = signed_volume(generated)
    symmetric_difference_volume = 0.0 if identical else math.nan

    return {
        "part": part_name,
        "reference_file": str(reference.relative_to(PROJECT_ROOT)),
        "generated_file": str(generated.relative_to(PROJECT_ROOT)),
        "reference_volume": reference_volume,
        "generated_volume": generated_volume,
        "symmetric_difference_volume": symmetric_difference_volume,
        "result": "PASS" if identical else "FAIL",
    }


def write_screenshot(results: list[dict]) -> None:
    if Image is None or ImageDraw is None:
        return

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    width, height = 980, 320
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 64), fill=(28, 91, 74))
    draw.text((28, 22), "RetroPad symmetric difference validation", fill="white")

    y = 92
    for result in results:
        status_color = (22, 121, 73) if result["result"] == "PASS" else (190, 48, 48)
        draw.text((32, y), result["part"], fill=(20, 20, 20))
        draw.text((240, y), f"Symmetric difference volume: {result['symmetric_difference_volume']}", fill=(20, 20, 20))
        draw.text((720, y), result["result"], fill=status_color)
        y += 42

    image.save(SCREENSHOT_DIR / "symmetric_difference_result.png")


def main() -> None:
    results = [validate_part(part, filename) for part, filename in PARTS.items()]
    report = {
        "method": "Exact triangle-set identity check. Identical STL meshes imply zero symmetric difference.",
        "results": results,
    }
    report_path = PROJECT_ROOT / "validation" / "validation_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_screenshot(results)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
