# coding=utf8
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import cess_esp
import ast
import csv
import regex
import sp_corpus_freq_list
import os
# GLR = General Language Rarity
OUTPUT_HEADER = "GLR_"
output_name = "daenerys_3_1"

# Initialize the stemmer
stemmer = SnowballStemmer("spanish")

# Define the text to be analyzed
text = ""
with open("input.txt", encoding='utf-8') as input_file:
    text = input_file.read()

SP_GENERAL_FREQ_LIST = sp_corpus_freq_list.SP_CORPUS_LIST


def indexOrNeg1(toCheck):
    _count = 0
    for e in SP_GENERAL_FREQ_LIST:
        if e[0] == toCheck:
            # print(toCheck +'\'s index is '  + str(_count))
            return _count
        _count += 1
    # print(toCheck+'\'s index is '+ str(-1))
    return -1
def GetWord(toCheck):
    _count = 0
    for e in SP_GENERAL_FREQ_LIST:
        if e[0] == toCheck:
            # print(toCheck +'\'s index is '  + str(_count))
            return _count
        _count += 1
    # print(toCheck+'\'s index is '+ str(-1))
    return -1
# Get rarity in context of the general language. -1 == not found, Most frequent == LEAST rare
def GetRarity(_stem):
    _index = indexOrNeg1(_stem)
    if (_index >= 0):
        return len(SP_GENERAL_FREQ_LIST) - _index
    return -1
# Returns list of (stem, rarity) tuples in context of the general language. -1 == not found, Most frequent == LEAST rare
def GetEntrysWithRarity(_stemList):
    newList = []
    for _stem in _stemList:
        newList.append((_stem, GetRarity(_stem)))
    return newList
def unique(_list):
    # insert the list to the set
    _list_set = set(_list)
    # convert the set to the list
    _unique_list = (list(_list_set))
    return _unique_list

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
        
inputStemmed = inputStemToWords.keys()
# Sorting by rarity. (unknown) then most to least
inputStemmed = sorted(inputStemmed, key=lambda x: GetRarity(x))


# print("inputStemmed after sort by rarity with but with index")
entries_with_rarity = GetEntrysWithRarity(inputStemmed)

# Get the directory containing the script
script_directory = os.path.dirname(__file__)
print("Writing files in {}".format(script_directory))

# Make sure to open the files in write mode
words_out_path = os.path.join(script_directory, "{}{}.csv".format(OUTPUT_HEADER, output_name))
with open(words_out_path, 'w', newline='', encoding="UTF-8") as wordsOut:
    for _stem in inputStemmed:
        # print(_stem)
        wordsOut.write(inputStemToWords[_stem][0] + "\n")
print("{}{}.csv".format(OUTPUT_HEADER, output_name))

#ewr = entries_with_rarity
ewr_path = os.path.join(script_directory, 'entries_with_rarity.csv')
with open(ewr_path, 'w', newline='', encoding="UTF-8") as ewr_file:
    writer = csv.writer(ewr_file)
    # write a row to the csv file
    for row in entries_with_rarity:
        writer.writerow(row)
print('entries_with_rarity.csv created')

run = True
choice = ""
currIndex = 0
def FindEntryIndex(_in):
    global entries_with_rarity
    count = 0
    for e in entries_with_rarity:
        if e[0] == _in:
            return count
        count += 1

    return -1

while(run):
    # print(entries_with_rarity)
    print("of.. " + str(len(SP_GENERAL_FREQ_LIST)))
    print("-{}) rarity:{} entry:{}\n{}".format(entries_with_rarity[currIndex][0], entries_with_rarity[currIndex][1], currIndex, inputStemToWords[entries_with_rarity[currIndex][0]]) )
    choice = input("type \"-stop\" to quit")
    if choice == "-stop":
        run = False
    else:
        if choice == "n":
            currIndex = currIndex + 1 if currIndex + 1 < len(entries_with_rarity) else 0
        elif choice == "b":
            currIndex = currIndex - 1 if currIndex - 1 >= 0 else len(entries_with_rarity) - 1
        res = FindEntryIndex(choice)
        if res > 0:
            currIndex = res
# So a coulpe of problems, the more rare a word is the
# higher it's rarity the it's rarity will be if ordered from most
# to least common. rarity = freq out of all the stems
# but if you have a word not in the corpus then I'd
# like to rep that with -1 which is confusing bc bigger NO
# LONGER MEANS more rare. Tech -1 is the most rare, kinda..

# Try to get only alpha portions of strings
