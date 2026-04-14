"""
Guia SADT Unimed — interface web local
Rode: python3 app.py
Acesse: http://localhost:5050
"""
from flask import Flask, request, send_file, render_template_string
import io
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject
import subprocess, threading, time, webbrowser

app = Flask(__name__)

import os
PDF_ORIGINAL = os.path.join(os.path.dirname(__file__), "formulario_sadt.pdf")

ORIG_W, ORIG_H = 2058.0, 2924.0
LAND_W, LAND_H = ORIG_H, ORIG_W   # 2924 x 2058

CAMPOS = {
    "nome":        {"x": 1217, "y": 1721, "tamanho": 34},
    "ind_clinica": {"x": 1375, "y": 1341, "tamanho": 34},
    "descricao":   {"x":  787, "y": 1274, "tamanho": 34},
}

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Guia SADT — Unimed</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #1e1e2e; color: #cdd6f4; font-family: Helvetica, sans-serif;
         display: flex; justify-content: center; align-items: center; min-height: 100vh; }
  .card { background: #181825; border-radius: 14px; padding: 36px 40px;
          width: 520px; box-shadow: 0 8px 32px #0008; }
  h1 { font-size: 20px; color: #fff; margin-bottom: 28px; }
  label { display: block; font-size: 13px; color: #a6adc8; margin-bottom: 5px; margin-top: 18px; }
  input[type=text] { width: 100%; padding: 10px 12px; border-radius: 7px;
                     background: #313244; border: 1px solid #45475a;
                     color: #cdd6f4; font-size: 15px; outline: none; }
  input[type=text]:focus { border-color: #89b4fa; }
  button { margin-top: 28px; width: 100%; padding: 13px; border-radius: 8px;
           background: #89b4fa; color: #1e1e2e; font-size: 15px; font-weight: bold;
           border: none; cursor: pointer; }
  button:hover { background: #b4d0fe; }
  {% if msg %}
  .msg { margin-top: 16px; padding: 10px; border-radius: 7px;
         background: {% if erro %}#f38ba855{% else %}#a6e3a122{% endif %};
         color: {% if erro %}#f38ba8{% else %}#a6e3a1{% endif %};
         font-size: 13px; text-align: center; }
  {% endif %}
</style>
</head>
<body>
<div class="card">
  <h1>Preencher Guia SADT — Unimed</h1>
  <form method="POST" action="/gerar">
    <label>Nome do Paciente</label>
    <input type="text" name="nome" value="{{ nome }}" autofocus>

    <label>Indicação Clínica</label>
    <input type="text" name="ind_clinica" value="{{ ind_clinica }}">

    <label>Descrição</label>
    <input type="text" name="descricao" value="{{ descricao }}">

    <button type="submit">Gerar PDF ↗</button>
  </form>
  {% if msg %}
  <div class="msg">{{ msg }}</div>
  {% endif %}
</div>
</body>
</html>"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML, nome="", ind_clinica="", descricao="", msg="", erro=False)


@app.route("/gerar", methods=["POST"])
def gerar():
    nome       = request.form.get("nome", "").strip()
    ind        = request.form.get("ind_clinica", "").strip()
    desc       = request.form.get("descricao", "").strip()

    try:
        reader = PdfReader(PDF_ORIGINAL)
        page   = reader.pages[0]
        t = Transformation((0, 1, -1, 0, ORIG_H, 0))
        page.add_transformation(t)
        page.mediabox = RectangleObject([0, 0, LAND_W, LAND_H])

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(LAND_W, LAND_H))
        c.setFillColor(black)
        for chave, texto in [("nome", nome), ("ind_clinica", ind), ("descricao", desc)]:
            if texto:
                cfg = CAMPOS[chave]
                c.setFont("Helvetica", cfg["tamanho"])
                c.drawString(cfg["x"], cfg["y"], texto)
        c.save()

        buf.seek(0)
        overlay = PdfReader(buf)
        page.merge_page(overlay.pages[0])

        writer = PdfWriter()
        writer.add_page(page)

        out = io.BytesIO()
        writer.write(out)
        out.seek(0)
        return send_file(out, mimetype="application/pdf",
                         download_name="GUIA_PREENCHIDA.pdf",
                         as_attachment=False)

    except Exception as e:
        return render_template_string(HTML, nome=nome, ind_clinica=ind,
                                      descricao=desc, msg=str(e), erro=True)


def abrir_browser():
    time.sleep(1.2)
    webbrowser.open("http://localhost:5050")

if __name__ == "__main__":
    threading.Thread(target=abrir_browser, daemon=True).start()
    print("Servidor rodando em http://localhost:5050  (Ctrl+C para parar)")
    app.run(host="127.0.0.1", port=5050, debug=False)
