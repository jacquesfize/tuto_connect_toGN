import streamlit as st
import requests


def get_token():
    url = f"{st.secrets['geonature']['api_url']}/auth/login"
    response = requests.post(
        url,
        json={
            "login": st.secrets["geonature"]["login"],
            "password": st.secrets["geonature"]["password"],
        },
    )
    return response.json().get("token")


def get_observations(token: str = None, limit: int = 100, **filters):
    if not token:
        token = get_token()
    url = f"{st.secrets['geonature']['api_url']}/synthese/for_web?limit={limit}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(url, headers=headers, json=filters)
    return response.json()


def autocomplete_taxons(search_str: str = None, token: str = None, full: bool = False):
    if not token:
        token = get_token()
    if not search_str:
        return []
    data = requests.get(
        f"{st.secrets['geonature']["api_url"]}/taxhub/api/taxref/search/lb_nom/{search_str}",
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    if full:
        return [
            (t["lb_nom"], {"lb_nom": t["lb_nom"], "cd_nom": t["cd_nom"]}) for t in data
        ]
    return [(t["lb_nom"], t["cd_ref"]) for t in data]
