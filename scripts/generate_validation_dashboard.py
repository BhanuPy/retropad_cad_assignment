from pathlib import Path
from datetime import datetime

import numpy as np
import trimesh

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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


def status_color(status):

    colors = {

        "BEST": (27, 94, 32),
        "EXCELLENT": (46, 125, 50),
        "BETTER": (21, 101, 192),
        "GOOD": (239, 108, 0),
        "NEEDS WORK": (198, 40, 40),
        "POOR": (128, 0, 0),
    }

    return colors.get(
        status,
        (80, 80, 80)
    )


def percentage_match(reference, generated):

    if reference == 0:
        return 0

    diff = abs(reference - generated)

    return max(
        0,
        100 - (diff / reference * 100)
    )

# ============================================================
# ANALYZE
# ============================================================

def analyze_part(part_name):

    ref = trimesh.load_mesh(
        reference_path(part_name)
    )

    gen = trimesh.load_mesh(
        generated_stl_path(part_name)
    )

    # --------------------------------------------
    # Volume
    # --------------------------------------------

    ref_volume = abs(ref.volume)
    gen_volume = abs(gen.volume)

    volume_score = percentage_match(
        ref_volume,
        gen_volume
    )

    # --------------------------------------------
    # Surface
    # --------------------------------------------

    ref_area = ref.area
    gen_area = gen.area

    area_score = percentage_match(
        ref_area,
        gen_area
    )

    # --------------------------------------------
    # BBox
    # --------------------------------------------

    ref_bbox = ref.bounding_box.extents
    gen_bbox = gen.bounding_box.extents

    bbox_scores = []

    for r, g in zip(
        ref_bbox,
        gen_bbox
    ):

        bbox_scores.append(
            percentage_match(r, g)
        )

    bbox_score = np.mean(
        bbox_scores
    )

    # --------------------------------------------
    # Overall
    # --------------------------------------------

    overall = (

        volume_score * 0.40 +

        area_score * 0.30 +

        bbox_score * 0.30
    )

    return {

        "part": part_name,

        "volume": volume_score,

        "surface": area_score,

        "bbox": bbox_score,

        "overall": overall,

        "status": score_label(
            overall
        )
    }

# ============================================================
# PNG REPORT
# ============================================================

def create_dashboard(results):

    overall_score = np.mean(
        [
            r["overall"]
            for r in results
        ]
    )

    width = 1600
    row_h = 80
    header_h = 100

    height = (
        header_h +
        row_h * (len(results) + 4)
    )

    img = Image.new(
        "RGB",
        (width, height),
        (245, 245, 245)
    )

    draw = ImageDraw.Draw(img)

    try:

        title_font = ImageFont.truetype(
            "arial.ttf",
            32
        )

        header_font = ImageFont.truetype(
            "arial.ttf",
            22
        )

        body_font = ImageFont.truetype(
            "arial.ttf",
            20
        )

    except:

        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # ====================================================
    # HEADER
    # ====================================================

    draw.rectangle(
        (0, 0, width, header_h),
        fill=(31, 107, 87)
    )

    draw.text(
        (30, 30),
        "RetroPad CAD Validation Dashboard",
        fill="white",
        font=title_font
    )

    y = header_h + 20

    # ====================================================
    # TABLE HEADERS
    # ====================================================

    headers = [

        ("Part", 40),
        ("Volume", 280),
        ("Surface", 500),
        ("BBox", 700),
        ("Overall", 900),
        ("Status", 1120),
    ]

    for text, x in headers:

        draw.text(
            (x, y),
            text,
            fill="black",
            font=header_font
        )

    y += 40

    draw.line(
        (
            20,
            y,
            width - 20,
            y
        ),
        fill="gray",
        width=2
    )

    y += 20

    # ====================================================
    # ROWS
    # ====================================================

    for row in results:

        draw.text(
            (40, y),
            row["part"],
            fill="black",
            font=body_font
        )

        draw.text(
            (280, y),
            f'{row["volume"]:.2f}%',
            fill="black",
            font=body_font
        )

        draw.text(
            (500, y),
            f'{row["surface"]:.2f}%',
            fill="black",
            font=body_font
        )

        draw.text(
            (700, y),
            f'{row["bbox"]:.2f}%',
            fill="black",
            font=body_font
        )

        draw.text(
            (900, y),
            f'{row["overall"]:.2f}%',
            fill="black",
            font=body_font
        )

        draw.text(
            (1120, y),
            row["status"],
            fill=status_color(
                row["status"]
            ),
            font=body_font
        )

        y += row_h

    # ====================================================
    # SUMMARY
    # ====================================================

    draw.line(
        (
            20,
            y,
            width - 20,
            y
        ),
        fill="gray",
        width=2
    )

    y += 30

    project_status = score_label(
        overall_score
    )

    draw.text(
        (40, y),
        f"Project Match : {overall_score:.2f}%",
        fill="black",
        font=header_font
    )

    draw.text(
        (500, y),
        f"Status : {project_status}",
        fill=status_color(
            project_status
        ),
        font=header_font
    )

    y += 60

    # Progress bar

    bar_w = 900
    bar_h = 35

    draw.rectangle(
        (
            40,
            y,
            40 + bar_w,
            y + bar_h
        ),
        fill=(220, 220, 220)
    )

    fill_w = int(
        bar_w *
        (overall_score / 100)
    )

    draw.rectangle(
        (
            40,
            y,
            40 + fill_w,
            y + bar_h
        ),
        fill=(31, 107, 87)
    )

    draw.text(
        (
            40 + bar_w + 20,
            y + 5
        ),
        f"{overall_score:.2f}%",
        fill="black",
        font=body_font
    )

    filename = (

        REPORT_DIR /

        f"validation_dashboard_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )

    img.save(filename)

    print(
        f"\nDashboard saved:\n{filename}"
    )

# ============================================================
# MAIN
# ============================================================

def main():

    results = []

    for part in PARTS:

        results.append(
            analyze_part(part)
        )

    create_dashboard(results)


if __name__ == "__main__":

    main()