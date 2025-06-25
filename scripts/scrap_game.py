import re
from scrap_game_url import *
from typing import List


class Scraper:
    def __init__(self):
          self.titre = ""
          self.note = ""
          self.date = ""
          self.commentaires_journaliste = []
          self.commentaires_joueurs = []
          self.jeux = [] ## permet de stocker les données 


    def parcourir_url(self, liste_url):
        for url in liste_url:
            soup = self.extraire_elements(url)
            self.reccuperer_donnees_principales(soup) 
            self.reccuperer_commentaires_journaliste(url)
            self.reccuperer_commentaires_joueurs(url)
            self.jeux.append({
                "titre": self.titre,
                "note": self.note,
                "date": self.date,
                "commentaires_journaliste": self.commentaires_journaliste.copy(),
                "commentaires_joueurs": self.commentaires_joueurs.copy()
            })
            self.afficher_jeux()


    def extraire_elements(self, url) -> BeautifulSoup:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
         

    def reccuperer_donnees_principales(self, soup : BeautifulSoup):   
        """On va parser la page pour réccupérer le titre, la date et la note"""

        titre = soup.find("h1", class_="my-2 my-md-4") 
        if titre:
                self.titre = titre.text.strip()   
        else:
                "Titre non trouvé"

        date = soup.find("div", class_="platforms") 
        if date:
                texte = date.text.strip()
                match = re.search(r"Release Date:\s*(.*?)\s*-\s*", texte)
                if match:
                    self.date = match.group(1)
                else:
                    self.date = "Date non trouvée"
        else:
            self.date = "Date non trouvée"

        notation = soup.find("div", class_="inner-orb") 
        if notation:
                self.note = notation.text.strip()
        else:
                "Note non trouvée"


    def reccuperer_commentaires_journaliste(self, url) -> List[str]:
        page = requests.get(url+ "/reviews")
        soup = BeautifulSoup(page.content, "html.parser")
        commentaires = soup.find_all("p", class_="mb-0 wspw")
        self.commentaires_journaliste = [self.nettoyer_texte(commentaire.text) for commentaire in commentaires]
     

    def reccuperer_commentaires_joueurs(self, url) -> List[str]:
        page = requests.get(url+ "/user-reviews")
        soup = BeautifulSoup(page.content, "html.parser")
        commentaires = soup.find_all("div", class_="w-100 excerpt")
        self.commentaires_joueurs = [self.nettoyer_texte(commentaire.text) for commentaire in commentaires]
     

    def nettoyer_texte(self, commentaire : str) -> str:
        """Pour retirer les caractères unicode spéciaux"""
        return commentaire.replace("\\'", "'").replace('\u200e', '').replace('\xa0', ' ').replace('\n', ' ').strip()


    def afficher_jeux(self):
        for jeu in self.jeux:
            print(f"Titre : {jeu['titre']}")
            print(f"Note : {jeu['note']}")
            print(f"Date : {jeu['date']}")
            print("Commentaires journaliste :")
            for c in jeu['commentaires_journaliste'][:3]:
                print(f"  - {c}")
            print("Commentaires joueurs :")
            for c in jeu['commentaires_joueurs'][:3]:
                print(f"  - {c}")
            print("\n" + "-"*40 + "\n")
            


liste_url = recuperation_url_jeux()
scraper = Scraper()
scraper.parcourir_url(liste_url)