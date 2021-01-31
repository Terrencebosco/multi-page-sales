import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import pathlib

# the problem child
from app import app

# read in csv from datasets folder.
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#specific data
df = pd.read_csv(DATA_PATH.joinpath("db_csv.csv"))
df = df[df['year']!=2017]

months = ['January','February','March','April','May','June'
        ,'July','August','September','October','November','December']

month_year_group = df.groupby(['year','month_name'])['sales_amount'].sum()
month_year_group = month_year_group.reindex(months, level='month_name').reset_index()

layout = dbc.Container([
    dbc.Row([
        dbc.Col([

            dcc.Dropdown(
                id='year3',
                options=[{'label':x, 'value':x}
                                   for x in sorted(month_year_group['year'].unique())],
                multi=False,
                value=2020,
                style={'width':'62%'}
                ),

            dcc.Input(
                id='look_at',
                placeholder='Value between 0 and total number of products',
                type='number',
                value=5,
                min=0,
                max=259
                ),

            dcc.Dropdown(
                id='market',
                options=[{'label':x, 'value':x}
                                   for x in sorted(df['markets_name'].unique())],
                multi=False,
                value='Mumbai',
                style={'width':'62%'}
                ),

            dcc.Graph(id='market_product_bar', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                ),

        dbc.Col([
            dcc.Graph(id='market_product_pie', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                )

        ],align='center')
])

@app.callback(
    Output('market_product_bar', 'figure'),
    [Input('year3', 'value'),
    Input('look_at', 'value'),
    Input('market', 'value')]
)

def update_graph(year, look_at, market):
    #checks for error in number to look at feild ets to 0 to by pass error.
    if (look_at == 0):
        look_at = None
    # data query
    dff = df.query(f'year=={year}')
    total_products = len(dff[dff['markets_name']==market]['product_code'].unique())

    temp = dff[dff['markets_name']==market]['product_code'].value_counts().head(look_at)
    fig = px.bar(temp, y=temp.values, x=temp.index,
                 title=f'top {look_at} out of {total_products} products sold in {market}')

    return fig

# ----- figure 5 ----
@app.callback(
    Output('market_product_pie', 'figure'),
    [Input('year3', 'value'),
    Input('look_at', 'value'),
    Input('market', 'value')]
)

def update_graph(year, look_at, market):

    #data
    dff = df.query(f'year=={year}')

    #checks for error in number to look at feild ets to 0 to by pass error.
    if (look_at == None):
        look_at = 0

    # get n out of total to show percent of total
    total = len(dff['product_code'].unique())
    zeros = np.zeros(total)
    pull = [.1] * int(look_at)
    test = list(np.concatenate([pull, zeros[10:]]))

    # expand 'look_at' amount for pie chart
    explode = len(dff['product_code'].unique())
    product_out_of_100 = dff[dff['markets_name']==market]['product_code'].value_counts()

    product_out_of_100.sum()
    fig = go.Figure(data=[go.Pie(labels=product_out_of_100.index, values=product_out_of_100.values, pull=test)])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig