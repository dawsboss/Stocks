import dash
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import time

from robinAPI import Stocks

stockPage = html.Div(
    [
        html.H1('MUR Stock',
                style={'textAlign':'center'}, id="stock-analysis-title"),
        dbc.Row(
            [
                dbc.Col(html.P('Select a stock for analysis: '),width=3),
                dbc.Col(dcc.Dropdown(me.tickers, me.tickers[0], id="stock-analysis-dropdown"),),
            ]
        ),
        dcc.Graph(id='stock-analysis-historical-line',figure = {},style=CARD_STYLE),
        dbc.Row(
            [
                dbc.Col([html.H3("Dividend Activity:"),]),
                dbc.Col([html.H3("News:"),]),
            ]
        ),

        html.Br(),

        dbc.Row(
            [
                dbc.Col([html.Div([html.H3("dividend stuff"),],style=CARD_STYLE),]),
                dbc.Col([html.Div([html.H3("News stuff"),],style=CARD_STYLE),]),
            ],
        ),

        dcc.Graph(id='stock-analysis-1w-live-line',figure = {},style=CARD_STYLE),

        dcc.Graph(id='stock-analysis-1d-live-line',figure = {},style=CARD_STYLE),


    ]
)