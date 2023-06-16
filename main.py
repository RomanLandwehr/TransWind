import Object as O
import Create as C
import pickle
from tqdm import tqdm

def Setup():
    Lokationen = O.Object('Lokationen', 
                          ['MastrNummer','NetzanschlusspunkteMaStRNummern','VerknuepfteEinheitenMaStRNummern'])
    
    NAP = O.Object('Netzanschlusspunkte', 
                  ['NetzanschlusspunktMastrNummer','LokationMaStRNummer','Nettoengpassleistung'])
    
    WEA = O.Object('EinheitenWind.xml', 
                  ['EinheitMastrNummer','LokationMaStRNummer','Nettonennleistung'])
    
    Solar = O.Object('EinheitenSolar', 
                  ['EinheitMastrNummer','LokationMaStRNummer','Nettonennleistung'])
    
    Lokationen = C.Create(Lokationen)
    NAP = C.Create(NAP)
    WEA = C.Create(WEA)
    Solar = C.Create(Solar)
    
    pickle.dump(Lokationen, open('Lokationen', 'wb'))
    pickle.dump(NAP, open('Netzanschlusspunkte', 'wb'))
    pickle.dump(WEA, open('EinheitenWind', 'wb'))
    pickle.dump(Solar, open('EinheitenSolar', 'wb'))

##################################################
try:
    Lokationen = pickle.load(open('Lokationen', 'rb'))
    NAP = pickle.load(open('Netzanschlusspunkte', 'rb'))
    WEA = pickle.load(open('EinheitenWind', 'rb'))
    Solar = pickle.load(open('EinheitenSolar', 'rb'))
except FileNotFoundError:
    Setup()
    Lokationen = pickle.load(open('Lokationen', 'rb'))
    NAP = pickle.load(open('Netzanschlusspunkte', 'rb'))
    WEA = pickle.load(open('EinheitenWind', 'rb'))
    Solar = pickle.load(open('EinheitenSolar', 'rb'))
##################################################
WEA_Key = WEA['EinheitMastrNummer'].tolist()
WEA_Lokation = WEA['LokationMaStRNummer'].tolist()
##################################################
NAP = NAP[NAP['LokationMaStRNummer'].isin(WEA_Lokation)]
NAP_Key = NAP['NetzanschlusspunktMastrNummer'].tolist()
NAP_Lokation = NAP['LokationMaStRNummer'].tolist()
##################################################
Solar = Solar[Solar['LokationMaStRNummer'].isin(WEA_Lokation)]
Solar_Key = Solar['EinheitMastrNummer'].tolist()
Solar_Lokation = Solar['LokationMaStRNummer'].tolist()
##################################################
Lokationen = Lokationen[Lokationen['MastrNummer'].isin(WEA_Lokation)]
Lokationen_Key = Lokationen['MastrNummer'].tolist()
Lokationen_NAP = Lokationen['NetzanschlusspunkteMaStRNummern'].tolist()
Lokationen_Sources = Lokationen['VerknuepfteEinheitenMaStRNummern'].tolist()
##################################################
Lokationen['Nettoengpassleistung'] = 0
Lokationen['Nettonennleistung'] = 0
##################################################

for Anlage in tqdm(WEA['EinheitMastrNummer']):
    for Sources in Lokationen['VerknuepfteEinheitenMaStRNummern']:
        if Anlage in Sources:
            i = WEA.index[WEA['EinheitMastrNummer'] == Anlage][0]
            Leistung = float(WEA.loc[i]['Nettonennleistung'])
            j = Lokationen.index[Lokationen['VerknuepfteEinheitenMaStRNummern'] == Sources][0]
            Lokationen.loc[Lokationen.index == j, 'Nettonennleistung'] += Leistung
            break
        
for Anlage in tqdm(Solar['EinheitMastrNummer']):
    for Sources in Lokationen['VerknuepfteEinheitenMaStRNummern']:
        if Anlage in Sources:
            i = Solar.index[Solar['EinheitMastrNummer'] == Anlage][0]
            Leistung = float(Solar.loc[i]['Nettonennleistung'])
            j = Lokationen.index[Lokationen['VerknuepfteEinheitenMaStRNummern'] == Sources][0]
            Lokationen.loc[Lokationen.index == j, 'Nettonennleistung'] += Leistung
            break
        
for NAPs in tqdm(NAP['NetzanschlusspunktMastrNummer']):
    for Key in Lokationen['NetzanschlusspunkteMaStRNummern']:
        if NAPs in Key:
            i = NAP.index[NAP['NetzanschlusspunktMastrNummer'] == NAPs][0]
            try:
                Leistung = float(NAP.loc[i]['Nettoengpassleistung'])
            except ValueError:
                Leistung = 0
            j = Lokationen.index[Lokationen['NetzanschlusspunkteMaStRNummern'] == Key][0]
            Lokationen.loc[Lokationen.index == j, 'Nettoengpassleistung'] += Leistung
            break
        
Lokationen['Auslastung'] = Lokationen['Nettonennleistung'] / Lokationen['Nettoengpassleistung']

Lokationen.to_excel('AuslastungNAPs.xlsx', index=False)