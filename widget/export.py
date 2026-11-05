import streamlit as st

from api.web import get_client


def export_input(session_key: str = None):
    """Searchable select box on a GeoNature export ID.

    Returns the selected `id_export` (or None if nothing is selected).
    """
    list_id_export = get_client().get_list_id_exports()
    return st.selectbox(
        "ID Export",
        options=list_id_export,
        index=None,
        placeholder="Search ID export...",
        # key=session_key or f"export_{code_type}",
    )
