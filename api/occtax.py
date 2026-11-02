from api.web import get_client

# parameter name -> nomenclature type code
RELEVE_NOMENCLATURES = {
    "id_nomenclature_grp_typ": "TYP_GRP",  # type de regroupement
}
OCCURRENCE_NOMENCLATURES = {
    "id_nomenclature_obs_technique": "METH_OBS",
    "id_nomenclature_bio_condition": "ETA_BIO",
    "id_nomenclature_bio_status": "STATUT_BIO",
    "id_nomenclature_naturalness": "NATURALITE",
    "id_nomenclature_exist_proof": "PREUVE_EXIST",
    "id_nomenclature_observation_status": "STATUT_OBS",
    "id_nomenclature_blurring": "DEE_FLOU",
    "id_nomenclature_source_status": "STATUT_SOURCE",
    "id_nomenclature_determination_method": "METH_DETERMIN",
}
COUNTING_NOMENCLATURES = {
    "id_nomenclature_life_stage": "STADE_VIE",
    "id_nomenclature_sex": "SEXE",
    "id_nomenclature_obj_count": "OBJ_DENBR",
    "id_nomenclature_type_count": "TYP_DENBR",
}
ALL_NOMENCLATURES = {
    **RELEVE_NOMENCLATURES,
    **OCCURRENCE_NOMENCLATURES,
    **COUNTING_NOMENCLATURES,
}


def _with_defaults(values: dict, mapping: dict) -> dict:
    """Fill unset (None) nomenclatures with the Occtax defaults given by the API."""
    values = {k: values.get(k) for k in mapping}
    if any(v is None for v in values.values()):
        defaults = get_client().get_default_nomenclatures(*mapping.values())
        values = {
            k: defaults.get(mapping[k]) if v is None else v for k, v in values.items()
        }
    return {k: v for k, v in values.items() if v is not None}


def add_observation(
    cd_nom,
    nom_cite,
    lat,
    lon,
    id_dataset=1,
    date_min="2026-10-28",
    date_max=None,
    observers_txt="Jacques Fize",
    count=1,
    **nomenclatures,  # id_nomenclature_*: None/unset -> default value from the API
):
    unknown = set(nomenclatures) - set(ALL_NOMENCLATURES)
    if unknown:
        raise TypeError(f"Unknown nomenclature parameter(s): {sorted(unknown)}")

    counting = {
        **_with_defaults(nomenclatures, COUNTING_NOMENCLATURES),
        "count_min": count,
        "count_max": count,
    }
    occurrence = {
        "cd_nom": cd_nom,
        "nom_cite": nom_cite,
        **_with_defaults(nomenclatures, OCCURRENCE_NOMENCLATURES),
        "cor_counting_occtax": [counting],
    }
    payload = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},  # lon, lat (WGS84)
        "properties": {
            "id_dataset": id_dataset,
            "date_min": str(date_min),
            "date_max": str(date_max or date_min),
            "observers_txt": observers_txt,
            **_with_defaults(nomenclatures, RELEVE_NOMENCLATURES),
            "t_occurrences_occtax": [occurrence],
        },
    }

    response = get_client().add_releve(payload)
    if response.status_code != 200:
        print(response.text)
    return response.status_code
