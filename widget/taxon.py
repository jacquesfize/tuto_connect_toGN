from streamlit_searchbox import st_searchbox
from ..api.web import autocomplete_taxons


def taxref_input(session_key: str = "cd_nom"):
    return st_searchbox(
        autocomplete_taxons,
        placeholder="Search Taxref... ",
        key=session_key,
    )
