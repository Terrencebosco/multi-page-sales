import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import pathlib

# the problem child
from app import app

# read in csv from datasets folder.
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#specific data
df = pd.read_csv(DATA_PATH.joinpath("db_csv.csv"))
df = df[df['year']!=2017]

geojson = ps.read_csv(DATA_PATH.joinpath("states_india.geojson"))

# do this in the callback, why be global??
months = ['January','February','March','April','May','June'
        ,'July','August','September','October','November','December']

month_year_group = df.groupby(['year','month_name'])['sales_amount'].sum()
month_year_group = month_year_group.reindex(months, level='month_name').reset_index()

layout= dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='year',
                options=[{'label':x, 'value':x}
                                   for x in sorted(month_year_group['year'].unique())],
                multi=False,
                value=2020,
                style={'width':'50%'}
                ),

                dcc.Graph(id='revenue', figure={})],
                xs=12, sm=12, md=12, lg=6, xl=6,
                ),

        dbc.Col([
            dcc.Graph(id='test', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                )
    ])
])

@app.callback(
    # outputs 1
    Output('revenue','figure'),
    # input from user
    Input('year', 'value')
)

def update_graph(option_selected):

    dff = df.copy()
    dff = dff[dff['year']== option_selected]

    fig = px.pie(
        dff,
        values='sales_amount',
        names='markets_name',
        title=f'revenue by market for year {option_selected}',
        )
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig