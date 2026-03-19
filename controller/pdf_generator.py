from fpdf import FPDF
from datetime import datetime


class Invoice_To_PDF(FPDF):
    def __init__(self, data):
        super().__init__()
        self.invoice_data = data

    def header(self):
        logo_path = "../model/logo/logo.jpg"
        site_name = "Waren Welt Online Shop"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.image(logo_path, 167, 8, 33)
        except (FileNotFoundError, RuntimeError):
            pass

        customer = self.invoice_data["customer_info"]
        display_header = customer.get('company_name') or customer.get('name') or "Kunde"

        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, f"{site_name}", 0, 1, 'L')
        self.cell(0, 10, f"Rechnung für {display_header}", 0, 1, 'L')

        self.set_font('Helvetica', '', 10)
        if customer.get('company_name'):
            self.cell(0, 5, f"Firma: {customer['company_name']}", 0, 1, 'L')

        if customer.get('name'):
            label = "Ansprechpartner: " if customer.get('company_name') else "Name: "
            self.cell(0, 5, f"{label}{customer['name']}", 0, 1, 'L')

        self.cell(0, 5, f"Adresse: {customer['address']}", 0, 1, 'L')
        self.cell(0, 5, f"Mail: {customer['mail']}", 0, 1, 'L')

        if customer.get('uid'):
            self.cell(0, 5, f"UID: {customer['uid']}", 0, 1, 'L')
        elif customer.get('geb_date'):
            self.cell(0, 5, f"Geb.-Datum: {customer['geb_date']}", 0, 1, 'L')

        self.set_xy(110, 42)
        self.set_font('Helvetica', 'B', 8)
        oid = self.invoice_data.get('order_id', 'N/A')
        self.cell(90, 5, f"Bestell-ID: {str(oid)}", 0, 1, 'R')
        self.set_font('Helvetica', '', 8)
        self.cell(0, 5, f"Erstellt am: {timestamp}", 0, 1, 'R')

        self.set_xy(10, 55)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Seite {self.page_no()} / {{nb}}', 0, 0, 'C')

    def create_invoice_to_pdf(self, file_name):
        self.alias_nb_pages()
        self.add_page()

        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(130, 10, " Produkt / Details", 1, 0, 'L', fill=True)
        self.cell(60, 10, "Preis ", 1, 1, 'C', fill=True)

        for item in self.invoice_data["items"]:
            start_y = self.get_y()

            self.set_font('Helvetica', 'B', 10)
            self.set_xy(12, start_y + 2)
            self.cell(126, 5, item['name'], 0, 1, 'L')

            self.set_font('Helvetica', '', 8)
            self.set_text_color(100, 100, 100)
            safe_details = item['details'].replace("€", "EUR")
            self.set_x(12)
            self.multi_cell(126, 4, safe_details, 0, 'L')

            self.set_text_color(0, 0, 0)
            end_y = self.get_y() + 2
            h = max(14.0, float(end_y - start_y))

            self.rect(10, start_y, 130, h)

            self.set_xy(140, start_y)
            self.set_font('Helvetica', '', 10)
            self.cell(60, h, f"{item['unit_price']:.2f} EUR", 1, 1, 'R')
            self.set_y(start_y + h)

        self.ln(5)

        # Berechnung der Zwischensumme (vor Rabatt)
        subtotal = self.invoice_data['total_sum'] + self.invoice_data['discount_sum']

        self.set_font('Helvetica', '', 11)
        self.cell(130, 8, "Zwischensumme:", 0, 0, 'R')
        self.cell(60, 8, f"{subtotal:.2f} EUR", 1, 1, 'R')

        self.set_text_color(200, 0, 0)  # Rabatt in Rot
        self.cell(130, 8, "Rabatt (5%):", 0, 0, 'R')
        self.cell(60, 8, f"- {self.invoice_data['discount_sum']:.2f} EUR", 1, 1, 'R')

        self.set_text_color(0, 0, 0)
        self.set_font('Helvetica', 'B', 12)
        self.cell(130, 10, "Gesamtpreis:", 0, 0, 'R')
        self.cell(60, 10, f"{self.invoice_data['total_sum']:.2f} EUR", 1, 1, 'R')

        self.output(file_name)