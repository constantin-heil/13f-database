from dash import Dash, html, dcc, Input, Output, State, callback
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

SLIDERTEXT = """
## Slider to define pie plots
Set value is lowest index of first pieplot in a set of 4 to plot
"""

SUMMARYBARPLOTTEXT = """
## Barplot that summarizes total holdings
Plot that holds the sum of all VALUE columns for each year and quartal"""

app.layout = html.Div(children = [
    dcc.Markdown(children = SUMMARYBARPLOTTEXT),
    dcc.Input(id = "query_company", value = "+Cameco", type = "text"),
    html.Button(id = "submit_query", children = "Submit"),
    dcc.Graph(id = "managers_barplot"),
    dcc.Markdown(children = SLIDERTEXT),
    dcc.Slider(id = "pie_ix", min = 0, step = 1, value = 0),
    dcc.Graph(id = "pie_plot"),
    dcc.Loading(dcc.Store(id = "querystore"), fullscreen = True)
])

@callback(
    [Output("querystore", "data"),
     Output("pie_ix", "max")],
    inputs = Input("submit_query", "n_clicks"),
    state = State("query_company", "value")
)
def get_top_holders_plots(n_clicks: int, company_query: str) -> dict:
    """Make database query and return the 2 plot types

    Args:
        company_query (str): Company to query in SQL BOOLEAN mode query
        pie_ix (int): Which pie plot will be the first of 4
    """
    query_str, param_dic = queryfunctions.top_holders(company_query)
    df = pd.read_sql_query(query_str, params = param_dic, con = engine)
    max_n_timeperiods = df[["YEAR", "QUARTAL"]].drop_duplicates().shape[0] - 4
    
    return df.to_dict(), max_n_timeperiods

@callback(output = [Output("managers_barplot", "figure"),
                     Output("pie_plot", "figure")],
           inputs = [Input("pie_ix", "value"),
                     Input("querystore", "data")])
def get_plots(pie_ix, df_dic) -> (go.Figure, go.Figure):
    df = pd.DataFrame(df_dic)
    plotter = plotfunctions.nameofissuer_plotter(df)
    
    barplot = plotter.get_bar_plot()
    pieplot = plotter.get_pie_plot(pie_ix)
    
    return barplot, pieplot

if __name__ == "__main__":
    app.run(debug = True)
    