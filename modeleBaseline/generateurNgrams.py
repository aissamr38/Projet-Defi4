# Ce scripte permet d'extraire les ngrams  avec leurs occurences dans tout le corpus,
# nous extrayons les ML-2 et ML-3,
# en respectant la syntaxe : mot \t mot\t occurence pour le ML-2, et mot \t mot\t mot\t occurence pour le ML-3,
# Les fichiers générer ce sont : dataBiGrams.txt et dataTriGrams.txt  
# Les fichiers seront sotcker dans le même réprtoir où le script était lancé

from pathlib import Path
import os
from pickle import EMPTY_DICT

import nltk
import nltk
from nltk import word_tokenize
from nltk.util import bigrams, ngrams
from collections import Counter
import random




# focntion qui permet de lire le contenu de chaque fichier dans le corpus
def lireFichier(fichier):
    with open(fichier, encoding='utf-8', errors='ignore') as f:
        content = f.readlines()
    return content



pathGlobale = "/home/aissam/Bureau/CERI M2/S9/Application D'innovation/TORESS/MEGALITE_FR/"

contentFile = ""
text = ""

corpus = []

for root, directories, files in os.walk(pathGlobale, topdown=False):
	for name in files:
         if name.endswith('.seg'):
            path_file = os.path.join(root, name)
            print(path_file)
            corpus.append(lireFichier(path_file))


frequencies = Counter([])


print(len(corpus))


tableauOfBigrammes = {}


dictionnaire = dict()

""" On Extrait tout les Bigrame dans le corpus, en calculant aussi leur occurences
"""

for text in corpus:
    lesNgrams = ngrams(str(text).split(), 2)
    for grams in lesNgrams:
        valeur = " ".join(grams)
        if valeur in dictionnaire :
            dictionnaire[valeur] += 1
        else :
            dictionnaire[valeur] = 1
        

with open("dataBiGrams.txt", "w") as fichier:
    #fichier.write(frequencies)
    for key in dictionnaire:
        ocuurence = dictionnaire[key]
        mot = key.replace("\\n","").replace("'","").replace(",","").replace(";","").replace("?","").replace("\n","") + "\t" + str(ocuurence) +"\n"
        fichier.write(mot)



# On génère tout les Trigrame (ML-3) avec leur occurences 

for text in corpus:
    lesNgrams = ngrams(str(text).split(), 3)
    for grams in lesNgrams:
        valeur = " ".join(grams)
        if valeur in dictionnaire :
            dictionnaire[valeur] += 1
        else :
            dictionnaire[valeur] = 1
        

with open("dataTriGrams.txt", "w") as fichier:
    #fichier.write(frequencies)
    for key in dictionnaire:
        ocuurence = dictionnaire[key]
        mot = key.replace("\\n","").replace("'","").replace(",","").replace(";","").replace("?","").replace("\n","") + "\t" + str(ocuurence) +"\n"
        fichier.write(mot)




dictionnaireDesSucesseur={}

def genererPhrase(word):
    for key in dictionnaire:
        if key.startswith(word):
            print(key)
            dictionnaireDesSucesseur[key] = dictionnaire[key]
    
    sentence = ""
    return sentence

sorted_d = dict(sorted(dictionnaireDesSucesseur.items(), key=lambda t: t[1],reverse=True))

