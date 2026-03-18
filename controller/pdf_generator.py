from fpdf import FPDF


class Invoice_To_PDF(FPDF):
    def create_invoice_to_pdf(self, data, file_name):
        self.add_page()
        self.set_font('Arial', 'B', size=15)

        #kundendaten
        customer = data["customer_info"]
        self.cell(0, 10, f"Rechnung für {customer['name']}", ln=True)
        self.set_font('Arial', '', size=12)
        self.cell(0, 10, f"Typ: {customer['type']}", ln=True)
        self.ln(10)

        self.set_font('Arial', 'B', size=12)
        self.cell(130, 10, "Produkt / Details", 1)
        self.cell(60, 10, "Preis", 1, ln=True)

        # Items durchlaufen
        self.set_font('Arial', '', size=11)
        for item in data["items"]:
            start_y = self.get_y()
            self_details = item['details'].replace("€", "EUR")
            self.multi_cell(130, 8, f"{item['name']}\n{self_details}", 1)
            end_y = self.get_y()

            self.set_xy(140, start_y)
            self.cell(60, end_y - start_y, f"{item['unit_price']:.2f} EUR", 1, ln=True)

        self.ln(10)
        self.set_font('Arial', 'B', size=12)
        self.cell(0, 10, f"Gesamtpreis: {data['total_sum']:.2f} EUR", 1, ln=True)

        # Speichern
        self.output(file_name)