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


#Unigrammeeeeeeeee
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


#bigrammeeeeeeeee
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


#ngrammeeeeeeeeee
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
