"""Récuppère les urls des jeux sur les 250 premieres pages du site OpenCritic et les sauvegarder dans un json"""

import requests
from bs4 import BeautifulSoup
from typing import List
import ujson


def recuperation_url_jeux(URL, liste_url) -> List[str]:
    """Retourne la liste des urls des pages des jeux"""
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    games = soup.find_all("div", class_="row no-gutters py-2 game-row align-items-center")

    for game in games:
        game_url = game.find("div", class_="game-name col ml-2")
        a = game_url.find('a', href=True)
        if a:
            liste_url.append("https://opencritic.com" + a['href'])

    return liste_url

def parcourir_les_pages() -> List[str]:
    liste_url = []
    for page in range(1,251):
        
        URL = f"https://opencritic.com/browse/all?page={page}" 
        recuperation_url_jeux(URL, liste_url)
        print(f"Page {page}")

    return liste_url


def sauvegarder_url(batch, file_path):
    """sauvegardes de la liste de toutes les url avec ujson"""
    with open(file_path, 'w') as f:
        ujson.dump(batch, f, indent=2)



def batcher_json(liste_urls, taille_batch=50):
    "Créer des batchs de la liste de nos urls afin d'alléger le scrapping plus tard"
    batch_nombre = 1
    for url in range(0, len(liste_urls), taille_batch):
        batch = liste_urls[url: url + taille_batch]
        file_json_path =f"../data/json/batch_urls_{batch_nombre}.json"
        batch_nombre += 1
        sauvegarder_url(batch, file_json_path)
    

def main():
    toutes_urls = parcourir_les_pages()
    print(toutes_urls)
    print(len(toutes_urls))
    batcher_json(toutes_urls)



if __name__ == "__main__":
    main()