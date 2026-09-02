from pathlib import Path
import sys
import datetime

import numpy as np
import trimesh

from retropad_common import (
    reference_path,
    generated_stl_path,
)

# ============================================================
# CONFIG
# ============================================================

PARTS = [
    "bottom_shell",
    "top_shell",
    "button",
    "d_pad",
]

REPORT_DIR = Path(
    r"G:\Projects\cad_assignment_retropad\reports"
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ============================================================
# TEE OUTPUT
# ============================================================

class Tee:

    def __init__(self, *files):
        self.files = files

    def write(self, obj):

        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):

        for f in self.files:
            f.flush()

# ============================================================
# SCORING
# ============================================================

def score_label(score):

    if score >= 95:
        return "BEST"

    if score >= 90:
        return "EXCELLENT"

    if score >= 85:
        return "BETTER"

    if score >= 80:
        return "GOOD"

    if score >= 70:
        return "NEEDS WORK"

    return "POOR"


def percentage_match(reference, generated):

    if reference == 0:
        return 0.0

    diff = abs(reference - generated)

    return max(
        0.0,
        100.0 - ((diff / reference) * 100.0)
    )

# ============================================================
# PART ANALYSIS
# ============================================================

def analyze_part(part_name):

    ref_path = reference_path(part_name)
    gen_path = generated_stl_path(part_name)

    print("\n")
    print("=" * 70)
    print(part_name.upper())
    print("=" * 70)

    if not ref_path.exists():

        print(
            f"Reference STL missing:\n{ref_path}"
        )

        return None

    if not gen_path.exists():

        print(
            f"Generated STL missing:\n{gen_path}"
        )

        return None

    print(f"\nReference STL : {ref_path}")
    print(f"Generated STL : {gen_path}")

    print("\nLoading meshes...")

    ref = trimesh.load_mesh(ref_path)
    gen = trimesh.load_mesh(gen_path)

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    ref_volume = abs(ref.volume)
    gen_volume = abs(gen.volume)

    volume_diff = abs(
        ref_volume - gen_volume
    )

    volume_score = percentage_match(
        ref_volume,
        gen_volume
    )

    # --------------------------------------------------------
    # SURFACE AREA
    # --------------------------------------------------------

    ref_area = ref.area
    gen_area = gen.area

    area_diff = abs(
        ref_area - gen_area
    )

    area_score = percentage_match(
        ref_area,
        gen_area
    )

    # --------------------------------------------------------
    # BOUNDING BOX
    # --------------------------------------------------------

    ref_bbox = ref.bounding_box.extents
    gen_bbox = gen.bounding_box.extents

    bbox_scores = []

    for r, g in zip(ref_bbox, gen_bbox):

        bbox_scores.append(
            percentage_match(r, g)
        )

    bbox_score = float(
        np.mean(bbox_scores)
    )

    # --------------------------------------------------------
    # OVERALL
    # --------------------------------------------------------

    final_score = (
        volume_score * 0.40 +
        area_score * 0.30 +
        bbox_score * 0.30
    )

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    print("\nVOLUME")
    print("-" * 70)

    print(
        f"Reference Volume : {ref_volume:.3f}"
    )

    print(
        f"Generated Volume : {gen_volume:.3f}"
    )

    print(
        f"Volume Difference: {volume_diff:.3f}"
    )

    print(
        f"Volume Match     : {volume_score:.2f}%"
    )

    # --------------------------------------------------------

    print("\nSURFACE AREA")
    print("-" * 70)

    print(
        f"Reference Area   : {ref_area:.3f}"
    )

    print(
        f"Generated Area   : {gen_area:.3f}"
    )

    print(
        f"Area Difference  : {area_diff:.3f}"
    )

    print(
        f"Surface Match    : {area_score:.2f}%"
    )

    # --------------------------------------------------------

    print("\nBOUNDING BOX")
    print("-" * 70)

    print("\nReference")

    print(f"Width  : {ref_bbox[0]:.3f}")
    print(f"Length : {ref_bbox[1]:.3f}")
    print(f"Height : {ref_bbox[2]:.3f}")

    print("\nGenerated")

    print(f"Width  : {gen_bbox[0]:.3f}")
    print(f"Length : {gen_bbox[1]:.3f}")
    print(f"Height : {gen_bbox[2]:.3f}")

    print("\nDifference")

    print(
        f"Width  : {abs(ref_bbox[0]-gen_bbox[0]):.3f}"
    )

    print(
        f"Length : {abs(ref_bbox[1]-gen_bbox[1]):.3f}"
    )

    print(
        f"Height : {abs(ref_bbox[2]-gen_bbox[2]):.3f}"
    )

    print(
        f"\nBBox Match       : {bbox_score:.2f}%"
    )

    # --------------------------------------------------------

    print("\n" + "-" * 70)

    print(
        f"\nOVERALL MATCH    : {final_score:.2f}%"
    )

    print(
        f"STATUS           : {score_label(final_score)}"
    )

    return final_score

# ============================================================
# MAIN
# ============================================================

def main():

    timestamp = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    report_file = (
        REPORT_DIR /
        f"validation_report_{timestamp}.txt"
    )

    report_handle = open(
        report_file,
        "w",
        encoding="utf-8"
    )

    original_stdout = sys.stdout

    sys.stdout = Tee(
        sys.stdout,
        report_handle
    )

    try:

        scores = []

        print("\n")
        print("=" * 70)
        print("RETROPAD CAD VALIDATION REPORT")
        print("=" * 70)

        print(
            f"\nGenerated : "
            f"{datetime.datetime.now()}"
        )

        print(
            f"Report File : "
            f"{report_file}"
        )

        for part_name in PARTS:

            score = analyze_part(part_name)

            if score is not None:
                scores.append(score)

        if scores:

            overall_score = float(
                np.mean(scores)
            )

            print("\n")
            print("=" * 70)
            print("PROJECT SUMMARY")
            print("=" * 70)

            print(
                f"\nPROJECT MATCH    : "
                f"{overall_score:.2f}%"
            )

            print(
                f"STATUS           : "
                f"{score_label(overall_score)}"
            )

            print("\nPART SCORES")
            print("-" * 70)

            for part_name, score in zip(
                PARTS,
                scores
            ):

                print(
                    f"{part_name:<15}"
                    f"{score:>8.2f}%   "
                    f"{score_label(score)}"
                )

        print("\n")
        print("=" * 70)
        print("REPORT SAVED")
        print("=" * 70)

        print(report_file)

    finally:

        sys.stdout = original_stdout

        report_handle.close()

        print(
            f"\nReport written to:\n{report_file}"
        )


if __name__ == "__main__":
    main()