import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import pandas as pd
from components import grafpath
import dash_bootstrap_components as dbc
import re
#!!!Оптимизировать этот кусок

# НЕ ЗАБУДЬ
def getdata():
    global data,data_for_tags,reva,df, all_data,first_5,second_3_4,therd_1_2
    data = pd.read_excel('./static/results.xlsx', sheet_name='table')
    data_for_tags = pd.read_excel('./static/results.xlsx', sheet_name='tags')
    reva = pd.read_excel('./static/results.xlsx', usecols=['Отзыв', 'Теги совпадений'])
    df = pd.read_excel('./input/model.xlsx')
    #main
    for number in range(len(reva)):
        #print(str(reva['Теги совпадений'][number]).split(" ~ ")[1:])
        for i in str(reva['Теги совпадений'][number]).split(" ~ "):
            if i!='':
                fl=True
                repl=re.findall(r"\w+t}",reva['Отзыв'][number].lower().replace(i, '{st}' + i + '{ft}'))
                for index in range(len(repl)-1):
                    if repl[index] == repl[index+1]:
                        fl=False
                if fl:
                    reva.at[number, 'Отзыв'] = reva['Отзыв'][number].lower().replace(i, '{st}' + i + '{ft}')
        reva.at[number, 'Теги совпадений'] = str(reva['Теги совпадений'][number]).replace(" ~ ", ' ')
        reva.at[number, 'Отзыв'] = reva['Отзыв'][number].replace("{st}", "**").replace("{ft}", "**")

    #main
    all_data = set()
    df.fillna('', inplace=True)
    for i in df.values.tolist():
        all_data.update(i)
    #home 2
    first_5 = []
    second_3_4 = []
    therd_1_2 = []
    for i in data.keys()[4:-1]:
        first_5.append(sum(data[data['Оценка'] == 5][f'{i}']))
        second_3_4.append(sum(data[data['Оценка'] == 3][f'{i}']) + sum(data[data['Оценка'] == 4][f'{i}']))
        therd_1_2.append(sum(data[data['Оценка'] < 3][f'{i}']))
    #print("The func was triggered 1")
def graf_home_1():
    mp = dcc.Graph(
        figure={
            'data': [go.Pie(values=list(len(data.loc[data['Оценка'] == i]) for i in range(1, 6)),
                            labels=['оценка 1', 'оценка 2', 'оценка 3', 'оценка 4', 'оценка 5'], hole=0.85)],
            'layout': go.Layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False, annotations=[
                dict(text=f'Всего отзывов <br>{len(data["Оценка"])}', x=0.5, y=0.5, font_size=20, showarrow=False)])

        },
        style={'height': 'auto'}
    )
    #print("The func was triggered 2")
    return mp

def graf_home_2():

    fig = px.bar(x=data.keys()[4:-1], y=[first_5, second_3_4, therd_1_2], labels=data.keys()[4:-1])
    fig.update_layout(template="seaborn", margin=dict(l=0, r=0, t=0, b=0), legend_orientation="v", )
    return dcc.Graph(figure=fig, style={'height': 'auto'}, id="tag_stats")
def graf_main_1():
    ma = [html.Div([
        dbc.Row([html.H4(category)]),
        html.Div([
            dcc.Dropdown(
                list(all_data)[1::],
                list(df[f"{category}"]),
                multi=True,
                clearable=False

            )
        ])
    ], className='card mb-3 p-2')
    for category in df.keys().tolist()]
    #print("The func was triggered 3")
    return ma
def graf_main_2():
    res = dcc.Graph(
        figure={
            'data': [
                go.Pie(values=[data_for_tags[i].sum() for i in data_for_tags], labels=data_for_tags.keys().tolist(),
                       hole=0.85, textinfo='none')],
            'layout': go.Layout(margin=dict(l=0, r=0, t=0, b=0), legend_orientation="h", annotations=[
                dict(text=f'Всего найдено<br>{sum(data_for_tags[i].sum() for i in data_for_tags)}', font_size=20,
                     showarrow=False)])

        },
        style={'height': 'auto'},
        id="AllDataGraf"
    )
    #print("The func was triggered 4")
    return res
def getRev():
    return [dbc.ListGroupItem([reva['Теги совпадений'][i],dcc.Markdown(reva['Отзыв'][i])]) for i in range(len(reva))]
def info():
    global data
    return data

getdata()
