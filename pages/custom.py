from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
from components import filelist

import plotly.express as px
from dash_bootstrap_templates import load_figure_template
list_group = dbc.ListGroup(children=filelist.uploaded_files(),
flush=True,id='file_list1',
)

from dash import dcc
#print(mp)
mvt = dcc.Dropdown(
    filelist.getfile().keys(),
    [],
    multi=True,
    id="file_names_drop",
    className="mb-2",
)
select = dbc.Select(
        ["простое тегирование", "Тегирование ключ-слово", "сканирование","перебор"],
        "простое тегирование",
        id=f"chose_v0", className="mb-2"
    )
dell= html.I(className="fas fa-trash",style=dict(display='inline',color='white'))
car = html.Div(
    [
                dbc.ListGroup(children=[dbc.ListGroupItem(dbc.Col([dbc.Row([dbc.Col(select,md=10,style={'paddingRight':'0','paddingLeft':'0'}),dbc.Col(dbc.Button(children=dell, id='del',type="submit",target=f"0", n_clicks=0,size='md',color="info",className="mb-2",disabled=True),md=2)]),
                                                           dbc.Row(children="", id=f'cont0')
                                                          ])),
                                        dbc.ListGroupItem("Добавить", id='add-field', action=True,style={'textAlign': 'center','backgroundColor':''}),
                                        #dbc.ListGroupItem()
                                        ], id='form-container',flush=True),
    ],style={"border":"none"}
)
card_mod2 = html.Div([
dbc.Col([html.Small(f"в файле {filelist.getfile_name()} найдено {len(filelist.getfile().keys())} столбцов и {len(filelist.getfile())} строк",id="file_name_card" ,className="mb-2"),
         car,
         dcc.Store(id='my-store'), #,html.Small(f"Выберите строки над которыми необходимо провести операцию"),mvt
         dbc.Alert(
            "Заполните все поля",
            color="danger",
            id="alert-warn",
            dismissable=True,
            fade=True,
            is_open=False,
             duration=2000
         ),
])
])



cont=html.Div([ dbc.Card(
            dbc.CardBody(list_group,id='body_files'),
            className="mb-2",style={'minHeight':'17em'}
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
upl =  dcc.Upload(
            id="upl_file",
            children=html.Div(
                ["Загрузить"]
            ),
            style={
                "borderWidth": "1px",
                "borderStyle": "solid",
                "borderRadius": "5px",
                "textAlign": "center",
                'borderColor':"green",
                "padding":"10px"
            },
            multiple=True,
        )
modal =html.Div([
    dbc.Button("+", outline=True, color="success", className="me-1", n_clicks=0,id="open-lg-new",size='lg',style={'--bs-btn-padding-x': '9.75rem','--bs-btn-padding-y': '9rem','borderStyle':'dashed','fontSize':'2em'}),
    dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Выберите файл")),
                dbc.ModalBody(dbc.Col([cont,upl]),id=''),
                dbc.ModalFooter(
                    dbc.Button(
                        "далее",
                        id="open-toggle-modal-2",
                        className="ms-auto",
                        n_clicks=0,
                        disabled=True
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