"""
Script para converter o arquivo markdown para PDF.
Requer: pip install markdown2 pdfkit
"""
import markdown2
import pdfkit
import os

def convert_md_to_pdf(md_file, pdf_file):
    # Ler o arquivo markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Converter markdown para HTML
    html_content = markdown2.markdown(
        md_content,
        extras=['tables', 'fenced-code-blocks', 'header-ids']
    )
    
    # Adicionar estilos CSS
    html_with_style = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 40px;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
            }}
            code {{
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                overflow-x: auto;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f8f9fa;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Configurar opções do PDF
    options = {
        'page-size': 'A4',
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'encoding': 'UTF-8',
        'no-outline': None
    }
    
    # Converter HTML para PDF
    pdfkit.from_string(html_with_style, pdf_file, options=options)

if __name__ == '__main__':
    # Caminhos dos arquivos
    current_dir = os.path.dirname(os.path.abspath(__file__))
    md_file = os.path.join(current_dir, 'melhorias_futuras.md')
    pdf_file = os.path.join(current_dir, 'melhorias_futuras.pdf')
    
    # Converter
    convert_md_to_pdf(md_file, pdf_file)
    print(f"PDF gerado com sucesso: {pdf_file}")
