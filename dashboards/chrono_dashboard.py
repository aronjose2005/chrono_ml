import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('training_rewards.csv')
df['smoothed'] = df['reward'].rolling(window=10).mean()

app = dash.Dash(__name__, assets_folder='../assets', title="ChronoDQN 3D Dashboard")
server = app.server  # for deployment

app.layout = html.Div([
    html.H1("⏳ ChronoDQN Reward Time Warp Dashboard", className='header'),

    html.Div([
        html.Label("Warp Time Speed:"),
        dcc.Slider(1, 20, 1, value=1, marks={i: f"{i}x" for i in range(1, 21)}, id='speed-slider'),
    ], className='slider-div'),

    dcc.Graph(id='3d-plot', style={'height': '80vh'})
])

@app.callback(
    Output('3d-plot', 'figure'),
    Input('speed-slider', 'value')
)
def update_figure(speed):
    sampled_df = df.iloc[::speed]
    trace = go.Scatter3d(
        x=sampled_df['episode'],
        y=sampled_df['reward'],
        z=sampled_df['smoothed'],
        mode='lines+markers',
        marker=dict(size=3, color=sampled_df['reward'], colorscale='Viridis'),
        line=dict(width=4, color='cyan')
    )

    layout = go.Layout(
        scene=dict(
            xaxis_title='Episode',
            yaxis_title='Reward',
            zaxis_title='Smoothed Reward'
        ),
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color='white'),
    )

    return go.Figure(data=[trace], layout=layout)

if __name__ == '__main__':
    app.run(debug=True)  # For local running

