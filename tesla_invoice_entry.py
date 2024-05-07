import streamlit as st
import pandas as pd
import base64
from io import BytesIO

def generate_csv(data):
    output = BytesIO()
    data.to_csv(output, index=False)
    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="P2PPortal-CSVFileTemplate.csv">Download CSV File</a>'
    return href

def main():
    st.title("Tesla Invoice Data Entry")
    
    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        vendor_number = st.text_input("Vendor Number")
        invoice_date = st.date_input("Invoice Date")
        invoice_number = st.text_input("Invoice Number")
        currency = st.text_input("Currency", value="USD")
    with col2:
        packing_slip_number = st.text_input("Packing Slip Number")
        payment_terms = st.text_input("Payment Terms")
        po_number = st.text_input("PO Number")

    # Line items
    num_lines = st.number_input("Number of Line Items", min_value=1, value=1, step=1)
    line_items = []
    line_item_expander = st.expander("Line Items")
    with line_item_expander:
        for i in range(num_lines):
            st.subheader(f"Line Item {i+1}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                po_line_number = st.text_input(f"PO Line Number {i+1}")
                part_number = st.text_input(f"Part Number {i+1}")
            with col2:
                unit_price = st.number_input(f"Unit Price {i+1}")
                quantity = st.number_input(f"Quantity {i+1}", min_value=1, value=1, step=1)
            with col3:
                uom = st.text_input(f"UOM {i+1}", value="EA")
                taxable_flag = st.selectbox(f"Taxable Flag {i+1}", ("I0", "I1"))
            with col4:
                tax_code = st.text_input(f"Tax Code {i+1}")
                tax_amount = st.number_input(f"Tax Amount {i+1}", value=0.0)
            line_items.append([po_line_number, part_number, unit_price, quantity, uom, taxable_flag, tax_code, tax_amount])

    # Surcharges
    surcharge_expander = st.expander("Surcharges")
    with surcharge_expander:
        surcharge_type = st.text_input("Surcharge Type")
        surcharge_amount = st.number_input("Surcharge Amount", value=0.0)

    if st.button("Generate CSV"):
        data = []
        invoice_total_amount = 0
        for item in line_items:
            po_line_number, part_number, unit_price, quantity, uom, taxable_flag, tax_code, tax_amount = item
            total_amount = unit_price * quantity
            invoice_total_amount += total_amount
            data.append([vendor_number, invoice_date.strftime("%Y%m%d"), invoice_number, currency, packing_slip_number,
                         payment_terms, po_number, po_line_number, part_number, unit_price, quantity, uom,
                         taxable_flag, tax_code, tax_amount, total_amount])
        invoice_tax_amount = sum(item[7] for item in line_items)
        invoice_total_amount += surcharge_amount
        for row in data:
            row.extend([invoice_total_amount, invoice_tax_amount, surcharge_type, surcharge_amount])
        df = pd.DataFrame(data, columns=["Vendor Number", "Invoice Date", "Invoice Number", "Currency", "Packing slip number",
                                         "Payment terms", "PO number", "PO line number", "Part number", "Unit Price",
                                         "Line Item Quantity", "Line Item UOM", "Line Item Taxable Flag", "Line Item Tax Code",
                                         "Line Item Tax Amount", "Total amount for line Item quantity", "Invoice Total Amount",
                                         "Invoice Tax Amount", "Surcharge Type", "Surcharge Amount"])
        st.markdown(generate_csv(df), unsafe_allow_html=True)

if __name__ == "__main__":
    main()