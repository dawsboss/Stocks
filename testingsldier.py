from dash import dcc
import dash
from dash import html
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv")
df["AAPL_x"] = pd.to_datetime(df["AAPL_x"])

fig = px.bar(df, x="AAPL_x", y="AAPL_y").update_layout(
    xaxis={
        "range": [df["AAPL_x"].quantile(0.9), df["AAPL_x"].max()],
        "rangeslider": {"visible": True},
    }
)

# Build App
app = dash.Dash(__name__)
app.layout = html.Div(
    [dcc.Graph(id="bargraph", figure=fig), html.Div(id="bartable", children=[])],
)


@app.callback(
    Output("bartable", "children"),
    Input("bargraph", "relayoutData"),
)
def updateTable(graphData):
    global df
    if graphData and "xaxis.range" in graphData.keys():
        d1 = pd.to_datetime(graphData["xaxis.range"][0])
        d2 = pd.to_datetime(graphData["xaxis.range"][1])
    else:
        d1 = df["AAPL_x"].quantile(0.9)
        d2 = df["AAPL_x"].max()
    dft = df.loc[df["AAPL_x"].between(d1, d2)]
    return dash_table.DataTable(
        columns=[{"name": c, "id": c} for c in dft.columns],
        data=dft.to_dict("records"),
    )


# Run app and display result inline in the notebook
app.run_server(debug=True, port=3000)
