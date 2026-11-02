from streamlit_searchbox import st_searchbox
from api.web import get_client


def taxref_input(session_key: str = "cd_nom"):
    return st_searchbox(
        lambda search: get_client().autocomplete_taxons(search),
        placeholder="Search Taxref... ",
        key=session_key,
    )
