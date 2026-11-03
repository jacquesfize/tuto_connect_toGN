import streamlit as st

from api.web import get_client
from utils import geojson_to_gdf


@st.cache_data(show_spinner="Loading data...")
def load_data_from_export(id_export: int, limit=1000, **filters):
    data = get_client().get_data_from_export(id_export, limit, **filters)
    return geojson_to_gdf(
        data
    )
