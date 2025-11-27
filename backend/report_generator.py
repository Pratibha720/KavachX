from fpdf import FPDF
from datetime import datetime
from pathlib import Path

def generate_privacy_report(out_dir, title, risk, technique, params, utility):
    out_dir.mkdir(exist_ok=True)
    filename = f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = out_dir / filename

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, title, ln=True)

    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(0, 8, f"Generated at: {datetime.now()}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Risk Assessment", ln=True)

    pdf.set_font("Arial", size=12)
    for k, v in risk.items():
        pdf.cell(0, 7, f"{k}: {v}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 8, f"Technique used: {technique}", ln=True)
    pdf.cell(0, 8, f"Utility Score: {utility}", ln=True)

    pdf.output(str(path))
    return path
