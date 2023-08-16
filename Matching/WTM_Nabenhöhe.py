import pandas as pd
import re
from tqdm import tqdm

def Load():
    df_new = pd.read_excel("WTM_with_UBA-clusters_modified.xlsx")
    df_new.columns = df_new.iloc[0]
    df_new = df_new.drop(0)
    df_new = df_new.reset_index()
    df_new = df_new[['Model',
                     'Nennleistung in kW',
                     'Durchmesser in m',
                     'Nabenhöhe in m',
                     'Offshore',
                     'Hersteller']]
    df_new.rename(columns={'Nennleistung in kW': 'Bruttoleistung der Einheit'}, inplace=True)
    df_new.rename(columns={'Durchmesser in m': 'Rotordurchmesser der Windenergieanlage'}, inplace=True)
    df_new = df_new.dropna()
    df_new = df_new.reset_index()
    df_new = df_new.drop('index', axis=1)
    return df_new

def Nabenhöhe(df_new):
    df_new.fillna(0, inplace=True)   
    Nabenhöhe = df_new['Nabenhöhe in m'].tolist()    
    df = pd.DataFrame()
   
    for i in tqdm(range(len(df_new))):
        input_string = df_new['Nabenhöhe in m'][i]
        numbers = re.findall(r'\b\d+\b', input_string)    
        number_list = [int(number) for number in numbers] 
        for number in number_list:
            df_i = df_new.iloc[i]
            df_i = df_i.to_frame(name=(i))
            df_i = df_i.transpose()
            df_i['Nabenhöhe in m'][i] = number
            df = pd.concat([df,df_i])
    df = df.reset_index()
    df = df.drop('index', axis=1)
    return df

def Hersteller(df):
    data_path = 'MaStR_Stromerzeuger_Wind_in Betrieb_Inbetriebnahmedatum bis 2010.csv'
    df_Hersteller = pd.read_csv(data_path, sep=';', decimal=',', dayfirst=True)
    df_Hersteller = df_Hersteller['Hersteller der Windenergieanlage'].dropna()
    akzeptierte_werte = df_Hersteller.values.tolist()
    akzeptierte_werte = list(set(list(akzeptierte_werte)))

    for i in range(len(df)):
        hersteller = df['Hersteller'][i]
        for j in akzeptierte_werte:
            if hersteller.upper() in j.upper():
                df['Hersteller'][i] = j
                         
    df = df[df['Hersteller'].isin(akzeptierte_werte)]
    df.rename(columns={'Hersteller': 'Hersteller der Windenergieanlage'}, inplace=True)
    return df

def Offshore(df):
    for i in range(len(df)):
        if df['Offshore'][i] == 'Ja':
            df['Offshore'][i] = 0
        else:
            df['Offshore'][i] = 1
    df['Offshore'] = df['Offshore'].astype(int)
    df.rename(columns={'Offshore': 'Lage der Einheit'}, inplace=True)
    df['Bruttoleistung der Einheit'] = df['Bruttoleistung der Einheit'].astype(int)
    df['Rotordurchmesser der Windenergieanlage'] = df['Rotordurchmesser der Windenergieanlage'].astype(int)
    df.rename(columns={'Nabenhöhe in m': 'Nabenhöhe der Windenergieanlage'}, inplace=True)
    df['Nabenhöhe der Windenergieanlage'] = df['Nabenhöhe der Windenergieanlage'].astype(int)
    return df
            
def Setup():
    df = Load()
    df = Nabenhöhe(df)
    df = Offshore(df)
    df = Hersteller(df)
    df = df.dropna()
    return df
    
a = Setup()
