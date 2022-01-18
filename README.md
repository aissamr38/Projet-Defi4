Ce projet est n notre travail réaliser sur  la génération de phrases au moyen d'énergie textuelle,  plus précisément  la génération de phrases littéraires.  Cette génération se comporte sur deux modèles  : générateur baseline de phrases par modèle de langage bigramme (ML-2) et trigramme (ML-3), ensuite le générateur de phrases par apprentissage neuronal (RNA) et un contexte (query). Notre travail est basé sur des ressources disponibles (corpus littéraire, table asociative, embeddings littéraires, baseline et ML). 

Nous nous sommes basés sur une évaluation manuelle pour évaluer la grammaticalité et la littéracité  des phrases générées. 



# Application-Innovation-Defi4
Génération de phrases au moyen d'énergie textuelle (L.-G. Moreno &amp; J.-M. Torres)

Le fichier `generateurNgrams.py` permet d'extraire les ngrams  avec leurs occurences dans tout le corpus,

nous extrayons les ML-2 et ML-3,

En respectant la syntaxe : `mot \t mot \t occurence`  pour le `ML-2`,

et:  `mot \t mot\t mot\t occurence` pour le `ML-3`,

Les fichiers générer ce sont : `dataBiGrams.txt` et `dataTriGrams.txt`  

Les fichiers seront sotcker dans le même réprtoir où le script était lancé

##  Générateur de phrases basé sur des bigrams et trigrams conçu par le générateurs de ces derniers

 Via le fichier `generateurNgrams.py`

Le fichier `data.dat` est un échantillon  pour tester le code

Il suffit que de mettre data.dat dans le même répertoire que le ficher courrant (generateurDePhrases.py)
Puis éxecuter ce dernier pour avoir des phrases générées (commade : `python3.8 generateurDePhrases.py`)

## Générateur de phrases : modèle neuronal RNA


le code source dans le fichier generateRNA.py permet de générer des phrases à partir des SGP : Structures Grammaticales Partiellement Vides données

utilisation python3.8  `generateRNA.py`
