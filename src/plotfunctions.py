from dash import Dash, html, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class nameofissuer_plotter:
    def __init__(self, df: pd.DataFrame, plottop: int = 10) -> None:
        """Plot 4 pie charts at a time, with arbitrary index
        Args:
            df (pd.DataFrame): Full dataframe with quartal data
        """
        df["YEAR"] = df["YEAR"].astype(int)
        df["QUARTAL"] = df["QUARTAL"].astype(int)
        df["VALUE"] = df["VALUE"].astype(int)
        plot_df = df.sort_values(["YEAR", "QUARTAL"])
        self.year_list, self.quartal_list, self.df_list_tmp = [], [], []
        
        for (year, quartal), df in plot_df.groupby(["YEAR", "QUARTAL"]):
            self.year_list.append(year)
            self.quartal_list.append(quartal)
            self.df_list_tmp.append(df.sort_values("VALUE", ascending = False))
            
        self.df_list = []
        for ix, df in enumerate(self.df_list_tmp):
            if df.shape[0] <= 10:
                self.df_list.append(df)
            else:
                df_top, df_low = df.iloc[:plottop], df.iloc[plottop:]
                other_ser = pd.Series(
                    ["OTHER", "OTHER", df_low["VALUE"].sum(), self.year_list[ix], self.quartal_list[ix]],
                    ["FILINGMANAGER_NAME", "NAMEOFISSUER", "VALUE", "YEAR", "QUARTAL"]
                )
                df_full = pd.concat([df_top, pd.DataFrame(other_ser).T])
                self.df_list.append(df_full)
            
    def get_pie_plot(self, firstplot_ix: int) -> None:
        """Plot 4 pie charts at a time, with arbitrary index

        Args:
            firstplot_ix (int): Index of first of 4 returned plots
        """
        firstplot_ix = min(firstplot_ix, len(self.df_list) - 4)
        
        fig = make_subplots(
            rows = 1,
            cols = 4,
            specs = [
                [
                    {"type": "pie"},
                    {"type": "pie"},
                    {"type": "pie"},
                    {"type": "pie"}
                ]
            ],
            subplot_titles = [
                f"{self.year_list[firstplot_ix]}:{self.quartal_list[firstplot_ix]}",
                f"{self.year_list[firstplot_ix+1]}:{self.quartal_list[firstplot_ix+1]}",
                f"{self.year_list[firstplot_ix+2]}:{self.quartal_list[firstplot_ix+2]}",
                f"{self.year_list[firstplot_ix+3]}:{self.quartal_list[firstplot_ix+3]}"
            ]
        )
        
        for j, i in enumerate(range(firstplot_ix, firstplot_ix + 4), 1):
            trace_dic = {
                "type": "pie",
                "labels": self.df_list[i]["FILINGMANAGER_NAME"],
                "values": self.df_list[i]["VALUE"],
                "hole": .3
            }
            
            fig.add_trace(trace_dic, row = 1, col = j)
            
        fig.update_layout(showlegend = False)
        return fig
        
    def get_bar_plot(self) -> None:
        """Plot a bar plot that summarizes the total amount of investments

        Args:
            firstplot_ix (int): Index of first of 4 returned plots
        """
        x_val, y_val = [], []
        for i, df in enumerate(self.df_list):
            x_val.append(f"{self.year_list[i]}:{self.quartal_list[i]}")
            y_val.append(df["VALUE"].sum())
            
        trace = {
            "type": "bar",
            "x": x_val,
            "y": y_val
        }
        
        layout = {
            "title": "Summary of total investments"
        }
        
        fig = go.Figure(trace, layout)
        return fig