#liste de ponctuation
PONC = ["!", '"', "'", " ", "’", ")", "(", ",", ".", ";", ":", "?", "-", "_", "«", "»"]


#Structure de mots et de frquence
class MyStruct():
    mot = []
    frequence = []



#liste ordonnee pour nieme mot plus frequent
def mergeSort(alist):
    #print("Splitting ",alist)
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] >= righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
    #print("Merging ",alist)
    return alist


#Unigrammeeeeeeeee (sans punctuation par defaut)
def unigramme(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        counts = {}
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
                    if smallWord not in counts:
                        counts[smallWord] = 1
                    else:
                        counts[smallWord] += 1
    del counts[""]
    for smallWord in counts:
        uni= MyStruct()
        uni.mot.append(smallWord)
        uni.frequence.append(counts[smallWord])
    return uni


#bigrammeeeeeeeee (sans punctuation par defaut)
def bigramme(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        livre = []
        counts = {}

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
    for i in range(1, len(livre)):
        split_string = livre[i-1] + ' ' + livre[i]
        if split_string not in counts:
            counts[split_string] = 1
        else:
            counts[split_string] += 1
    for split_string in counts:
        bi = MyStruct()
        bi.mot.append(split_string)
        bi.frequence.append(counts[split_string])
    return bi


#ngrammeeeeeeeeee (sans punctuation par defaut)
def ngramme(fichier, n):
    with open(fichier, 'r', encoding='utf-8') as f:
        livre = []
        counts = {}

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
    for i in range(1, len(livre)):
        if i+n-1> len(livre): break
        split_string = livre[i-1]
        for j in range (0,n-1):
            if i+j < len(livre):
                split_string += ' ' + livre[i+j]
        if split_string not in counts:
            counts[split_string] = 1
        else:
            counts[split_string] += 1
    for split_string in counts:
        print(split_string, counts[split_string])


#nieme mot le plus frequent pour unigramme
def motFreqUni(index):
    uni= unigramme("Victor Hugo - L'homme qui rit.txt")
    copieFreq= uni.frequence[:]
    uniFreq= mergeSort(uni.frequence)

    for i in range(0, len(uni.mot)):
        if copieFreq[i] == uniFreq[index]:
            lesMot = uni.mot[i]
    print(uniFreq[index])
    print(lesMot)


#nieme mot plus frequent pour bigramme
def motFreqBi(index):
    bi= bigramme("Victor Hugo - Notre-Dame de Paris.txt")
    copieFreq = bi.frequence[:]
    uniFreq = mergeSort(bi.frequence)

    for i in range(0, len(bi.mot)):
        if copieFreq[i] == uniFreq[index]:
            lesMot = bi.mot[i]
    print(uniFreq[index])
    print(lesMot)

#MAIN
def main():
    ngramme("Victor Hugo - Les miserables - Tome I.txt", 1)

    #unigramme("Victor Hugo - L'homme qui rit.txt")

main()

#TODO: LES FONCTIONS SUIVANTES SONT A REALISER
def selectionAuteur(nomAuteur):
    print("Auteur:"+ nomAuteur)
    #il doit y avoir un repertoire contenant les sous repertoires des auteurs
    #selon la selection de lauteur a traiter, differents textes seront regardes

def UniAvecPunct():
    print("wesh...")
    #les ponctuactions sont alors consideres comme un mot
    # on doit le faire pour bi et ngramme aussi

def selectionModeAnalyse(Mode):
    print("wesh...")
    #mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.

def generationTexte(nbMots, fichierSortie):
    print("wesh...")
    # generation dun texte: le nombre de mots Ã  generer doit Ãªtre indique,le nom du fichier en sortie est indique

def rangMot(mot):
    print("wesh...")
    # le rang d'un certain mot, on utilise avec les fonctions motFreq uni et bi....
    # on en a besoin pour connaitre le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
    # ###       donnÃ© avec le parametre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus

def ensembleOeuvre():
    print("wesh...")
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