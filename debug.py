import sys
import pdfplumber
from extractor import TITLES, LAYOUT, norm, parse_qty, parse_price, clean_sku

def debug_pdf(pdf_path):
    current_section = None
    current_title = None
    finished_titles = set()

    with pdfplumber.open(pdf_path) as pdf:
        for p_idx, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            print(f"\n===== PÁGINA {p_idx+1} — {len(tables)} tabela(s) detectada(s) =====")

            if not tables:
                print("  [!] Nenhuma tabela detectada nesta página (extract_tables retornou vazio).")

            for t_idx, table in enumerate(tables):
                print(f"  -- Tabela {t_idx+1} ({len(table)} linhas) --")
                for row in table:
                    if not row:
                        continue
                    first_cell = norm(row[0]).upper()
                    print(f"    RAW: {row}")

                    if first_cell in TITLES:
                        status = "JÁ FINALIZADO (ignorado)" if first_cell in finished_titles else "SEÇÃO ATIVADA"
                        print(f"      -> TÍTULO reconhecido: '{first_cell}' -> {TITLES[first_cell]} [{status}]")
                        if first_cell in finished_titles:
                            current_section = None
                        else:
                            current_section = TITLES[first_cell]
                            current_title = first_cell
                        continue

                    if first_cell in ("PRODUCT CODE", "PRODUCT", "CATALOG ID"):
                        print("      -> Cabeçalho de coluna, ignorado")
                        continue

                    if current_section is None:
                        print("      -> DESCARTADO: nenhuma seção ativa no momento")
                        continue

                    if all(c is None or norm(c) == "" for c in row):
                        print("      -> Linha vazia, ignorada")
                        continue

                    if len(row) < 4:
                        print(f"      -> DESCARTADO: linha tem só {len(row)} colunas (precisa >=4)")
                        continue

                    qty = parse_qty(row[-3])
                    price = parse_price(row[-2])
                    print(f"      -> qty parseado: {row[-3]!r} -> {qty} | price parseado: {row[-2]!r} -> {price}")

                    if qty is None or price is None:
                        print(f"      -> DESCARTADO: qty ou price None. Seção '{current_title}' marcada como finalizada.")
                        if current_title is not None:
                            finished_titles.add(current_title)
                        current_section = None
                        continue

                    layout = LAYOUT[current_section]
                    if layout == "software":
                        sku = clean_sku(row[0])
                        product = " ".join(norm(c) for c in row[1:-3] if norm(c))
                    else:
                        sku = ""
                        product = norm(row[0])

                    if not product:
                        print("      -> DESCARTADO: product vazio, seção finalizada")
                        finished_titles.add(current_title)
                        current_section = None
                        continue

                    print(f"      -> ACEITO em '{current_section}': sku={sku!r} product={product!r} qty={qty} price={price}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python debug_extract.py <arquivo.pdf>")
        sys.exit(1)
    debug_pdf(sys.argv[1])