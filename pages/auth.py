from dash import Dash, dcc, html, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_bootstrap_templates import load_figure_template

email_input = html.Div(
    [
        dbc.Label("Email", html_for="example-email"),
        dbc.Input(type="email", id="example-email", placeholder="Введите ваш почтовый адрес"),
        dbc.FormText(
            "",
            color="secondary",
        ),
    ],
    className="mb-3",
)

password_input = html.Div(
    [
        dbc.Label("Password", html_for="example-password"),
        dbc.Input(
            type="password",
            id="example-password",
            placeholder="Введите пароль",
        ),
        dbc.FormText(
            "Пароль от 5 символов", color="secondary"
        ),
    ],
    className="mb-3",
)

form = dbc.Form([email_input, password_input])

layout = dbc.Container(
    [
dbc.Row(
            [
                dbc.Col(),
                dbc.Col(form),
                dbc.Col(),
            ],
            align="center",
        ),
    ],
    fluid=True,
    className="dbc",
)