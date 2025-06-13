import pandas as pd

def lade_csv(pfad):
    try:
        df = pd.read_csv(pfad, sep=';', parse_dates=['Datum'])
        return df
    except Exception as e:
        raise ValueError(f"Fehler beim Laden der CSV: {e}")
