"""Renderiza la infografía de alta resolución (`infografia_equipo_licitaciones.png`)
con la estética oscura de IDE (árbol de 8 carpetas a la izquierda + 8 tarjetas con las 50 habilidades a la derecha)
para el Equipo de Licitaciones IA de Geologgia Ltda.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(r"C:\Users\geolo\.gemini\antigravity\brain\62ed66f6-4ba4-4c5f-b03f-e01bcc1f2f58\scratch")))
from generar_habilidades import FASES, H  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = Path(r"C:\Users\geolo\.gemini\antigravity\brain\62ed66f6-4ba4-4c5f-b03f-e01bcc1f2f58")

COLORES = {
    1: (56, 189, 248),    # Cyan
    2: (251, 146, 60),    # Orange
    3: (168, 85, 247),    # Purple
    4: (244, 63, 94),     # Rose
    5: (250, 204, 21),    # Yellow
    6: (45, 212, 191),    # Teal
    7: (232, 121, 249),   # Pink
    8: (52, 211, 153),    # Emerald
}


def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    win_fonts = Path(r"C:\Windows\Fonts")
    candidates = (
        ["consolab.ttf", "consola.ttf"]
        if mono
        else (["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"] if bold else ["segoeui.ttf", "arial.ttf", "calibri.ttf"])
    )
    for name in candidates:
        p = win_fonts / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def generar_infografia() -> Path:
    W, H_IMG = 1600, 1920
    img = Image.new("RGB", (W, H_IMG), (7, 11, 20))
    draw = ImageDraw.Draw(img)

    f_hero_brand = load_font(54, bold=True)
    f_hero_title = load_font(50, bold=True)
    f_sub = load_font(21, bold=False)
    f_card_title = load_font(22, bold=True)
    f_badge = load_font(15, bold=True)
    f_skill = load_font(17, bold=False)
    f_num = load_font(15, bold=True, mono=True)
    f_tree_folder = load_font(15, bold=True, mono=True)
    f_tree_file = load_font(13, bold=False, mono=True)
    f_top = load_font(15, bold=True)
    f_banner = load_font(24, bold=True)

    # 1. Barra superior estilo IDE
    draw.rectangle([0, 0, W, 46], fill=(4, 7, 15))
    for i, c in enumerate([(239, 68, 68), (245, 158, 11), (16, 185, 129)]):
        draw.ellipse([20 + i * 22, 16, 34 + i * 22, 30], fill=c)
    draw.rounded_rectangle([460, 8, 1140, 38], radius=6, fill=(15, 23, 42), outline=(51, 65, 85))
    draw.text((490, 13), "geologgia-equipo-licitaciones · 50 Habilidades IA", fill=(203, 213, 225), font=f_top)
    draw.text((1200, 13), "REVISOR FINAL & APROBADOR: CARLOS ÁVILA", fill=(52, 211, 153), font=f_top)

    # 2. Barra de pestañas
    draw.rectangle([0, 46, W, 86], fill=(9, 14, 26))
    draw.rectangle([290, 46, 610, 86], fill=(7, 11, 20))
    draw.rectangle([290, 46, 610, 49], fill=(249, 115, 22))
    draw.text((22, 57), "README.md", fill=(148, 163, 184), font=f_top)
    draw.text((310, 57), "50-habilidades-licitaciones.md  ×", fill=(248, 250, 252), font=f_top)

    # 3. Columna izquierda (Explorador de archivos)
    SIDEBAR_W = 290
    draw.rectangle([0, 86, SIDEBAR_W, H_IMG - 90], fill=(5, 9, 18))
    draw.line([(SIDEBAR_W, 86), (SIDEBAR_W, H_IMG - 90)], fill=(30, 41, 59), width=2)
    draw.text((16, 100), "EXPLORADOR · 50 SKILLS", fill=(100, 116, 139), font=f_badge)

    y_tree = 132
    for f_id, (carpeta, _) in FASES.items():
        col = COLORES[f_id]
        habs_f = [x for x in H if x["f"] == f_id]
        draw.text((14, y_tree), f"▸ {carpeta}/", fill=col, font=f_tree_folder)
        draw.text((SIDEBAR_W - 28, y_tree), str(len(habs_f)), fill=(148, 163, 184), font=f_tree_folder)
        y_tree += 22
        for h in habs_f:
            if y_tree < H_IMG - 115:
                draw.text((28, y_tree), f"habilidad-{h['n']:02d}.md", fill=(148, 163, 184), font=f_tree_file)
                y_tree += 17
        y_tree += 8

    # 4. Encabezado principal
    X0 = SIDEBAR_W + 36
    draw.text((X0, 104), "Geologgia IA", fill=(249, 115, 22), font=f_hero_brand)
    draw.text((X0, 166), "Equipo de Licitaciones", fill=(248, 250, 252), font=f_hero_title)
    draw.text(
        (X0, 232),
        "50 habilidades preconfiguradas: desde el correo de invitación hasta el Revisor Final y Aprobador de envío.",
        fill=(203, 213, 225),
        font=f_sub,
    )
    draw.text(
        (X0, 262),
        "Especializado en Geología · Geotecnia · Túneles · Minería · Construcción · Energía (con scripts Gmail + Excel + Word)",
        fill=(56, 189, 248),
        font=f_badge,
    )

    # 5. Grid 2x4 de las 8 fases y 50 habilidades
    GRID_TOP = 305
    COL_W = 605
    GAP_X = 24
    ROW_HEIGHTS = [310, 385, 315, 290]  # Filas adaptadas a la cantidad de habilidades por fase
    y_cursor = GRID_TOP

    for row_idx in range(4):
        rh = ROW_HEIGHTS[row_idx]
        for col_idx in range(2):
            f_id = row_idx * 2 + col_idx + 1
            col = COLORES[f_id]
            _, titulo_fase = FASES[f_id]
            habs_f = [x for x in H if x["f"] == f_id]
            rango_txt = f"Habilidades {habs_f[0]['n']}–{habs_f[-1]['n']}"

            cx = X0 + col_idx * (COL_W + GAP_X)
            cy = y_cursor

            # Fondo de tarjeta
            draw.rounded_rectangle([cx, cy, cx + COL_W, cy + rh], radius=12, fill=(13, 20, 36), outline=(30, 41, 59), width=2)
            # Borde superior de color
            draw.rounded_rectangle([cx, cy, cx + COL_W, cy + 6], radius=3, fill=col)

            # Título de fase y badge
            draw.text((cx + 18, cy + 16), titulo_fase, fill=col, font=f_card_title)
            draw.rounded_rectangle([cx + COL_W - 165, cy + 16, cx + COL_W - 14, cy + 42], radius=12, fill=(15, 23, 42), outline=col, width=1)
            draw.text((cx + COL_W - 153, cy + 20), rango_txt, fill=col, font=f_badge)
            draw.line([(cx + 16, cy + 52), (cx + COL_W - 16, cy + 52)], fill=(30, 41, 59), width=1)

            # Filas de habilidades
            sy = cy + 62
            for h in habs_f:
                # Cajita con número
                draw.rounded_rectangle([cx + 18, sy + 2, cx + 52, sy + 24], radius=5, fill=(15, 23, 42), outline=col, width=1)
                draw.text((cx + 25, sy + 4), f"{h['n']:02d}", fill=col, font=f_num)

                nombre_mostrar = h["nombre"]
                es_hitl = h["n"] in {6, 16, 34, 47, 48}
                color_txt = (254, 226, 226) if es_hitl else (226, 232, 240)
                sufijo = "  [CONTROL CARLOS]" if es_hitl else ""
                draw.text((cx + 64, sy + 2), nombre_mostrar + sufijo, fill=color_txt, font=f_skill)
                sy += 27

        y_cursor += rh + 18

    # 6. Franja inferior naranja estilo poster
    draw.rectangle([0, H_IMG - 84, W, H_IMG], fill=(234, 88, 12))
    draw.text(
        (45, H_IMG - 57),
        "GEOLOGGIA LTDA. · EQUIPO DE LICITACIONES IA · DE LA INVITACIÓN AL ENVÍO APROBADO",
        fill=(255, 255, 255),
        font=f_banner,
    )

    out_png = ROOT / "infografia_equipo_licitaciones.png"
    img.save(out_png, "PNG")
    # Copiar también al directorio de artifacts para mostrarlo en el chat
    art_png = ARTIFACT_DIR / "infografia_equipo_licitaciones.png"
    img.save(art_png, "PNG")
    print(f"[OK] Infografía PNG generada en: {out_png}")
    return out_png


if __name__ == "__main__":
    generar_infografia()
