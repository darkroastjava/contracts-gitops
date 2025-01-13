import os
import tempfile
from unittest import TestCase

from scripts.generate_pdf import generate_pdf

class GeneratePDFTest(TestCase):
    def setUp(self):
        self.templateFile = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md")
        self.templateFile.close()
        self.dataFile = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml")
        self.dataFile.close()
        self.outputFile = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".pdf")
        self.outputFile.close()

    def tearDown(self):
        os.unlink(self.templateFile.name)
        os.unlink(self.dataFile.name)
        os.unlink(self.outputFile.name)

    def test_generate_pdf(self):
        # arrange
        with open(self.templateFile.name, "w") as f:
            f.write("""
# Liefervertrag

Dieser Vertrag wird geschlossen zwischen:

- **Name des Lieferanten:** {{ supplier_name }}
- **Adresse des Lieferanten:** {{ supplier_address }}

## Vertragsdetails:

- **Startdatum:** {{ contract_date }}
- **Laufzeit:** {{ contract_duration }}

## Bedingungen:

Die genauen Vertragsbedingungen finden Sie in den beigefügten Dokumenten.
""")
        
        with open(self.dataFile.name, "w") as f:
            f.write("""
template: liefervertrag.md
supplier_name: Supplier A
supplier_address: Musterstraße 123, 12345 Musterstadt
contract_duration: 12 Monate
contract_date: 2025-01-13
amount: 200000  # Betrag für die Schwellenprüfung
""")

        # act
        generate_pdf(template_path=self.templateFile.name, data_path=self.dataFile.name, output_path=self.outputFile.name)

        # assert
        with open(self.outputFile.name, "rb") as f:
            file_content = f.read()
        self.assertIn(b'/Title (Liefervertrag)', file_content)
        self.assertIn(b'/Title (Vertragsdetails:)', file_content)
        self.assertIn(b'''Gb!<L9lldX&;KZQ'mk$a[DM22M;FCeF)j>%1"2=>,RCF$i"SRBP@*2NCtI]6LSd3kUHo0fKV!''', file_content)
