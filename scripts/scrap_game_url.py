"""Récuppère les urls des jeux sur la page qui les regroupe"""

import requests
from bs4 import BeautifulSoup
from typing import List


def recuperation_url_jeux() -> List[str]:
    """Retourne la liste des urls des pages des jeux"""
    liste_url = []

    URL = "https://opencritic.com/browse/all"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    games = soup.find_all("div", class_="row no-gutters py-2 game-row align-items-center")

    for game in games:
        game_url = game.find("div", class_="game-name col ml-2")
        a = game_url.find('a', href=True)
        if a:
            liste_url.append("https://opencritic.com" + a['href'])
    
    return liste_url




