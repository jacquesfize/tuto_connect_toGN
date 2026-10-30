import streamlit as st

LAST_OBSERVATIONS_QUERY = """
SELECT *
FROM gn_synthese.synthese
LIMIT 10;
"""

NEW_SPECIES_QUERY = lambda date: f"""
select distinct t.cd_ref, t.lb_nom, t.group2_inpn, t.regne, t.ordre, t.famille, string_agg(distinct observers, ', ')
    from gn_synthese.synthese s 
    join taxonomie.taxref t using(cd_nom)
    LEFT JOIN (
        select distinct t2.cd_ref
        from gn_synthese.synthese s2
        join taxonomie.taxref t2 ON s2.cd_nom = t2.cd_nom
        where s2.date_min < '{date}'
    ) as exist ON exist.cd_ref = t.cd_ref 
    where s.date_min > '{date}' and exist.cd_ref is null AND (t.id_rang = 'ES' OR t.id_rang = 'SSES')
    group by t.cd_ref, t.lb_nom, t.group2_inpn, t.regne, t.ordre, t.famille

"""


def last_observations():
    conn = st.connection("sql")
    df = conn.query(LAST_OBSERVATIONS_QUERY)
    conn.close()
    return df


def new_species(date: str):
    conn = st.connection("sql")
    df = conn.query(NEW_SPECIES_QUERY(date))
    conn.close()
    return df
