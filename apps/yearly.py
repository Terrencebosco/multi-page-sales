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

# #specific data
# df = pd.read_csv(DATA_PATH.joinpath("db_csv.csv"))
# df = df[df['year']!=2017]

df = pd.read_csv(DATA_PATH.joinpath("updated_data.csv"))

month_year_group = df.groupby(['year','month_name'])['sales_amount'].sum()
month_year_group = month_year_group.reindex(months, level='month_name').reset_index()

layout = dbc.Container([
    # header
    dbc.Row([
            dbc.Col(html.H1("Sales Breakdown by Year",
            style={'text-align':'center'},
            className='mb-5'),width=12),

            dbc.Col(html.P('''
            A breakdown of the yearly sales data for Company A. Select years to
            be included in analysis. Breakdowns include yearly porgressions, earnings
            per type of product sold, earnings by markets, and earnings by customer bases.
            ''',
            style={'text-align':'left'},
            className='mb-5'),width=6)
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

    dbc.Row([
        dbc.Col([
              dcc.Input(
                id='look_at2',
                placeholder='Value between 0 and 259',
                type='number',
                value=3,
                min=0,
                max=259
                ),

            dcc.Graph(id='market_sales', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                ),

        # bar: year breakdown revenue by product to show num slected as % of total
        dbc.Col([
            dcc.Graph(id='market_sales_pie', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
        )
        ]),

    dbc.Row([
        dbc.Col([
              dcc.Input(
                id='look_at3',
                placeholder='Value between 0 and 259',
                type='number',
                value=3,
                min=0,
                max=259
                ),

            dcc.Graph(id='customer_sales', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                ),

        # bar: year breakdown revenue by product to show num slected as % of total
        dbc.Col([
            dcc.Graph(id='customer_sales_pie', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
        )
        ])
    ])

@app.callback(
    Output('month_year', 'figure'),
    Input('year', 'value')
)

# line graph for revenue
def update_graph(year):
    temp = month_year_group[month_year_group['year'].isin(year)]
    fig = px.line(temp, x="month_name", y='sales_amount', color='year')
    fig.update_xaxes(type='category', tick0='January')
    fig.update_layout(hovermode="x")
    return fig


@app.callback(
        Output('product_sales','figure'),
        [Input('year', 'value'),
        Input('look_at', 'value')]
)

# bar Graph for product
def update_graph(year, look_at):

    if year == []:
        year = None
    year_to_string = "".join(str(year)).strip("[]")
    temp = df[df['year'].isin(year)]
    product_group = temp.groupby('product_code')['sales_amount'] \
    .sum().reset_index().sort_values('sales_amount',ascending=False)[:look_at]

    fig = px.bar(
        product_group,
        y='sales_amount',
        x='product_code',
        title=f'Top {look_at} highest earning products for year/s {year_to_string}')

    return fig


@app.callback(
    Output('product_sales_pie','figure'),
    [Input('year', 'value'),
    Input('look_at', 'value')]
)

# pie graph for product
def update_graph(year, look_at):

    #error supression
    if look_at == None:
        look_at = 0

    #data
    temp = df[df['year'].isin(year)]
    product_group = temp.groupby('product_code')['sales_amount'].sum().reset_index() \
    .sort_values('sales_amount',ascending=False)

    # get the percent of looked at out of total.
    percent_of_look_at =round(sum(product_group['sales_amount'][:look_at]) \
        /sum(product_group['sales_amount'])*100,2)
    year_to_string = "".join(str(year)).strip("[]")

    # get popout for pie
    total = len(temp['product_code'].unique())
    zeros = np.zeros(total)
    pull = [.1] * look_at
    test = list(np.concatenate([pull, zeros[look_at:]]))

    explode = len(product_group['product_code'].unique())

    fig = go.Figure(
        data=[go.Pie(
            labels=product_group['product_code'],
            values=product_group['sales_amount'],
            pull=test)])
    fig.update_traces(textposition='inside', textinfo='percent+label'),
    fig.update_layout(
        title={
            'text':f'''Top {look_at} make up {percent_of_look_at}% of all revenue for year/s {year_to_string}'''
        }
    )

    return fig

###########################
######### row two #########
###########################

@app.callback(
    Output('market_sales','figure'),
    [Input('year', 'value'),
    Input('look_at2', 'value')]
)

# bar Graph for markets
def update_graph(year, look_at2):

    if year == []:
        year = None
    year_to_string = "".join(str(year)).strip("[]")
    temp = df[df['year'].isin(year)]
    product_group = temp.groupby('markets_code')['sales_amount'] \
    .sum().reset_index().sort_values('sales_amount',ascending=False)[:look_at2]

    fig = px.bar(
        product_group,
        y='sales_amount',
        x='markets_code',
        title=f'Top {look_at2} highest earning Markets for year/s {year_to_string}')

    return fig


@app.callback(
    Output('market_sales_pie','figure'),
    [Input('year', 'value'),
    Input('look_at2', 'value')]
)

# pie graph for markets
def update_graph(year, look_at2):
    #error supression
    if look_at2 == None:
        look_at2 = 0

    temp = df[df['year'].isin(year)]
    product_group = temp.groupby('markets_code')['sales_amount'].sum().reset_index() \
    .sort_values('sales_amount',ascending=False)

    percent_of_look_at =round(sum(product_group['sales_amount'][:look_at2]) \
    /sum(product_group['sales_amount'])*100,2)

    year_to_string = "".join(str(year)).strip("[]")

    total = len(temp['markets_code'].unique())
    zeros = np.zeros(total)
    pull = [.1] * look_at2
    test = list(np.concatenate([pull, zeros[look_at2:]]))

    explode = len(product_group['markets_code'].unique())

    fig = go.Figure(data=[go.Pie(labels=product_group['markets_code'], values=product_group['sales_amount'], pull=test)])
    fig.update_traces(textposition='inside', textinfo='percent+label'),
    fig.update_layout(
        title={
            'text':f'''Top {look_at2} make up {percent_of_look_at}% of all revenue for year/s {year_to_string}'''
        }
    )
    return fig

###########################
######## row three ########
###########################


@app.callback(
    Output('customer_sales','figure'),
    [Input('year', 'value'),
    Input('look_at3', 'value')]
)

# bar Graph for customers
def update_graph(year, look_at2):

    if year == []:
        year = None
    year_to_string = "".join(str(year)).strip("[]")
    temp = df[df['year'].isin(year)]
    product_group = temp.groupby('customer_code')['sales_amount'] \
    .sum().reset_index().sort_values('sales_amount',ascending=False)[:look_at2]

    fig = px.bar(
        product_group,
        y='sales_amount',
        x='customer_code',
        title=f'Top {look_at2} highest earning Customers for year/s {year_to_string}')

    return fig


@app.callback(
    Output('customer_sales_pie','figure'),
    [Input('year', 'value'),
    Input('look_at3', 'value')]
)

# pie graph for customers
def update_graph(year, look_at3):
    #error supression
    if look_at3 == None:
        look_at3 = 0

    temp = df[df['year'].isin(year)]
    product_group = temp.groupby('customer_code')['sales_amount'].sum().reset_index() \
    .sort_values('sales_amount',ascending=False)

    percent_of_look_at =round(sum(product_group['sales_amount'][:look_at3]) \
    /sum(product_group['sales_amount'])*100,2)

    year_to_string = "".join(str(year)).strip("[]")

    total = len(temp['customer_code'].unique())
    zeros = np.zeros(total)
    pull = [.1] * look_at3
    test = list(np.concatenate([pull, zeros[look_at3:]]))

    explode = len(product_group['customer_code'].unique())

    fig = go.Figure(data=[go.Pie(labels=product_group['customer_code'], values=product_group['sales_amount'], pull=test)])
    fig.update_traces(textposition='inside', textinfo='percent+label'),
    fig.update_layout(
        title={
            'text':f'''Top {look_at3} make up {percent_of_look_at}% of all revenue for year/s {year_to_string}'''
        }
    )
    return fig

    # TODO
    # get titles as paragraps with descriptions rather than long sentances in title