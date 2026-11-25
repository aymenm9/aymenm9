"""Generates assets/header-dark.svg and assets/header-light.svg.

Run: python3 assets/make_header.py
"""
import json
from pathlib import Path

# Montserrat subsets (900 for the name, 400 for the tagline), embedded so the
# header looks the same without the font installed.
FONTS = json.loads((Path(__file__).parent / "montserrat_subset.json").read_text())
FONT_CSS = "".join(
    f"@font-face {{ font-family: 'MontserratEmbed'; font-weight: {w}; src: url(data:font/{fmt};base64,{data}) format('{fmt}'); }}"
    for w, (fmt, data) in FONTS.items()
)

THEMES = {
    "dark": dict(bg="#0d0d0d", fg="#ffffff", muted="#8a8a8a", rule="#2a2a2a", accent="#e01b1b"),
    "light": dict(bg="#f6f5f2", fg="#0d0d0d", muted="#6b6b6b", rule="#d9d7d2", accent="#ac0000"),
}

W, H = 1000, 340
SANS = "MontserratEmbed, Montserrat, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def build(t: dict) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Aymen Merad</title>
  <desc id="desc">AI Engineer and Backend Developer. Sétif, Algeria. Open to work, remote.</desc>
  <style>
    {FONT_CSS}
    .sans {{ font-family: {SANS}; }}
    .mono {{ font-family: {MONO}; letter-spacing: 1.5px; }}
  </style>
  <rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>

  <!-- top bar -->
  <text x="48" y="54" class="mono" font-size="13" fill="{t["muted"]}">A.MERAD — FOLIO/2026</text>
  <text x="{W - 48}" y="54" text-anchor="end" class="mono" font-size="13" fill="{t["muted"]}">SÉTIF, DZ · 36.19°N 5.41°E</text>
  <line x1="48" y1="72" x2="{W - 48}" y2="72" stroke="{t["rule"]}"/>

  <!-- name -->
  <text x="42" y="168" class="sans" font-size="92" font-weight="900" letter-spacing="-3" fill="{t["fg"]}">AYMEN</text>
  <text x="42" y="258" class="sans" font-size="92" font-weight="900" letter-spacing="-3" fill="{t["bg"]}" stroke="{t["fg"]}" stroke-width="3.2" paint-order="stroke" stroke-linejoin="round">MERAD<tspan fill="{t["accent"]}" stroke="none">.</tspan></text>

  <!-- right column -->
  <g class="mono" font-size="14" fill="{t["fg"]}">
    <text x="610" y="124">AI ENGINEER</text>
    <text x="610" y="152">BACKEND DEVELOPER</text>
    <text x="610" y="180">AGENTIC SYSTEMS BUILDER</text>
  </g>
  <line x1="610" y1="204" x2="{W - 48}" y2="204" stroke="{t["rule"]}"/>
  <circle cx="616" cy="232" r="5" fill="{t["accent"]}">
    <animate attributeName="opacity" values="1;0.25;1" dur="1.8s" repeatCount="indefinite"/>
  </circle>
  <text x="632" y="237" class="mono" font-size="14" fill="{t["fg"]}">OPEN TO WORK · SÉTIF → REMOTE</text>

  <!-- tagline -->
  <line x1="48" y1="290" x2="{W - 48}" y2="290" stroke="{t["rule"]}"/>
  <text x="48" y="318" class="sans" font-size="17" fill="{t["muted"]}">I make backends behave <tspan fill="{t["accent"]}">&amp;</tspan> frontends feel.</text>
  <text x="{W - 48}" y="318" text-anchor="end" class="mono" font-size="12" fill="{t["muted"]}">AI ENGINEERING / AGENTS / BACKEND</text>
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).parent
    for name, theme in THEMES.items():
        (out / f"header-{name}.svg").write_text(build(theme), encoding="utf-8")
        print("wrote", out / f"header-{name}.svg")
