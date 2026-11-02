# Atelier Connexion d'une application avec GeoNature

Dans cette atelier, l'objectif est de montré quels sont les différentes entrées pour récupérer (de manière dynamique) et saisir des données dans GeoNature et les valoriser dans une application. 


## Trois grand groupe d'accès au données 

L'accès aux données de GeoNature

### API

GeoNature est une application divisée en deux parties: (1) le _frontend_: l'interface client, (2) le _backend_ (entre autre) qui s'occupe de retourner les données à l'interface pour que ces dernières soient affichées. On parle aussi d'API.

C'est cette dernière partie qui nous intéresse ! Cette API est utilisable à l'aide du protocole HTTP. Ce protocole d'échange de données est implémenté dans une large partie des langages de programmations mais aussi de data analyse.

Par exemple, il est possible de récupérer la liste des cadres d'acquisitions avec l'adresse suivante :

`/meta/acquisition_frameworks`

```json
{
  "has_next": true,
  "has_prev": false,
  "items": [
    {
      "acquisition_framework_desc": "Inventaire amphibiens, odonates et flore de zone humide avant et aprés travaux par struture GEMAPI du 82",
      "acquisition_framework_end_date": "2025-10-31",
      "acquisition_framework_name": "AAP Entente sur l'Eau Restauration de ZH en tête de BV 82",
      "acquisition_framework_parent_id": null,
      "acquisition_framework_start_date": "2021-01-01",
      "additional_data": {
        "test number": 0
      },
      "cor_af_actor": [
        {
          "id_acquisition_framework": 58,
          "id_cafa": 82,
          "id_nomenclature_actor_role": 363,
          "id_organism": 14,
          ...
        }
      ]
    },
    ...
  ]
}
```

Dans une requête, il est possible d'ajouter des paramètres pour filtrer les données.


### Export

Un des points d'entrée les plus affichées est le module Export. Pour rappel, le module Export permet
de définir une "vue" (un objet de base de données)

#### Export - Fichier (statique)



#### Export - API

### SQL 




## Streamlit
Pour développer cette application, nous prenons un framework simple d'utilisation : [Streamlit](https://streamlit.io/). Ce framework a pour avantage de proposer une programmation simple et très haut-niveau. Par exemple, ce code suffit à afficher un formulaire pour calculer la distance entre deux coordonnées : 

```python
import streamlit as st
from geopy.distance import geodesic



st.header("Application de calcul de distance géodésique")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Premières coordonnées")
    lon1 = st.number_input("lon1")
    lat1 = st.number_input("lat1")
with col2:
    st.subheader("Deuxièmes coordonnées")
    lon2 = st.number_input("lon2")
    lat2 = st.number_input("lat2")
distance_km = None

if lon1 and lat1 and lon2 and lat2:
    distance_km = geodesic((lon1, lat1), (lon2, lat2))

st.header("Résultat")
if distance_km:
    st.write(f"Distance entre les deux coordonnées {distance_km}")
else:
    st.write("Indiquer des coordonnées")
```

`streamlit` est construit autour de méthodes permettant de faire des choses simples avec le moins de ligne de code possible. Dans l'exemple ci-dessus :

 - `st.write` affiche du texte 
 - `st.number_input` créer un formulaire pour saisir un nombre et le stock dans la variable associée. **Si une valeur d'un formulaire est modifiée, alors l'ensemble du code qui utilise les variables associées (ici, `lon1, lon2, lat1, lat2`) se relance.**
 - `st.subheader` créer un sous-titre et `st.header` créer un titre.
 - `st.columns(n)` créer deux colonnes


 Pour plus d'informations, rendez-vous sur la doc de [**Streamlit** ](https://docs.streamlit.io/develop/api-reference)


<div class="alert aler-block alert-info">
    Dans ce tutoriel, nous utilisons <strong>Streamlit</strong> pour sa simplicité et la rapidité pour mettre en place rapidement des POCs. Toutefois, ils existent plusieurs technologies --chacune avec ses avantages et inconvénients-- permettant de faire de la visualisation de données. Pour n'en citer qu'une infime partie : 
    <ul>
        <li><img src="https://cdn.simpleicons.org/python" height="20"> Dash est un framework Python spécialisée dans la création d'application Web pour la création de dashboard. Il s'appuie principalement sur Plotly une librairie utilisé pour générer des graphiques interactifs. <a href="https://dash.plotly.com/">https://dash.plotly.com/</a></li>
        <li><img src="https://cdn.simpleicons.org/r" height="20">
 RShiny est un autre framework de création de Dashboard bien connu de la communauté R. Très puissant, stable et supporté par les créateurs de R. <a href="https://dash.plotly.com/">https://dash.plotly.com/</a></li>
        <li><img src="https://cdn.simpleicons.org/grafana" height="20">Grafana est un outil de monitoring qui permet de créer des dashboards. Plutôt utilisées comme outils de surveillance la plupart du temps. Malgré tout, il est possible de créer des graphiques en s'appuyant sur des données provenant d'API. A la différence des précédents, ce dernier ne demande pas de "coder" vu que les dashboards sont fait uniquement à l'aide d'une interface. <a href="https://grafana.com/">https://grafana.com/</a> </li>
        <li><img src="https://cdn.simpleicons.org/gradio" height="20"> Gradio est un framework qui permet de faire des interfaces Web mais plus orienté pour sa connectivité avec les modèles de machine-learning, deep-learning, etc. <a href="https://gradio.app/">https://gradio.app/</a></li>
        <li>Autres : <a href="https://observablehq.com/">Observable</a> (équivalent notebook 100% JS, uniquement utilisable en ligne), <a href="https://flet.dev/">Flet</a> </li>
    </ul>
</div>




## Préparer son environnement de développement

Comme vous l'avez peu-être devinez, nous allons nous appuyer sur le langage Python pour cette atelier !  

### Installer `uv`

Il est d'usage dans Python de créer des environnements virtuels pour cloisonner les applications et leur dépendances à certaines versions de librairies. Une des technologies récentes qui fait ses preuves dans la communauté est `uv`.

Pour installer `uv`, je vous recommande la documentation officielle :https://docs.astral.sh/uv/getting-started/installation/

**Pour les utilisateurs de Windows** UV est compatible avec Windows mais il est possible de créer des environnements virtuelles avec Anaconda.

### Créer un environnement virtuel et installer les librairies

Il suffit de lancer la commande `uv sync`.

Un fois terminée, lancer `uv run check_env.py` pour vérifier que l'environnement virtuel est bien installé !

### Lancement de l'app