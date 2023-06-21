import Object as O
import Create as C
import pickle   #Modul um Listen lokal als Dateien zu speicher -> Zeitersparnis
from tqdm import tqdm     #Modul um den Fortschrittsbalken anzuzeigen

def Setup():
    ##### Definitionen
    Lokationen = O.Object('Lokationen', 
                          ['MastrNummer','NetzanschlusspunkteMaStRNummern','VerknuepfteEinheitenMaStRNummern'])
    
    NAP = O.Object('Netzanschlusspunkte', 
                  ['NetzanschlusspunktMastrNummer','LokationMaStRNummer','Nettoengpassleistung'])
    
    #####Erzeuger
    WEA = O.Object('EinheitenWind.xml', 
                  ['EinheitMastrNummer','LokationMaStRNummer','Nettonennleistung'])
    
    Solar = O.Object('EinheitenSolar', 
                  ['EinheitMastrNummer','LokationMaStRNummer','Nettonennleistung'])
    
    Biomasse = O.Object('EinheitenBiomasse.xml', 
                  ['EinheitMastrNummer','LokationMaStRNummer','Nettonennleistung'])
    
    GasErzeuger = O.Object('EinheitenGasErzeuger.xml', 
                  ['EinheitMastrNummer','LokationMaStRNummer','Erzeugungsleistung'])
    
    Geothermie = O.Object('EinheitenGeothermieGrubengasDruckentspannung.xml', 
                  ['EinheitMastrNummer','LokationMaStRNummer','Nettonennleistung'])
    
    Verbrennung = O.Object('EinheitenVerbrennung.xml', 
                  ['EinheitMastrNummer','LokationMaStRNummer','Nettonennleistung'])
    
    Wasser = O.Object('EinheitenWasser.xml', 
                  ['EinheitMastrNummer','LokationMaStRNummer','Nettonennleistung'])
    ####Speicher
    GasSpeicher = O.Object('EinheitenGasSpeicher.xml', 
                  ['EinheitMastrNummer','LokationMaStRNummer','MaximaleAusspeicherleistung'])
    StromSpeicher = O.Object('EinheitenStromSpeicher', 
                  ['EinheitMastrNummer','LokationMaStRNummer','Nettonennleistung'])
    
    ##### Objekte Erzeugen
    Lokationen = C.Create(Lokationen)
    NAP = C.Create(NAP)
    WEA = C.Create(WEA)
    Solar = C.Create(Solar)
    Biomasse = C.Create(Biomasse)
    GasErzeuger = C.Create(GasErzeuger)
    Geothermie = C.Create(Geothermie)
    Verbrennung = C.Create(Verbrennung)
    Wasser = C.Create(Wasser)
    GasSpeicher = C.Create(GasSpeicher)
    StromSpeicher = C.Create(StromSpeicher)
    
    #Speichern
    pickle.dump(Lokationen, open('Lokationen', 'wb'))
    pickle.dump(NAP, open('Netzanschlusspunkte', 'wb'))
    pickle.dump(WEA, open('EinheitenWind', 'wb'))
    pickle.dump(Solar, open('EinheitenSolar', 'wb'))
    pickle.dump(Biomasse, open('EinheitenBiomasse', 'wb'))
    pickle.dump(GasErzeuger, open('EinheitenGasErzeuger', 'wb'))
    pickle.dump(Geothermie, open('EinheitenGeothermie', 'wb'))
    pickle.dump(Verbrennung, open('EinheitenVerbrennung', 'wb'))
    pickle.dump(Wasser, open('EinheitenWasser', 'wb'))
    pickle.dump(GasSpeicher, open('EinheitenGasSpeicher', 'wb'))
    pickle.dump(StromSpeicher, open('EinheitenStromspeicher', 'wb'))

##### Dateien laden
try:
    #####Zeitersparnis durch gespeicherte Dateien
    Lokationen = pickle.load(open('Lokationen', 'rb'))
    NAP = pickle.load(open('Netzanschlusspunkte', 'rb'))
    WEA = pickle.load(open('EinheitenWind', 'rb'))
    Solar = pickle.load(open('EinheitenSolar', 'rb'))
    Biomasse = pickle.load(open('EinheitenBiomasse', 'rb'))
    GasErzeuger = pickle.load(open('EinheitenGasErzeuger', 'rb'))
    Geothermie = pickle.load(open('EinheitenGeothermie', 'rb'))
    Verbrennung = pickle.load(open('EinheitenVerbrennung', 'rb'))
    Wasser = pickle.load(open('EinheitenWasser', 'rb'))
    GasSpeicher = pickle.load(open('EinheitenGasSpeicher', 'rb'))
    StromSpeicher = pickle.load(open('EinheitenStromspeicher', 'rb'))
except FileNotFoundError:
    Setup()
    print("Dateien erstellt. Skript erneut ausführen!")
    
##################################################
WEA_Key = WEA['EinheitMastrNummer'].tolist()
WEA_Lokation = WEA['LokationMaStRNummer'].tolist()
##################################################
NAP = NAP[NAP['LokationMaStRNummer'].isin(WEA_Lokation)]
Lokationen = Lokationen[Lokationen['MastrNummer'].isin(WEA_Lokation)]
#####Nur Quellen verwenden die zusammen mit WEA einspeisen
Solar = Solar[Solar['LokationMaStRNummer'].isin(WEA_Lokation)]
GasErzeuger = GasErzeuger[GasErzeuger['LokationMaStRNummer'].isin(WEA_Lokation)]
Biomasse = Biomasse[Biomasse['LokationMaStRNummer'].isin(WEA_Lokation)]
Geothermie = Geothermie[Geothermie['LokationMaStRNummer'].isin(WEA_Lokation)]
Verbrennung = Verbrennung[Verbrennung['LokationMaStRNummer'].isin(WEA_Lokation)]
Wasser = Wasser[Wasser['LokationMaStRNummer'].isin(WEA_Lokation)]
#####Nur Speicher verwenden die zusammen mit WEA einspeisen
GasSpeicher = GasSpeicher[GasSpeicher['LokationMaStRNummer'].isin(WEA_Lokation)]
StromSpeicher = StromSpeicher[StromSpeicher['LokationMaStRNummer'].isin(WEA_Lokation)]
##### Spalten Nettoengpassleistung und Nettonennleistung initialisieren
Lokationen['Nettoengpassleistung'] = 0
Lokationen['Nettonennleistung'] = 0

#####Erstelle Liste aller Erzeuger
Sources = [WEA,Solar,Biomasse,Geothermie,Verbrennung,Wasser]
Storages = [StromSpeicher] #Einträge GasSpeicher = 0, daher weggelassen

#####Summiere die Nettonennleistung der Erzeuger je Lokation (NAP)
for source in Sources:
    for Anlage in tqdm(source['EinheitMastrNummer']):
        for Einheiten in Lokationen['VerknuepfteEinheitenMaStRNummern']:
            if Anlage in Einheiten:
                i = source[source['EinheitMastrNummer'] == Anlage].index[0]
                Leistung = float(source.loc[i]['Nettonennleistung'])
                j = Lokationen[Lokationen['VerknuepfteEinheitenMaStRNummern'] == Einheiten].index[0]
                Lokationen.loc[Lokationen.index == j, 'Nettonennleistung'] += Leistung
                break
            
#####Summiere die Nettonennleistung der Speicher je Lokation (NAP)
for storage in Storages:
    for Anlage in tqdm(storage['EinheitMastrNummer']):
        for Einheiten in Lokationen['VerknuepfteEinheitenMaStRNummern']:
            if Anlage in Einheiten:
                i = storage[storage['EinheitMastrNummer'] == Anlage].index[0]
                Leistung = float(storage.loc[i]['Nettonennleistung'])
                j = Lokationen[Lokationen['VerknuepfteEinheitenMaStRNummern'] == Einheiten].index[0]
                Lokationen.loc[Lokationen.index == j, 'Nettonennleistung'] += Leistung
                break

#####Summiere die Nettoengpassleistung der NAPs je Lokation (NAP)
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

##### Füge Spalte Auslastung hinzu        
Lokationen['Auslastung'] = Lokationen['Nettonennleistung'] / Lokationen['Nettoengpassleistung']

#####Speichere die Ergebnisse als Excel für Grafic.py
Lokationen.to_excel('AuslastungNAPs.xlsx', index=False)


