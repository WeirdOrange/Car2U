from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from datetime import datetime

# Create a function for header and footer
def add_header_footer(canvas, doc_title):
    width, height = A4
    print(width,height)

    # Add Header
    canvas.setFont("Helvetica Bold", 16)
    canvas.drawString(40, height - 40, doc_title)
    canvas.setFont("Helvetica", 10)
    canvas.drawString(40, height - 60, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    canvas.line(40, height - 65, width - 40, height - 65)

    # Add Footer
    canvas.setFont("Helvetica", 10)
    canvas.drawString(40, 30, "Car2U Official Car Rental Services")
    canvas.drawString(width - 200, 30, "Contact Us: car2uofficial@gmail.com")
    canvas.line(40, 50, width - 40, 50)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(width - 60, 20, f"Page {canvas.getPageNumber()}")

# Create a PDF layout
def generate_pdf_layout(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title and basic info
    title = Paragraph("Monthly Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.2 * inch))

    agency_info = [
        ["Agency Name:", ""],
        ["Email:", ""],
        ["Address:", ""]
    ]
    table = Table(agency_info, colWidths=[100, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.2 * inch))

    # Table Headers
    data = [
        ["Car No.", "Car Average Rating", "Number(s) of New Rating"],
        ["", "", ""]
    ]
    table = Table(data, colWidths=[100, 150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    # Another table example for other sections
    data = [
        ["Car Rented", "Car Number", "Number of days booked", "Earnings"],
        ["Car Cancelled", "", "", ""],
        ["Car Rejected", "", "", ""],
        ["Total", "", "", ""]
    ]
    table = Table(data, colWidths=[100, 100, 150, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(table)
    doc_title = "Monthly"
    # Build the document with header and footer callbacks
    doc.build(elements, onFirstPage=add_header_footer(doc,doc_title), onLaterPages=add_header_footer(doc,doc_title))

# Generate the PDF
generate_pdf_layout("monthly_report.pdf")

width, height = A4
print(width,height)