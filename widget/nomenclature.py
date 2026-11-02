import streamlit as st

from api.web import get_client


def nomenclature_input(code_type: str, label: str = None, session_key: str = None):
    """Searchable select box on a GeoNature nomenclature type.

    Returns the selected `id_nomenclature` (or None if nothing is selected).
    """
    terms = {n["id_nomenclature"]: n for n in get_client().get_nomenclatures(code_type)}
    return st.selectbox(
        label or code_type,
        options=list(terms),
        index=None,
        format_func=lambda i: f"{terms[i]['label_default']} ({terms[i]['cd_nomenclature']})",
        placeholder="Search nomenclature...",
        key=session_key or f"nomenclature_{code_type}",
    )
