""" Constitution de la classe Scrapper en se servant des batches, et en faisant des requetes sur les url contenues dans les pages. 
Utilisation d'un User-agent et d'un sleep pour controler le scrapping et ne pas saturer le service.
La class Scrapper est ensuite enregistrer sous format json"""

import re
from scrap_game_url import BeautifulSoup, requests, ujson
from pathlib import Path
from typing import List
import time

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
class Scraper:
    def __init__(self):
          self.titre = ""
          self.note = ""
          self.date = ""
          self.plateforme = ""
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
                "plateforme": self.plateforme,
                "commentaires_journaliste": self.commentaires_journaliste.copy(),
                "commentaires_joueurs": self.commentaires_joueurs.copy()
            })
            # self.afficher_jeux()


    def extraire_elements(self, url) -> BeautifulSoup:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup
         

    def reccuperer_donnees_principales(self, soup : BeautifulSoup):   
        """On va parser la page pour réccupérer le titre, la date et la note"""

        titre = soup.find("h1", class_="my-2 my-md-4") 
        if titre:
                self.titre = titre.text.strip()   
        else:
                "Titre non trouvé"

        ## on reccupére la date et les plateformes
        date_div = soup.find("div", class_="platforms") 
        if date_div:
                texte = date_div.text.strip()
                match = re.search(r"Release Date:\s*(.*?)\s*-\s*", texte)
                if match:
                    self.date = match.group(1)
                    plateformes = []

                    ## pour réccupérer les plateformes
                    spans = date_div.find_all('span')
                    for span in spans:
                        strong = span.find('strong')
                        if strong:
                            plateformes.append(strong.text.strip())
                            self.plateforme = ", ".join(plateformes) if plateformes else "Plateforme non trouvée"
        
                else:
                    self.date = "Date non trouvée"
                    self.plateforme = "Plateforme non trouvée"
                
        else:
            self.date = "Date non trouvée"
            self.plateforme = "Plateforme non trouvée"

        notation = soup.find("div", class_="inner-orb") 
        if notation:
                self.note = notation.text.strip()
        else:
                "Note non trouvée"


    def reccuperer_commentaires_journaliste(self, url) -> List[str]:
        page = requests.get(url+ "/reviews", headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        commentaires = soup.find_all("p", class_="mb-0 wspw")
        self.commentaires_journaliste = [self.nettoyer_texte(commentaire.text) for commentaire in commentaires]
     

    def reccuperer_commentaires_joueurs(self, url) -> List[str]:
        page = requests.get(url+ "/user-reviews", headers=headers)
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
            print(f"plateforme : {jeu['plateforme']}")
            print("Commentaires journaliste :")
            for c in jeu['commentaires_journaliste'][:3]:
                print(f"  - {c}")
            print("Commentaires joueurs :")
            for c in jeu['commentaires_joueurs'][:3]:
                print(f"  - {c}")
            print("\n" + "-"*40 + "\n")
            



def charger_json_batches(chemin : Path) -> List[Path]:
    """Trie les fichiers batches jsons"""
    
    batches = list(chemin.glob('../batches_urls/*.json'))
    batches_sorted = sorted(batches, key=lambda f: int(re.search(r'\d+', f.name).group()))
    return batches_sorted

def ouvrir_json(chemin, scrapper, batches : List[Path]):
    batch_number = 1
    for batch_json in batches: 
        with open(batch_json) as url_file:
            urls = ujson.load(url_file)
            scrapper.parcourir_url(urls)
           
            sauvegarder_scrapper_json(chemin, scrapper)
        batch_number +=1
        print(f"{batch_number}")
        time.sleep(10)
             
def sauvegarder_scrapper_json(file_path, scrapper):
    """Sauvegarder les resultats de notre class dans un json"""
    
    with open(file_path, 'w') as f:
        ujson.dump(scrapper.jeux, f, indent=2)



def main():
   
    scraper = Scraper()
    chemin_batches = Path('../data/json/batches_urls/')
    chemin_sauvegarde_fichier = "../data/json/scrapper_results.json"
    liste_batches_sorted = charger_json_batches(chemin_batches)
    ouvrir_json(chemin_sauvegarde_fichier, scraper, liste_batches_sorted)



main()


