import pandas as pd
import WTM_Nabenhöhe as WTMN

data_path = 'MaStR_Stromerzeuger_Wind_in Betrieb_Inbetriebnahmedatum bis 2010.csv'

df = pd.read_csv(data_path, sep=';', decimal=',', dayfirst=True)
df['neue_datumsvariable'] = pd.to_datetime(df['Inbetriebnahmedatum der Einheit'])
df['Jahr'] = df['neue_datumsvariable'].dt.year

df = df[['Typenbezeichnung',
         'Bruttoleistung der Einheit',
         'Rotordurchmesser der Windenergieanlage',
         'Nabenhöhe der Windenergieanlage',
         'Lage der Einheit',
         'Hersteller der Windenergieanlage']]

for i in range(len(df)):
    if df['Lage der Einheit'][i] == 'Windkraft an Land':
        df['Lage der Einheit'][i] = 1
    else:
        df['Lage der Einheit'][i] = 0

df['Lage der Einheit'] = df['Lage der Einheit'].astype(int)

Hersteller = WTMN.Setup()['Hersteller der Windenergieanlage'].drop_duplicates().to_list()

df = df[df['Hersteller der Windenergieanlage'].isin(Hersteller)]