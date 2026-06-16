import os
import sys
import markdown
from xhtml2pdf import pisa

sys.stdout.reconfigure(encoding='utf-8')

ENTREGABLES_DIR = r"D:\proyecto16\healthcare-etl-platform\Entregables"

CSS_STYLE = """
@page { size: A4; margin: 2cm; }
body { font-family: 'Helvetica','Arial',sans-serif; font-size: 11pt; line-height: 1.6; color: #000000; }
h1 { font-size: 20pt; color: #1e3a8a; border-bottom: 2px solid #1e3a8a; padding-bottom: 6px; margin-top: 30px; margin-bottom: 15px; }
h2 { font-size: 16pt; color: #2563eb; margin-top: 25px; margin-bottom: 10px; }
h3 { font-size: 13pt; color: #000000; margin-top: 20px; margin-bottom: 8px; }
h4 { font-size: 11pt; color: #000000; }
p { margin: 8px 0; text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 15px 0; font-size: 9pt; }
th { background-color: #1e3a8a; color: #ffffff; padding: 8px 10px; text-align: left; font-weight: bold; }
td { border: 1px solid #999999; padding: 6px 10px; }
tr:nth-child(even) td { background-color: #f0f4ff; }
code { font-family: 'Courier New', monospace; font-size: 9pt; }
pre { background-color: #f5f5f5; padding: 12px 15px; border: 1px solid #cccccc; font-size: 8pt; line-height: 1.3; margin: 10px 0; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
blockquote { border-left: 4px solid #2563eb; padding: 10px 15px; background: #f0f4ff; margin: 15px 0; }
ul, ol { padding-left: 25px; margin: 8px 0; }
li { margin-bottom: 4px; }
a { color: #2563eb; text-decoration: none; }
strong { color: #000000; }
em { font-style: italic; }
hr { border: none; border-top: 1px solid #cccccc; margin: 25px 0; }
img { max-width: 100%; }
.page-break { page-break-before: always; }
"""

def convert_md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_content = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables', 'codehilite', 'nl2br', 'sane_lists']
    )

    full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <style>{CSS_STYLE}</style>
</head>
<body>
    {html_content}
</body>
</html>"""

    with open(pdf_path, 'wb') as f:
        pisa_status = pisa.CreatePDF(
            src=full_html,
            dest=f,
            encoding='utf-8'
        )

    if pisa_status.err:
        print("ERROR:", os.path.basename(pdf_path))
    else:
        print("OK:", os.path.basename(pdf_path))

files = [
    "01_Codificacion_y_BD.md",
    "02_Evidencias_ETL.md",
    "03_Documentacion_Tecnica.md",
    "04_Manual_Usuario.md",
    "05_Diagramas_Arquitectura.md",
    "06_Evidencia_ML.md"
]

print("Convirtiendo documentos a PDF...\n")

for fname in files:
    md_file = os.path.join(ENTREGABLES_DIR, fname)
    pdf_file = os.path.join(ENTREGABLES_DIR, fname.replace('.md', '.pdf'))
    if os.path.exists(md_file):
        try:
            convert_md_to_pdf(md_file, pdf_file)
        except Exception as e:
            print("ERROR:", fname, "-", str(e)[:120])
    else:
        print("NO ENCONTRADO:", fname)

print("\nListo.")
