import pandas as pd
from google_play_scraper import app, reviews ,Sort ,reviews_all
import glob
import pandas
import os
import string

import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.graph_objs as go
import pandas as pd
rev_number = None
if rev_number is not None:
    result, continuation_token = reviews(
        'com.bssys.roscapretail',
        lang='ru',  # defaults to 'en'
        country='us',  # defaults to 'us'
        sort=Sort.NEWEST, # defaults to Sort.NEWEST
        count=rev_number, # defaults to 100
        filter_score_with=None # defaults to None(means all score)
    )
else:
    result = reviews_all(
        'com.bssys.roscapretail',
        sleep_milliseconds=0,  # defaults to 0
        lang='ru',  # defaults to 'en'
        country='us',  # defaults to 'us'
        sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
        filter_score_with=None  # defaults to None(means all score)
    )
if not os.path.isdir("./output"):
     os.mkdir("output")
temp= {}
temp_tags =[]
file = glob.glob('*.xlsx')
try:
    tag_data = pandas.read_excel(file[0])
except IndexError:
    print("Закиньте в корневую папку с main.py файл с тегами")
    raise
except Exception:
    print("Неизвестная ошибка")
    raise
finally:
    print(f"открыт файл {file[0]} в качесте файла тегирования")
table_colums=['Отзыв','кол. совпадений','Теги совпадений', 'Оценка',*tag_data.columns,'Дата создания отзыва']
data = pandas.DataFrame(columns=table_colums)
m=0
for index,i in enumerate(result):
    temp['Дата создания отзыва']=i['at']
    temp['Отзыв'] = i['content']
    temp['Оценка'] = i['score']
    for column_name in tag_data.columns:
        for column_data in tag_data[f'{column_name}']:
            if pandas.notnull(column_data):
                if temp['Отзыв'].find(column_data) > 0:
                    m+=1
                    print(column_data,column_name,temp['Отзыв'],"\n")
                    temp_tags.append(column_data)
                    #print("да",column_name,temp['Отзыв'])
                    temp[f'{column_name}'] = 1

    temp['кол. совпадений'] = sum(list(temp.values())[2:])
    temp['Теги совпадений'] = str(temp_tags)
    for i in table_colums:
        if i not in temp.keys():
            temp[f'{i}']=0
    #print(temp)
    data = pandas.concat([data, pd.DataFrame([temp])],)
    #data = data.append(temp,ignore_index=True)
    temp_tags.clear()
    temp.clear()
print('Найдено совпадений: '+ str(m))




writer = pd.ExcelWriter('./output/results.xlsx')
data.to_excel(writer, sheet_name='table', index=False, na_rep=0)
worksheet=writer.sheets['table']
format1 = writer.book.add_format({'bg_color': '#e0f2cb','border':1})
format2 = writer.book.add_format({'bg_color': 'ffa799','border':1})
format3= format4 = writer.book.add_format({'bg_color': 'ffdca3','border':1})
for column in data:
    column_width = max(data[column].astype(str).map(len).max(), len(column))+5
    if column_width > 70:
        column_width=70
    col_idx = data.columns.get_loc(column)
    worksheet.set_column(col_idx, col_idx, column_width)
#worksheet.autofilter(f'B1:{string.ascii_uppercase[len(data.keys())-1]+"1"}')
worksheet.freeze_panes(1,2)
crits=['>4','<3','=3','=4']
formats = [format1,format2,format3,format4]
for index, i in enumerate(data['Оценка'],start=2): #по сути рудимент - потом заменить на цикл по колличеству строк
    #print(f"A{str(index)}:{string.ascii_uppercase[len(data.keys())]+str(index)}")
    #worksheet.write_row(f"A{str(index)}:{string.ascii_uppercase[len(data.keys())]+str(index)}", 'Ray', format4)
    for i in range(4):
        worksheet.conditional_format(f"A{str(index)}:{string.ascii_uppercase[len(data.keys())-1]+str(index)}", {'type': 'formula', 'criteria': f'=${string.ascii_uppercase[table_colums.index("Оценка")]}${index}{crits[i]}', 'format': formats[i]})
writer.save()





