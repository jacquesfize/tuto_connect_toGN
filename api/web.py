import streamlit as st
import requests


def get_token():
    response = requests.post(
        f"{st.secrets['geonature']['api_url']}/auth/login",
        json={
            "login": st.secrets["geonature"]["login"],
            "password": st.secrets["geonature"]["password"],
        },
    )
    return response.json().get("token")


class GeoNatureClient:
    """Thin client for the GeoNature API: base URL and authentication in one place."""

    def __init__(self):
        self.base_url = st.secrets["geonature"]["api_url"]
        self.token = get_token()

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        return requests.request(
            method,
            f"{self.base_url}{path}",
            headers={"Authorization": f"Bearer {self.token}"},
            **kwargs,
        )

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    # --- synthese -------------------------------------------------------
    def get_observations(self, limit: int = 100, query_params: dict = {}, **filters):
        return self.post(
            "/synthese/for_web", params={"limit": limit, **query_params}, json=filters
        ).json()

    # --- taxhub ---------------------------------------------------------
    def autocomplete_taxons(self, search_str: str = None, full: bool = False):
        if not search_str:
            return []
        data = self.get(f"/taxhub/api/taxref/search/nom_valide/{search_str}").json()
        if full:
            return [
                (
                    t["nom_valide"],
                    {
                        "nom_valide": t["nom_valide"],
                        "cd_nom": t["cd_nom"],
                    },
                )
                for t in data
            ]
        return [(t["nom_valide"], t["cd_ref"]) for t in data]

    # --- nomenclatures --------------------------------------------------
    @st.cache_data(show_spinner=False, ttl=3600)
    def get_nomenclatures(_self, code_type: str) -> list:
        """Active terms of a nomenclature type (e.g. "STATUT_BIO")."""
        response = _self.get(f"/nomenclatures/nomenclature/{code_type}")
        if response.status_code != 200:
            return []
        return response.json().get("values", [])

    @st.cache_data(show_spinner=False, ttl=3600)
    def get_default_nomenclatures(_self, *code_types: str) -> dict:
        """{code_type: id_nomenclature} of the Occtax default nomenclatures."""
        response = _self.get(
            "/occtax/defaultNomenclatures", params={"id_type": list(code_types)}
        )
        if response.status_code != 200:
            return {}
        return response.json()

    # --- occtax ---------------------------------------------------------
    def add_releve(self, payload: dict) -> requests.Response:
        return self.post("/occtax/releve", json=payload)


@st.cache_resource(ttl=3600, show_spinner=False)
def get_client() -> GeoNatureClient:
    """The one shared client; rebuilt every hour so the token stays fresh."""
    return GeoNatureClient()
