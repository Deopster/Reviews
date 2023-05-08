import pandas as pd
import datetime
from components import filelist
def scan(got):
    spis = filelist.getfile()
    df = pd.DataFrame(columns=spis.columns)
    schet=0
    for i, row in spis.iterrows():
            #print(schet)
            if got[0][1] != "Содержит":
                #print(operation[0])
                value = spis[got[0][0]].iloc[schet]
                #print(value)
                #print(value)
                znak=got[0][1]
                if znak== "=":
                    znak="=="
                if eval("{} {} {}".format(value,znak,got[0][2])):
                    # print("\n")
                    # print(value)
                    # print(spis[got[0][0]].iloc[schet])
                    # print("\n")
                    df = df._append(spis.iloc[schet])
            else:
                if value.lower().count(str(got[0][2])) > 0:
                    pass
            schet += 1
    #df = pd.DataFrame(data={"коммы":data})
    #print (df)
    df.to_excel(f'temp.xlsx')
#scan([["Оценка", '<=', '2']])