from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("League Leaders", href="/leaders")),
                dbc.NavItem(dbc.NavLink("Player Search", href="/search")),
            ] ,
            brand="MLS Dashboard",
            brand_href="/leaders",
            color="dark",
            dark=True,
        ),
    ])

    return layout
