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


def add_observation(cd_nom, nom_cite, lat, lon):
    payload = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},  # lon, lat (WGS84)
        "properties": {
            "id_dataset": 1,
            "date_min": "2026-10-28",
            "date_max": "2026-10-28",
            "id_nomenclature_grp_typ": 132,  # type de regroupement
            "observers_txt": "Jacques Fize",  # or "observers_txt": "Nom"
            "t_occurrences_occtax": [
                {
                    "cd_nom": cd_nom,
                    "nom_cite": nom_cite,
                    "id_nomenclature_obs_technique": 41,
                    "id_nomenclature_bio_condition": 157,
                    "id_nomenclature_bio_status": 29,
                    "id_nomenclature_naturalness": 160,
                    "id_nomenclature_exist_proof": 81,
                    "id_nomenclature_observation_status": 88,
                    "id_nomenclature_blurring": 175,
                    "id_nomenclature_source_status": 75,
                    "id_nomenclature_determination_method": 445,
                    "cor_counting_occtax": [
                        {
                            "id_nomenclature_life_stage": 2,
                            "id_nomenclature_sex": 168,
                            "id_nomenclature_obj_count": 146,
                            "id_nomenclature_type_count": 94,
                            "count_min": 1,
                            "count_max": 1,
                        }
                    ],
                }
            ],
        },
    }

    response = requests.post(
        f"{st.secrets['geonature']['api_url']}/occtax/releve",
        headers={"Authorization": f"Bearer {get_token()}"},
        json=payload,
    )
    if response.status_code != 200:
        print(response.text)
    return response.status_code
