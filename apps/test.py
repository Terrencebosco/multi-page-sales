import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import json

import plotly.express as px
import pandas as pd
import pathlib

# the problem child
from app import app

# read in csv from datasets folder.
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# load csvs
df = pd.read_csv(DATA_PATH.joinpath("updated_data.csv"))

month_year_group = pd.read_csv(DATA_PATH.joinpath("year_sales_group.csv"))

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

#load in new geo_json
with open('datasets/data.json') as f:
    india_geojson = json.load(f)

layout= dbc.Container([
    dbc.Row([
        dbc.Col([
           dcc.Checklist(id='year', value=[2020,2019,2018],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(month_year_group['year'].unique())],
                          labelClassName="mr-3"),

                dcc.Graph(id='geo', figure={})],
                xs=12, sm=12, md=12, lg=12, xl=12,
                ),
        dbc.Col([
                dcc.Graph(id='test', figure={})],
                xs=12, sm=12, md=12, lg=12, xl=12,
                ),

        # click json object store location.
        dbc.Col([
            dcc.Store(id='click-data',storage_type='session') #style=styles['pre']),
        ])

    ])
])

@app.callback(
    #store click, output and input
    [Output('geo','figure'),Output('click-data', 'children')],
    [Input('year', 'value'), Input('geo', 'clickData')]
)

def update_graph(values, clickData):
    temp = df[df['year'].isin(values)]

    t = temp.groupby(['state_code', 'markets_list', 'state'])['sales_amount'].sum()
    t = t.reset_index()
    fig = px.choropleth_mapbox(
            t,
            locations='state_code',
            geojson=india_geojson,
            mapbox_style="carto-positron",
            color='sales_amount',
            color_continuous_scale='bugn',
            center={"lat": 20, "lon": 77},
            hover_data=['state', 'markets_list'],
            zoom=3,
            opacity=1)

    # clickable graph
    fig.update_layout(clickmode='event+select')

    # we are storing the "click data" into a json string object to itter later.
    return fig , json.dumps(clickData, indent=2)


# read in stored data from json object.. see above in layout.
@app.callback(
    Output('test', 'figure'),
    [Input('year', 'value') ,Input('geo', 'clickData')])
def display_click_data(year, clickData):

    temp = df[df['year'].isin(year)]

    product_group = temp.groupby(['product_code', 'id'])['sales_amount'].sum().reset_index() \
    .sort_values('sales_amount',ascending=False)

    # if click data is non return all data for country
    if clickData != None:
        l = clickData['points'][0]['location']
        product_group = product_group[product_group['id']==l]
        fig = px.bar(product_group, y='sales_amount', x='product_code')
    else:
        fig = px.bar(product_group, y='sales_amount', x='product_code')

    return fig

# --------------------------------------------------------------------------------------------------------------------------------------------------- 
