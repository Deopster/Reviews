from dash import Dash, callback
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
from dash.dependencies import Input, Output, State
import dash
import pandas as pd
from components import grafpath

graf = dbc.Card(
    [
        dbc.CardHeader("общая статистика анализа тегов"),
        dbc.CardBody(id="AllDataGraf",children=''
        ),
        #dbc.CardFooter("..."),
    ],
    className="mb-3",
)
sec = html.Div([
    html.Div(id="cat_list",children="", className='row')
], className='container')

items = ["Item 1"]
down = dbc.Card(
    dbc.CardBody([
    dbc.ListGroup(
        flush=True,numbered=True,children=dbc.Spinner(html.Div(id="loading-output",style={"margin-top":"4em","margin-bottom":"4em"})),id="hello"
    )
    ]),style={"overflowY": "auto", "maxHeight": "90vh"}
)
upl = dbc.Card(
    dbc.CardBody([
        dbc.Alert(
            "Файл был успешно загружен",
            id="alert-fade",
            dismissable=True,
            is_open=True,
        ),
html.Hr(),
dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Перетяни сюда новый файл тегирования "]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
            },
            multiple=False,
            last_modified=123
        ),
        html.Hr(),
        html.H2("Список файлов"),
        html.Ul(id="file-list"),
    ]),className="mb-3"
)

layout = dbc.Container([
    dbc.Row([
        dbc.Col(sec, md=3),
        dbc.Col([graf,upl], md=4),
        dbc.Col(down, md=5)
    ])
],fluid=True,className="dbc",)



