from dash import html,dcc
import dash_bootstrap_components as dbc

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
    html.Div(id="cat_list",children="", className='row',style={"overflowY": "auto", "maxHeight": "90vh"})
], className='container')
search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search",id="ser_input")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0,id="ser"
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)
items = ["Item 1"]
down = dbc.Card([
    dbc.CardHeader(search_bar),
    dbc.CardBody(
    dbc.ListGroup(flush=True,numbered=True,children=dbc.Spinner(html.Div(id="loading-output",style={"margin-top":"4em","margin-bottom":"4em"})),id="hello"),style={"overflowY": "auto", "maxHeight": "90vh"}
    )
    ]
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
    dcc.Upload(html.A('Upload File'))
    ,
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



