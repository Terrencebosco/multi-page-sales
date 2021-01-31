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


@app.callback(
    Output('month_year', 'figure'),
    Input('year', 'value')
)

# line graph
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

# bar Graph
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

# pie graph
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

    # TODO
    # get titles as paragraps with descriptions rather than long sentances in title