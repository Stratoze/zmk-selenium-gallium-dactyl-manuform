"""
Generate visual layer maps for Gallium Dactyl (40-key, 4x10 matrix).
Run: python generate_layers.py
Output: layers/*.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

os.makedirs("layers", exist_ok=True)

# ─── Layout geometry ───────────────────────────────────────────────
# 4 rows x 10 cols, bottom row only has 6 active keys (cols 2-7)
ROWS = 4
COLS = 10
KEY_W = 1.0
KEY_H = 1.0
GAP = 0.15       # gap between keys
HALF_GAP = 0.6   # extra gap between left/right halves

# Colors
C_ALPHA   = "#E8E8E8"
C_MOD     = "#B3D9FF"  # HRM / modifier
C_LAYER   = "#C8F7C5"  # layer-tap / momentary
C_SYM     = "#FFE4B5"  # symbols
C_NAV     = "#E6CCFF"  # nav / arrows
C_MEDIA   = "#FFD1DC"  # media / F-keys
C_NUM     = "#FFFACD"  # numbers
C_DEAD    = "#555555"  # &none
C_THUMB   = "#D4EDDA"  # thumb keys
C_SPECIAL = "#F0E68C"

def key_pos(row, col):
    """Return (x, y) for a key at (row, col)."""
    x = col * (KEY_W + GAP)
    if col >= 5:
        x += HALF_GAP
    y = (ROWS - 1 - row) * (KEY_H + GAP)
    return x, y

def draw_layer(ax, layer_data, title, subtitle=""):
    """Draw one layer onto the given axes."""
    ax.set_xlim(-0.5, COLS * (KEY_W + GAP) + HALF_GAP - GAP + 0.5)
    ax.set_ylim(-0.8, ROWS * (KEY_H + GAP) + 0.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    if subtitle:
        ax.text(
            (COLS * (KEY_W + GAP) + HALF_GAP - GAP) / 2,
            ROWS * (KEY_H + GAP) + 0.35,
            subtitle, ha="center", fontsize=9, color="#666"
        )

    for row in range(ROWS):
        for col in range(COLS):
            # Bottom row: only cols 2..7 are active
            if row == 3 and (col < 2 or col > 7):
                x, y = key_pos(row, col)
                rect = FancyBboxPatch(
                    (x, y), KEY_W, KEY_H,
                    boxstyle="round,pad=0.05",
                    facecolor=C_DEAD, edgecolor="#333", linewidth=0.5, alpha=0.3
                )
                ax.add_patch(rect)
                continue

            label, color = layer_data[row][col]
            x, y = key_pos(row, col)
            rect = FancyBboxPatch(
                (x, y), KEY_W, KEY_H,
                boxstyle="round,pad=0.05",
                facecolor=color, edgecolor="#333", linewidth=0.8
            )
            ax.add_patch(rect)

            # Multi-line label
            lines = label.split("\n")
            fontsize = 7 if len(lines) > 1 else 8
            ax.text(
                x + KEY_W / 2, y + KEY_H / 2, label,
                ha="center", va="center", fontsize=fontsize,
                fontweight="bold" if len(lines) == 1 else "normal"
            )


# ─── Layer definitions ─────────────────────────────────────────────
# Each layer is a 4x10 grid of (label, color) tuples.
# Row 3 (thumbs): cols 2,3,4 = left thumbs (outer→inner), cols 5,6,7 = right thumbs (inner→outer)

def mk(label, color):
    return (label, color)

BASE = [
    [mk("B",C_ALPHA), mk("L",C_ALPHA), mk("D",C_ALPHA), mk("C",C_ALPHA), mk("V",C_ALPHA),
     mk("J",C_ALPHA), mk("Y",C_ALPHA), mk("O",C_ALPHA), mk("U",C_ALPHA), mk(",",C_ALPHA)],
    [mk("N\n⌘",C_MOD), mk("R\n⌥",C_MOD), mk("T\n⇧",C_MOD), mk("S\n⌃",C_MOD), mk("G",C_ALPHA),
     mk("P",C_ALPHA), mk("H\n⌃",C_MOD), mk("A\n⇧",C_MOD), mk("E\n⌥",C_MOD), mk("I\n⌘",C_MOD)],
    [mk("X",C_ALPHA), mk("Q",C_ALPHA), mk("M",C_ALPHA), mk("W",C_ALPHA), mk("Z",C_ALPHA),
     mk("K",C_ALPHA), mk("F",C_ALPHA), mk("'",C_ALPHA), mk(";",C_ALPHA), mk(".",C_ALPHA)],
    [mk("",C_DEAD), mk("",C_DEAD),
     mk("⇧\nsticky",C_LAYER), mk("⌫\nVimNav",C_LAYER), mk("Esc\nNumRow",C_LAYER),
     mk("↵\nNumRow",C_LAYER), mk("␣\nVimNav",C_LAYER), mk("Sym\n⇧AltGr",C_LAYER),
     mk("",C_DEAD), mk("",C_DEAD)],
]

VIMNAV = [
    [mk("⌃W\nclose",C_NAV), mk("←\ntab",C_NAV), mk("→\ntab",C_NAV), mk("",C_DEAD), mk("",C_DEAD),
     mk("Home",C_NAV), mk("PgDn",C_NAV), mk("PgUp",C_NAV), mk("End",C_NAV), mk("Del",C_NAV)],
    [mk("⌘A\nsel all",C_NAV), mk("⌘S\nsave",C_NAV), mk("⇧Tab",C_NAV), mk("Tab",C_NAV), mk("",C_DEAD),
     mk("←",C_NAV), mk("↓",C_NAV), mk("↑",C_NAV), mk("→",C_NAV), mk("",C_DEAD)],
    [mk("⌘Z\nundo",C_NAV), mk("⌘X\ncut",C_NAV), mk("⌘C\ncopy",C_NAV), mk("⌘V\npaste",C_NAV), mk("⌘Y\nredo",C_NAV),
     mk("🖱←",C_NAV), mk("🖱↓",C_NAV), mk("🖱↑",C_NAV), mk("🖱→",C_NAV), mk("",C_DEAD)],
    [mk("",C_DEAD), mk("",C_DEAD),
     mk("Caps",C_LAYER), mk("Del\nFnMed",C_LAYER), mk("NumRow",C_LAYER),
     mk("⌥\nostick",C_LAYER), mk("FnMed",C_LAYER), mk("",C_DEAD),
     mk("",C_DEAD), mk("",C_DEAD)],
]

NUMROW = [
    [mk("!⇧1",C_NUM), mk("@⇧2",C_NUM), mk("#⇧3",C_NUM), mk("$⇧4",C_NUM), mk("%⇧5",C_NUM),
     mk("^⇧6",C_NUM), mk("&⇧7",C_NUM), mk("*⇧8",C_NUM), mk("(⇧9",C_NUM), mk(")⇧0",C_NUM)],
    [mk("1",C_NUM), mk("2",C_NUM), mk("3",C_NUM), mk("4",C_NUM), mk("5",C_NUM),
     mk("6",C_NUM), mk("7",C_NUM), mk("8",C_NUM), mk("9",C_NUM), mk("0",C_NUM)],
    [mk("",C_DEAD), mk("",C_DEAD), mk("",C_DEAD), mk("",C_DEAD), mk("",C_DEAD),
     mk("-",C_SYM), mk(",",C_SYM), mk(".",C_SYM), mk(":",C_SYM), mk("/",C_SYM)],
    [mk("",C_DEAD), mk("",C_DEAD),
     mk("␣⇧",C_NUM), mk("␣⇧",C_NUM), mk("␣⇧",C_NUM),
     mk("␣⇧",C_NUM), mk("␣⇧",C_NUM), mk("⌥",C_MOD),
     mk("",C_DEAD), mk("",C_DEAD)],
]

SYMBOLS = [
    [mk("^",C_SYM), mk("<",C_SYM), mk(">",C_SYM), mk("$",C_SYM), mk("%",C_SYM),
     mk("@",C_SYM), mk("&",C_SYM), mk("*",C_SYM), mk("'",C_SYM), mk("`",C_SYM)],
    [mk("{",C_SYM), mk("(",C_SYM), mk(")",C_SYM), mk("}",C_SYM), mk("=",C_SYM),
     mk("\\",C_SYM), mk("+",C_SYM), mk("-",C_SYM), mk("/",C_SYM), mk('"',C_SYM)],
    [mk("~",C_SYM), mk("[",C_SYM), mk("]",C_SYM), mk("_",C_SYM), mk("#",C_SYM),
     mk("|",C_SYM), mk("!",C_SYM), mk(";",C_SYM), mk(":",C_SYM), mk("?",C_SYM)],
    [mk("",C_DEAD), mk("",C_DEAD),
     mk("NumRow",C_LAYER), mk("␣",C_LAYER), mk("↵",C_LAYER),
     mk("␣",C_LAYER), mk("␣",C_LAYER), mk("␣",C_LAYER),
     mk("",C_DEAD), mk("",C_DEAD)],
]

FNMEDIA = [
    [mk("F1",C_MEDIA), mk("F2",C_MEDIA), mk("F3",C_MEDIA), mk("F4",C_MEDIA), mk("",C_DEAD),
     mk("BT3",C_MEDIA), mk("⏭",C_MEDIA), mk("🔊+",C_MEDIA), mk("☀+",C_MEDIA), mk("ScrLk",C_MEDIA)],
    [mk("F5",C_MEDIA), mk("F6",C_MEDIA), mk("F7",C_MEDIA), mk("F8",C_MEDIA), mk("",C_DEAD),
     mk("BT1\nclr",C_MEDIA), mk("⏯",C_MEDIA), mk("🔇",C_MEDIA), mk("🔒",C_MEDIA), mk("PrtSc",C_MEDIA)],
    [mk("F9",C_MEDIA), mk("F10",C_MEDIA), mk("F11",C_MEDIA), mk("F12",C_MEDIA), mk("",C_DEAD),
     mk("BT0",C_MEDIA), mk("⏮",C_MEDIA), mk("🔊-",C_MEDIA), mk("☀-",C_MEDIA), mk("Ins",C_MEDIA)],
    [mk("",C_DEAD), mk("",C_DEAD),
     mk("␣",C_LAYER), mk("Boot",C_SPECIAL), mk("␣",C_LAYER),
     mk("␣",C_LAYER), mk("Reset",C_SPECIAL), mk("Studio\nUnlock",C_SPECIAL),
     mk("",C_DEAD), mk("",C_DEAD)],
]

NAVNUM = [
    [mk("Esc",C_NAV), mk("Home",C_NAV), mk("↑",C_NAV), mk("End",C_NAV), mk("PgUp",C_NAV),
     mk("NumLk",C_NUM), mk("7",C_NUM), mk("8",C_NUM), mk("9",C_NUM), mk("/",C_NUM)],
    [mk("⌘A",C_NAV), mk("←",C_NAV), mk("↓",C_NAV), mk("→",C_NAV), mk("PgDn",C_NAV),
     mk("-",C_NUM), mk("4",C_NUM), mk("5",C_NUM), mk("6",C_NUM), mk("0",C_NUM)],
    [mk("⌘Z",C_NAV), mk("⌘X",C_NAV), mk("⌘C",C_NAV), mk("⌘V",C_NAV), mk("⌘Y",C_NAV),
     mk(",",C_NUM), mk("1",C_NUM), mk("2",C_NUM), mk("3",C_NUM), mk(".",C_NUM)],
    [mk("",C_DEAD), mk("",C_DEAD),
     mk("Caps",C_LAYER), mk("Del\nFnMed",C_LAYER), mk("⇧Tab",C_LAYER),
     mk("Esc",C_LAYER), mk("FnMed",C_LAYER), mk("⌥",C_LAYER),
     mk("",C_DEAD), mk("",C_DEAD)],
]

# ─── Render ────────────────────────────────────────────────────────
layers = [
    ("base",     "Base (Gallium)",     "GASC HRMs: ⌘GUI ⌥ALT ⇧SHIFT ⌃CTRL",  BASE),
    ("vimnav",   "VimNav",             "Hold left-middle or right-middle thumb", VIMNAV),
    ("numrow",   "NumRow",             "Hold left-inner or right-inner thumb",   NUMROW),
    ("symbols",  "Symbols",            "Tap right-outer thumb (Sym/AltGr)",      SYMBOLS),
    ("fnmedia",  "FnMedia",            "Hold thumb from VimNav or NavNum",       FNMEDIA),
    ("navnum",   "NavNum",             "Non-vim nav + numpad",                   NAVNUM),
]

for filename, title, subtitle, data in layers:
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    draw_layer(ax, data, title, subtitle)
    out = f"layers/{filename}.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {out}")

# ─── Overview (all layers in one image) ────────────────────────────
fig, axes = plt.subplots(3, 2, figsize=(20, 18))
fig.suptitle("Gallium Dactyl — All Layers", fontsize=18, fontweight="bold", y=0.98)
for ax, (filename, title, subtitle, data) in zip(axes.flat, layers):
    draw_layer(ax, data, title, subtitle)
fig.savefig("layers/overview.png", dpi=120, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("  ✓ layers/overview.png")

print("\nDone! Open layers/overview.png for the full reference.")
