# Import necessary libraries
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd
from difflib import SequenceMatcher
import plotly.express as px
import plotly.graph_objects as go

# Connect to your app pages
from pages import leaders, search

# Connect the navbar to the index
from components import navbar

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SOLAR],
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)

# define the navbar
nav = navbar.Navbar()

#Get Player Stats
with sqlite3.connect('mlsdb.sqlite') as conn:
    query = conn.execute("""
		SELECT
			p.name as Name,
			p.nation as Nation,
			p.pos as Position,
			p.squad as Squad,
			p.age as Age,
			pt.mp as Matches,
			pt.starts as Starts,
			pt."min" as Minutes,
			p."90s" as "90s",
			ps.gls as Gls,
			pp.ast as Ast,
			ps.pk as "G-PK",
			ps.pkAtt as "PKatt",
			ROUND(ps.gls/p."90s", 2) as "Gls/90",
			ROUND(pp.ast/p."90s", 2) as "Ast/90",
			ROUND((ps.gls + pp.ast)/p."90s", 2) as "Gls+ast/90",
			pd.tkl as "TKLatt",
			ROUND(CAST(pd.tklW as REAL)/pd.tkl, 2) as "Tkl%",
			pd.blk as Blks,
			pd.int as Int,
			ROUND(pd.tkl/p."90s", 2) as "Tkl/90",
			ROUND(pd.blk/p."90s", 2) as "Blk/90",
			ROUND(pd.int/p."90s", 2) as "Int/90",
			pm.crdY as Ycard,
			pm.crdR as Rcard
		FROM players p
		INNER JOIN playerTime pt
			ON p.id = pt.player_id
		INNER JOIN playerShooting ps
			ON p.id = ps.player_id
		INNER JOIN playerPassing pp
			ON p.id = pp.player_id
		INNER JOIN playerDefense pd
			ON p.id = pd.player_id
		INNER JOIN playerMisc pm
			ON p.id = pm.player_id;""")
    cols = [column[0] for column in query.description]
    playerStats= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/leaders':
        return leaders.layout
    if pathname == '/search':
        return search.layout
    if pathname == '/':
        return leaders.layout
    else:
        return "404 Page Error! Please choose a link"
@app.callback(
    Output('table1', 'children'),
    Output('plot1', 'children'),
    Output('plot2', 'children'),
    Output('plot3', 'children'),
    Output('plot4', 'children'),
    Input('name', 'value')
)
def search_player(name):
    if (name is not None ):
        target = name
        lst = playerStats['Name']

        a = [SequenceMatcher(None, i, target).ratio() for i in lst]

        index = a.index(max(a))
        match = lst[index]
        df=playerStats[playerStats['Name'] == match]
        table =dash_table.DataTable(data=df.to_dict('records'),columns=[{"name": i, "id": i} for i in df.columns])
        goalPlot = px.bar(x=[match, 'League Avg'], y=[df['Gls/90'].max(), playerStats['Gls/90'].mean()], color = [match, 'League Average'], template = 'plotly_dark', title='Goals Per 90 vs League Avg')
        goalPlot.update_layout(title_x=0.5, xaxis_title="", yaxis_title="Goals/90")
        astPlot = px.bar(x=[match, 'League Avg'], y=[df['Ast/90'].max(), playerStats['Ast/90'].mean()], color = [match, 'League Average'], template = 'plotly_dark', title='Assists Per 90 vs League Avg')
        astPlot.update_layout(title_x=0.5, xaxis_title="", yaxis_title="Assists/90")
        tklPlot = px.bar(x=[match, 'League Avg'], y=[df['Tkl/90'].max(), playerStats['Tkl/90'].mean()], color = [match, 'League Average'], template = 'plotly_dark', title='Tackles Per 90 vs League Avg')
        tklPlot.update_layout(title_x=0.5, xaxis_title="", yaxis_title="Tackles/90")
        intPlot = px.bar(x=[match, 'League Avg'], y=[df['Int/90'].max(), playerStats['Int/90'].mean()], color = [match, 'League Average'], template = 'plotly_dark', title='Interceptions Per 90 vs League Avg')
        intPlot.update_layout(title_x=0.5, xaxis_title="", yaxis_title="Interceptions/90")

        return(table, dcc.Graph(figure = goalPlot), dcc.Graph(figure = astPlot), dcc.Graph(figure = tklPlot), dcc.Graph(figure = intPlot))
        #return(generate_table(playerStats[playerStats['Name'] == match]))
    else:
        return("","","","","")
# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
