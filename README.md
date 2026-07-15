# Extrator de Cotações NiCE

Lê um PDF de cotação e preenche automaticamente um template Excel, com interface gráfica (Tkinter).

## Requisitos

- Python instalado (https://www.python.org/downloads/)
- Bibliotecas:
  ```bash
  pip install openpyxl pdfplumber pyinstaller
  ```

## Rodando sem gerar executável

```bash
python3 app.py
```

## Debug (quando uma seção não vem pro Excel)

Use `debug.py` pra ver linha por linha o que o PDF entregou e por que cada uma foi aceita ou descartada:
```bash
python3 debug.py cotacaoParaTeste.pdf

ou 

py debug.py cotacaoParaTeste.pdf
```

Para fazer o teste dessa forma no terminal o PDF que deseja testar deve estar na raiz junto com o debug.py

## Known bug

### Seção não importar

O extractor só reconhece títulos de seção **cadastrados exatamente** no dicionário `TITLES`, em `extractor.py`. Cada PDF (dependendo do formato/exportação) pode usar um nome de seção diferente (ex: `"NICE Subscriptions"`, `"Monthly Network Connectivity Subscriptions"`).

**Se uma seção nova não for importada:** rode o `debug.py`, veja o `RAW` do título que não foi reconhecido, e adicione no `TITLES` em maiúsculo, sem quebras de linha, apontando pra seção correta (`mrc`, `nrc`, `usage`, `connectivity_mrc`, `connectivity_nrc`):

```python
TITLES = {
    # ...
    "NOME DO TÍTULO EM MAIÚSCULO": "mrc",
}
```

Outras causas comuns de linha descartada: preço com prefixo de moeda não tratado em `parse_price` (hoje cobre `R$`, `$`, `BRL`, `USD`), ou quantidade negativa (linhas de ajuste/remoção são ignoradas de propósito).

## Gerar executável no Mac

No Terminal, dentro da pasta raiz do projeto:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install openpyxl pdfplumber pyinstaller

pyinstaller --windowed --onedir --name ExtratorCotacoesNiCE --icon="utils/icon.icns" --add-data "utils/template.xlsx:utils" app.py
```

Talvez peça para instalar o xcode caso você ainda não tenha, se pedir autorize.

O resultado fica em `dist/ExtratorCotacoesNiCE.app`.

ATENÇÃO: Se você já tiver um executavel aberto e tentar gerar um outro pode dar erro, sempre feche.

## Gerar executável no Windows

No Terminal, dentro da pasta raiz do projeto:

```bash
py -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install openpyxl pdfplumber pyinstaller

pyinstaller --noconfirm --onefile --noconsole --name="Extrator_Cotações_NiCE" --icon="utils\icon.ico" --add-data "utils\template.xlsx;utils" --add-data "utils\icon.ico;utils" app.py
```
ATENÇÃO: Se você já tiver um executavel aberto e tentar gerar um outro pode dar erro, sempre feche.

## Atualização do template

Se o template Excel mudar (novo layout, mais linhas, colunas diferentes), ajuste o dicionário `EXCEL_MAP` em `extractor.py`. **Sempre mantenha o arquivo com o mesmo nome** (`utils/template.xlsx`), só troque o conteúdo.

Cada seção (`mrc`, `nrc`, `usage`, `connectivity_mrc`, `connectivity_nrc`) tem:

```python
"mrc": {
    "sheet": None,        # nome da aba, se o template tiver mais de uma (None = aba ativa)
    "start_row": 6,        # linha do Excel onde a seção começa a preencher
    "max_row": 21,          # última linha permitida pra essa seção
    "cols": {"product": "C", "sku": "D", "qty": "E", "price": "H"},  # colunas de cada campo
},
```

- **`start_row`**: em qual linha do Excel a primeira linha extraída do PDF entra. Se o template mudar e a tabela de "MRC" passar a começar na linha 8 em vez da 6, muda esse número.
- **`max_row`**: até qual linha essa seção pode preencher. Se a cotação tiver mais linhas do que cabe (ex: 20 produtos, mas `max_row` só permite até a linha 21 = 15 produtos), as linhas excedentes **não são escritas** — só aparece um aviso no terminal (`[AVISO] Seção 'mrc' estourou o limite operacional estabelecido.`) e essas linhas se perdem. Se o template ganhar mais espaço, aumente esse número.
- **`cols`**: em qual coluna cada campo (produto, SKU, quantidade, preço) vai. Se o template mudar a ordem das colunas, ajusta as letras aqui.

**Resumindo:** se a cotação normalmente tem poucos produtos mas às vezes vem uma bem grande e passa do limite, o ajuste é aumentar o `max_row` da seção correspondente (e garantir que o template Excel realmente tem linhas até lá, com a formatação certa).
