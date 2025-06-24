"""Creation et insertion des données dans la database """

import sqlite3 
from sqlite3 import Error
from scrap_game import *





def creation_connexion(path):
    connexion = None
    try:
        connexion = sqlite3.connect(path)
        print("Connexion réussie")
    except Error as e:
        print(f"Erreur : {e}")

    return connexion


scraper = Scraper()
liste_url = recuperation_url_jeux()
scraper.parcourir_url(liste_url)
data = [(scraper.titre, scraper.note, scraper.date)]


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        cursor.executemany('''INSERT INTO GAMES (titre, note, date) VALUES (?,?,?)''', data)
        cursor.close()
    except Error as e:
        print(f"The error '{e}' occurred")


create_games_table = """
CREATE TABLE IF NOT EXISTS GAMES (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titre TEXT NOT NULL,
  note INTEGER,
  date DATE
);
"""



connection = creation_connexion("../data/sm_app.sqlite")
execute_query(connection, create_games_table)
