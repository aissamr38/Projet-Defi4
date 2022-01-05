# Générateur de phrases basé sur des bigrams et trigrams conçu par le générateurs de ces derniers
# Via le fichier generateurNgrams.py
# Le fichier data.dat est un échantiant pour tester le code

# Il suffit que de mettre data.dat dans le même répertoire que le ficher courrant (generateurDePhrases.py)
# Puis éxecuter ce dernier pour avoir des phrases générées (commade : python3.8 generateurDePhrases.py)


import numpy as np

def makeWordsWithIndexBigram(corpus):
    wordsWithIndex = {
    "DEBUT DEBUT":0,
    "FIN":1
    }
    words = ['DEBUT DEBUT', 'FIN']

    for file in corpus:
        for i in range(len(file)):
            if i == 0:
                word = 'DEBUT ' + file[0]
            else:
                word = file[i-1] + ' ' + file[i]

            if word not in words:
                wordsWithIndex[word] = len(words)
                words.append(word)
            
    return wordsWithIndex, words

def makeMatrixOfBigrams(wordsWithIndex, words, wordsWithIndex_unigram, corpus):
    size = len(words)
    unigrams = len(wordsWithIndex_unigram)
    matrix = np.zeros((size, unigrams))

    for sentence in corpus:
        for i in range(len(sentence)):
            if i == 0:
                matrix[wordsWithIndex['DEBUT DEBUT'], wordsWithIndex_unigram[sentence[0]]] += 1            
                matrix[wordsWithIndex['DEBUT '+sentence[0]], wordsWithIndex_unigram[sentence[1]]] += 1

            elif i >= (len(sentence)-1):
                matrix[wordsWithIndex[sentence[i-1]+' '+sentence[i]], 1] += 1
       
            else: 
                matrix[wordsWithIndex[sentence[i-1]+' '+sentence[i]], wordsWithIndex_unigram[sentence[i+1]]] += 1

   
    return matrix


def makeWordsWithIndexUnigram(corpus):
    wordsWithIndex = {
    "DEBUT":0,
    "FIN":1
    }
    
    words = ['DEBUT', 'FIN']

    for file in corpus:
        for word in file:
            if word not in words:
                wordsWithIndex[word] = len(words)
                words.append(word)
                
    return wordsWithIndex, words


def getBestSuccesorOfWord(mot):

    temp = [];
    for i in range(1000000):
        temp.append(0);

    index = wordsWithIndex[""+mot+""];


    for j in range(2,len(words)):
         if matrix[index][j] > 0:
             temp[j] = matrix[index][j]

    if not temp:
        print("votre mot ne contient aucun successeur");
    else:
        max_value = max(temp);
        max_index = temp.index(max_value)
        
    return words[max_index];


text_file = open("data.dat", "r")
corpus = text_file.read().split(",\n")
corpus = [corpus]

wordsWithIndex_bigram, words_bigram = makeWordsWithIndexBigram(corpus)

"""print(wordsWithIndex_bigram)"""

res = makeWordsWithIndexUnigram(corpus);


#unigram
wordsWithIndex = res[0];
words = res[1];

"""print (wordsWithIndex);
print ("\n");
print (words)"""

matrix = makeMatrixOfBigrams(wordsWithIndex_bigram, words_bigram, wordsWithIndex, corpus)


while True:

    mot = input("Entrer le mot de départ : ");
    nbr = input("Choisir la taille de la phrase (5, 10, 15) : ")
    sentence = mot;


    for i in range(int(nbr)-1):
        succesor = getBestSuccesorOfWord(mot)
        sentence += " " + succesor;
        mot = succesor;


    print (sentence)