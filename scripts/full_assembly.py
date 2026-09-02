from build123d import *

from retropad_common import (
    generated_stl_path,
)

# ============================================================
# LOAD PARTS
# ============================================================

bottom_shell = import_stl(
    generated_stl_path("bottom_shell")
)

top_shell = import_stl(
    generated_stl_path("top_shell")
)

button = import_stl(
    generated_stl_path("button")
)

d_pad = import_stl(
    generated_stl_path("d_pad")
)

# ============================================================
# XY POSITIONS
# ============================================================

DPAD_X = -38.0
DPAD_Y = 1.0

BTN_X = 38.0
BTN_Y = 2.0

BTN_VERTICAL = 8.5
BTN_HORIZONTAL = 10.0

# ============================================================
# Z POSITIONS
# ============================================================

# Controls live INSIDE the housing

CONTROL_Z = 8.0

BUTTON_Z = CONTROL_Z
DPAD_Z = CONTROL_Z

# Visible seam between shells
TOP_SHELL_Z = 7.5

# ============================================================
# BUTTON POSITIONS
# ============================================================

BUTTON_POSITIONS = [

    (
        BTN_X,
        BTN_Y + BTN_VERTICAL,
        BUTTON_Z,
    ),

    (
        BTN_X,
        BTN_Y - BTN_VERTICAL,
        BUTTON_Z,
    ),

    (
        BTN_X - BTN_HORIZONTAL,
        BTN_Y,
        BUTTON_Z,
    ),

    (
        BTN_X + BTN_HORIZONTAL,
        BTN_Y,
        BUTTON_Z,
    ),
]

# ============================================================
# BUILD ASSEMBLY
# ============================================================

parts = []

# ------------------------------------------------------------
# Bottom shell
# ------------------------------------------------------------

parts.append(bottom_shell)

# ------------------------------------------------------------
# D-Pad
# ------------------------------------------------------------

parts.append(
    d_pad.moved(
        Location(
            (
                DPAD_X,
                DPAD_Y,
                DPAD_Z,
            )
        )
    )
)

# ------------------------------------------------------------
# Buttons
# ------------------------------------------------------------

for pos in BUTTON_POSITIONS:

    parts.append(
        button.moved(
            Location(pos)
        )
    )

# ------------------------------------------------------------
# Top shell
# ------------------------------------------------------------

parts.append(
    top_shell.moved(
        Location(
            (
                0.0,
                0.0,
                TOP_SHELL_Z,
            )
        )
    )
)

# ============================================================
# CREATE COMPOUND
# ============================================================

assembly = Compound(
    children=parts
)

print("Assembly created")
print(type(assembly))

# ============================================================
# EXPORT STL
# ============================================================

export_stl(
    assembly,
    "full_assembly.stl"
)

# ============================================================
# EXPORT STEP
# ============================================================

try:

    export_step(
        assembly,
        "full_assembly.step"
    )

except Exception as e:

    print(
        f"STEP export skipped: {e}"
    )

print("full_assembly exported")