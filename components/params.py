import dash_bootstrap_components as dbc
from dash import html, dcc
from components import grafpath
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
mp = grafpath.info()
# print(mp)
mvt = dcc.Dropdown(
    mp.keys(),
    [],
    multi=False,
    className="mb-2",
)
switches1 = html.Div(
    [
        dbc.Checklist(
            options=[
                {"label": "Записать теги в отдельный столбец", "value": 1},
            ],
            value=[1],
            id="switches-input",
            switch=True,
        ),
    ],className="mb-2 ml-1"
)
simple=dbc.Card(
    dbc.Col([
        dbc.Label("укажите модель"),
        dbc.Select(
                ["test.xmls", "test-key.xmls"],
                "test.xmls",
                id="shorthand-select",
            ),

        dbc.Label("Столбец exel таблицы в который будут записываться результаты"),
        dbc.Input(placeholder="Укажите название поля записи",type="text"),
    ],className="mb-2 mt-2")
)
tag_key=dbc.Card(
    dbc.Col([
        dbc.Label("укажите модель"),
        dbc.Select(
                ["test.xmls", "test-key.xmls"],
                "test.xmls",
                id="shorthand-select",
            ),
        dbc.Label("Исходный столбец парсинга"),
        mvt,
        switches,
        switches1,
        dbc.Label("Столбец exel таблицы в который будут записываться результаты"),
        dbc.Input(placeholder="Укажите название поля записи",type="text"),
    ],className="mb-2 mt-2")
)



sel=dbc.Select(
        ["=", "<", ">","<=",">="],
        "=",
        id="shorthand-select",

    )
scan=dbc.Card(
    dbc.Col([
        dbc.Row([
            dbc.Col(mvt,md=5),
            dbc.Col(sel,md=2),
            dbc.Col(dbc.Input(placeholder="Значение",type="text"),md=5),
        ]),
        dbc.Label("Столбец exel таблицы в который будут записываться результаты"),
        dbc.Input(placeholder="Укажите название поля записи",type="text"),
    ],className="mb-2 mt-2")
)