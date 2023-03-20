import pandas as pd
tag_data = pd.read_excel('./input/разбор_ответов_с_портала.xls')
data = pd.DataFrame(columns=['Функционал в мобильном приложении, который хотят','что хорошо в банке','Критика банка','Что нужно изменить в банке в целом','Пожелания не связанные с мобильным приложением','хорошие кейсы других банков о которы вспоминают клиенты','с чем был связан плохой клиентский опыт'])
#print(tag_data.keys())
fir_m = []
sec_good_m = []
sec_bad_m = []
third_m = []
fors_m = []
fifs_m=[]
ter=[]
for i in range(235):
        first = tag_data.iloc[i]['14. Есть ли что-то еще, чем вы хотели бы поделиться, а мы у вас не спросили?']
        sec= tag_data.iloc[i]['7. Теперь поговорим о своем, родном! Нравятся ли вам продукты / услуги нашего Банка? Если нет, то почему?']
        therd=tag_data.iloc[i]['6. А в каком банке у вас был самый ужасный клиентский опыт? С чем это было связано?']
        fors=tag_data.iloc[i]['13. Если бы у вас была волшебная палочка, что бы вы исправили в наших продуктах и услугах?']
        fifs=tag_data.iloc[i]['4. Чем именно вам нравится выбранный / выбранные банки?']

        if len(str(first)) >=80:
            #data.at[i, 'Пожелания не связанные с мобильным приложением'] = first
            if first.lower().count('прилож')>0:
                ter.append(first)
            else:
                fir_m.append(first)
            #print(first)
        mu=False
        if len(str(sec)) >= 80:
            for bank in ['да','нравятся','нравится','да,']:
                if str(sec).lower().find(bank)!=-1:
                    if str(sec).lower().count('не нравятся')==0:
                        mu=True
                        break
            if mu == True:
                #data.at[i, 'что хорошо в банке '] = sec
                sec_good_m.append(sec.replace('Да',''))
            else:
                #data.at[i, 'Критика банка'] = sec
                sec_bad_m.append(sec.replace('нет',''))
            # print(first)
        if len(str(therd)) >= 50:
            #data.at[i, 'с чем был связан плохой клиентский опыт'] = therd
            third_m.append(therd)
        if len(str(fors)) >= 50:
            fors_m.append(fors)
            #data.at[i,'Что нужно изменить в банке в целом'] = fors
        me=False
        if len(str(fifs)) >= 50:
            for bank in ['тинькофф','втб','альфабанк','cбер','сбера','сбербанк']:
                if fifs.lower().find(bank)!=-1:
                    me=True
                    break
            if me == True:
                fifs_m.append(fifs)

final={'Пожелания не связанные с мобильным приложением':fir_m,'что хорошо в банке':sec_good_m,'Критика банка':sec_bad_m,'с чем был связан плохой клиентский опыт':third_m,'Что нужно изменить в банке в целом':fors_m,'хорошие кейсы других банков о которы вспоминают клиенты':fifs_m,'Функционал в мобильном приложении, который хотят':ter}
for key in final.keys():
    for index ,i in enumerate(final[key]):
        data.at[index,key]=i
writer = pd.ExcelWriter('data.xlsx')
data.to_excel(writer, sheet_name='table', index=False)
worksheet = writer.sheets['table']
for column in data:
    column_width = max(data[column].astype(str).map(len).max(), len(column)) + 5
    if column_width > 70:
        column_width = 70
    col_idx = data.columns.get_loc(column)
    worksheet.set_column(col_idx, col_idx, column_width)
#worksheet.autofilter(f'B1:C1')
#worksheet.freeze_panes(1, 0)
writer.save()

