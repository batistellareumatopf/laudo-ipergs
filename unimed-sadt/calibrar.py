"""
Ferramenta de calibração - gera PDF em modo paisagem (horizontal) real,
com grade de coordenadas para identificar a posição dos campos.
"""
import subprocess
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, blue
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject
import io

PDF_ORIGINAL = "/Users/clinicabeneser/Downloads/EXAMES UNIMED.pdf"
PDF_SAIDA   = "/Users/clinicabeneser/Downloads/CALIBRACAO.pdf"

# Dimensões originais (retrato escaneado)
ORIG_W = 2058.0
ORIG_H = 2924.0

# Dimensões após rotação física 90° CCW → paisagem real
LAND_W = ORIG_H   # 2924  (eixo X: esquerda→direita)
LAND_H = ORIG_W   # 2058  (eixo Y: baixo→cima)


def rotacionar_pagina_fisicamente(page):
    """Rota o conteúdo da página 90° CCW e atualiza o MediaBox para paisagem."""
    # Matriz de rotação 90° CCW + translação para manter coords positivas:
    #   x' = -y + ORIG_H  →  a=0, c=-1, e=ORIG_H
    #   y' =  x            →  b=1,  d=0, f=0
    t = Transformation((0, 1, -1, 0, ORIG_H, 0))
    page.add_transformation(t)
    page.mediabox = RectangleObject([0, 0, LAND_W, LAND_H])
    return page


def gerar_calibracao():
    # ── 1. Lê e rotaciona fisicamente o formulário ──────────────────────────
    reader = PdfReader(PDF_ORIGINAL)
    page   = reader.pages[0]
    rotacionar_pagina_fisicamente(page)

    # ── 2. Cria overlay com grade + marcadores em coordenadas paisagem ──────
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(LAND_W, LAND_H))

    # Grade a cada 200 unidades
    c.setFont("Helvetica", 16)
    c.setFillColor(red)
    c.setStrokeColor(red)
    c.setLineWidth(0.8)

    # Linhas a cada 100 unidades (traço fino) e a cada 500 (traço mais visível)
    for x in range(0, int(LAND_W) + 1, 100):
        bold = (x % 500 == 0)
        c.setLineWidth(1.5 if bold else 0.4)
        c.setDash(1, 0) if bold else c.setDash(3, 3)
        c.line(x, 0, x, LAND_H)
        if bold and x > 0:
            c.setFont("Helvetica-Bold", 18)
            c.drawString(x + 3, LAND_H - 28, str(x))
        elif x % 200 == 0 and x > 0:
            c.setFont("Helvetica", 13)
            c.drawString(x + 2, LAND_H - 22, str(x))

    for y in range(0, int(LAND_H) + 1, 100):
        bold = (y % 500 == 0)
        c.setLineWidth(1.5 if bold else 0.4)
        c.setDash(1, 0) if bold else c.setDash(3, 3)
        c.line(0, y, LAND_W, y)
        if bold and y > 0:
            c.setFont("Helvetica-Bold", 18)
            c.drawString(4, y + 3, str(y))
        elif y % 200 == 0 and y > 0:
            c.setFont("Helvetica", 13)
            c.drawString(4, y + 2, str(y))

    # Verifica posições informadas pelo usuário
    campos = [
        ("NOME",         1200, 1800, 1400, 55),
        ("IND.CLINICA",   800, 1400, 1400, 55),
        ("DESCRICAO",     600, 1400, 1400, 55),
    ]
    c.setFont("Helvetica-Bold", 26)
    c.setStrokeColor(blue)
    c.setDash(1, 0)
    for label, x, y, w, h in campos:
        c.setFillColor(blue)
        c.rect(x, y, w, h, stroke=1, fill=0)
        c.drawString(x + 5, y + 12, label)

    c.save()

    # ── 3. Mescla overlay na página já rotacionada ──────────────────────────
    buf.seek(0)
    overlay_reader = PdfReader(buf)
    page.merge_page(overlay_reader.pages[0])

    writer = PdfWriter()
    writer.add_page(page)

    with open(PDF_SAIDA, "wb") as f:
        writer.write(f)

    print(f"Calibração gerada: {PDF_SAIDA}")
    subprocess.Popen(["open", PDF_SAIDA])


if __name__ == "__main__":
    gerar_calibracao()
