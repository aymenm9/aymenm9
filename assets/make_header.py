"""Generates assets/header-dark.svg and assets/header-light.svg.

Run: python3 assets/make_header.py
"""
from pathlib import Path

THEMES = {
    "dark": dict(
        name="#e6edf3", muted="#8b949e", accent="#ff4d4d",
        sq_light="#2b313a", sq_dark="#1c2128", edge="#30363d",
        pawn="#f0f3f6", pawn_stroke="#0d1117", hi="#ff4d4d",
    ),
    "light": dict(
        name="#1f2328", muted="#59636e", accent="#b80000",
        sq_light="#efede8", sq_dark="#d9d4c9", edge="#d0d7de",
        pawn="#ffffff", pawn_stroke="#1f2328", hi="#b80000",
    ),
}

W, H = 900, 270
SQ = 24
BX, BY = 650, 26  # board top-left

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def center(file_idx: int, rank: int) -> tuple[int, int]:
    return BX + file_idx * SQ + SQ // 2, BY + (8 - rank) * SQ + SQ // 2


def build(t: dict) -> str:
    squares = []
    for f in range(8):
        for r in range(1, 9):
            fill = t["sq_dark"] if (f + r) % 2 == 0 else t["sq_light"]
            x, y = BX + f * SQ, BY + (8 - r) * SQ
            squares.append(f'<rect x="{x}" y="{y}" width="{SQ}" height="{SQ}" fill="{fill}"/>')

    files = "".join(
        f'<text x="{BX + i * SQ + SQ / 2}" y="{BY + 8 * SQ + 16}" text-anchor="middle">{c}</text>'
        for i, c in enumerate("abcdefgh")
    )
    ranks = "".join(
        f'<text x="{BX - 9}" y="{BY + (8 - r) * SQ + SQ / 2 + 3.5}" text-anchor="middle">{r}</text>'
        for r in range(1, 9)
    )

    (e2x, e2y), (e4x, e4y) = center(4, 2), center(4, 4)
    dy = e4y - e2y

    def hi(cx, cy):
        return (
            f'<rect x="{cx - SQ / 2}" y="{cy - SQ / 2}" width="{SQ}" height="{SQ}" '
            f'fill="{t["hi"]}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="0.32" begin="1.9s" dur="0.35s" fill="freeze"/>'
            f"</rect>"
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Aymen Merad</title>
  <desc id="desc">Backend developer building AI agents, from Sétif, Algeria. A white pawn plays 1. e4 on a chessboard.</desc>
  <style>
    .sans {{ font-family: {SANS}; }}
    .mono {{ font-family: {MONO}; }}
  </style>

  <!-- left: identity -->
  <text x="0" y="62" class="mono" font-size="15" fill="{t["muted"]}">~/sétif, algeria</text>
  <text x="-3" y="128" class="sans" font-size="64" font-weight="800" letter-spacing="-2" fill="{t["name"]}">Aymen Merad</text>
  <text x="0" y="170" class="sans" font-size="22" fill="{t["muted"]}">Backend developer · AI agents · Python</text>
  <text x="0" y="222" class="mono" font-size="18" fill="{t["accent"]}">$ I make servers behave.<tspan fill="{t["accent"]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>▍</tspan></text>

  <!-- right: board -->
  <rect x="{BX - 1}" y="{BY - 1}" width="{8 * SQ + 2}" height="{8 * SQ + 2}" fill="none" stroke="{t["edge"]}" stroke-width="1" rx="2"/>
  {"".join(squares)}
  {hi(e2x, e2y)}
  {hi(e4x, e4y)}
  <g class="mono" font-size="10" fill="{t["muted"]}">{files}{ranks}</g>

  <g transform="translate({e2x} {e2y})">
    <g>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="0 {dy}" begin="1.2s" dur="0.7s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"/>
      <g fill="{t["pawn"]}" stroke="{t["pawn_stroke"]}" stroke-width="1.3" stroke-linejoin="round">
        <circle cx="0" cy="-5.2" r="3.6"/>
        <path d="M-3.2 -1.6 Q0 -3.2 3.2 -1.6 L4.6 5.6 L-4.6 5.6 Z"/>
        <rect x="-6.4" y="5.6" width="12.8" height="3" rx="1.2"/>
      </g>
    </g>
  </g>

  <text x="{BX + 4 * SQ}" y="{BY + 8 * SQ + 40}" text-anchor="middle" class="mono" font-size="13" fill="{t["muted"]}" opacity="0">1. e4 · your move<animate attributeName="opacity" from="0" to="1" begin="2.2s" dur="0.5s" fill="freeze"/></text>
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).parent
    for name, theme in THEMES.items():
        (out / f"header-{name}.svg").write_text(build(theme), encoding="utf-8")
        print("wrote", out / f"header-{name}.svg")
