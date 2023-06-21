import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm

def ReadXML(tree, Object):
    Tag = Object.Tag
    ####################
    ColumnA = []
    ColumnB = []
    ColumnC = []
    ####################
    tree = ET.parse(tree)
    root = tree.getroot()
    for child in root:
        for subchild in child:
            tag = subchild.tag
            text = subchild.text 
            if tag == Tag[0]:
                ColumnA.append(text)
            if tag == Tag[1]:
                ColumnB.append(text)
            if tag == Tag[2]:
                ColumnC.append(text)
            if tag == 'Netzanschlusskapazitaet':
                print(text)
                ColumnC.append(text)
        if len(ColumnA) > len(ColumnB):
            ColumnB.append('None')
        if len(ColumnA) > len(ColumnC):
            ColumnC.append('None')
    return ColumnA, ColumnB, ColumnC

def Create(Object):
    df = pd.DataFrame()
    Objectname = Object.Name
    Tag = Object.Tag
    for i in tqdm(range(50)):
        Filename = Objectname + '_' + str(i+1) + '.xml'
        try:
            File = ReadXML(Filename, Object)
        except FileNotFoundError:
            if Objectname == 'EinheitenWind.xml':
                File = ReadXML(Objectname, Object)
            if Objectname == 'EinheitenBiomasse.xml':
                File = ReadXML(Objectname, Object)
            if Objectname == 'EinheitenGasErzeuger.xml':
                File = ReadXML(Objectname, Object)
            if Objectname == 'EinheitenGeothermieGrubengasDruckentspannung.xml':
                File = ReadXML(Objectname, Object)
            if Objectname == 'EinheitenVerbrennung.xml':
                File = ReadXML(Objectname, Object)
            if Objectname == 'EinheitenWasser.xml':
                File = ReadXML(Objectname, Object)
            if Objectname == 'EinheitenGasSpeicher.xml':
                File = ReadXML(Objectname, Object)
            df_i = pd.DataFrame(File).transpose()
            df_i.columns = [Tag[0],Tag[1],Tag[2]]
            df_i = df_i.drop(df_i[df_i[Tag[1]].str.contains('None')].index)
            try:
                df_i = df_i.drop(df_i[df_i[Tag[2]].str.contains('None')].index)
            except ValueError:
                pass
            df = pd.concat([df, df_i], ignore_index=True)
            return df
        df_i = pd.DataFrame(File).transpose()
        df_i.columns = [Tag[0],Tag[1],Tag[2]]
        df_i = df_i.drop(df_i[df_i[Tag[1]].str.contains('None')].index)
        df = pd.concat([df, df_i], ignore_index=True)
    return df