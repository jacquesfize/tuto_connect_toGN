import plotly.express as px
import pandas as pd
import streamlit as st

rank_hierarchy = "regne phylum classe ordre famille".split()


def taxon_distribution_plot(dataframe: pd.DataFrame, column: str):
    data = dataframe[column].value_counts().reset_index()
    data["percent"] = data["count"] / data["count"].sum()
    data = data[data.percent > 0.02]
    fig = px.pie(data, values="count", names=column)
    st.plotly_chart(fig)


def taxon_treemap_plot(dataframe):
    data = dataframe.copy()
    data["count"] = 1
    data.fillna("NSP", inplace=True)
    fig = px.treemap(
        data,
        path=[*rank_hierarchy, "lb_nom"],
        maxdepth=4,
        values="count",
        color="count",
    )
    st.plotly_chart(fig)
