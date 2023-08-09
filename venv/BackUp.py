# coding=utf8
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import cess_esp

def indexOrNeg1(toCheck, _list):
    result = -1;
    try:
        result = _list.index(toCheck)
        #print (toCheck + ": " + _list[result])
    except:
        #print(toCheck + ": none")
        result = -1;
    return result;
# def GetEntryWithFreq(_uniqueList, _dictList):
#     _listOfHits = {}
#     for _inStem in _uniqueList:
#         for _entry in _dictList:
#             if(_inStem == _entry[0]):
#                 _listOfHits[_inStem] = _dictList.keys().index(_inStem)
#             #_listOfHits[_inStem] = _dict[_inStem]
#     return _listOfHits
def GetEntryWithFreq(_uniqueList, _dict):
    _listOfHits = {}
    for _inStem in _uniqueList:
        if _inStem in _dict:
            _listOfHits[_inStem] = list(_dict.keys()).index(_inStem)
            #_listOfHits[_inStem] = _dict[_inStem]
    return _listOfHits;
def unique(_list):
    # insert the list to the set
    _list_set = set(_list)
    # convert the set to the list
    _unique_list = (list(_list_set))
    return _unique_list



# Initialize the stemmer
stemmer = SnowballStemmer("spanish")

# Define the text to be analyzed
text = ""



words = cess_esp.words()
#words = nltk.word_tokenize(text)
#words = text.split()
# Stem the words
stemmedCorpusWords = [stemmer.stem(word) for word in words]
#stemmedCorpusWords = text.split()
corpusFreqCount = {}

count = 0
countPercent = -0.05
#Get word frequency in the corpus
for word in stemmedCorpusWords:
    if((count / len(stemmedCorpusWords)) >= countPercent + 0.05):
        countPercent = (count / len(stemmedCorpusWords))
        print("progress..." + str(countPercent))
    #adds the word to the dictionary with the that word's count
    corpusFreqCount[word] = stemmedCorpusWords.count(word)
    count = count + 1

sorted_words = sorted(corpusFreqCount.items(), key=lambda x: x[1], reverse=True)

#Turn corpus into list to get access to indices 
corpusList = []
for key,_ in sorted_words:
    corpusList.append(key)

sorted_words = dict(sorted_words)



# Tokenize the text into words

inputWords = nltk.word_tokenize(text)
#inputWords = text.split()
inputStemmed = [stemmer.stem(w) for w in inputWords]
inputStemmed = unique(inputStemmed)

# print(sorted_words)
print(inputStemmed)

inputStemmed = sorted(inputStemmed, key=lambda x: indexOrNeg1(x, corpusList), reverse=True)
print("inputStemmed after sort")
print(inputStemmed)
input_as_dict = GetEntryWithFreq(inputStemmed, sorted_words)

print(input_as_dict)
