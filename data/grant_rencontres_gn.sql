-- Droits de lecture seule pour l'utilisateur rencontres_gn sur une base GeoNature
-- À exécuter en tant que propriétaire des schémas (ou superutilisateur)

DO $$
BEGIN
    EXECUTE format('GRANT CONNECT ON DATABASE %I TO rencontres_gn', current_database());
END
$$;

-- Repart de zéro : retire tout droit existant (écriture, CREATE...) sur ces schémas
REVOKE ALL ON ALL TABLES IN SCHEMA
    pr_occtax,
    gn_synthese,
    gn_meta,
    gn_commons,
    taxonomie,
    ref_nomenclatures,
    ref_geo,
    gn_sensitivity,
    gn_exports,
    utilisateurs
FROM rencontres_gn;

REVOKE ALL ON ALL SEQUENCES IN SCHEMA
    pr_occtax,
    gn_synthese,
    gn_meta,
    gn_commons,
    taxonomie,
    ref_nomenclatures,
    ref_geo,
    gn_sensitivity,
    gn_exports,
    utilisateurs
FROM rencontres_gn;

REVOKE ALL ON SCHEMA
    pr_occtax,
    gn_synthese,
    gn_meta,
    gn_commons,
    taxonomie,
    ref_nomenclatures,
    ref_geo,
    gn_sensitivity,
    gn_exports,
    utilisateurs
FROM rencontres_gn;

-- Schémas en lecture complète
GRANT USAGE ON SCHEMA
    pr_occtax,
    gn_synthese,
    gn_meta,
    gn_commons,
    taxonomie,
    ref_nomenclatures,
    ref_geo,
    gn_sensitivity,
    gn_exports
TO rencontres_gn;

-- SELECT sur toutes les tables, vues et vues matérialisées existantes
GRANT SELECT ON ALL TABLES IN SCHEMA
    pr_occtax,
    gn_synthese,
    gn_meta,
    gn_commons,
    taxonomie,
    ref_nomenclatures,
    ref_geo,
    gn_sensitivity,
    gn_exports
TO rencontres_gn;

-- Schéma utilisateurs : uniquement bib_organismes et t_roles (sans pass, pass_plus, email)
GRANT USAGE ON SCHEMA utilisateurs TO rencontres_gn;

GRANT SELECT ON utilisateurs.bib_organismes TO rencontres_gn;

DO $$
DECLARE
    cols text;
BEGIN
    SELECT string_agg(quote_ident(column_name), ', ' ORDER BY ordinal_position)
    INTO cols
    FROM information_schema.columns
    WHERE table_schema = 'utilisateurs'
      AND table_name = 't_roles'
      AND column_name NOT IN ('pass', 'pass_plus', 'email');

    EXECUTE format('GRANT SELECT (%s) ON utilisateurs.t_roles TO rencontres_gn', cols);
END
$$;
