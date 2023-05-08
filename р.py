import pandas as pd
import datetime
reve = pd.read_excel('./Приложение Банка ДОМ.xlsx')
temp_num =0
data=[]
for i in reve['Unnamed: 1']:
    if i=="Какое у вас устройство?":
        break
    else:
        temp=True
        for znad in ['зна','понятия','впервые',"в первый",'информации','предл']:
            if str(i).lower().count(znad) > 0:
                temp_num += 1
                break
            else:
                if temp:
                    data.append(i)
                    temp=False
print(temp_num)
df = pd.DataFrame(data={"коммы":data})
print (df)
df.to_excel('dict1.xlsx')
