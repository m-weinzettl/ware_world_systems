from fpdf import FPDF


class Invoice_To_PDF(FPDF):
    def __init__(self, data):
        super().__init__()
        self.invoice_data = data



    def header(self):
        logo_path = "../model/logo/logo.jpg"
        # Logo oder der Titel oben auf JEDER Seite
        self.image(logo_path, 10, 8, 33)
        self.set_font('Helvetica', 'B', 15)
        customer = self.invoice_data["customer_info"]
        self.cell(0, 10, f"Rechnung für {customer['name']}", 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 5, f"Kunden-Typ: {customer['type']}", 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Seite {self.page_no()} / {{nb}}', 0, 0, 'C')

    def create_invoice_to_pdf(self, file_name):
        self.alias_nb_pages()
        self.add_page()

        # Tabellenkopf
        self.set_font('Helvetica', 'B', 12)
        self.cell(130, 10, "Produkt / Details", 1)
        self.cell(60, 10, "Preis", 1, ln=True, align='C')

        # Items durchlaufen
        self.set_font('Helvetica', '', 11)
        for item in self.invoice_data["items"]:
            start_y = self.get_y()

            safe_details = item['details'].replace("€", "EUR")

            # Multi-Cell für den Text
            self.multi_cell(130, 8, f"{item['name']}\n{safe_details}", 1)
            end_y = self.get_y()

            # Preis-Zelle
            self.set_xy(10 + 130, start_y)
            self.cell(60, end_y - start_y, f"{item['unit_price']:.2f} EUR", 1, ln=True, align='R')

        # Gesamtsumme
        self.ln(10)
        self.set_font('Helvetica', 'B', 12)
        self.cell(130, 10, "Gesamtpreis:", 0, align='R')
        self.cell(60, 10, f"{self.invoice_data['total_sum']:.2f} EUR", 1, ln=True, align='R')

        self.output(file_name)