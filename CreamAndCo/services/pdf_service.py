"""
Cream & Co. — PDF Invoice Service
====================================
Generates branded PDF invoices for orders.
Uses fpdf2 (pip install fpdf2).
"""

import base64
from datetime import datetime
from fpdf import FPDF


def generate_invoice_pdf_base64(
    order_number: str,
    customer_name: str,
    delivery_address: str,
    items: list[dict],
    subtotal: float,
    delivery_fee: float,
    total_amount: float,
) -> str:
    """
    Generate a professional PDF invoice and return as base64 string.

    Parameters
    ----------
    items : list of dict
        Each dict must have keys: name, quantity, unit_price, total_price
    """
    pdf = FPDF()
    pdf.add_page()
    pw = pdf.w - pdf.l_margin - pdf.r_margin  # printable width

    # ── Header ────────────────────────────────────────────────────────────
    pdf.set_fill_color(212, 163, 115)  # #D4A373
    pdf.rect(0, 0, 210, 45, "F")
    pdf.set_font("Helvetica", style="B", size=26)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(10)
    pdf.cell(0, 12, "Cream & Co.", ln=True, align="C")
    pdf.set_font("Helvetica", size=9)
    pdf.set_text_color(250, 237, 205)  # #FAEDCD
    pdf.cell(
        0, 6,
        "103, Mukti Marg, Dewas  |  FSSAI: 21422790001224",
        ln=True, align="C",
    )

    pdf.set_y(52)

    # ── Invoice Title ─────────────────────────────────────────────────────
    pdf.set_font("Helvetica", style="B", size=18)
    pdf.set_text_color(43, 43, 43)
    pdf.cell(pw / 2, 10, "INVOICE")
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(pw / 2, 10, datetime.now().strftime("%d %B %Y"), align="R", ln=True)
    pdf.ln(4)

    # ── Order + Customer Info ─────────────────────────────────────────────
    pdf.set_font("Helvetica", style="B", size=10)
    pdf.set_text_color(43, 43, 43)
    pdf.cell(pw / 2, 6, f"Order: {order_number}")
    pdf.cell(pw / 2, 6, "Billed To:", ln=True)

    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(pw / 2, 6, "")
    pdf.cell(pw / 2, 6, customer_name, ln=True)

    if delivery_address:
        pdf.cell(pw / 2, 6, "")
        pdf.cell(pw / 2, 6, delivery_address[:60], ln=True)

    pdf.ln(10)

    # ── Items Table ───────────────────────────────────────────────────────
    col_w = [pw * 0.06, pw * 0.48, pw * 0.12, pw * 0.16, pw * 0.18]

    # Table header
    pdf.set_fill_color(250, 237, 205)  # #FAEDCD
    pdf.set_font("Helvetica", style="B", size=10)
    pdf.set_text_color(43, 43, 43)
    headers = ["#", "Item", "Qty", "Price", "Total"]
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 8, h, border=0, fill=True, align="C" if i > 0 else "L")
    pdf.ln()

    # Table rows
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(75, 85, 99)
    for idx, item in enumerate(items, 1):
        pdf.cell(col_w[0], 7, str(idx))
        pdf.cell(col_w[1], 7, str(item.get("name", ""))[:35])
        pdf.cell(col_w[2], 7, str(item.get("quantity", 0)), align="C")
        pdf.cell(col_w[3], 7, f"{item.get('unit_price', 0):.2f}", align="R")
        pdf.cell(col_w[4], 7, f"{item.get('total_price', 0):.2f}", align="R")
        pdf.ln()

    # Divider
    pdf.ln(2)
    pdf.set_draw_color(229, 231, 235)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + pw, pdf.get_y())
    pdf.ln(4)

    # ── Totals ────────────────────────────────────────────────────────────
    totals_x = pw * 0.60
    totals_w = pw * 0.40

    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(totals_x, 6, "")
    pdf.cell(totals_w / 2, 6, "Subtotal:")
    pdf.cell(totals_w / 2, 6, f"INR {subtotal:.2f}", align="R", ln=True)

    pdf.cell(totals_x, 6, "")
    pdf.cell(totals_w / 2, 6, "Delivery:")
    pdf.cell(
        totals_w / 2, 6,
        "FREE" if delivery_fee == 0 else f"INR {delivery_fee:.2f}",
        align="R", ln=True,
    )

    pdf.ln(2)
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.set_text_color(212, 163, 115)
    pdf.cell(totals_x, 8, "")
    pdf.cell(totals_w / 2, 8, "Total:")
    pdf.cell(totals_w / 2, 8, f"INR {total_amount:.2f}", align="R", ln=True)

    # ── Footer ────────────────────────────────────────────────────────────
    pdf.set_y(-30)
    pdf.set_font("Helvetica", size=8)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(0, 5, "Thank you for choosing Cream & Co.!", align="C", ln=True)
    pdf.cell(0, 5, "This is a computer-generated invoice.", align="C")

    # Return base64 string
    pdf_bytes = pdf.output()
    return base64.b64encode(pdf_bytes).decode("utf-8")
