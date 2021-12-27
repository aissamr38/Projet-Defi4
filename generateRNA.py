from pathlib import Path
import os
from pickle import EMPTY_DICT, TRUE
import nltk
from nltk import word_tokenize
from nltk.util import bigrams, ngrams
from collections import Counter
import random
import re
import pandas as pnd
import csv
from csv import reader
from scipy.spatial import distance
import numpy as np
import sys
import math
import operator



SGP = "Il n' y a ni *AQ0FS00/morale/moral ni *NCFS000/responsabilité/responsabilité en *NCFS000/littérature/littérature ."
#On recupère le les position qui existe de la SGP
res = re.findall(r'[*]\w+[/]\w+[/]\w+', SGP, flags=re.IGNORECASE)


print(res)

#la premier POS
pos_1 =  res[0].split('/')[0].replace("*","")
#le Premier mot
mot_1 =  res[0].split('/')[1].replace("*","")


#La deuxième POS
pos_2 =  res[1].split('/')[0].replace("*","")
#le deuxième mot
mot_2 =  res[1].split('/')[1].replace("*","")

print(pos_1)
print(mot_1)

print(pos_2)
print(mot_2)


# tableau des POS qui exstent dans la SGP
tableaux_POS = []
# Tableau des /mots  qui existent dans la SGP
tableaux_mots = []

[tableaux_POS.append(res[i].split('/')[0].replace("*","")) for i  in range(len(res)) ]

[tableaux_mots.append(res[i].split('/')[1].replace("*","")) for i  in range(len(res)) ]




print(tableaux_POS)
print(tableaux_mots)

#Lire  le data du 
path_table_asociative= "/home/aissam/Bureau/CERI M2/S9/Application D'innovation/TORESS/Ressources/TableAssociative"
# path vers  le fichier embidding
path_table_embidding  = "/home/aissam/Bureau/CERI M2/S9/Application D'innovation/TORESS/Ressources/embeddings-Fr.txt"

dataset = pnd.read_csv(path_table_asociative, sep='\n')


dataset = pnd.DataFrame(dataset)


#print(dataset.iloc[[1]])
csv.field_size_limit(sys.maxsize)



dictionnaire_table_asociative  =  []

dictionnaire_table_embidding  =  []



# Focntion qui permet de calculer les distance euclidiens entres deux  vecteur de 100 dimensions:

def distance_entre_vecteurs(vect1,vect2):
    
    dist = 0
    
    for i in range(100):
        
        dist += pow(vect1[i]-vect2[i],2)

    return math.sqrt(dist) 


# Calculer la distance euclidiene entre deux vecteur : 

def calcule_distance_euclidienne(vect1, vect2):

    return distance.euclidean(vect1, vect2)


# Caculer la similarité cosinus  entre deux vecteurs
def calcule_distance_similarity(vect1,vect2):
    c = 0
    normA = 0
    normB = 0
    for i in range(100):
        c+= vect1[i]*vect2[i]
        normA += math.pow(vect1[i],2)
        normB += math.pow(vect2[i],2) 
    DistanceCosine = c / float(math.sqrt(normA)*math.sqrt(normB))
    return DistanceCosine

# Lire toutes les données du fichier table asociative
with open(path_table_asociative, 'r') as read_obj:
    dictionnaire_table_asociative = read_obj.readlines()

# Lire toutes les données du fichier embidding
with open(path_table_embidding, 'r') as read_obj:
    dictionnaire_table_embidding = read_obj.readlines()





print((dictionnaire_table_asociative[5]))

print("la taille du fichier embidding est {}".format(len(dictionnaire_table_asociative)))
print("---------------------------------------------------------------")



print("la taille du fichier embidding est {}".format(len(dictionnaire_table_embidding)))

print("---------------------------------------------------------------")
print("---------------------------------------------------------------")

# Ici on va créer un dictionnaire qui contient pour chaque POS les mots qui lui représente: 
 
dictionnaire_des_pos = dict()



for row in dictionnaire_table_asociative:

    tab = row.split("\t")
    pos = tab[0]   #pour chaque ligne on récupère le POS
    tab[len(tab)-1]= tab[len(tab)-1].replace("\n","")  # Supprimer le retour à ligne dans le  dernier element 
    dictionnaire_des_pos[pos] = tab[1:]     # On récupère tout les mots


#print((dictionnaire_des_pos['PP2CSN0']))


# Ici on va construire notre structure de données pour la table Embedding
# dictionnaire_des_mot_embiding  Dictionnaire qui  contientedra pour chaque mot son vecteur de  100 dimesnion  
dictionnaire_des_mot_embiding = dict()


for row in dictionnaire_table_embidding:

    tab_vecteur_embbiding = row.replace('[',"").replace("]","").replace("\t"," ").replace(",","").replace("\n","").split(" ")    
    tab_vecteur_embbiding = [i for i in tab_vecteur_embbiding if i!=''] #On supprime les champs  vides
    dictionnaire_des_mot_embiding[tab_vecteur_embbiding[0]] = np.asarray(tab_vecteur_embbiding[1:], dtype = float) # Transferer le tableau embedding en des floats
    if(len(tab_vecteur_embbiding)!=101):
        print("oui")
        print(len(tab_vecteur_embbiding))


print(dictionnaire_table_embidding[0])

print(dictionnaire_des_mot_embiding['de'])

#print(dictionnaire_des_mot_embiding['gynécologie'])



# Cette fonction permet de calculer la sosinus similarité entre un mot et/ou Query avec les autres mots qui composent le POS 
def recherche_mots_proches_de_query(pos,query):
   
    dictionnaire_mot_proche = dict()

    vecteur_mot  = dictionnaire_des_mot_embiding[query]

    for el in dictionnaire_des_pos[pos]:

        if el in dictionnaire_des_mot_embiding: #On verifier si le mot à un vecteur embbiding de 100 dimension
            
            pr_scalaire = calcule_distance_similarity(dictionnaire_des_mot_embiding[el], vecteur_mot)
            if pr_scalaire <0:
                pr_scalaire = abs(pr_scalaire)
            dictionnaire_mot_proche[el]  = (pr_scalaire)

    return dictionnaire_mot_proche



# Cette fonction permet de calculer la sosinus similarité entre un mot les autres mots qui composent le POS
# Pour détérminer les mots éloignés  
def recherche_mots_proches_de_mot(pos,mot):
   
    dictionnaire_mot_eloigner = dict()

    vecteur_mot  = dictionnaire_des_mot_embiding[mot]

    for el in dictionnaire_des_pos[pos]:

        if el in dictionnaire_des_mot_embiding: #On verifier si le mot à un vecteur embbiding de 100 dimension
            
            pr_scalaire = calcule_distance_similarity(dictionnaire_des_mot_embiding[el], vecteur_mot)
            if pr_scalaire <0:    
                pr_scalaire = abs(pr_scalaire)
            dictionnaire_mot_eloigner[el]  = (pr_scalaire)

    return dictionnaire_mot_eloigner

# Cette fonction return le mot candidat parmi les mot du POS
def mot_candidat(dict_mots_proches, dict_mots_eloigne):
    
    mot_candidat=""
    best = 0
    for el in dict_mots_proches:
        
        current =dict_mots_proches[el] - dict_mots_eloigne[el]
        if(current > best):
            best = current
            print(current)
            mot_candidat = el
            print(mot_candidat)

    return mot_candidat

# Cette fonction return le mot candidat suivant de la SGP
def mot_candidat_suivant(dict_mots_proches, dict_mots_eloigne):
    
    mot_candidat=""
    best = 0
    for el in dict_mots_proches:
        
        current =dict_mots_proches[el] - dict_mots_eloigne[el]
        if(current > best):
            best = current
            print(current)
            mot_candidat = el
            print(mot_candidat)

    return mot_candidat

# Cette fonction permet de regrouper les phrases générées selon leur Query
def phrase_generees(phrase,query, dictiontionnaire_phrases):
    dictiontionnaire_phrases[phrase] = query

# Cette fonction a pour but de générer le fichier en utf8 qui contientedra les 30 phrases générées
def generateur_de_fichier_de_phrase(nomFIchier, dictiontionnaire_phrases):
    with open(nomFIchier, "w") as fichier:
        for key in dictiontionnaire_phrases:
            query = dictiontionnaire_phrases[key]
            mot = key + "\t" + query +"\n"
            fichier.write(mot)

    


print("--------------------------------------------------------------")
print("|-------------------- DEBUT DU PROGRAMME --------------------|")
print("--------------------------------------------------------------")



print("----------------------------------------------------------")

# On demande de saisir la query correspondante
#query = input("Entrer la query : ")

#vecteur_query=dictionnaire_des_mot_embiding[query]


dictionnaire_des_phrase = dict()
tableau_des_query = ['tristesse', 'amour', 'joie', 'haine', 'bleu']



for query in tableau_des_query:

    tableau_mots_candidat=[]
    phrase  = SGP
    print("****************************************************")
    print(phrase)
    print("****************************************************")

    for i in range(len(res)):
        
        # On calcule le produit  scalaire entre les mots POSs et le Query  afin de prendre le mot le plus proche
        dictionnaire_mot_proche = dict()

        print("--------------- Recherche des mots proches -------------------\n")
        print("---------------- Calcul des distances ------------------------\n")

        #Chercher tout les mots proche de la query
        dictionnaire_mot_proche = recherche_mots_proches_de_query(tableaux_POS[i], query)
        #trier les mots proches selon l'ordre croissant
        sortdictionnaire_mot_prochedict = sorted(dictionnaire_mot_proche.items(), key=lambda x:x[1],reverse=True)

        dictionnaire_mot_proche = dict(sortdictionnaire_mot_prochedict)
        if query in dictionnaire_mot_proche:
            del dictionnaire_mot_proche[query]


        print("--------------- Recherche des mots eloignés -------------------\n")
        print("------------------- Calcul des distances -----------------------\n")

        dictionnaire_mot_eloigner = dict()

        # Normalement il suffit de passer par le dictionnaire  dictionnaire_mot_proche par ce que
        # il contient que les mots qui ont des vecteurs dans le fichier Embidding

        dictionnaire_mot_eloigner = recherche_mots_proches_de_mot(tableaux_POS[i],tableaux_mots[i])

        # Trier les mots eloigné selon l'ordre décroissant 
        sortdictionnaire_mot_eloignee = sorted(dictionnaire_mot_eloigner.items(), key=lambda x:x[1], reverse=True)
        dictionnaire_mot_eloigner = dict(sortdictionnaire_mot_eloignee)
        if query in dictionnaire_mot_eloigner:
            del dictionnaire_mot_eloigner[query]
        
        if tableaux_mots[i] in dictionnaire_mot_eloigner:
            del dictionnaire_mot_proche[tableaux_mots[i]]
            del dictionnaire_mot_eloigner[tableaux_mots[i]]


        print("\n---------------les mots proches------------------ \n")
        # On affiche les mot proches et les mot éloignées
        i=0
        for el in dictionnaire_mot_proche:
            
            print(el + "  "+ str(dictionnaire_mot_proche[el]))

            if i>=15:
                break
            i+=1


        print("\n---------------les mots éloignés------------------ \n")

        # On affiche les mot proches et les mot éloignées
        i=0
        for el in dictionnaire_mot_eloigner:
            
            print(el + "  "+ str(dictionnaire_mot_eloigner[el]) )

            if i>=15:
                break
            i+=1

        print("----------------------------------------------------")
        print("---------------- le mot à choisir est ---------------")
        mot_choisit = mot_candidat(dictionnaire_mot_proche, dictionnaire_mot_eloigner)
        print(mot_choisit)

        tableau_mots_candidat.append(mot_choisit)

        print(type(dictionnaire_mot_proche))

        print(type(dictionnaire_des_mot_embiding))



        print("--------------------------------- Recherche Pour le Mot Suivant -------------------------------")
    

    # Remplacer les POS calculer dans la SGP
    j=0
    for j in range(len(tableaux_POS)):
        phrase = phrase.replace(res[j],tableau_mots_candidat[j])
        print("\n yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy  {}".format(tableau_mots_candidat[j]))
    
    
    print("--------------- Voici la phrase finale ------------------\n")
    print(phrase)
    # Ajouter la phrase au 
    phrase_generees(phrase,query,dictionnaire_des_phrase)
    phrase = SGP


generateur_de_fichier_de_phrase("fihcierDesPhrase",dictionnaire_des_phrase)
""" 
    # On calcule le produit  scalaire entre les mots POSs et le Query  afin de prendre le mot le plus proche

    dictionnaire_mot_proche = dict()

    print("--------------- Recherche des mots proches -------------------\n")
    print("---------------- Calcul des distances ------------------------\n")

    # Chercher tout les mots proche de la query
    dictionnaire_mot_proche = recherche_mots_proches_de_query(pos_2, query)
    #trier les mots proches selon l'ordre croissant
    sortdictionnaire_mot_prochedict = sorted(dictionnaire_mot_proche.items(), key=lambda x:x[1],reverse=True)

    dictionnaire_mot_proche = dict(sortdictionnaire_mot_prochedict)
    #del dictionnaire_mot_proche[mot_choisit]


    print("--------------- Recherche des mots eloignés -------------------\n")
    print("------------------- Calcul des distances -----------------------\n")

    dictionnaire_mot_eloigner = dict()

    # Normalement il suffit de passer par le dictionnaire  dictionnaire_mot_proche par ce que
    # il contient que les mots qui ont des vecteurs dans le fichier Embidding

    dictionnaire_mot_eloigner = recherche_mots_proches_de_mot(pos_2,mot_2)

    # Trier les mots eloigné selon l'ordre décroissant 
    sortdictionnaire_mot_eloignee = sorted(dictionnaire_mot_eloigner.items(), key=lambda x:x[1], reverse=True)
    dictionnaire_mot_eloigner = dict(sortdictionnaire_mot_eloignee)
    #del dictionnaire_mot_eloigner[mot_choisit]



    print("\n---------------les mots proches------------------ \n")
    # On affiche les mot proches et les mot éloignées
    i=0
    for el in dictionnaire_mot_proche:
        
        print(el + "  "+ str(dictionnaire_mot_proche[el]))

        if i>=15:
            break
        i+=1


    print("\n---------------les mots éloignés------------------ \n")

    # On affiche les mot proches et les mot éloignées
    i=0
    for el in dictionnaire_mot_eloigner:
        
        print(el + "  "+ str(dictionnaire_mot_eloigner[el]) )

        if i>=15:
            break
        i+=1

    mot_choisit = mot_candidat(dictionnaire_mot_proche, dictionnaire_mot_eloigner)
    print(mot_choisit)

    tableau_mots_candidat.append(mot_choisit) """







    # Poue le mot suivant pensé a rajouter les 3 params : motPrécedent + query + mmote proche et  éloigné,
    # faire la soustraction deux fois ; 
    # la déffirence entre les   distances cosinus similarité  distance(mot proche - mot éloigné) - distance (Query))
