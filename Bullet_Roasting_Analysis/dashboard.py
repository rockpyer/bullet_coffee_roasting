
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

#load data
df = pd.read_csv('csvExports/point_df.csv')

# Initialize the Dash application:
app = dash.Dash(__name__)

# Define the layout of the dashboard:
app.layout = html.Div(children=[
    html.H1('Roast Analysis Dashboard'),
    dcc.Dropdown(
        id='x-axis-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='roastName'
    ),
    dcc.Dropdown(
        id='y-axis-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns],
        value='dateTime'
    ),
    dcc.Graph(id='scatter-plot')
])
# Define the callback functions for interactivity:
@app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [dash.dependencies.Input('x-axis-dropdown', 'value'),
     dash.dependencies.Input('y-axis-dropdown', 'value')]
)
def update_scatter_plot(x_axis, y_axis):
    fig = px.scatter(df, x=x_axis, y=y_axis)
    return fig

RUN
if __name__ == '__main__':
     app.run_server(debug=True)

