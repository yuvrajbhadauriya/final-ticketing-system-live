import qrcode
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing

def generate_ticket_pdf(submission):
    """
    Generates a branded ticket PDF using the secure qr_code_id.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=(8.5 * inch, 4 * inch))
    width, height = (8.5 * inch, 4 * inch)
    tedx_red = HexColor("#e62b1e")

    # --- Ticket Design ---
    p.setFillColorRGB(0.1, 0.1, 0.1)
    p.rect(0, 0, width, height, fill=1, stroke=0)
    p.setFillColor(tedx_red)
    p.rect(0, height - 0.25 * inch, width, 0.25 * inch, fill=1, stroke=0)
    p.setFillColorRGB(1, 1, 1)
    p.setFont("Helvetica-Bold", 36)
    p.drawString(0.5 * inch, height - 1 * inch, "TEDxVIPS'25")
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(tedx_red)
    p.drawString(0.5 * inch, height - 1.5 * inch, "| IGNITED")

    # --- Attendee Details ---
    p.setFillColorRGB(0.9, 0.9, 0.9)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(0.5 * inch, 1.8 * inch, "ATTENDEE:")
    p.setFont("Helvetica", 11)
    p.drawString(1.5 * inch, 1.8 * inch, submission.full_name)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(0.5 * inch, 1.5 * inch, "EMAIL:")
    p.setFont("Helvetica", 11)
    p.drawString(1.5 * inch, 1.5 * inch, submission.email)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(0.5 * inch, 1.2 * inch, "TICKET ID:")
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(tedx_red)
    p.drawString(1.5 * inch, 1.2 * inch, submission.ticket_id) # Human-readable ID
    p.setFillColorRGB(0.9, 0.9, 0.9)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(0.5 * inch, 0.9 * inch, "GATE:")
    p.setFont("Helvetica", 11)
    p.drawString(1.5 * inch, 0.9 * inch, "1")

    # --- Secure QR Code ---
    # Use the secure, random qr_code_id for the QR code's data
    qr_code_data = str(submission.qr_code_id)
    qr_code = qr.QrCodeWidget(qr_code_data, barFillColor=tedx_red)
    bounds = qr_code.getBounds()
    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]
    d = Drawing(2.5 * inch, 2.5 * inch, transform=[2.5*inch/qr_width, 0, 0, 2.5*inch/qr_height, 0, 0])
    d.add(qr_code)
    p.setFillColorRGB(1, 1, 1)
    p.rect(width - 3.3 * inch, 0.4 * inch, 2.7 * inch, 2.7 * inch, fill=1, stroke=0)
    renderPDF.draw(d, p, width - 3.2 * inch, 0.5 * inch)

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer