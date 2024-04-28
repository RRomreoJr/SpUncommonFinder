# coding=utf8
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import cess_esp

def GetStemFreqDict(wordList):
    _stemDict = {}
    _stemmer = SnowballStemmer("spanish")
    count = 0
    countPercent = -0.05


    for w in wordList:
        if ((count / len(wordList)) >= countPercent + 0.05):
            countPercent = (count / len(wordList))
            print("progress..." + str(countPercent))
        stem = _stemmer.stem(w)
        if(stem in _stemDict):
            _stemDict[stem] += 1
        else:
            _stemDict[stem] = 1
    return _stemDict

# Initialize the stemmer
stemmer = SnowballStemmer("spanish")

words = cess_esp.words()
# dont know why this was there: cess_esp.
print('total words: ' + str(len(words)))

# print('uniqued: ' + str(len(unique(words))))
# uniqueStemmed = [stemmer.stem(word) for word in words]
# uniqueStemmed = unique(uniqueStemmed)
# print('unique stemmed: ' + str(len(uniqueStemmed)))

freqDict = GetStemFreqDict(words)
corpusFreqCount = list(freqDict.items())
corpusFreqCount.sort(reverse=True, key= lambda x: x[1])
print('freqDict: ' + str(len(freqDict)))
print('corpusFreqCount: ' + str(len(corpusFreqCount)))
f = open("throwaway.txt", "a", encoding='utf-8')
f.write(str(corpusFreqCount))
f.close()