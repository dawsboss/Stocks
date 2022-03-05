#This is not good fo rlice data

import streamlit as st
import pandas as pd
import numpy as np
from robinAPI import Stocks
import streamlit_modal as modal
import plotly.express as px
import time

#Setting up robinhood account
import os
from dotenv import load_dotenv
import pyotp
import yfinance as yf

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

#streamlist run gui.py
#Setting up vissuals
st.title('Stock profolio')

st.header('header')

st.subheader('subheader')

st.write('write')

some_dic = {
    "key": "Value",
    "key2": "Value2",
}

some_list = [1,2,3]

st.write(some_dic)

st.write(some_list)

st.write(me.tickers)

st.sidebar.write("Sidebar text")
selectedStock = st.sidebar.selectbox('Choose a stock',me.tickers)
graphData = yf.download(selectedStock)
graphData['Data'] = graphData.index

st.dataframe(graphData)

fig = px.line(graphData, x='Data', y='Close')
st.plotly_chart(fig, use_container_width=True)

df = pd.DataFrame(np.random.randn(50,20), columns=('col %d' % i for i in range(20)))

st.dataframe(df)

#After load keep info up to date _ BREAKS stream lit
# import time
# ct = 1
# while True:
#     time.sleep(1)
#     print(ct)
#     if ct % 5 == 0:
#         me.update()
#         print("5 seconds")
#     if ct % 30 == 0:
#         print("30 seconds")
#     if ct%10 == 0:
#         print("10 seconds")
#     ct = ct+1