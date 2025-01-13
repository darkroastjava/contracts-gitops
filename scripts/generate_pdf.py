import sys
import yaml
from jinja2 import Template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(template_path, data_path, output_path):
    # Load template
    with open(template_path, 'r') as f:
        template_content = f.read()
    template = Template(template_content)

    # Load contract data
    with open(data_path, 'r') as f:
        data = yaml.safe_load(f)

    # Render contract text
    rendered_text = template.render(data)

    # Create PDF
    c = canvas.Canvas(output_path, pagesize=letter)
    c.drawString(100, 750, "Vertrag")
    text = c.beginText(100, 730)
    text.setFont("Helvetica", 10)
    for line in rendered_text.splitlines():
        text.textLine(line)
    c.drawText(text)
    c.save()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_pdf.py <template_path> <data_path> <output_path>")
        sys.exit(1)

    generate_pdf(sys.argv[1], sys.argv[2], sys.argv[3])
