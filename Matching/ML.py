import pandas as pd
import numpy as np
import MaStR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

df = MaStR.df
df = df.dropna()



################
X_n = df[['Bruttoleistung der Einheit',
        'Rotordurchmesser der Windenergieanlage',
        'Nabenhöhe der Windenergieanlage',
        'Lage der Einheit']]  # Numerische Features

X_c = df[['Hersteller der Windenergieanlage']]  # Kategoriale Features
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(X_c)
X = np.hstack((X_n, X_encoded.toarray()))

y = df['Typenbezeichnung']  # Kategoriale Ausprägungsvariable

def MachineLearning(j):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, classification_report
    import joblib
    
    # Aufteilung der Daten
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.11, random_state=42)
    
    # Klassifikationsmodell (z.B. Random Forest) initialisieren und trainieren    
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    # Vorhersagen auf dem Testset
    predictions = model.predict(X_test)
    df = pd.DataFrame(predictions,y_test)
    
    # Auswertung des Modells    
    
    accuracy = round(accuracy_score(y_test, predictions),3)
    report = classification_report(y_test, predictions, zero_division=1)
    joblib.dump(model, 'trainiertes_modell.pkl')
    print(j, f"Accuracy: {accuracy}")
    return df


predictions = MachineLearning(0)