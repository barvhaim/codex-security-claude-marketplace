#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "plugins" / "codex-security-skills" / "assets" / "logo.png"
OUTPUT = ROOT / "docs" / "social-preview.png"
WIDTH, HEIGHT = 1280, 640


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidates = [
        Path("/usr/share/fonts/truetype/dejavu") / name,
        Path("/usr/share/fonts/dejavu") / name,
        Path("/usr/share/fonts/urw-base35")
        / ("NimbusSans-Bold.otf" if bold else "NimbusSans-Regular.otf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", (WIDTH, HEIGHT), "#07111f")
    pixels = image.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            glow = max(0.0, 1.0 - (((x - 250) / 720) ** 2 + ((y - 300) / 500) ** 2))
            edge = max(0.0, 1.0 - (((x - 1120) / 680) ** 2 + ((y - 60) / 420) ** 2))
            pixels[x, y] = (
                int(7 + 4 * glow),
                int(17 + 24 * glow + 7 * edge),
                int(31 + 42 * glow + 22 * edge),
            )

    glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.ellipse((15, 70, 500, 555), fill=(50, 142, 255, 95))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(80))
    image = Image.alpha_composite(image.convert("RGBA"), glow_layer)

    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((54, 52, 1226, 588), radius=34, fill=(8, 19, 36, 228), outline=(75, 147, 255, 95), width=2)

    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((335, 335), Image.Resampling.LANCZOS)
    logo_shadow = Image.new("RGBA", (410, 410), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(logo_shadow)
    shadow_draw.ellipse((45, 45, 365, 365), fill=(33, 126, 255, 90))
    logo_shadow = logo_shadow.filter(ImageFilter.GaussianBlur(45))
    image.alpha_composite(logo_shadow, (40, 112))
    image.alpha_composite(logo, (82, 150))

    pill = (486, 106, 738, 151)
    draw.rounded_rectangle(pill, radius=22, fill=(32, 98, 190, 110), outline=(90, 164, 255, 175), width=1)
    draw.text((510, 117), "CLAUDE CODE PLUGIN", font=font(20, True), fill="#bcd8ff")

    draw.text((480, 190), "Codex Security Skills", font=font(58, True), fill="#f7fbff")
    draw.text((480, 260), "for Claude Code", font=font(58, True), fill="#70a9ff")
    draw.text((484, 354), "13 security workflows. One install.", font=font(30), fill="#d0dded")
    draw.text((484, 404), "Threat modeling  |  review  |  validation  |  SARIF", font=font(24), fill="#8fa7c1")

    draw.line((484, 481, 1168, 481), fill=(83, 112, 150, 120), width=2)
    draw.text((484, 507), "Unofficial Apache-2.0 adaptation of OpenAI Codex Security", font=font(19), fill="#8398b1")

    image.convert("RGB").save(OUTPUT, quality=95, optimize=True)
    print(f"wrote {OUTPUT} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
