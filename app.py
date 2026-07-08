import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from extractor import extract_pdf, write_to_excel

# Descobre a pasta onde está o .exe (Sua lógica robusta)
if getattr(sys, "frozen", False):
    exe_dir = os.path.dirname(sys.executable)

    if sys.platform == "darwin":
        BASE_DIR = os.path.abspath(
            os.path.join(exe_dir, "..", "..", "..")
        )
    else:
        BASE_DIR = exe_dir
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_PATH = os.path.join(BASE_DIR, "utils", "template.xlsx")


def selecionar_pdf():
    caminho = filedialog.askopenfilename(
        title="Selecione a cotação",
        filetypes=[("PDF", "*.pdf")]
    )
    if caminho:
        pdf_var.set(caminho)


def gerar_excel():
    pdf_path = pdf_var.get()

    if not pdf_path:
        messagebox.showerror("Erro", "Selecione um PDF.")
        return

    output = filedialog.asksaveasfilename(
        title="Salvar Excel",
        defaultextension=".xlsx",
        filetypes=[("Excel", "*.xlsx")],
        initialfile="Cotacao_Preenchida.xlsx"
    )

    if not output:
        return

    try:
        # Extração direta do PDF purificado
        data = extract_pdf(pdf_path)
        write_to_excel(data, TEMPLATE_PATH, output)

        messagebox.showinfo(
            "Sucesso",
            f"Arquivo gerado com sucesso:\n{output}"
        )

    except Exception as e:
        messagebox.showerror("Erro", str(e))


# =====================================================================
# CONSTRUÇÃO DA INTERFACE GRÁFICA
# =====================================================================
root = tk.Tk()
root.title("Extrator de Cotações NiCE")
root.geometry("600x180")
root.resizable(False, False)

pdf_var = tk.StringVar()

tk.Label(root, text="PDF da cotação", font=("Arial", 10, "bold")).pack(pady=(20, 5))

tk.Entry(root, textvariable=pdf_var, width=60).pack()

tk.Button(root, text="Selecionar PDF", command=selecionar_pdf).pack(pady=10)

tk.Button(
    root,
    text="Gerar Excel",
    command=gerar_excel,
    height=2,
    width=20,
    bg="#0d6efd",
    fg="white",
    font=("Arial", 10, "bold")
).pack()

root.mainloop()