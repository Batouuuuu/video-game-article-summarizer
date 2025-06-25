"""Creation et insertion des données dans la database """
import sqlite3 
from sqlite3 import Error
from scrap_game import Scraper, recuperation_url_jeux


def creation_connexion(path):
    connexion = None
    try:
        connexion = sqlite3.connect(path)
        print("Connexion réussie")
        
    except Error as e:
        print(f"Erreur : {e}")

    return connexion


def creation_tables(connection, reset= True):
    """Création des 3 tables"""
    cursor = connection.cursor()

    if reset: 
    ## supression des tables
        tables = ["COMMENTAIRES_JOURNALISTES", "COMMENTAIRES_JOUEURS", "JEUX"]
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")

    try:

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS JEUX (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            note INTEGER,
            date   
            );
            """)
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS COMMENTAIRES_JOURNALISTES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texte TEXT NOT NULL,
            jeu_id INTEGER,
            FOREIGN KEY (jeu_id) REFERENCES JEUX(id) 
            );
            """)
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS COMMENTAIRES_JOUEURS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texte TEXT NOT NULL,
            jeu_id INTEGER,
            FOREIGN KEY (jeu_id) REFERENCES JEUX(id) 
            );
            """)
        
        
    except Error as e:
        print(f"Erreur : {e}")


def ajouter_donnees(connection, data):
    cursor = connection.cursor()
    for jeu in data:
        data_note_titre_date(cursor, jeu )
        last_id = cursor.lastrowid ## permet de garder l'id du jeu et de l'associer aux commentaires
        commentaires_journalistes(cursor, last_id, jeu)
        commentaires_joueurs(cursor, last_id, jeu)

    connection.commit()   


def data_note_titre_date(cursor, jeu):
    return cursor.execute('''INSERT INTO JEUX (titre, note, date) VALUES (:titre, :note, :date)''', jeu)

def commentaires_journalistes(cursor, last_id, jeu):
    liste_commentaires_journalistes = [{"texte": c, "jeu_id": last_id} for c in jeu["commentaires_journaliste"]]
    return cursor.executemany('''INSERT INTO COMMENTAIRES_JOURNALISTES  (jeu_id , texte) VALUES (:jeu_id , :texte)''', liste_commentaires_journalistes)

def commentaires_joueurs(cursor, last_id, jeu):
    liste_commentaires_joueurs = [{"texte": c, "jeu_id": last_id} for c in jeu["commentaires_joueurs"]]
    return cursor.executemany('''INSERT INTO COMMENTAIRES_JOUEURS  (jeu_id , texte) VALUES (:jeu_id , :texte)''', liste_commentaires_joueurs)


def verification(connection):
    cursor = connection.cursor()
    for row in cursor.execute("SELECT jeu_id, texte FROM COMMENTAIRES_JOURNALISTES"):
        print(row)


def main():
    scraper = Scraper()
    liste_url = recuperation_url_jeux()
    scraper.parcourir_url(liste_url)

    connection = creation_connexion("../data/sm_app.sqlite")
    creation_tables(connection)
    ajouter_donnees(connection, scraper.jeux)
    # verification(connection)


if __name__ == "__main__":
    main()