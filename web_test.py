import pandas as pd
tag_data = pd.read_excel('./input/kat.xlsx', skiprows=[0])
head = pd.read_excel('./input/kat.xlsx', nrows = 1)
reve = pd.read_excel('./static/results.xlsx')
data = pd.DataFrame(columns=['Отзыв','тег','категория','подкатегория'])
#print(data.keys())
#print(head.keys())
head_list=[]
temp_list=[]
rez={}
summ=-1
for index,i in enumerate(head):
    if "Unnamed:" not in tag_data.keys()[index]:
        temp_list.append(tag_data.keys()[index])
    else:
        rez[head_list[summ]]=temp_list
        temp_list=[]
    if "Unnamed:" not in i:
        head_list.append(i)
        summ+=1
print(rez)
perc=1
tag_data.fillna('', inplace=True)
all_data = set()
for columns in ['Отзыв']:
    for znach in reve[columns]:
        for column_name in tag_data.columns:
            for column_data in tag_data[f'{column_name}']:
                #print(column_name)
                if column_data != '':
                    temp_num=0
                    for tag in column_data.split():
                        if znach.lower().count(tag) > 0:
                            temp_num+=1
                    if temp_num / len(column_data.split()) >=perc:
                        for key_name in rez.keys():
                            if column_name in rez[key_name]:
                                #print(column_name, rez[key_name])
                                fin_key=key_name
                                #print(key_name)
                        data=data.append({'Отзыв':znach,'тег':column_data,'категория':fin_key,'подкатегория':column_name}, ignore_index = True)
data.to_excel('rety.xlsx')
print(znach,'\n',column_data)








