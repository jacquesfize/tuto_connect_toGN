import streamlit as st

from api.occtax import add_observation
from api.sql_queries import new_species
from api.synthese import load_observations

from widget.taxon import taxref_input

import folium
from streamlit_folium import st_folium

st.title("Use GeoNature to build an app")


st.header("Parcourir les dernières observations (API)")
col1, col2 = st.columns(2)
with col1:
    limit = st.number_input("limit", 1, 25000, 10)
    cd_ref = taxref_input("cd_ref")
    st.write(f"Selected value: {cd_ref}")
    filters = {"cd_ref": [cd_ref]} if cd_ref else {}
with col2:
    st.map(load_observations(limit, **filters))

st.header("Nouvelles espèces découverte (SQL)")
col1, col2 = st.columns(2)
with col1:
    date = st.date_input("Date", "2020-01-01")
    species = new_species(date)
    event = st.dataframe(
        species,
        on_select="rerun",
        selection_mode="single-row",
        hide_index=True,
    )
with col2:
    rows = event.selection.rows
    if rows:
        selected_cd_ref = int(species.iloc[rows[0]]["cd_ref"])
        st.map(load_observations(limit, cd_ref=[selected_cd_ref]))
    else:
        st.info("Sélectionnez une ligne pour voir les observations sur la carte.")

st.header("Add a new Observation (API)")
taxon = taxref_input("taxon_add")

pick_map = folium.Map(location=[45.18, 5.72], zoom_start=8)
# keep the previously picked point visible
if "picked" in st.session_state:
    folium.Marker(st.session_state.picked).add_to(pick_map)

out = st_folium(pick_map, height=400, width=None, returned_objects=["last_clicked"])
lat, lon = None, None
if out and out.get("last_clicked"):
    st.session_state.picked = (out["last_clicked"]["lat"], out["last_clicked"]["lng"])

if "picked" in st.session_state:
    lat, lon = st.session_state.picked
    st.write(f"lat={lat:.5f}, lon={lon:.5f}")
if taxon and lat and lon:
    st.write(taxon["lb_nom"], taxon["cd_nom"], lat, lon)
    st.button(
        "Ajouter une obs",
        on_click=lambda: add_observation(taxon["cd_nom"], taxon["lb_nom"], lat, lon),
    )
