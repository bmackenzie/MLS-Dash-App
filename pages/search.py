import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


layout = html.Div(children=[
    html.H1('MLS Dashboard',
             style={'textAlign': 'center', 'color': 'white','font-size': 40, 'margin-bottom':'.5em'}),
    html.H2('Search Players',
             style={'textAlign': 'center', 'color': 'white','font-size': 30}),

    dcc.Input(id='name', type='text', placeholder='Player Name', style ={'margin': 'auto', 'display': 'block'}),
    html.Div(id='table1'),

    dbc.Row(
        [
            dbc.Col(html.Div([], id='plot1'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
            dbc.Col(html.Div([], id='plot2'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
        ],
        style={'margin-bottom': '.5em', 'margin-top': '.5em'}
    ),

    dbc.Row(
        [
            dbc.Col(html.Div([], id='plot3'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
            dbc.Col(html.Div([], id='plot4'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
        ]
    ),

])
