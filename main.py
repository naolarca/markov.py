###
###  Gabarit pour l'application de traitement des frequences de mots dans les oeuvres d'auteurs divers
###  Le traitement des arguments a ete inclus:
###     Tous les arguments requis sont presents et accessibles dans args
###     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
###
###  Frederic Mailhot, 26 fevrier 2018
###    Revise 16 avril 2018
###    Revise 7 janvier 2020

###  Parametres utilises, leur fonction et code a generer
###
###  -d   Deja traite dans le gabarit:  la variable rep_auth contiendra le chemin complet vers le repertoire d'auteurs
###       La liste d'auteurs est extraite de ce repertoire, et est comprise dans la variable authors
###
###  -P   Si utilise, indique au systeme d'utiliser la ponctuation.  Ce qui est considÃ©re comme un signe de ponctuation
###       est defini dans la liste PONC
###       Si -P EST utilise, cela indique qu'on dÃ©sire conserver la ponctuation (chaque signe est alors considere
###       comme un mot.  Par defaut, la ponctuation devrait etre retiree
###
###  -m   mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.
###
###  -a   Auteur (unique a traiter).  Utile en combinaison avec -g, -G, pour la generation d'un texte aleatoire
###       avec les caracteristiques de l'auteur indique
###
###  -G   Indique qu'on veut generer un texte (voir -a ci-haut), le nombre de mots Ã  generer doit Ãªtre indique
###
###  -g   Indique qu'on veut generer un texte (voir -a ci-haut), le nom du fichier en sortie est indique
###
###  -F   Indique qu'on desire connaitre le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
###       donnÃ© avec le parametre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus
###
###  -v   Deja traite dans le gabarit:  mode "verbose",  va imprimer les valeurs donnÃ©es en parametre
###
###
###  Le systeme doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la presence et la valeur
###  des autres parametres, le systeme produira differentes sorties:
###
###  avec -a, -g, -G:  generation d'un texte aleatoire avec les caracteristiques de l'auteur identifie
###  avec -a, -F:  imprimer la frequence d'un mot d'un certain auteur.  Format de sortie:  "auteur:  mot  frequence"
###                la frequence doit Ãªtre un nombre reel entre 0 et 1, qui represente la probabilite de ce mot
###                pour cet auteur
###  avec -f:  indiquer l'auteur le plus probable du texte identifie par le nom de fichier qui suit -f
###            Format de sortie:  "nom du fichier: auteur"
###  avec ou sans -P:  indique que les calculs doivent etre faits avec ou sans ponctuation
###  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramÃ¨tres (fait deja partie du gabarit)

import math
import argparse
import glob
import sys
import os
from collections import Counter
from pathlib import Path
from random import randint
from random import choice

### Ajouter ici les signes de ponctuation Ã  retirer
PONC = ["!", '"', "'", " ", "’", ")", "(", ",", ".", ";", ":", "?", "-", "_", "«", "»"]

###  Vous devriez inclure vos classes et mÃ©thodes ici, qui seront appellÃ©es Ã  partir du main

#liste ordonnee pour nieme mot plus frequent
def mergeSort(alist, blist):
    new_dict = {}

    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]
        lefthalfB = blist[:mid]
        righthalfB = blist[mid:]

        mergeSort(lefthalf, lefthalfB)
        mergeSort(righthalf, righthalfB)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and i < len(lefthalfB) and j < len(righthalf) and j< len(righthalfB):
            if lefthalf[i] >= righthalf[j]:
                alist[k]=lefthalf[i]
                blist[k] = lefthalfB[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                blist[k] = righthalfB[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            blist[k] = lefthalfB[i]
            i=i+1
            k=k+1

        while j < len(righthalf)and j< len(righthalfB):
            alist[k] = righthalf[j]
            blist[k] = righthalfB[j]
            j=j+1
            k=k+1

    new_dict = {key: value for key, value in zip(blist, alist)}
    return new_dict

#Unigrammeeeeeeeee (sans punctuation par defaut)
def unigramme(fichier, ponctu):
    with open(fichier, 'r', encoding='utf-8') as f:
        dictionnaire = {}
        for line in f:
            for word in line.split():
                word = word.lower()
                if ponctu == False:
                    for char in word:
                        if char in PONC:
                            word = word.replace("--", " ")
                            word = word.replace("-", " ")
                            word = word.replace(char, " ")
                    for smallWord in word.split():
                        if len(smallWord) < 3:
                              smallWord = smallWord.replace(smallWord, "")
                        if smallWord not in dictionnaire:
                           dictionnaire[smallWord] = 1
                        else:
                            dictionnaire[smallWord] += 1
                if ponctu == True:
                    if len(word) < 3:
                        word = word.replace(word, "")
                    for char in word:
                        if char in PONC:
                            if char not in dictionnaire:
                                dictionnaire[char] = 1
                            else:
                                dictionnaire[char] += 1
                            word = word.replace("--", " ")
                            word = word.replace("-", " ")
                            word = word.replace(char, " ")
                    for smallWord in word.split():
                        if smallWord not in dictionnaire:
                            dictionnaire[smallWord] = 1
                        else:
                            dictionnaire[smallWord] += 1
    alist = []
    blist = []
    for value in dictionnaire.values():
        alist.append(value)
    for cle in dictionnaire.keys():
        blist.append(cle)
    dictionnaire = mergeSort(alist, blist)
    return dictionnaire


#bigrammeeeeeeeee (sans punctuation par defaut)
def bigramme(fichier, ponctu):
    with open(fichier, 'r', encoding='utf-8') as f:
        livre = []
        dictionnaire = {}
        if ponctu == False:
            for line in f:
               for word in line.split():
                    word = word.lower()
                    for char in word:
                        if char in PONC:
                            word = word.replace("--", " ")
                            word = word.replace("-", " ")
                            word = word.replace(char, " ")
                    for smallWord in word.split():
                        if len(smallWord) < 3:
                            smallWord = smallWord.replace(smallWord, "")
                        if smallWord != "":
                            livre.append(smallWord)
        if ponctu == True:
            for line in f:
               for word in line.split():
                    word = word.lower()
                    if len(word) < 3:
                        word = word.replace(word, "")
                    for char in word:
                        if char in PONC:
                            word = char
                            livre.append(word)
                    for smallWord in word.split():
                        if smallWord != "":
                            livre.append(smallWord)
    for i in range(1, len(livre)):
        split_string = livre[i-1] + ' ' + livre[i]
        if split_string not in dictionnaire:
            dictionnaire[split_string] = 1
        else:
            dictionnaire[split_string] += 1
    alist = []
    blist = []
    for value in dictionnaire.values():
        alist.append(value)
    for cle in dictionnaire.keys():
        blist.append(cle)
    dictionnaire = mergeSort(alist, blist)

    return dictionnaire


#ngrammeeeeeeeeee (sans punctuation par defaut)
def ngramme(fichier, ponctu, n):
    with open(fichier, 'r', encoding='utf-8') as f:
        livre = []
        dictionnaire = {}
        if ponctu == False:
            for line in f:
               for word in line.split():
                    word = word.lower()
                    for char in word:
                        if char in PONC:
                            word = word.replace("--", " ")
                            word = word.replace("-", " ")
                            word = word.replace(char, " ")
                    for smallWord in word.split():
                        if len(smallWord) < 3:
                            smallWord = smallWord.replace(smallWord, "")
                        if smallWord != "":
                            livre.append(smallWord)
        if ponctu == True:
            for line in f:
               for word in line.split():
                    word = word.lower()
                    if len(word) < 3:
                        word = word.replace(word, "")
                    for char in word:
                        if char in PONC:
                            word = char
                            livre.append(word)
                    for smallWord in word.split():
                        if smallWord != "":
                            livre.append(smallWord)
    for i in range(1, len(livre)):
        if i+n-1> len(livre): break
        split_string = livre[i-1]
        for j in range (0,n-1):
            if i+j < len(livre):
                split_string += ' ' + livre[i+j]
        if split_string not in dictionnaire:
            dictionnaire[split_string] = 1
        else:
            dictionnaire[split_string] += 1
    alist = []
    blist = []
    for value in dictionnaire.values():
        alist.append(value)
    for cle in dictionnaire.keys():
        blist.append(cle)
    dictionnaire = mergeSort(alist, blist)

    return dictionnaire


#freq mot unigramme
def motFreqUni(mot, fichier, ponctu):
    uni= unigramme(fichier, ponctu)
    for key, value in zip(uni.keys(), uni.values()):
        if key == mot:
            return value

#freq mot bigramme
def motFreqBi(mot, fichier, ponctu):
    bi = bigramme(fichier, ponctu)
    for key, value in zip(bi.keys(), bi.values()):
        if key == mot:
            return value


# la liste des dictionnaire dUN auteur
def listeDictioAuteur(mode, ponctu, auteur):
    DictionaryList = []
    dictionary = {}
    newDic = {}
    if mode == 1:
        for i in range(len(authors)):
            if auteur == authors[i]:
                files = os.listdir(rep_aut + "\\" + authors[i])
                for j in range(len(files)):

                    dictionary = unigramme(rep_aut + "\\" + authors[i] + "\\" + files[j], ponctu)
                DictionaryList.append(dictionary)

    elif mode == 2:
        for i in range(len(authors)):
            if auteur == authors[i]:
                files = os.listdir(rep_aut + "\\" + authors[i])
                for j in range(len(files)):
                    file = open(rep_aut + "\\" + authors[i] + "\\" + files[j], 'r', encoding='utf-8')
                    dictionary = bigramme(file, ponctu)
                    file.close()
                DictionaryList.append(dictionary)
    for i in range(len(DictionaryList)):
        newDic+= Counter(DictionaryList[i])

    return newDic

#la liste des dictionnaires de tous les auteurs
def listeDictio(mode, ponctu):
    for auteur in authors:
        listDict= listeDictioAuteur(mode, ponctu, auteur)
    return listDict


#comparaison texte dun auteur inconnu avec repertoire
def determinerAuteur(fichierInconnu, mode, ponctu):
    newDictio= {}

    motsCommuns = []
    if mode == 1:
        dictioInconnu= unigramme(fichierInconnu, ponctu)
    if mode == 2:
        dictioInconnu= bigramme(fichierInconnu, ponctu)








### Main: lecture des paramÃ¨tres et appel des mÃ©thodes appropriÃ©es
###
###       argparse permet de lire les paramÃ¨tres sur la ligne de commande
###             Certains paramÃ¨tres sont obligatoires ("required=True")
###             Ces paramÃ¨tres doivent Ãªtres fournis Ã  python lorsque l'application est exÃ©cutÃ©e
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 3),
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    args = parser.parse_args()

    ### Lecture du répertoire des auteurs, obtenir la liste des auteurs
    ### Note:  args.d est obligatoire
    ### auteurs devrait comprendre la liste des répertoires d'auteurs, peu importe le système d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)

    ### Enlever les signes de ponctuation (ou non) - Définis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    ### Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Calcul avec les auteurs du repertoire: " + args.d)
        if args.f:
            print("Fichier inconnu a,"
                  " etudier: " + args.f)

        print("Calcul avec des " + str(args.m) + "-grammes")
        if args.F:
            print(str(args.F) + "e mot (ou digramme) le plus frequent sera calcule")

        if args.a:
            print("Auteur etudie: " + args.a)

        if args.P:
            print("Retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])

### Ã€ partir d'ici, vous devriez inclure les appels Ã  votre code

#MAIN
mode = args.m
ponctu = remove_ponc

haha= listeDictioAuteur(mode,ponctu,"Hugo")
for word in haha:
    print(word, haha[word])

#TODO: LES FONCTIONS SUIVANTES SONT A REALISER
#def selectionAuteur(nomAuteur):
    #il doit y avoir un repertoire contenant les sous repertoires des auteurs
    #selon la selection de lauteur a traiter, differents textes seront regardes
#def generationTexte(nbMots, fichierSortie):
    #print("wesh...")
    # generation dun texte: le nombre de mots Ã  generer doit Ãªtre indique,le nom du fichier en sortie est indique

#def ensembleOeuvre():
    # Le systeme doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la presence et la valeur
    # ###  des autres parametres, le systeme produira differentes sorties:
    # pour le moment fait avec une seule oeuvre

#TODO: LES POINTS SUIVANTS EN RESPECTANT FORMAT SORTIE
###  avec -a, -g, -G:  generation d'un texte aleatoire avec les caracteristiques de l'auteur identifie
###  avec -a, -F:  imprimer la frequence d'un mot d'un certain auteur.  Format de sortie:  "auteur:  mot  frequence"
###                la frequence doit Ãªtre un nombre reel entre 0 et 1, qui represente la probabilite de ce mot
###                pour cet auteur
###  avec -f:  indiquer l'auteur le plus probable du texte identifie par le nom de fichier qui suit -f
###            Format de sortie:  "nom du fichier: auteur"
###  avec ou sans -P:  indique que les calculs doivent etre faits avec ou sans ponctuation
###  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramÃ¨tres (fait deja partie du gabarit)

#TODO: INCORPORER CODE AVEC GABARIT