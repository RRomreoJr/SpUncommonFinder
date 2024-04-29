# coding=utf8
import nltk
from nltk.stem import SnowballStemmer
import csv
import regex
import os

def indexOrNeg1(toCheck, freq_tups):
    _count = 0
    for e in freq_tups:
        if e[0] == toCheck:
            # print(toCheck +'\'s index is '  + str(_count))
            return _count
        _count += 1
    # print(toCheck+'\'s index is '+ str(-1))
    return -1
def GetWord(toCheck, freq_tups):
    _count = 0
    for e in freq_tups:
        if e[0] == toCheck:
            # print(toCheck +'\'s index is '  + str(_count))
            return _count
        _count += 1
    # print(toCheck+'\'s index is '+ str(-1))
    return -1
# Get rarity in context of the general language. -1 == not found, Most frequent == LEAST rare
def GetRarity(_stem, freq_tups):
    _index = indexOrNeg1(_stem, freq_tups)
    if (_index >= 0):
        return len(freq_tups) - _index
    return -1
# Returns list of (stem, rarity) tuples in context of the general language. -1 == not found, Most frequent == LEAST rare
def GetEntrysWithRarity(_stemList, freq_tups):
    newList = []
    for _stem in _stemList:
        newList.append((_stem, GetRarity(_stem, freq_tups)))
    return newList
def unique(_list):
    # insert the list to the set
    _list_set = set(_list)
    # convert the set to the list
    _unique_list = (list(_list_set))
    return _unique_list

def get_stem_dict(text, stemmer):

    #new lines replace with space. operating system independent
    text = regex.sub(r'\r?\n', r' ', text)
    #removing special charaters
    text = regex.sub(r'[^\p{L} ]', r'', text)

    # Tokenize the text into words
    inputWords = nltk.word_tokenize(text)


    # Used to get the orginal words that generated that stem
    inputStemToWords = dict()

    for w in inputWords:
        _stemmed = stemmer.stem(w)
        if _stemmed not in inputStemToWords:
            # inputStemmed.append(_stemmed)
            inputStemToWords[_stemmed] = [w]
        else:
            inputStemToWords[_stemmed].append(w)
    
    return inputStemToWords
# happens in main vvvvvv
# inputStemmed = inputStemToWords.keys()
def get_stem_rarity_list(inputStemmed, freq_tups):
    # Sorting by rarity. (unknown) then most to least
    inputStemmed = sorted(inputStemmed, key=lambda x: GetRarity(x, freq_tups))
    
    # print("inputStemmed after sort by rarity with but with index")
    entries_with_rarity = GetEntrysWithRarity(inputStemmed, freq_tups)
    return entries_with_rarity
