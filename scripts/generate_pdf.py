import sys
import yaml
from jinja2 import Template
from markdown import markdown
from xhtml2pdf import pisa


def generate_pdf(template_path, data_path, output_path):
    # Load template
    with open(template_path, 'r') as f:
        template_content = f.read()
    template = Template(template_content)

    # Load contract data
    with open(data_path, 'r') as f:
        data = yaml.safe_load(f)

    # Render contract text with Jinja2
    rendered_text = template.render(data)

    # Convert rendered Markdown to HTML
    rendered_html = markdown(rendered_text)

    # Write the HTML to PDF
    with open(output_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(rendered_html, dest=pdf_file)
    
    if pisa_status.err:
        print("Error during PDF generation")
    else:
        print(f"PDF successfully generated: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_pdf.py <template_path> <data_path> <output_path>")
        sys.exit(1)

    generate_pdf(sys.argv[1], sys.argv[2], sys.argv[3])
