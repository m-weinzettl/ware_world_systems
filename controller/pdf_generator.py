from fpdf import FPDF

class Invoice_To_PDF(FPDF):
    def __init__(self, data):
        super().__init__()
        self.invoice_data = data

    def header(self):
        logo_path = "../model/logo/logo.jpg"
        try:
            self.image(logo_path, 167, 8, 33)
        except:
            pass

        customer = self.invoice_data["customer_info"]
        display_header = customer.get('company_name') or customer.get('name') or "Kunde"

        self.set_font('Helvetica', 'B', 15)
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

        self.set_font('Helvetica', '', 10)
        for item in self.invoice_data["items"]:
            start_y = self.get_y()
            safe_details = item['details'].replace("€", "EUR")

            self.multi_cell(130, 7, f"{item['name']}\n{safe_details}", 1)
            end_y = self.get_y()
            h = end_y - start_y

            self.set_xy(140, start_y)
            self.cell(60, h, f"{item['unit_price']:.2f} EUR", 1, 1, 'R')

        self.ln(5)
        self.set_font('Helvetica', 'B', 12)
        self.cell(130, 10, "Gesamtpreis:", 0, 0, 'R')
        self.cell(60, 10, f"{self.invoice_data['total_sum']:.2f} EUR", 1, 1, 'R')

        self.output(file_name)