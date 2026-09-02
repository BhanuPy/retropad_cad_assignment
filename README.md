# RetroPad CAD Reverse Engineering Assignment

## Overview

This project recreates a RetroPad game controller using parametric CAD modeling in Build123d.

The supplied STL reference models were reverse engineered and rebuilt as fully parametric models while preserving the overall dimensions, proportions, and assembly relationships of the original design.

Generated parts:

* Bottom Shell
* Top Shell
* Button
* D-Pad
* Full Assembly

The project also includes validation and analysis tools for comparing generated geometry against the supplied reference models.

---

# Project Structure

```text
cad_assignment_retropad/

├── reference/
│   ├── bottom_shell.stl
│   ├── top_shell.stl
│   ├── button.stl
│   └── d_pad.stl
│
├── generated/
│   ├── bottom_shell.stl
│   ├── top_shell.stl
│   ├── button.stl
│   ├── d_pad.stl
│   ├── full_assembly.stl
│   └── *.step
│
├── reports/
│   └── validation_report_*.txt
│
├── scripts/
│   ├── bottom_shell.py
│   ├── top_shell.py
│   ├── button.py
│   ├── d_pad.py
│   ├── full_assembly.py
│   ├── diff_using_trimesh.py
│   ├── profile_references.py
│   └── retropad_common.py
│
└── README.md
```

---

# Requirements

## Python

```bash
Python 3.11+
```

## Dependencies

Install dependencies:

```bash
pip install build123d
pip install trimesh
pip install numpy
```

---

# Part Generation

Generate individual parts.

## Bottom Shell

```bash
python bottom_shell.py
```

Output:

```text
generated/bottom_shell.stl
```

---

## Top Shell

```bash
python top_shell.py
```

Output:

```text
generated/top_shell.stl
```

---

## Button

```bash
python button.py
```

Output:

```text
generated/button.stl
```

---

## D-Pad

```bash
python d_pad.py
```

Output:

```text
generated/d_pad.stl
```

---

# Utility Scripts

## retropad_common.py

Common helper module used across the entire project.

Responsibilities:

* Project path management
* Reference STL lookup
* Generated STL lookup
* STL import
* STL export
* STEP export
* Common utility functions

Example:

```python
from retropad_common import (
    reference_path,
    generated_stl_path,
    export_with_build123d,
)
```

Benefits:

* Eliminates duplicated code
* Centralizes file management
* Keeps scripts clean and maintainable

---

## profile_references.py

Reference analysis utility.

This script loads all supplied STL reference models and reports:

* Width
* Length
* Height
* Center Point

Run:

```bash
python profile_references.py
```

Example Output:

```text
=== TOP_SHELL ===
Size X (Width): 135.00 mm
Size Y (Length): 53.00 mm
Size Z (Height): 14.82 mm
Center Point: (0.00, 0.00, 7.41)
```

Purpose:

* Determine overall dimensions
* Verify extracted measurements
* Assist in assembly positioning

---

## diff_using_trimesh.py

Automated validation system.

This tool compares generated models against supplied reference STL files.

Run:

```bash
python diff_using_trimesh.py
```

Reports are automatically written to:

```text
reports/
```

Example:

```text
validation_report_20260610_143210.txt
```

---

# Validation Methodology

The validation tool computes:

## Volume Match

Measures similarity of enclosed volume.

```text
Reference Volume
Generated Volume
Volume Difference
Volume Match %
```

---

## Surface Area Match

Measures similarity of total surface area.

```text
Reference Area
Generated Area
Area Difference
Surface Match %
```

---

## Bounding Box Match

Measures dimensional similarity.

```text
Width Match
Length Match
Height Match
Bounding Box Match %
```

---

## Overall Match Score

Weighted score:

```text
40% Volume Match
30% Surface Match
30% Bounding Box Match
```

Formula:

```text
Overall =
0.40 × Volume Match
+
0.30 × Surface Match
+
0.30 × Bounding Box Match
```

---

## Status Labels

```text
95%+   BEST
90%+   EXCELLENT
85%+   BETTER
80%+   GOOD
70%+   NEEDS WORK
<70%   POOR
```

---

# Full Assembly

The project includes an assembly generator.

Run:

```bash
python full_assembly.py
```

Generated Outputs:

```text
generated/full_assembly.stl
generated/full_assembly.step
```

Assembly includes:

* Bottom Shell
* Top Shell
* D-Pad
* Four Action Buttons

The assembly script:

1. Loads generated parts.
2. Positions D-Pad.
3. Positions buttons.
4. Places top shell.
5. Exports complete assembly.

---

# Reverse Engineering Workflow

The supplied STL models were reconstructed using the following process.

## 1. Reference Analysis

Reference STL files were imported into Blender.

Measurements extracted:

* Overall dimensions
* Heights
* Hole diameters
* Boss locations
* Button locations
* D-Pad dimensions

---

## 2. Parametric Reconstruction

Each part was recreated using Build123d.

Features implemented:

### Bottom Shell

* Outer enclosure
* Internal cavity
* Screw bosses
* Internal support structures

### Top Shell

* Hollow shell
* D-Pad cutout
* Button cutouts
* Internal guide rings
* Screw boss receptacles
* Cable opening
* Internal support wall

### Button

* Cylindrical body
* Retention ribs
* Top chamfer

### D-Pad

* Cross profile
* Elliptical center section
* Retention lip
* Bottom pivot

---

## 3. Visual Overlay Verification

Generated models were overlaid against reference STL files in Blender.

Comparison views:

* Top
* Front
* Right
* Perspective

Used to refine:

* Heights
* Widths
* Chamfers
* Boss placement
* Internal feature positioning

---

## 4. Automated Validation

Trimesh validation was used to compare:

* Volume
* Surface Area
* Bounding Box

This provided objective measurements of similarity.

---

# Deliverables

Generated files:

```text
bottom_shell.stl
top_shell.stl
button.stl
d_pad.stl
full_assembly.stl
```

Source files:

```text
bottom_shell.py
top_shell.py
button.py
d_pad.py
full_assembly.py
```

Utility files:

```text
retropad_common.py
profile_references.py
diff_using_trimesh.py
```

Validation reports:

```text
reports/*.txt
```

---

# Tools Used

* Python
* Build123d
* Trimesh
* Blender

---

# Author

Bhanu Pratap

Pipeline TD / Python Developer

Experience:

* Python Development
* CAD Automation
* VFX / Animation Pipelines
* Build123d
* Geometry Processing
* Reverse Engineering Workflows

```
```
