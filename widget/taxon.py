from streamlit_searchbox import st_searchbox
from api.web import get_client


def taxref_input(session_key: str = "cd_nom", full: bool = False):
    """Taxref search box: returns cd_ref, or {nom_valide, cd_nom} if `full`."""
    return st_searchbox(
        lambda search: get_client().autocomplete_taxons(search, full),
        placeholder="Search Taxref... ",
        key=session_key,
    )
