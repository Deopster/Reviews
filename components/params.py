import dash_bootstrap_components as dbc
from dash import html, dcc
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
    ])
)
tag_key=dbc.Card(
    dbc.Col([
        dbc.Label("укажите модель"),
        dbc.Select(
                ["test.xmls", "test-key.xmls"],
                "test.xmls",
                id="shorthand-select",
            ),
        switches,
        switches1,

        dbc.Label("Столбец exel таблицы в который будут записываться результаты"),
        dbc.Input(placeholder="Укажите название поля записи",type="text"),
    ])
)