import streamlit as st

from api.web import get_client
from utils import geojson_to_gdf


@st.cache_data(show_spinner="Loading observations...")
def load_observations(limit: int, **filters):
    return geojson_to_gdf(get_client().get_observations(limit, **filters))
