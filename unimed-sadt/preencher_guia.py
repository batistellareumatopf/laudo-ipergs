"""
Preencher Guia SADT - Unimed
Preenche NOME, INDICAÇÃO CLÍNICA e DESCRIÇÃO e gera PDF pronto para imprimir.
"""
import tkinter as tk
from tkinter import messagebox
import subprocess
import io
import os

from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject

# ── Caminhos ────────────────────────────────────────────────────────────────
PDF_ORIGINAL = "/Users/clinicabeneser/Downloads/EXAMES UNIMED.pdf"
PDF_SAIDA    = "/Users/clinicabeneser/Downloads/GUIA_PREENCHIDA.pdf"

# ── Dimensões originais do scan (retrato) ───────────────────────────────────
ORIG_W = 2058.0
ORIG_H = 2924.0

# ── Dimensões paisagem real (após rotação 90° CCW) ──────────────────────────
LAND_W = ORIG_H   # 2924
LAND_H = ORIG_W   # 2058

# ── Posições dos campos (coordenadas em espaço paisagem) ────────────────────
CAMPOS = {
    "nome":         {"x": 1217, "y": 1721, "tamanho": 34},
    "ind_clinica":  {"x": 1375, "y": 1341, "tamanho": 34},
    "descricao":    {"x":  787, "y": 1274, "tamanho": 34},
}


def gerar_pdf(nome: str, ind_clinica: str, descricao: str) -> str:
    # 1. Rotaciona fisicamente o formulário para paisagem
    reader = PdfReader(PDF_ORIGINAL)
    page   = reader.pages[0]
    t = Transformation((0, 1, -1, 0, ORIG_H, 0))
    page.add_transformation(t)
    page.mediabox = RectangleObject([0, 0, LAND_W, LAND_H])

    # 2. Cria overlay com os textos
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(LAND_W, LAND_H))
    c.setFillColor(black)

    for chave, texto in [("nome", nome), ("ind_clinica", ind_clinica), ("descricao", descricao)]:
        cfg = CAMPOS[chave]
        c.setFont("Helvetica", cfg["tamanho"])
        c.drawString(cfg["x"], cfg["y"], texto)

    c.save()

    # 3. Mescla overlay na página rotacionada
    buf.seek(0)
    overlay = PdfReader(buf)
    page.merge_page(overlay.pages[0])

    writer = PdfWriter()
    writer.add_page(page)

    with open(PDF_SAIDA, "wb") as f:
        writer.write(f)

    return PDF_SAIDA


# ── Interface gráfica ────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guia SADT — Unimed")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e", padx=28, pady=24)

        self._build()

    def _build(self):
        cor_bg    = "#1e1e2e"
        cor_entry = "#313244"
        cor_texto = "#cdd6f4"
        cor_label = "#a6adc8"

        tk.Label(self, text="Preencher Guia SADT", font=("Helvetica", 17, "bold"),
                 fg="white", bg=cor_bg).grid(row=0, column=0, columnspan=2,
                 pady=(0, 18), sticky="w")

        campos_ui = [
            ("Nome do Paciente",   "nome_var"),
            ("Indicação Clínica",  "ind_var"),
            ("Descrição",          "desc_var"),
        ]

        self.nome_var = tk.StringVar()
        self.ind_var  = tk.StringVar()
        self.desc_var = tk.StringVar()

        for i, (label, var_name) in enumerate(campos_ui, start=1):
            tk.Label(self, text=label, font=("Helvetica", 12),
                     fg=cor_label, bg=cor_bg).grid(row=i*2-1, column=0,
                     columnspan=2, sticky="w", pady=(10, 2))
            entry = tk.Entry(self, textvariable=getattr(self, var_name),
                             font=("Helvetica", 13), width=52,
                             bg=cor_entry, fg=cor_texto,
                             insertbackground=cor_texto,
                             relief="flat", bd=6)
            entry.grid(row=i*2, column=0, columnspan=2, sticky="ew")
            if i == 1:
                entry.focus_set()

        tk.Button(
            self,
            text="  Gerar PDF e Imprimir  ",
            font=("Helvetica", 13, "bold"),
            bg="#89b4fa", fg="#1e1e2e",
            relief="flat", bd=0, pady=8, padx=12,
            cursor="hand2",
            command=self.gerar
        ).grid(row=10, column=0, columnspan=2, pady=(24, 0), sticky="ew")

        # Atalho Enter
        self.bind("<Return>", lambda e: self.gerar())

    def gerar(self):
        nome       = self.nome_var.get().strip()
        ind        = self.ind_var.get().strip()
        desc       = self.desc_var.get().strip()

        if not nome and not ind and not desc:
            messagebox.showwarning("Atenção", "Preencha pelo menos um campo.")
            return

        try:
            caminho = gerar_pdf(nome, ind, desc)
            subprocess.Popen(["open", caminho])
        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    App().mainloop()
