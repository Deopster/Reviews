import plotly.express as px
import pandas as pd
dates_list =[]
reve = pd.read_excel('./static/results.xlsx',usecols="D,S")

for date in reve.iterrows():
    cur_date = str(date[1]['Дата создания отзыва'])
    cur_date = cur_date.replace('-'," ").split()[0:2]
    real_date=cur_date[0]+'-'+cur_date[1]
    if real_date not in dates_list:
        dates_list.append(real_date)
rezalts = pd.DataFrame(columns=['1','2','3','4','5'],index=dates_list)
rezalts.fillna(0, inplace=True)
for date in reve.iterrows():
    cur_date = str(date[1]['Дата создания отзыва'])
    cur_date = cur_date.replace('-', " ").split()[0:2]
    real_date = cur_date[0] + '-' + cur_date[1]
    mark=cur_date = str(date[1]['Оценка'])
    rezalts.at[real_date, mark] = 1 + rezalts.at[real_date, mark]
print(rezalts)
fig = px.line(rezalts, labels=['оценка 1', 'оценка 2', 'оценка 3', 'оценка 4', 'оценка 5'])
fig.update_layout(xaxis_title="Даты", yaxis_title="Пользовательские оценки приложения",)
for index,zna in enumerate(['оценка 1', 'оценка 2', 'оценка 3', 'оценка 4', 'оценка 5']):
    fig.data[index].name=zna
fig.show()