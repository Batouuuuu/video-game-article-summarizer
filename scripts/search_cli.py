"""Recherche à travers la base de données"""

import argparse 
import sqlite3
from elasticsearch import Elasticsearch

parser = argparse.ArgumentParser(
                    prog='VideoGameSummarizer',
                    description="Ce programme affiche les notes ainsi qu'un résumé automatique des critiques des joueurs et de la presse.",
                    epilog='Exemple : python search_cli.py "Zelda"')


parser.add_argument('game_name', help="Jeu que vous voulez recherher")      



args = parser.parse_args()
print(args.game_name)

con = sqlite3.connect("data/sm_app.sqlite")
cur = con.cursor()
param = "%" + args.game_name + "%"
res = cur.execute("SELECT * FROM JEUX WHERE titre LIKE ?", (param,))
print(res.fetchone())