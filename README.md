📊 Algorithmic Trading System with Kite Connect + Plotly Dash
📈 Real-time EMA Crossover + Volume Breakout Strategy
Live Market Algo Execution + Interactive Monitoring Dashboard

📑 Overview
This project implements a fully automated real-time algorithmic trading system using the Zerodha Kite Connect API for live trade execution and Plotly Dash for dynamic monitoring.

It executes a 1-minute EMA 5/15 crossover strategy with volume breakout confirmation, and logs trades + PnL live into Excel, while charting OHLC data, trade actions, and PnL in a Dash dashboard.

🛠️ Components
File/Module	Description
KiteOrderPlacement.py	Runs the live algo trading loop — reads OHLC data, detects signals, places orders via KiteConnect, logs actions to Log.xlsx and Practice.db
PlotlyLiveplots.py	Interactive Plotly Dash dashboard showing live OHLC + EMA crossover charts, volume bars, algo trade logs, and cumulative PnL graph
Practice.db	SQLite database storing 1-minute tick OHLC + Volume data for multiple stocks
Log.xlsx	Excel file with multiple sheets logging trade actions, order prices, and open positions
AccessToken.txt	Text file storing the current access token (excluded from repo)

🎯 Trading Strategy
EMA 5 / EMA 15 Crossover

Buy when EMA 5 crosses above EMA 15

Sell when EMA 5 crosses below EMA 15

Trade executed as a MARKET order via Zerodha Kite REST API

Position is squared off on reverse signal

📊 Live Dash Dashboard
Dropdown: Select stock (HB, RS, IB, ISS)

OHLC Candlestick Chart: 1-minute bars with EMA 5 & EMA 15

Volume Bar Chart

Live Trade Logs: Color-coded by action (Buy, Sell, Square-off)

Cumulative PnL Graph: Based on executed prices in log

🎥 Demo Videos
📺 Real-time Data Streaming & Trade Signal Detection (Unlisted YouTube)

📺 Order Placement & Square-Off Execution

📺 Live Plotly Dash Monitoring Dashboard
