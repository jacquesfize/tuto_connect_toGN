"""Vérifie que l'environnement de l'atelier est correctement installé.

Usage : uv run python check_env.py
"""

import importlib
import sys
from importlib import metadata

MIN_PYTHON = (3, 13)

# (nom du module à importer, nom de la distribution pip)
PACKAGES = [
    ("flet", "flet"),
    ("flet_map", "flet-map"),
    ("folium", "folium"),
    ("geopandas", "geopandas"),
    ("geopy", "geopy"),
    ("IPython", "ipython"),
    ("psycopg2", "psycopg2"),
    ("requests", "requests"),
    ("sqlalchemy", "sqlalchemy"),
    ("streamlit", "streamlit"),
    ("streamlit_folium", "streamlit-folium"),
    ("streamlit_searchbox", "streamlit-searchbox"),
    ("watchdog", "watchdog"),
]

OK, KO = "[OK]", "[ERREUR]"


def check_python() -> bool:
    ok = sys.version_info >= MIN_PYTHON
    version = ".".join(map(str, sys.version_info[:3]))
    wanted = ".".join(map(str, MIN_PYTHON))
    print(f"{OK if ok else KO} Python {version} (>= {wanted} requis)")
    return ok


def check_package(module: str, dist: str) -> bool:
    try:
        importlib.import_module(module)
    except Exception as e:
        print(f"{KO} {dist} : import impossible ({type(e).__name__}: {e})")
        return False
    try:
        version = metadata.version(dist)
    except metadata.PackageNotFoundError:
        version = "?"
    print(f"{OK} {dist} {version}")
    return True


def main() -> int:
    results = [check_python()]
    results += [check_package(m, d) for m, d in PACKAGES]

    failed = results.count(False)
    print()
    if failed:
        print(f"{failed} vérification(s) en échec. Essayez : uv sync")
        return 1
    print("Tout est prêt pour l'atelier !")
    return 0


if __name__ == "__main__":
    sys.exit(main())
