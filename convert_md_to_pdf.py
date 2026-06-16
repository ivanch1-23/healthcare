import os
import sys
import markdown
from xhtml2pdf import pisa

sys.stdout.reconfigure(encoding='utf-8')

ENTREGABLES_DIR = r"D:\proyecto16\healthcare-etl-platform\Entregables"

CSS_STYLE = """
@page { size: A4; margin: 2cm 2.2cm; }
body { font-family: 'Helvetica','Arial',sans-serif; font-size: 10pt; line-height: 1.5; color: #1e293b; }
h1 { font-size: 18pt; color: #1e3a8a; border-bottom: 3px solid #1e3a8a; padding-bottom: 6px; margin-top: 25px; }
h2 { font-size: 14pt; color: #2563eb; margin-top: 20px; }
h3 { font-size: 12pt; color: #334155; margin-top: 15px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 8.5pt; }
th { background-color: #1e3a8a; color: white; padding: 6px 8px; text-align: left; }
td { border: 1px solid #cbd5e1; padding: 4px 8px; }
tr:nth-child(even) { background-color: #f1f5f9; }
code { background-color: #f1f5f9; padding: 1px 4px; font-size: 8pt; }
pre { background-color: #1e293b; color: #e2e8f0; padding: 10px 12px; font-size: 7.5pt; }
pre code { background: none; padding: 0; color: inherit; }
blockquote { border-left: 3px solid #2563eb; padding: 6px 12px; background: #f0f4ff; margin: 12px 0; }
ul, ol { padding-left: 22px; }
li { margin-bottom: 3px; }
p { margin: 6px 0; }
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
    <meta charset="UTF-8">
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

print("=== Convirtiendo documentos a PDF ===\n")

for fname in files:
    md_file = os.path.join(ENTREGABLES_DIR, fname)
    pdf_file = os.path.join(ENTREGABLES_DIR, fname.replace('.md', '.pdf'))
    if os.path.exists(md_file):
        try:
            convert_md_to_pdf(md_file, pdf_file)
        except Exception as e:
            print("ERROR:", fname, str(e)[:100])
    else:
        print("NOT FOUND:", fname)

print("\n=== Conversion completada ===")
