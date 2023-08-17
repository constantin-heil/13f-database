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
    html.Button(id = "submit_query", children = "Submit"),
    dcc.Graph(id = "managers_barplot"),
    dcc.Input(id = "pie_ix", value = "0"),
    dcc.Graph(id = "pie_plot"),
    dcc.Store(id = "querystore")
])

@callback(
    Output("querystore", "data"),
    Input("query_company", "value"),
    Input("submit_query", "n_clicks")
)
def get_top_holders_plots(company_query: str, n_clicks: int) -> dict:
    """Make database query and return the 2 plot types

    Args:
        company_query (str): Company to query in SQL BOOLEAN mode query
        pie_ix (int): Which pie plot will be the first of 4
    """
    df = pd.read_sql_query(queryfunctions.top_holders(company_query), con = engine)
    return df.to_dict()

@callback([Output("managers_barplot", "figure"),
            Output("pie_plot", "figure")],
           [Input("querystore", "data"),
            Input("pie_ix", "value")])
def get_plots(df_dic, pie_ix) -> (go.Figure, go.Figure):
    df = pd.DataFrame(df_dic)
    plotter = plotfunctions.nameofissuer_plotter(df)
    
    barplot = plotter.get_bar_plot()
    pieplot = plotter.get_pie_plot(int(pie_ix))
    
    return barplot, pieplot

if __name__ == "__main__":
    app.run(debug = True)
    