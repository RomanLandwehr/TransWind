import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

df = pd.read_excel('AuslastungNAPs.xlsx')
df = df.set_index('MastrNummer')
df = df.drop(df[df['Nettoengpassleistung'] == 0].index)
df = df[~df.index.duplicated(keep='first')]


y = 0
Key = []
Count = []

for i in tqdm(range(20)):
    count = 0
    x = y
    y = x + 500
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

df2 = pd.DataFrame([Key,Count]).transpose()  
df2.columns= ['Nettoengpassleistung','Anzahl']
#df2 = df2.set_index(0)    


ax = df2.plot.bar(x=0,y='Anzahl')
ax.set_xticks(df2.index[::2])
plt.show()
