from dash import Dash
from generate import programm
import os
import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.graph_objs as go
from datetime import date
import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash
import pandas as pd

df = pd.read_excel('./input/model.xlsx')
all_data = set()
df.fillna('',inplace=True)
for i in df.values.tolist():
    all_data.update(i)
#print(list(all_data)[1::])
#print(len(list(all_data)))
#print([map(lambda num: num, *df.values.tolist())])


dash.register_page(__name__,path='/tags')

graf = dbc.Card(
    [
        dbc.CardHeader("This is the header"),
        dbc.CardBody(
            [
                dcc.Graph(
                    figure={
                        'data': [go.Pie(values=[10, 20, 30], labels=['A', 'B', 'C'], hole=0.85)],
                        'layout': go.Layout( margin=dict(l=0, r=0, t=0, b=0),
    legend_orientation="h",)

                    },
                    style={}
                )
            ]
        ),
        dbc.CardFooter("This is the footer"),
    ],
    style={},
)
sec = html.Div([
    html.Div([
        html.Div([
            html.H3(category),
            html.Div([
                         dcc.Dropdown(
                             list(all_data)[1::],
                             list(df[f"{category}"]),
                             multi=True
                         )
            ])
        ], className='card mb-3 p-2') for category in df.keys().tolist()
    ], className='row')
], className='container')
layout = dbc.Container([
    dbc.Row([
        dbc.Col(sec, md=3),
        dbc.Col(graf, md=4),
        dbc.Col(html.Div([]), md=5),
    ])
],fluid=True,
    className="dbc",)
def revies_ammount(data):
    #for i in data['Дата создания отзыва']:
    series1 = np.array([3, 4, 5, 3])
    series2 = np.array([1, 2, 2, 5])
    series3 = np.array([2, 3, 3, 4])
    index = np.arange(4)
    plt.axis([-0.5, 3.5, 0, 15])
    plt.title('колличество отзывов по датам (зелёные положительные, синие нейтрал, красные отрицательные)')
    plt.bar(index, series1, color='r')
    plt.bar(index, series2, color='b', bottom=series1)
    plt.bar(index, series3, color='g', bottom=(series2 + series1))
    plt.xticks(index, ['Jan18', 'Feb18', 'Mar18', 'Apr18'])
    plt.show()
#revies_ammount(1)

def ctegory_ammount(data,m):
    first_5=[]
    second_3_4=[]
    therd_1_2=[]
    #print(data.keys()[4:-1])
    for i in data.keys()[4:-1]:
        first_5.append(sum(data[data['Оценка'] ==5][f'{i}']))
        second_3_4.append(sum(data[data['Оценка']==3][f'{i}'])+sum(data[data['Оценка']==4][f'{i}']))
        therd_1_2.append(sum(data[data['Оценка'] <3][f'{i}']))
    index = np.arange(len(first_5))
    plt.figure(figsize=(len(first_5)*2.5, len(first_5)*1.5))
    print(len(first_5))
    print(len(second_3_4))
    print(len(therd_1_2))
    bw = 0.3
    plt.title(f'найдено тегов по каждому параметру (зелёные в положительных отзывах, жёлтые в нейтральных, красные в отрицательных), всего {m}', fontsize=20)
    for i in range(len(data.keys()[4:-1])):
        plt.text(i, first_5[i], first_5[i], ha='center',fontsize=20)
    for i in range(len(data.keys()[4:-1])):
        plt.text(i+bw, second_3_4[i], second_3_4[i], ha='center',fontsize=20)
    for i in range(len(data.keys()[4:-1])):
        plt.text(i+bw*2, therd_1_2[i], therd_1_2[i], ha='center',fontsize=20)
    plt.bar(index, first_5,bw, color='g')
    plt.bar(index+bw, second_3_4,bw, color='y')
    plt.bar(index+bw*2, therd_1_2,bw, color='r')
    plt.xticks(index+1.5*bw,data.keys()[4:-1])
    plt.tight_layout()
    plt.savefig('./output/foo.png')
#ctegory_ammount(data,m)