import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import tempfile

def erstelle_pdf(df, pdf_pfad):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Monatlicher Budgetreport", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)

    gesamt_einnahmen = df[df['Betrag'] > 0]['Betrag'].sum()
    gesamt_ausgaben = df[df['Betrag'] < 0]['Betrag'].sum()
    saldo = gesamt_einnahmen + gesamt_ausgaben

    pdf.cell(0, 10, f"Gesamte Einnahmen: CHF {gesamt_einnahmen:,.2f}", ln=True)
    pdf.cell(0, 10, f"Gesamte Ausgaben: CHF {gesamt_ausgaben:,.2f}", ln=True)
    pdf.cell(0, 10, f"Saldo: CHF {saldo:,.2f}", ln=True)
    pdf.ln(5)

    # Gruppieren
    einnahmen = df[df['Betrag'] > 0].groupby('Kategorie')['Betrag'].sum()
    ausgaben = df[df['Betrag'] < 0].groupby('Kategorie')['Betrag'].sum()

    with tempfile.TemporaryDirectory() as tmpdir:
        pfad_einnahmen = os.path.join(tmpdir, "einnahmen.png")
        pfad_ausgaben = os.path.join(tmpdir, "ausgaben.png")

        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        if not einnahmen.empty:
            axs[0].pie(einnahmen, labels=einnahmen.index, autopct='%1.1f%%', startangle=140)
            axs[0].set_title("Einnahmen")
        if not ausgaben.empty:
            axs[1].pie(-ausgaben, labels=ausgaben.index, autopct='%1.1f%%', startangle=140)
            axs[1].set_title("Ausgaben")

        plt.tight_layout()
        chart_path = os.path.join(tmpdir, "charts.png")
        fig.savefig(chart_path)
        plt.close(fig)

        pdf.image(chart_path, x=10, w=190)

    # Detaillierte Tabelle
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Details:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.ln(4)

    for index, row in df.iterrows():
        pdf.cell(0, 8, f"{row['Datum'].strftime('%d.%m.%Y')} | {row['Kategorie']}: CHF {row['Betrag']:.2f}", ln=True)

    pdf.output(pdf_pfad)
