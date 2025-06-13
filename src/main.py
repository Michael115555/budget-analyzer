import os
from csv_import import lade_csv
from pdf_export import erstelle_pdf
import pandas as pd

def main():
    csv_pfad = '../data/beispiel_budget.csv'
    report_ordner = '../reports'
    os.makedirs(report_ordner, exist_ok=True)

    df = lade_csv(csv_pfad)

    # Alle vorhandenen Monate im CSV extrahieren
    df['Monat'] = df['Datum'].dt.month
    vorhandene_monate = sorted(df['Monat'].unique())

    if not vorhandene_monate:
        print("Keine gültigen Daten im CSV.")
        return

    for monat in vorhandene_monate:
        df_monat = df[df['Monat'] == monat]

        if df_monat.empty:
            print(f"Keine Daten für Monat {monat}.")
            continue

        pdf_pfad = os.path.join(report_ordner, f'report_monat_{monat:02d}.pdf')
        erstelle_pdf(df_monat, pdf_pfad)
        print(f"✅ Report für Monat {monat} erstellt: {pdf_pfad}")

if __name__ == "__main__":
    main()


