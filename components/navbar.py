from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Главная", href="/page1")),
                dbc.NavItem(dbc.NavLink("Теги", href="/page2")),
            ] ,
            brand="UI UX Lab",
            brand_href="/page1",
            color="dark",
            dark=True,
            style={'marginbottom':'200px'}
        ),
        html.Br(),
    ])

    return layout