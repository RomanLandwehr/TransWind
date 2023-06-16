import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm


def Column(tree):
    New_Columns = []
    tree = ET.parse(tree)
    root = tree.getroot()
    for child in tqdm(root):
        Column = []
        for subchild in child:
            tag = subchild.tag
            Column.append(tag)
        if len(Column) > len(New_Columns):
            New_Columns = Column
    return New_Columns


def ReadXML(tree):
    Data = [[], []]
    tree = ET.parse(tree)
    root = tree.getroot()
    for child in root:
        Tag = []
        Text = []
        for subchild in child:
            tag = subchild.tag
            text = subchild.text
            Tag.append(tag)
            Text.append(text)
        Data[0].append(Tag)
        Data[1].append(Text)
    return Data


def Dataframe(Data, Column):
    for dataset in range(len(Data[0])):
        Key = []
        D_C = Data[0][dataset]
        D_D = Data[1][dataset]
        for j in range(len(D_C)):
            boolean = 0
            for i in range(len(Column)):
                if D_C[j] == Column[i]:
                    boolean = 1
                    Key.append(i)
            if boolean == 0:
                Key.append("Fail")
        Data_x = []
        for i in range(len(Column)):
            Data_x.append("Fail")
        for y in range(len(D_D)):
            K = Key[y]
            if K == "Fail":
                K = y
            Data_x[K] = D_D[y]
        Data[0][dataset] = Column
        Data[1][dataset] = Data_x
    return Data


########################################
Lokationen = "Lokationen_"
Columns = Column("Lokationen_1.xml")
Data_Lokationen = [[], []]
for i in tqdm(range(50)):
    try:
        x = Lokationen + str(i + 1) + ".xml"
        Data = ReadXML(x)
        Data_Lokationen[0] += Data[0]
        Data_Lokationen[1] += Data[1]
    except FileNotFoundError:
        break
Lokationen = Dataframe(Data_Lokationen, Columns)
##########
for i in range(len(Lokationen[1])):
    New = []
    x = []
    WE = Lokationen[1][i][4]
    j = int(len(WE) / 17)
    for k in range(j):
        if len(WE) > 17 * k:
            x.append(WE[17 * (k + 1) : 15 * (k + 2) + 2 * k])
    for l in range(len(x)):
        for l in range(6):
            New.append(Lokationen[1][i][l])
    if len(x) > 0:
        Lokationen[1].append(New)

########################################
NAP = "Netzanschlusspunkte_"
Columns = Column("Netzanschlusspunkte_1.xml")
Data_NAP = [[], []]
for i in tqdm(range(50)):
    try:
        x = NAP + str(i + 1) + ".xml"
        Data = ReadXML(x)
        Data_NAP[0] += Data[0]
        Data_NAP[1] += Data[1]
    except FileNotFoundError:
        break
NAP = Dataframe(Data_NAP, Columns)
########################################
Columns = Column("EinheitenWind.xml")
Data_Wind = [[], []]
Data = ReadXML("EinheitenWind.xml")
Data_Wind[0] += Data[0]
Data_Wind[1] += Data[1]
Wind = Dataframe(Data_Wind, Columns)
########################################

for i in tqdm(range(len(Wind[1]))):
    SEE = Wind[1][i][0]
    SEE_P = Wind[1][i][31]
    for j in range(len(Lokationen[1])):
        if SEE == Lokationen[1][j][4]:
            NAP = Lokationen[1][j][5]
            print(NAP)
            break

NAP = "SAN947309701293"
for i in range(len(Lokationen[1])):
    if Lokationen[1][i][5] == NAP:
        SEE = Lokationen[1][i][4]
        print(SEE)

for i in range(len(NAP)):
    if NAP[1][i][99] == NAP:
        NAP_P = NAP[1][i][99]
        print(NAP_P)

# test
