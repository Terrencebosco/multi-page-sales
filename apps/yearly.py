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

from app import app

months = ['January','February','March','April','May','June'
        ,'July','August','September','October','November','December']

## do this before loading in data ##
# read in csv from datasets folder.
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#specific data
df = pd.read_csv(DATA_PATH.joinpath("db_csv.csv"))
df = df[df['year']!=2017]

month_year_group = df.groupby(['year','month_name'])['sales_amount'].sum()
month_year_group = month_year_group.reindex(months, level='month_name').reset_index()

layout = dbc.Container([
    # header
    dbc.Row([
            dbc.Col(html.H1("web application, sales by year",
            style={'text-align':'center'},
            className='mb-5'),width=12)
    ]),

    # year vs year revenue over time
    dbc.Row([

            dbc.Col([

            dcc.Checklist(id='year', value=[2018,2019,2020],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(month_year_group['year'].unique())],
                          labelClassName="mr-3"),

            dcc.Graph(id='month_year', figure={})],
            xs=12, sm=12, md=12, lg=12, xl=12
                )
            ]),
# ])
    # second row of graphs
    dbc.Row([

        # bar: year breakdown revenue by product
        dbc.Col([
             dcc.Input(
                id='look_at',
                placeholder='Value between 0 and 259',
                type='number',
                value=5,
                min=0,
                max=259
                ),

            dcc.Graph(id='product_sales', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                ),

        # bar: year breakdown revenue by product to show num slected as % of total
        dbc.Col([
            dcc.Graph(id='product_sales_pie', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
        )

    ], align='center'),
])


## callbacks ##
# ------ figure 1 row 1 -------
@app.callback(
    Output('month_year', 'figure'),
    Input('year', 'value')
)

def update_graph(year):
    temp = month_year_group[month_year_group['year'].isin(year)]
    fig2 = px.line(temp, x="month_name", y='sales_amount', color='year')
    fig2.update_xaxes(type='category', tick0='January')
    fig2.update_layout(hovermode="x")
    return fig2


# ------- figure 1 row 2 ------
@app.callback(
        # input and output of controls on web app to adjust graph
        Output('product_sales','figure'),
        [Input('year', 'value'),
        Input('look_at', 'value')]
)

def update_graph(year, look_at):

    if year == None: ################## no work #############
        year = 2018

    temp = df[df['year'].isin(year)]
    product_group = temp.groupby('product_code')['sales_amount'] \
    .sum().reset_index().sort_values('sales_amount',ascending=False)[:look_at]

    fig = px.bar(product_group, y='sales_amount', x='product_code')

    return fig


# ----- figure 3 row 2-----
@app.callback(
    # outputs 1
    Output('product_sales_pie','figure'),
    # input from user
    [Input('year', 'value'),
    Input('look_at', 'value')]
)

def update_graph(year, look_at):

    if look_at == None:
        look_at = 0

    temp = df[df['year'].isin(year)]
    product_group = temp.groupby('product_code')['sales_amount'].sum().reset_index() \
    .sort_values('sales_amount',ascending=False)

    total = len(temp['product_code'].unique())
    zeros = np.zeros(total)
    pull = [.1] * look_at
    test = list(np.concatenate([pull, zeros[look_at:]]))

    explode = len(product_group['product_code'].unique())

    fig = go.Figure(data=[go.Pie(labels=product_group['product_code'], values=product_group['sales_amount'], pull=test)])
    fig.update_traces(textposition='inside', textinfo='percent+label')\

    return fig