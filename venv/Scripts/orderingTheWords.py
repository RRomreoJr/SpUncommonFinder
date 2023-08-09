import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import cess_esp
import ast

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
def tupsToDict(tups):
    dictToReturn = {}
    for tup in tups:
        dictToReturn[tup[0]] = tup[1]
    return dictToReturn
f = open("corpusFreqCount.txt", "r",  encoding='utf-8')
tupleList = ast.literal_eval(f.read())
# tupleDict = tupsToDict(tupleList)
f.close()
print('tupleList ' + str(len(tupleList)))
# Dont need any more
