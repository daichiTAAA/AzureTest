from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

from adls import ADLS
import settings

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv"
)

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(children="Title of Dash App", style={"textAlign": "center"}),
        dcc.Dropdown(df.country.unique(), "Canada", id="dropdown-selection"),
        dcc.Graph(id="graph-content"),
        # Get the data from ADLS
        html.Div(
            [
                html.H1(children="ADLS Data", style={"textAlign": "center"}),
                html.P(children="File Names in Directory"),
                html.Button("Show Files", id="show-files-button"),
                html.Div(id="files-list"),
            ]
        ),
    ]
)


@app.callback(Output("files-list", "children"), Input("show-files-button", "n_clicks"))
def display_files(n):
    if n is None:
        return []
    try:
        return ADLS().get_files_in_directory("test", "data")
    except Exception as e:
        return f"Error connecting to ADLS: {str(e)}"


@app.callback(Output("graph-content", "figure"), Input("dropdown-selection", "value"))
def update_graph(value):
    dff = df[df.country == value]
    return px.line(dff, x="year", y="pop")


if settings.ENV != "LOCAL":
    server = app.server

if __name__ == "__main__":
    app.run(debug=True)
    # server = app.server
