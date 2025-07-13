import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import sqlite3
from datetime import datetime
from plotly.subplots import make_subplots
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'Practice.db')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'Log.xlsx')

# List of stock columns
stocks = ['HB', 'RS', 'IB', 'ISS']

# Initialize the app
app = dash.Dash(__name__)
app.title = "Realtime OHLC + Volume + EMA + Log Viewer"

# App layout
# App layout
app.layout = html.Div([
    html.Div([

        html.Div([
            html.H2([
    "Realtime 1-Min OHLC Chart with Volume",
    html.Br(),
    "EMA 5 and EMA 15 Crossover"
], style={'textAlign': 'left'}),
            dcc.Dropdown(
                id='stock-dropdown',
                options=[{'label': stock, 'value': stock} for stock in stocks],
                value='HB',
                style={'width': '200px', 'margin-bottom': '20px'}
            ),
            dcc.Graph(id='ohlc-chart')
        ], style={'flex': '4', 'padding': '0 20px'}),  # 80% width

        html.Div([
    html.H4("Algo Trade Logs", style={'textAlign': 'center'}),
    html.Div(id='log-output', style={
        'height': '500px',
        'overflowY': 'scroll',
        'backgroundColor': '#1e1e1e',
        'color': '#ffffff',
        'padding': '10px',
        'border': '1px solid #444'
    }),
    dcc.Graph(id='pnl-graph', style={'height': '200px', 'margin-top': '10px'})
], style={'flex': '1', 'padding': '0 10px'})  # 20% width

    ], style={'display': 'flex', 'flexDirection': 'row'}),  # Flex container for side by side layout

    # Interval here
    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    )

], style={'backgroundColor': '#111111', 'color': '#FFFFFF'})

# Callback to update chart
@app.callback(
    Output('ohlc-chart', 'figure'),
    [Input('stock-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(selected_stock, n_intervals):
    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    vol_col = f"{selected_stock}V"
    query = f"SELECT datestamp, `{selected_stock}`, `{vol_col}` FROM testTable"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert datestamp to datetime
    df['datestamp'] = pd.to_datetime(df['datestamp'])
    df.set_index('datestamp', inplace=True)

    # Resample 3-min OHLC
    ohlc = df[selected_stock].resample('1T').ohlc()
    ohlc.dropna(inplace=True)

    # Handle cumulative volume
    df['volume_diff'] = df[vol_col].diff().clip(lower=0)
    vol = df['volume_diff'].resample('1T').sum()
    vol = vol.loc[ohlc.index]

    # EMA 9-period
    ema1 = ohlc['close'].ewm(span=5, adjust=False).mean()
    ema2 = ohlc['close'].ewm(span=15, adjust=False).mean()

    if selected_stock == 'HB':
        SS = 'HDFCBANK'
    elif selected_stock == 'RS':
        SS = 'RELIANCE'
    elif selected_stock == 'IB':
        SS = 'ICICIBANK'
    else:
        SS = 'INFY'
        
    # Figure with subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3], subplot_titles=(f"{SS} 1-Min OHLC with EMA (5,15)", f"{SS} Volume"))
    fig.add_trace(go.Candlestick(x=ohlc.index, open=ohlc['open'], high=ohlc['high'], low=ohlc['low'], close=ohlc['close'], name='OHLC'), row=1, col=1)
    fig.add_trace(go.Scatter(x=ohlc.index, y=ema1, mode='lines', line=dict(color='orange', width=1.5), name='EMA 5'), row=1, col=1)
    fig.add_trace(go.Scatter(x=ohlc.index, y=ema2, mode='lines', line=dict(color='teal', width=1.5), name='EMA 15'), row=1, col=1)
    fig.add_trace(go.Bar(x=ohlc.index, y=vol, name='Volume', marker_color='lightblue'), row=2, col=1)
    fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=700, showlegend=False)

    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_xaxes(title_text="Time", row=2, col=1)

    return fig


# Callback to update log output
@app.callback(
    Output('log-output', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_log(n_intervals):
    if os.path.exists(LOG_PATH):
        try:
            log_df = pd.read_excel(LOG_PATH)
            # Use only last 30 rows, newest first
            latest_logs = log_df.tail(30).iloc[::-1]

            log_lines = []
            for row in latest_logs.iloc[:, 0]:  # Assuming logs in first column
                log_text = str(row)

                # Assign color based on keywords
                if 'position' in log_text.lower():
                    color = 'white'
                elif 'buy' in log_text.lower():
                    color = 'lightgreen'
                elif 'sell' in log_text.lower():
                    color = 'salmon'
                else:
                    color = 'white'

                log_lines.append(html.Div(log_text, style={'color': color, 'margin-bottom': '5px'}))

        except Exception as e:
            log_lines = [html.Div(f"Error reading log file: {e}", style={'color': 'orange'})]
    else:
        log_lines = [html.Div("Log file not found.", style={'color': 'grey'})]

    return log_lines

@app.callback(
    Output('pnl-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_pnl(n_intervals):
    if os.path.exists(LOG_PATH):
        fig = go.Figure()
        try:
            pnl_df = pd.read_excel(LOG_PATH, sheet_name='Sheet2')
            pnl_df.dropna(inplace=True)

            if pnl_df.empty:
                fig = go.Figure()
                fig.add_annotation(text="No PnL data yet.",
                                   xref="paper", yref="paper",
                                   showarrow=False, font=dict(color="grey"))
                return fig

            # Initialize PnL column
            pnl_df['PnL'] = 0.0

            # Loop through dataframe starting from index 1 with step 2
            for i in range(1, len(pnl_df), 2):
                pnl_df.loc[i, 'PnL'] = (pnl_df.loc[i, 'Executed Price'] + pnl_df.loc[i-1, 'Executed Price'])*-1

            # Now compute cumulative PnL
            pnl_df['CumulativePnL'] = pnl_df['PnL'].cumsum()
            
            pnl_df['Time'] = pd.to_datetime(pnl_df['Timestamp']).dt.strftime('%H:%M:%S')

            # Create figure
            fig.add_trace(go.Scatter(x=pnl_df['Time'], y=pnl_df['CumulativePnL'], mode='lines+markers', line=dict(color='gold'), marker=dict(size=4), name='PnL'))
            fig.update_layout(template='plotly_dark', margin=dict(l=30, r=30, t=20, b=20), height=100, showlegend=False, xaxis=dict(showticklabels=True), yaxis_title="PnL", xaxis_title=None)

        except Exception as e:
            fig = go.Figure(); fig.add_annotation(text=f"Error reading PnL: {e}", xref="paper", yref="paper", showarrow=False, font=dict(color="orange"))

    else:        
        fig = go.Figure(); fig.add_annotation(text="Log file not found.", xref="paper", yref="paper", showarrow=False, font=dict(color="grey"))

    fig.update_layout(template='plotly_dark', margin=dict(l=30, r=30, t=30, b=30), height=200, showlegend=False, yaxis_title="PnL")
    return fig

# Interval component (single shared)
app.layout.children.append(
    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    )
)

if __name__ == '__main__':
    app.run_server(debug=True)
