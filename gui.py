import dash
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import time

from alpha_vantage.timeseries import TimeSeries

#-------------------------------------------------------------
#First part - Get data ready
#prepare data for the screen
#
#
#
#
#
#

#Setting up robinhood account
import os
from dotenv import load_dotenv
import pyotp
import yfinance as yf

from robinAPI import Stocks

load_dotenv()

if ("USERNAME" not in os.environ) or ("PASSWORD" not in os.environ) or ("MFA" not in os.environ):
    st.modal.text("No .env detected, input your username and password below:")
    username = st.modal.text_input("Username")
    password = st.modal.text_input("Password")
    MFA = st,modal.text_input("2 Factor Auth")
else:     
    code = os.getenv('MFA')
    MFA = pyotp.TOTP(code).now()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')


me = Stocks(username, password, MFA)

df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
CARD_STYLE={
  'border': '1px solid',
  'padding': '10px',
  'box-shadow': '2px 3px #888888',
  'margin-top': '35px', 
}
NAV_CARD_STYLE={
  'border': '1px solid',
  'padding': '10px',
  'box-shadow': '2px 3px #888888',
}

PRICE_INC_STYLE = {
    'color':'green'
}
PRICE_DEC_STYLE= {
    'color':'red'
}

def add_NavLink(sym, prev=0, price=0):
    greenORred = PRICE_INC_STYLE
    if ((price-prev) < 0):
        greenORred = PRICE_DEC_STYLE
    return dbc.NavLink(children=[
        html.Div([
                           dbc.Row([
                               dbc.Col([html.P(f"{sym}")]),
                               dbc.Col([html.P(f"${price-prev}")],style=greenORred)
                           ]),
                           
                                    
        ] ,style=NAV_CARD_STYLE),        
                           
                       ],
                       
                       href="/"+sym, active="exact")


#from stockPage import stockPage TODO




stockAnalysisPage = html.Div(
    [
        html.H1(f'MUR Stock',
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




sidebar = html.Div(
    [
        html.H2("Stock Helper", className="display-4"),
        html.Hr(),
        html.P(
            "Your stocks with more information", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink(children=[html.Div(html.P("Home"),style=NAV_CARD_STYLE)], href="/", active="exact"),
                dbc.NavLink(children=[html.Div(html.P("Total"),style=NAV_CARD_STYLE)], href="/total", active="exact"),
                dbc.NavLink(children=[html.Div(html.P("Stock Analysis"),style=NAV_CARD_STYLE)], href="/stock-analysis", active="exact"),
                
                
            ]+[add_NavLink(i) for i in me.tickers],
            id="stock-list",
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)


def render_page_content(pathname):

    symbol_check = pathname.replace("/","")
    if pathname == "/":
        return [
        
        html.H1("Hello!"),
        
        ]
    elif pathname == "/stock-analysis":
        return stockAnalysisPage
    
    elif pathname == "/total":
        return [
                html.H1('High School in Iran',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls High School', 'Boys High School']))
                ]
    

    elif symbol_check in me.tickers:
        return genstockPage(symbol_check)
    
    # If the user tries to reach a different page, return a 404 message
    else:
        return [
                html.H1('Error 404',
                        style={'textAlign':'center'}),
                ]

    
    
    
    
    
    
def genstockPage(sym):
    historyGraph = pd.DataFrame(me.yTicker[sym].history(period="max"))
    historyGraph['Date'] = historyGraph.index
    historyFig = px.line(historyGraph, x="Date", y="Close", title="Price History").update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="MAX", step="all", stepmode="todate"),

            ])
        )
    )
    
    oneWeekLiveGraph = me.live_update(sym, "7d", "1m")
    oneWeekLiveGraph['Date'] = oneWeekLiveGraph.index
    oneWeekLiveGraph.reset_index(drop=True, inplace=True)
    oneWeekLiveGraph['Index'] = oneWeekLiveGraph.index
    oneWeekLiveFig = px.line(oneWeekLiveGraph, x="Index", y="Close", title="Price History").update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="MAX", step="all", stepmode="todate"),

            ])
        )
    )
    
    oneDayLiveGraph = me.live_update(sym, "1d", "1m")
    oneDayLiveGraph['Date'] = oneDayLiveGraph.index
    oneDayLiveFig = go.Figure(data=[go.Candlestick(x=oneDayLiveGraph['Date'],
                        open=oneDayLiveGraph['Open'],
                        high=oneDayLiveGraph['High'],
                        low=oneDayLiveGraph['Low'],
                        close=oneDayLiveGraph['Close']
                    )]).update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=5, label="5m", step="minute", stepmode="backward"),
                dict(count=30, label="30m", step="minute", stepmode="backward"),
                dict(count=1, label="1h", step="hour", stepmode="backward"),
                dict(count=1, label="MAX", step="all", stepmode="todate"),

            ])
        )
    )
#     oneDayLiveFig = px.line(oneDayLiveGraph, x="Date", y="Close", title="Price History").update_xaxes(
#         rangeslider_visible=True,
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=1, label="1m", step="minute", stepmode="backward"),
#                 dict(count=10, label="10m", step="minute", stepmode="backward"),
#                 dict(count=1, label="1h", step="hour", stepmode="backward"),
#                 dict(count=1, label="MAX", step="all", stepmode="todate"),

#             ])
#         )
#     )
    
    
    
    stockPage = html.Div(
    [
        html.H1(f'{sym} Stock',
                style={'textAlign':'center'}),

        dcc.Graph(figure = historyFig,style=CARD_STYLE),
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

        dcc.Graph(figure = oneWeekLiveFig,style=CARD_STYLE),

        dcc.Graph(figure = oneDayLiveFig,style=CARD_STYLE),
    ]
)
    return stockPage
    
    
#------------------------------------------------------
#
# Below is for the stock analysis page
#
#------------------------------------------------------
@app.callback(
    [Output("stock-analysis-title","children"), Output("stock-analysis-historical-line","figure")],
    [Input("stock-analysis-dropdown", "value")]
)
def update_dropdown_graph(value):
    dfGraph = pd.DataFrame(me.yTicker[value].history(period="max"))
    dfGraph['Date'] = dfGraph.index
    fig = px.line(dfGraph, x="Date", y="Close", title="Price History").update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="MAX", step="all", stepmode="todate"),

            ])
        )
    )
    return f'{value} Stock',fig

@app.callback(
    Output("stock-analysis-1w-live-line","figure"),
    [Input("stock-analysis-dropdown", "value")]
)
def update_dropdown_1w_live_graph(value):
    dfGraph = me.live_update(value, "7d")
    dfGraph['Date'] = dfGraph.index
    fig = px.line(dfGraph, x="Date", y="Close", title="Live Price").update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=5, label="5m", step="minute", stepmode="backward"),
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=5, label="5d", step="day", stepmode="backward"),
                dict(count=1, label="1w", step="all", stepmode="todate"),

            ])
        )
    )
    return fig


@app.callback(
    Output("stock-analysis-1d-live-line","figure"),
    [Input("stock-analysis-dropdown", "value")]
)
def update_dropdown_1d_live_graph(value):
    dfGraph1 = me.live_update(value, "1d")
    dfGraph1['Date'] = dfGraph1.index
    fig = px.line(dfGraph1, x="Date", y="Close", title="fsdfdsfs Price")
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=5, label="5m", step="minute", stepmode="backward"),
                dict(count=1, label="1h", step="hour", stepmode="backward"),
                dict(count=5, label="MAX", step="all", stepmode="todate"),


            ])
        )
    )
    return fig
    
    

if __name__=='__main__':
    app.run_server(debug=True, port=3000)

   
