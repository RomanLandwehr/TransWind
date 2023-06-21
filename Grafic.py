import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

#####Lege die Schrittweite fest
step = 1000
#####Lege die Leistung fest, bis zu der die NAPs betrachtet werden sollen
maximum = 1000000

#####Lese das Dataframe ein. Die Datei AuslastungNAPs.xlsx wir durch 
#####Ausführung von main.py erstellt
df = pd.read_excel('AuslastungNAPs.xlsx')
df = df.set_index('MastrNummer')
#####Lösche alle unvollständingen (Nettoengpassleistung = 0) NAPs
df = df.drop(df[df['Nettoengpassleistung'] == 0].index)
#####Betrachte nur NAps mit Auslastung > 1
df = df.drop(df[df['Auslastung'] <= 1].index)
df = df[~df.index.duplicated(keep='first')]


y = 0
Key = []
Count = []
iterations = int(maximum/step)

#####Zähle die entsprechenden NAPs gemaess Gruppierung
for i in tqdm(range(iterations)):
    count = 0
    x = y
    y = x + step
    for MastrNummer in df.index:
        Nettoengpassleistung = df.loc[MastrNummer]['Nettoengpassleistung']
        if Nettoengpassleistung > x:
            if Nettoengpassleistung <= y:
                df = df.drop(MastrNummer)
                count += 1   
    if count > 0:
        key = str(x) + ' - ' + str(y)
        Key.append(key)
        Count.append(count)

#####Erstelle DataFrame
df2 = pd.DataFrame([Key,Count]).transpose()  
df2.columns= ['Netzanschlusskapazität','Anzahl']

#####Erstelle Diagramme
ax = df2.plot.bar(x=0,y='Anzahl')
ax.set_xticks(df2.index[::2])
plt.show()
