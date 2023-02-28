from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
from components import filelist
from components import grafpath

import pymystem3

import plotly.express as px
from dash_bootstrap_templates import load_figure_template
list_group = dbc.ListGroup(children=filelist.uploaded_files(),
flush=True,id='file_list',
)
switches = html.Div(
    [
        dbc.Checklist(
            options=[
                {"label": "Использовать лематизацию текста", "value": 1},
            ],
            value=[1],
            id="switches-input",
            switch=True,
        ),
    ],className="mb-2 ml-1"
)
select = html.Div(
    dbc.Select(
        ["простое тегирование", "Тегирование ключ-слово", "сканирование","перебор"],
        "простое тегирование",
        id="shorthand-select",
    ),
    className="py-2 mb-2",
)
from dash import dcc
mp = grafpath.info()
#print(mp)
mvt = dcc.Dropdown(
    mp.keys(),
    [],
    multi=True,
    className="mb-2",
)
car = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("", className="card-title"),
                html.P("", className="card-text"),
            ]
        ),
    ],
)
card_mod2 = html.Div([
dbc.Col([html.Small(f"в файле найдено {len(mp.keys())} столбцов и {len(mp)} строк"),select,html.Small(f"Выберите строки над которыми необходимо провести операцию"),mvt,switches,car
])
])



cont=html.Div([ dbc.Card(
            dbc.CardBody(list_group),
            className="mb-3",style={'min-height':'17em'}
        ),
])
modal_2 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Выберите параметры")),
        dbc.ModalBody(card_mod2),
        dbc.ModalFooter([

            dbc.Button(
                "Назад",
                id="open-toggle-modal-1",
                n_clicks=0,
            ),
            dbc.Button(
                "начать",
                id="start",
                className="ms-auto",
                n_clicks=0,
            )
        ]),
    ],
    id="toggle-modal-2",
    is_open=False,
    centered=True,
)

modal =html.Div([
    dbc.Button("+", outline=True, color="success", className="me-1", n_clicks=0,id="open-lg-new",size='lg',style={'--bs-btn-padding-x': '9.75rem','--bs-btn-padding-y': '9rem','border-style':'dashed','font-size':'2em'}),
    dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Выберите файл")),
                dbc.ModalBody(cont,id=''),
                dbc.ModalFooter(
                    dbc.Button(
                        "далее",
                        id="open-toggle-modal-2",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="toggle-modal-1",
            size="md",
            is_open=False,
            centered=True,
        )
])

layout = dbc.Container(
    [
dbc.Row(
            [
                dbc.Col([modal,modal_2]),
                dbc.Col(),
                dbc.Col(),
            ],
            align="center",
        ),
    ],
    fluid=True,
    className="dbc",
)