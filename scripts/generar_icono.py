"""Genera el icono oficial de escritorio (`geologgia_licitaciones.ico`) en resoluciones
múltiples (256x256, 128x128, 64x64, 48x48, 32x32, 16x16) para la Fábrica de Licitaciones IA.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for name in ["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf"]:
        p = Path(r"C:\Windows\Fonts") / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def crear_icono() -> Path:
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fondo circular/redondeado azul marino oscuro con borde naranja y cian
    draw.rounded_rectangle([8, 8, 248, 248], radius=54, fill=(11, 22, 48, 255), outline=(249, 115, 22, 255), width=8)
    draw.rounded_rectangle([20, 20, 236, 236], radius=44, fill=(13, 37, 96, 255), outline=(56, 189, 248, 180), width=3)

    # Dibujar arco de túnel / estratos geológicos estilizados en la parte superior
    draw.arc([52, 42, 204, 194], start=180, end=360, fill=(56, 189, 248, 255), width=7)
    draw.arc([68, 58, 188, 178], start=180, end=360, fill=(249, 115, 22, 255), width=6)

    # Monograma "GL" + badge "IA"
    f_big = load_font(92)
    f_sub = load_font(30)
    draw.text((62, 74), "GL", fill=(248, 250, 252, 255), font=f_big)

    # Cinta inferior naranja "LICITACIONES"
    draw.rounded_rectangle([34, 184, 222, 224], radius=12, fill=(234, 88, 12, 255))
    draw.text((54, 187), "LICITACIONES", fill=(255, 255, 255, 255), font=f_sub)

    ico_path = ROOT / "geologgia_licitaciones.ico"
    img.save(
        ico_path,
        format="ICO",
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)],
    )
    print(f"[OK] Icono generado en: {ico_path}")
    return ico_path


if __name__ == "__main__":
    crear_icono()
