import re
from scrap_game_url import *
from typing import List


liste_url = recuperation_url_jeux()



class Scraper:
    def __init__(self):
          self.titre = ""
          self.note = ""
          self.date = ""
          self.commentaires_journaliste = []
          self.commentaires_joueurs = []


    def parcourir_url(self, liste_url):
        for url in liste_url:
            self.reccuperer_note(url) 
            self.reccuperer_commentaires_journaliste(url)
            self.reccuperer_commentaires_joueurs(url)


    def reccuperer_titre(self, titre):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        titre = soup.find("h1", class_="my-2 my-md-4")
        if titre:
                self.titre = titre.text.strip()
        else:
                "Titre non trouvé"

    def reccuperer_date(self, date):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
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


    def reccuperer_note(self, url):
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
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



    def afficher(self):
        print(f"Titre : {self.titre}")
        print(f"Note : {self.note}")
        print(f"Date : {self.date}")
        print(f"\nCommentaires journaliste ({len(self.commentaires_journaliste)}) :")
        for c in self.commentaires_journaliste[:3]: 
            print(f"- {c}")
        print(f"\nCommentaires joueurs ({len(self.commentaires_joueurs)}) :")
        for c in self.commentaires_joueurs[:3]:
            print(f"- {c}")
        print("\n")
         

for url in liste_url: 
    scraper = Scraper()
    scraper.reccuperer_note(url)
    scraper.reccuperer_titre(url)
    scraper.reccuperer_date(url)
    scraper.reccuperer_commentaires_journaliste(url)
    scraper.reccuperer_commentaires_joueurs(url)
    scraper.afficher()