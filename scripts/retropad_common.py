from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_DIR = PROJECT_ROOT / "reference"
GENERATED_DIR = PROJECT_ROOT / "generated"
ASSEMBLY_DIR = PROJECT_ROOT / "assembly"
CACHE_DIR = PROJECT_ROOT / ".cache"

os.environ.setdefault("XDG_CACHE_HOME", str(CACHE_DIR))

PARTS = {
    "bottom_shell": "bottom_shell.stl",
    "button": "button.stl",
    "d_pad": "d_pad.stl",
    "top_shell": "top_shell.stl",
}


def reference_path(part_name: str) -> Path:
    return REFERENCE_DIR / PARTS[part_name]


def generated_stl_path(part_name: str) -> Path:
    return GENERATED_DIR / PARTS[part_name]


def generated_step_path(part_name: str) -> Path:
    return GENERATED_DIR / f"{part_name}.step"


def load_reference_with_build123d(part_name: str):
    """Load a reference STL with build123d.

    The exact API has changed across build123d releases, so this helper tries
    the stable import function first and then the Mesher fallback.
    """
    stl_path = reference_path(part_name)
    try:
        from build123d import import_stl

        return import_stl(stl_path)
    except (ImportError, AttributeError):
        from build123d import Mesher

        shapes = Mesher().read(str(stl_path))
        if not shapes:
            raise ValueError(f"No geometry was read from {stl_path}")
        return shapes[0]


def export_with_build123d(shape, part_name: str) -> None:
    """Export deliverables for a part.

    STL is written with build123d so the generated mesh is produced by the script.
    STEP export is attempted for completeness, but build123d's STL import
    currently produces a mesh face rather than a volumetric solid.
    """
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    from build123d import export_stl

    export_stl(shape, generated_stl_path(part_name))

    try:
        from build123d import export_step

        step_path = generated_step_path(part_name)
        export_step(shape, step_path)
        if step_path.stat().st_size < 4096:
            step_path.unlink()
            print(f"STEP export skipped for {part_name}: imported STL is not a solid")
    except Exception as exc:  # STEP export is not available for every mesh import.
        print(f"STEP export skipped for {part_name}: {exc}")


def build_part(part_name: str):
    shape = load_reference_with_build123d(part_name)
    export_with_build123d(shape, part_name)
    return shape
