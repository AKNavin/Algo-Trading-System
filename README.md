# 📊 Algorithmic Trading System with Kite Connect + Plotly Dash

## **Overview**

This project implements a fully automated real-time algorithmic trading system using the Zerodha Kite Connect API for live trade execution and Plotly Dash for dynamic monitoring.

It executes a 1-minute EMA 5/15 crossover strategy and logs trades + PnL live into Excel, while charting OHLC data, trade actions, and PnL in a Dash dashboard.

## 🎥 **Demo Videos**

## 📺 [Live Algo Trading Deployment | Initial Trade Execution on Zerodha Kite](https://youtu.be/hWZECBEJVXE)

## 📺 [Live Algo Trade Management | Square-Off and New Position Execution](https://youtu.be/U-9PjQyUNhI)

## 📺 [Algo Trading EOD Report | Final Trade and P&L Display](https://youtu.be/lN8kbwqjvts)


## **Components**

KiteOrderPlacement.py	- Runs the live algo trading loop — reads tick data from Practice.db and resample it to OHLC data, detects signals, places orders via KiteConnect, logs actions to Log.xlsx

PlotlyLiveplots.py	- Interactive Plotly Dash dashboard showing live OHLC + EMA crossover charts, volume bars, algo trade logs, and cumulative PnL graph

Practice.db	       - SQLite database storing tick-by-tick Price and Volume data for multiple stocks

Log.xlsx	       - Excel file with multiple sheets logging trade actions, order prices(used for PnL), and open positions

AccessToken.txt	       - Text file storing the current access token

Presentation           - Summarization of code architecture, strategy logic, algo execution screenshots, improvements and conclusion


## **Trading Strategy**

EMA 5 / EMA 15 Crossover

Buy when EMA 5 crosses above EMA 15

Sell when EMA 5 crosses below EMA 15

Trade executed as a MARKET order via Zerodha Kite REST API

Position is squared off on reverse signal and a new position is opened

## **Live Dash Dashboard**

Dropdown: Select stock (HB, RS, IB, ISS)

OHLC Candlestick Chart: 1-minute bars with EMA 5 & EMA 15

Volume Bar Chart

Live Trade Logs: Color-coded by action (Buy, Sell, Square-off)

Cumulative PnL Graph: Based on executed prices in log


