import pandas as pd
tag_data = pd.read_excel('./input/kat.xlsx', skiprows=[0])
head = pd.read_excel('./input/kat.xlsx', nrows = 1)
reve = pd.read_excel('./static/results.xlsx')
data = pd.DataFrame(columns=['Отзыв','категория','подкатегория','Дата'])



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
perc=0.67
tag_data.fillna('', inplace=True)
kt = set()
pkt= set()
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
                        kt.add(fin_key)
                        pkt.add(column_name)
        #print(reve.loc[reve['Отзыв'] == znach]['Дата создания отзыва'])
        data=data.append({'Отзыв':znach,'категория':str(list(kt))[1:-1].replace("'",''),'подкатегория':str(list(pkt))[1:-1].replace("'",''),'Дата':str(reve.loc[reve['Отзыв'] == znach]['Дата создания отзыва'].values)[2:12]}, ignore_index = True)
        kt.clear()
        pkt.clear()
writer = pd.ExcelWriter('rety.xlsx')
data.to_excel(writer, sheet_name='table', index=False)
worksheet = writer.sheets['table']
for column in data:
    column_width = max(data[column].astype(str).map(len).max(), len(column)) + 5
    if column_width > 70:
        column_width = 70
    col_idx = data.columns.get_loc(column)
    worksheet.set_column(col_idx, col_idx, column_width)
workbook=writer.book
header_format = workbook.add_format({'text_wrap': True})
for col_num, value in enumerate(data['Отзыв']):
    worksheet.write(col_num + 1,0, value, header_format)
worksheet.autofilter(f'B1:C1')
worksheet.freeze_panes(1, 0)
writer.save()










