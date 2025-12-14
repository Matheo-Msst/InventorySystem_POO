import json
import random
from Domain.item.item import Item 
from Domain.item.arme import Arme
from Domain.item.objet import Objet
from Domain.item.armure import Armure
from Domain.item.rareter import Rareter

class Item_factory:

    def generer_rareter(self): 
        r = random.random() 
        cumul = 0 
        for rareter in Rareter: 
            cumul += rareter.chance_drop() 
            if r <= cumul: 
                return rareter 

    def arme_aleatoire(self) :
        #chemin vers le JSON
        with open("infrastructure/arme_data.json", "r", encoding="utf-8") as f:
            armes= json.load(f)
    
        resultat = random.choice(armes)

        return Arme(
            nom=resultat["nom"],
            rareter= self.generer_rareter(),
            degat= resultat["degat"],
            porter= resultat["porter"]
        )
    
    def armure_aleatoire(self) :
         #chemin vers le JSON
        with open("infrastructure/armure_data.json", "r", encoding="utf-8") as f:
            armures= json.load(f)
    
        resultat = random.choice(armures)

        return Armure(
            nom=resultat["nom"],
            point_armure= resultat["point_armure"],
            soliditer = resultat ["soliditer"]         
        )
    
    def objet_aleatoire(self) :
        #chemin vers le JSON
        with open("infrastructure/objet_data.json", "r", encoding="utf-8") as f:
            objets = json.load(f)
    
        resultat = random.choice(objets)

        return Objet(
            nom=resultat["nom"] ,
            type = resultat["type"], 
            soin = resultat.get("soin")
        )
    
    def choix_aleatoire(self) :
        """ Choix de l'objet entre l'arme , l'armure et l'objet"""
        categorie = random.choice(["armes", "armure", "objet"])
        if categorie == "armes" :
            return self.arme_aleatoire()
        elif categorie == "armure" :
            return self.armure_aleatoire()
        else :
            return self.objet_aleatoire()