from thefuzz import fuzz, process
import pandas as pd
import WTM_Nabenhöhe as WTMN
from tqdm import tqdm

data_path = 'MaStR_Stromerzeuger_Wind_in Betrieb_Inbetriebnahmedatum bis 2010.csv'
df_MSR = pd.read_csv(data_path, sep=';', decimal=',', dayfirst=True)
df_MSR = df_MSR[['Typenbezeichnung',
          'Bruttoleistung der Einheit',
          'Rotordurchmesser der Windenergieanlage',
          'Nabenhöhe der Windenergieanlage',
          'Hersteller der Windenergieanlage']]

df_MSR.rename(columns={'Typenbezeichnung': 'Model'}, inplace=True)
df_MSR.rename(columns={'Bruttoleistung der Einheit': 'Nennleistung in kW'}, inplace=True)
df_MSR.rename(columns={'Rotordurchmesser der Windenergieanlage': 'Durchmesser in m'}, inplace=True)
df_MSR.rename(columns={'Nabenhöhe der Windenergieanlage': 'Nabenhöhe in m'}, inplace=True)
df_MSR.rename(columns={'Hersteller der Windenergieanlage': 'Hersteller'}, inplace=True)
df_MSR = df_MSR.dropna()
df_MSR = df_MSR.reset_index()
df_MSR = df_MSR.drop('index', axis=1)
    
df_WTM = pd.read_excel("WTM_with_UBA-clusters_modified.xlsx")
df_WTM.columns = df_WTM.iloc[0]
df_WTM = df_WTM.drop(0)
df_WTM = df_WTM.reset_index()
df_WTM = df_WTM[['Model',
                 'Nennleistung in kW',
                 'Durchmesser in m',
                 'Nabenhöhe in m',
                 'Hersteller']]
df_WTM = WTMN.Nabenhöhe(df_WTM)
df_WTM['Nennleistung in kW'] = df_WTM['Nennleistung in kW'].astype(int)
df_WTM['Durchmesser in m'] = df_WTM['Durchmesser in m'].astype(int)
df_WTM['Nabenhöhe in m'] = df_WTM['Nabenhöhe in m'].astype(int)


df = pd.DataFrame()
for j in tqdm(range(len(df_MSR))):
    f_min = 9e9
    for i in range(len(df_WTM)):
    
        x1 = df_MSR['Model'][j]
        y1 = df_WTM['Model'][i]   
        fuzz1 = fuzz.ratio(x1,y1)
        
        x2 = df_MSR['Hersteller'][j]
        y2 = df_WTM['Hersteller'][i]   
        fuzz2 = fuzz.ratio(x2,y2)
    
        x3 = df_MSR['Nennleistung in kW'][j]
        y3 = df_WTM['Nennleistung in kW'][i]
        fuzz3 = round(100*(pow(x3-y3,2)/pow(x3,2)),0)
        
        x4 = df_MSR['Durchmesser in m'][j]
        y4 = df_WTM['Durchmesser in m'][i]
        fuzz4 = round(100*(pow(x4-y4,2)/pow(x4,2)),0)
        
        x5 = df_MSR['Nabenhöhe in m'][j]
        y5 = df_WTM['Nabenhöhe in m'][i]
        fuzz5 = round(100*(pow(x5-y5,2)/pow(x5,2)),0)
        
        f = fuzz1 + fuzz2 + fuzz3 + fuzz4 + fuzz5
        if f<f_min:
            df_i = pd.DataFrame([x1,y1,f]).transpose()
            f_min = f
    df = pd.concat([df,df_i])

