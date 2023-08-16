import pandas as pd
import numpy as np
import WTM_Nabenhöhe as WTMN
import joblib
from sklearn.preprocessing import OneHotEncoder
from tqdm import tqdm
import random
import MaStR as MaStR


#####

df = WTMN.Setup()

X_n = df[['Bruttoleistung der Einheit',
              'Rotordurchmesser der Windenergieanlage',
              'Nabenhöhe der Windenergieanlage',
              'Lage der Einheit'
              ]]  # Numerische Features
X_c = df[['Hersteller der Windenergieanlage']]   # Kategoriale Features

encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(X_c)
X = np.hstack((X_n, X_encoded.toarray()))

# Annahme: Das trainierte Modell wurde als "trainiertes_modell.pkl" gespeichert
trained_model = joblib.load("trainiertes_modell.pkl")

# Annahme: df_new sind die neuen Daten, die du kategorisieren möchtest
# Achte darauf, dass diese Daten die gleichen Vorverarbeitungsschritte wie die Trainingsdaten durchlaufen

# Mache Vorhersagen für die neuen Daten
predictions = trained_model.predict(X)
df['Predictions'] = predictions

# Die Variable "predictions" enthält nun die vorhergesagten Kategorien für die neuen Daten

model = df['Predictions'].drop_duplicates().to_list()
df.set_index('Predictions', inplace=True)

df_MaStR = MaStR.df
df_MaStR = df_MaStR.dropna()
df_MaStR = df_MaStR.reset_index()
df_MaStR = df_MaStR.drop('index', axis=1)

df['Trenn'] = '-'
df['Bruttoleistung der Einheit 2'] = '-'
df['Rotordurchmesser der Windenergieanlage 2'] = '-'
df['Nabenhöhe der Windenergieanlage 2'] = '-'
df['Lage 2'] = '-'
df['Match'] = 0

for i in tqdm(range(len(df_MaStR))):
    Typ = df_MaStR['Typenbezeichnung'][i]
    Leistung = df_MaStR['Bruttoleistung der Einheit'][i]
    Durchmesser = df_MaStR['Rotordurchmesser der Windenergieanlage'][i]
    Höhe = df_MaStR['Nabenhöhe der Windenergieanlage'][i]
    Lage = df_MaStR['Lage der Einheit'][i]
    for j in range(len(df)):
        Model = df.index[j]
        if Typ == Model:
            df['Bruttoleistung der Einheit 2'][j] = Leistung
            df['Rotordurchmesser der Windenergieanlage 2'][j] = Durchmesser
            df['Nabenhöhe der Windenergieanlage 2'][j] = Höhe
            df['Lage 2'][j] = Lage
            if Model in df['Model'][j]:
                df['Match'][j] = 1                
            continue
        
df['Rotordurchmesser der Windenergieanlage 2'] = df['Rotordurchmesser der Windenergieanlage 2'].astype(int)
df['Bruttoleistung der Einheit 2'] = df['Bruttoleistung der Einheit 2'].astype(int)
df['Nabenhöhe der Windenergieanlage 2'] = df['Nabenhöhe der Windenergieanlage 2'].astype(int)
df['Lage 2'] = df['Lage 2'].astype(int)
 
Result = pd.DataFrame()   
for m in model:
    b = df.loc[m]
    try:
        z = b.shape[1]
    except IndexError:
        b = pd.DataFrame(b).transpose()
    b['Similartiy'] = '-'
    x = b[['Model',
           'Bruttoleistung der Einheit',
          'Rotordurchmesser der Windenergieanlage',
          'Nabenhöhe der Windenergieanlage']]
    y = b[[
           'Bruttoleistung der Einheit 2',
          'Rotordurchmesser der Windenergieanlage 2',
          'Nabenhöhe der Windenergieanlage 2']]
    index = b.index[0]
    y['Model'] = index
    min_distance = 9e9
    for i in range(len(b)):
            x1 = x['Bruttoleistung der Einheit'][i]
            y1 = y['Bruttoleistung der Einheit 2'][i]
            distance1 = np.sqrt(np.sum((x1 - y1)**2))/y1
            
            x2 = x['Rotordurchmesser der Windenergieanlage'][i]
            y2 = y['Rotordurchmesser der Windenergieanlage 2'][i]
            distance2 = np.sqrt(np.sum((x2 - y2)**2))/y2
            
            x3 = x['Nabenhöhe der Windenergieanlage'][i]
            y3 = y['Nabenhöhe der Windenergieanlage 2'][i]
            distance3 = np.sqrt(np.sum((x3 - y3)**2))/y3
            
            x4 = x['Model'][i] 
            y4 = y['Model'][i]
            x4 = set(x4)
            y4 = set(y4)
            intersection = len(x4.intersection(y4))
            union = len(x4) + len(y4) - intersection
            distance4 = round((1-intersection / union),4)
            distance = round(100*(distance1+distance2+distance3+distance4),2)
            b['Similartiy'][i] = int(distance)
            if distance < min_distance:
                df_i = pd.DataFrame(b.iloc[i]).transpose()
                min_distance = distance
            print(distance)
    Result = pd.concat([Result, df_i])
        
Result.to_excel('Matching.xlsx')   

     

