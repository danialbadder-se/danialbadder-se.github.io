"""Render portfolio artwork from the public case-study data and worksheet excerpt."""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DIST = Path(__file__).resolve().parents[1]
ASSETS = DIST / "assets"


def font(size, weight="regular"):
    name = "serif-italic.ttf" if weight == "italic" else f"sans-{weight}.woff2"
    return ImageFont.truetype(str(ASSETS / name), size)


def research_chart():
    rows = json.loads((DIST / "data/caml.json").read_text())["missing"]
    canvas = Image.new("RGB", (1080, 374), "#ffffff")
    draw = ImageDraw.Draw(canvas)
    draw.text((38, 18), "Micro F1 as reports are removed", font=font(41, "semibold"), fill="#14294b")
    left, right, top, bottom = 90, 1006, 109, 280

    def y(score):
        return bottom - (score - 0.4) / 0.5 * (bottom - top)

    for tick in (0.4, 0.65, 0.9):
        py = y(tick)
        draw.line((left, py, right, py), fill="#dee5f1", width=2)
        draw.text((left - 12, py), f"{tick:.2f}", font=font(24), fill="#475e7d", anchor="rm")
    points = [(left + row["missing"] / 80 * (right - left), y(row["micro_f1"])) for row in rows]
    draw.polygon([(left, bottom), *points, (right, bottom)], fill="#e7effe")
    draw.line(points, fill="#315fd1", width=7, joint="curve")
    for row, (px, py) in zip(rows, points):
        draw.ellipse((px - 8, py - 8, px + 8, py + 8), fill="white", outline="#315fd1", width=5)
        draw.text((px, bottom + 12), f'{row["missing"]}%', font=font(26), anchor="mt", fill="#354d70")
    # Endpoint labels sit inside the plot edges and clear the data line.
    for row, (px, py), anchor in [(rows[0], points[0], "lb"), (rows[-1], points[-1], "rb")]:
        draw.text((px, py - 13), f'{row["micro_f1"]:.3f}', font=font(28, "semibold"), anchor=anchor, fill="#204cae")
    draw.text(((left + right) // 2, 328), "Share of reports removed", font=font(26), anchor="mt", fill="#425a7a")
    canvas.save(ASSETS / "caml-report-removal.webp", lossless=True, method=6)


def social_preview():
    canvas = Image.new("RGB", (1200, 630), "#101f3a")
    draw = ImageDraw.Draw(canvas)
    for radius in (250, 335, 420, 505, 590, 675):
        draw.ellipse((1150 - radius, -80 - radius, 1150 + radius, -80 + radius), outline="#243958", width=2)
    draw.line((60, 119, 101, 119), fill="#81aaff", width=3)
    draw.text((115, 119), "SOFTWARE ENGINEER", font=font(22, "semibold"), fill="#b6d0ff", anchor="lm")
    draw.text((54, 166), "Muhammad", font=font(91, "semibold"), fill="#f6f8ff")
    draw.text((53, 260), "Danial.", font=font(119, "italic"), fill="#aac9ff")
    draw.text((60, 423), "Websites, Excel reporting", font=font(32), fill="#e1eaf9")
    draw.text((60, 469), "and applied AI research", font=font(32), fill="#e1eaf9")
    draw.rounded_rectangle((594, 111, 1143, 508), radius=15, fill="#f7faff", outline="#b8cce9", width=2)
    draw.text((622, 141), "NTDC EXCEL WORKBOOK", font=font(22, "semibold"), fill="#325590")
    draw.text((622, 184), "Transformer worksheet", font=font(39, "semibold"), fill="#162a49")
    with Image.open(ASSETS / "ntdc-formula-detail.webp") as source:
        excerpt = source.convert("RGB")
        excerpt.thumbnail((492, 204), Image.Resampling.LANCZOS)
        canvas.paste(excerpt, (622, 256))
    draw.text((62, 563), "Multan, Pakistan", font=font(22), fill="#b4c6e1")
    canvas.save(ASSETS / "portfolio-preview.jpg", quality=91, optimize=True)


if __name__ == "__main__":
    research_chart()
    social_preview()
