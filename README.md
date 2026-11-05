# tuto_connect_toGN

## Installation

Prérequis : [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
git clone https://github.com/jacquesfize/tuto_connect_toGN.git
cd tuto_connect_toGN
sudo apt install libpq-dev
uv sync
```

## Configuration

```bash
cp .streamlit/secrets.toml.sample .streamlit/secrets.toml
```

Renseigner l'URL de l'API GeoNature, les identifiants et la connexion à la base dans `.streamlit/secrets.toml`.

## Lancement

```bash
uv run streamlit run main.py
```
