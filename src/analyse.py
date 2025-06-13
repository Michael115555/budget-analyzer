def analysiere_budget(df):
    einnahmen = df[df['Betrag'] > 0]['Betrag'].sum()
    ausgaben = df[df['Betrag'] < 0]['Betrag'].sum()
    saldo = einnahmen + ausgaben
    return {
        'Einnahmen': einnahmen,
        'Ausgaben': ausgaben,
        'Saldo': saldo
    }

def gruppiere_nach_monat(df):
    df['JahrMonat'] = df['Datum'].dt.to_period('M').astype(str)
    monate = df['JahrMonat'].unique()
    return {monat: df[df['JahrMonat'] == monat] for monat in monate}

def gruppiere_kategorien(df):
    # Einnahmen und Ausgaben nach Kategorie summieren
    einnahmen = df[df['Betrag'] > 0].groupby('Kategorie')['Betrag'].sum()
    ausgaben = df[df['Betrag'] < 0].groupby('Kategorie')['Betrag'].sum().abs()
    return einnahmen, ausgaben
