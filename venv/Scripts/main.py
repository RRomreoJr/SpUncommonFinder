# coding=utf8
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import cess_esp
import ast

# Initialize the stemmer
stemmer = SnowballStemmer("spanish")

# Define the text to be analyzed
text = "Es la Posada del Hombre Arrodillado, mi señora —respondió Ser Cleos—. Está en el mismo lugar donde el último Rey en el Norte se arrodilló frente a Aegon el Conquistador como muestra de sumisión. Supongo que el de la tablilla es él."

corpusList = []
f = open("corpusFreqCount.txt", "r",  encoding='utf-8')
corpusList = ast.literal_eval(f.read())
f.close()
def indexOrNeg1(toCheck):
    _count = 0
    for e in corpusList:
        if e[0] == toCheck:
            # print(toCheck +'\'s index is '  + str(_count))
            return _count
        _count += 1
    # print(toCheck+'\'s index is '+ str(-1))
    return -1

def GetRarity(_stem):
    #lower number is more rare
    #Freq 0 == Rarity len(corpusList)
    _index = indexOrNeg1(_stem)
    if (_index >= 0):
        # if the stem was in the corpusList
        return len(corpusList) - _index
    else:
        return -1
# def GetEntryWithFreq(_uniqueList, _dictList):
#     _listOfHits = {}
#     for _inStem in _uniqueList:
#         for _entry in _dictList:
#             if(_inStem == _entry[0]):
#                 _listOfHits[_inStem] = _dictList.keys().index(_inStem)
#             #_listOfHits[_inStem] = _dict[_inStem]
#     return _listOfHits
def GetEntrysWithRarity(_stemList):
    newList = []
    for _stem in _stemList:
        newList.append((_stem, indexOrNeg1(_stem)))
    return newList
def unique(_list):
    # insert the list to the set
    _list_set = set(_list)
    # convert the set to the list
    _unique_list = (list(_list_set))
    return _unique_list


# Tokenize the text into words
inputWords = nltk.word_tokenize(text)
inputStemmed = [stemmer.stem(w) for w in inputWords]
inputStemmed = unique(inputStemmed)

# Sorting by rarity. (unknown) then most to least
inputStemmed = sorted(inputStemmed, key=lambda x: GetRarity(x))

print(inputStemmed)
print("inputStemmed after sort by rarity with but with index")
print(GetEntrysWithRarity(inputStemmed))
print("of.. " + str(len(corpusList)))

# So a coulpe of problems, the more rare a word is the
# higher it's rarity the it's rarity will be if ordered from most
# to least common. rarity = freq out of all the stems
# but if you have a word not in the corpus then I'd
# like to rep that with -1 which is confusing bc bigger NO
# LONGER MEANS more rare. Tech -1 is the most rare, kinda..

# Try to get only alpha portions of strings
