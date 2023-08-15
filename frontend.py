from dash import Dash, html, dcc, Input, Output, callback
import plotly.graph_objects as go
from sqlalchemy import create_engine
import pandas as pd
import plotfunctions
import queryfunctions

username = 'remoteuser'
password = 'password'
host = 'localhost'
database = 'sec13f'

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

app = Dash(__name__)

app.layout = html.Div(children = [
    html.H1(children = "Holdings plot"),
    dcc.Input(id = "query_company", value = "+Cameco", type = "text"),
    dcc.Graph(id = "managers_barplot"),
    dcc.Input(id = "pie_ix", value = "0"),
    dcc.Graph(id = "pie_plot")
])

@callback(
    Output("managers_barplot", "figure"),
    Output("pie_plot", "figure"),
    Input("query_company", "value"),
    Input("pie_ix", "value")
)
def get_top_holders_plots(company_query: str, pie_ix: int):
    """Make database query and return the 2 plot types

    Args:
        company_query (str): Company to query in SQL BOOLEAN mode query
        pie_ix (int): Which pie plot will be the first of 4
    """
    df = pd.read_sql_query(queryfunctions.top_holders(company_query), con = engine)
    plotter = plotfunctions.nameofissuer_plotter(df)
    
    barplot = plotter.get_bar_plot()
    pieplot = plotter.get_pie_plot(int(pie_ix))
    
    return barplot, pieplot

if __name__ == "__main__":
    app.run(debug = True)
    