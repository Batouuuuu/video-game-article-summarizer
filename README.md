# Video Game Article Summarizer

Ce projet permet de rechercher dans une base de données des notes de jeux vidéo (+5000 jeux) de la platforme OpenCritic et de proposer un résumé automatique des avis de la presse et des joueurs grâce à Mistral.

2 modes d'utilisation sont disponibles :

- une recherche via CLI
- une recherche dans le frontend

## Prérequis

- **Node.js** pour faire tourner le frontend avec Vite.

- **Compte ElasticSearch** : Créez un compte sur [Elastic Cloud](https://www.elastic.co/cloud/) et générez une clé API pour accéder à votre instance ElasticSearch.

- **Python 3.x**  
  Pour exécuter le backend (CLI, traitement, appels API).  
  Assurez-vous d’avoir installé les dépendances Python via `requirements.txt`.

## Recherche avec la CLI
