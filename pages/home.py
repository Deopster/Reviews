import os
import time

import dash
from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
load_figure_template('SLATE')
from generate import programm
import pandas as pd
import numpy as np
df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()
# stylesheet with the .dbc class

header = html.H4(
    "<UI UX LAB>", className="bg-primary text-white p-2 mb-2 text-center"
)
ells = html.Div([
    dcc.Dropdown(['заморозить столбцы', 'Заморозить первую строку', 'Добавить автофильтр'], 'Заморозить первую строку', multi=True,className="dash-bootstrap mb-2")
])



number_input = html.Div([
    dcc.Input(
            id="dtrue", type="number",
            debounce=False, placeholder="0 - все отзывы",className="dash-bootstrap p-1 rt"
        )
])
dropdown = html.Div([
    dcc.Dropdown(
    options=[
        {'label': 'Новые', 'value': 'NEWEST'},
        {'label': 'Ревенантные', 'value': 'MOST_RELEVANT'},
   ],
    value='NEWEST',
    id="indicator",
    className="dash-bootstrap",
    clearable=False
            )
])


radio = html.Div(

)

list_data = dbc.Row(
    [
        dbc.Col(html.Div(dropdown)),
        dbc.Col(html.Div(number_input)),
    ],className="mb-2"
)
slider = html.Div(
    [
        dbc.Label("Применить фильтр оценок отзывов"),
        dcc.RangeSlider(1, 5, 1, value=[1, 5],className="p-0")
    ],
    className="mb-4",
)
terminal= html.I(className="fas fa-terminal",style=dict(display='inline',color='white'))
reload= html.I(className="fas fa-redo",style=dict(display='inline',color='white'))
download = html.I(className="fas fa-cloud-download",style={'textAlign': 'center','verticalAlign': 'bottom','display':'inline'})

row_content = [
    html.Div([
        dbc.Button(children=reload, id='button',type="reset", n_clicks=0, className="but",size='lg',color="info"),
        dbc.Button(children=download,href="/static/results.xlsx",download="my_data.xlsx",external_link=True, color="success",size="lg", className="but"),
 html.Div(
    [
        dbc.Button(children=terminal, color="dark", className="but",size="lg",id="open-body-scroll", n_clicks=0),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Web Terminal")),
                dbc.ModalBody("Test output\nnext line",style={'color':'white','background-color':'black'}),
                dbc.ModalFooter(
                    dbc.Button(
                        "Send",
                        id="close-body-scroll",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal-body-scroll",
            scrollable=True,
            is_open=False,
            fullscreen=True
        ),
    ]
),
],className="pb-3",style={'float': 'right', 'display':'flex'})
]


buttonrow= html.Div(
        row_content,
)
#buttonrow= dbc.Card([],className=["mb-3"])
stateline = dbc.Card(
                    [
                        dbc.Row([
                                dbc.Card([
                                    dbc.CardBody(id='my-output',children='Первичная загрузка',className='p-1'),
                            ],style={'diplay':'block'},id='block_1'),
                        ], className="p-2"),
                    ],className=["mb-3"]
                )
controls = dbc.Card(
    [list_data, ells, slider],
    body=True,
)
template = "seaborn"
import plotly.graph_objects as go
fig = go.Figure()
#fig.show()
import plotly.express as px



data = pd.read_excel('./static/results.xlsx',sheet_name='table')
temp= []
first_5=[]
second_3_4=[]
therd_1_2=[]

for i in data.keys()[4:-1]:
    first_5.append(sum(data[data['Оценка'] ==5][f'{i}']))
    second_3_4.append(sum(data[data['Оценка']==3][f'{i}'])+sum(data[data['Оценка']==4][f'{i}']))
    therd_1_2.append(sum(data[data['Оценка'] <3][f'{i}']))
#print(len(data.keys()[4:-1]))
#print(index)
fig = px.bar(x=data.keys()[4:-1], y=[first_5,second_3_4,therd_1_2], labels=data.keys()[4:-1])
fig.update_layout(template=template,margin=dict(l=0, r=0, t=0, b=0),legend_orientation="v",)

#print([len(df[data['Оценка'] == 1]),len(df[data['Оценка'] == 2]),len(df[data['Оценка'] == 3]),len(df[data['Оценка'] == 4]),len(df[data['Оценка'] == 5])])
#print(list(len(df.loc[data['Оценка']== i]) for i in range(1,6)))

graf = dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Graph(
                    figure={
                        'data': [go.Pie(values=list(len(df.loc[data['Оценка']== i]) for i in range(1,6)), labels=['оценка 1','оценка 2','оценка 3','оценка 4','оценка 5'], hole=0.85)],
                        'layout': go.Layout( margin=dict(l=0, r=0, t=0, b=0),showlegend=False,annotations=[dict(text=f'Всего отзывов <br>{len(data["Оценка"])}', x=0.5, y=0.5, font_size=20, showarrow=False)])

                    },
                    style={'height':'auto'}
                )
            ]
        ),
        #dbc.CardFooter("Соотношение отзывов"),
    ],
)



tabs = dbc.Card([
dbc.CardBody(
            [
            dcc.Graph(figure=fig,style={'height':'auto'})
            ]
        ),
]
)

layout = dbc.Container(
    [
        dbc.Row(
            [

                dbc.Col([

            html.Div([
                dbc.Row(
                    [
                        buttonrow,
                    ],
                ),
                        dbc.Row(
                            [
                                stateline,
                            ]
                        ),

                dbc.Row(
                    [
                        controls,
                    ],
                ),



                        ], className='container')],md=3,className="mb-3"),
                dbc.Col([
                    html.Div([
dbc.Row(
            [
                                graf
                ])
                ], className='container')], md=3,className="mb-3"),
            dbc.Col([
                    html.Div([
dbc.Row(
            [
                                tabs
                ])
                ], className='container')], md=6,className="mb-3"),
            ]
        ),
        dcc.Loading([html.Div(id="loading-demo")],fullscreen=True,type='cube',style={'backgroundColor': 'black'}),
    ],
    fluid=True,
    className="dbc",
)


