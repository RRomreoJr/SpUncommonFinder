'''
GOAL: To check a list of words to see if they are alredy cards in my 
        anki deck(s)
'''
import csv
import csv_tools
import nltk
from nltk.stem import SnowballStemmer
import os
stemmer = SnowballStemmer("spanish")

def get_first_stem(inp):
    global stemmer

    inpTokenized = nltk.word_tokenize(inp)
    if not inpTokenized:
        return None

    return stemmer.stem(inpTokenized[0])
    
def get_anki_stem_dict(ankiCSVPath, notetype_wordCol_list=[]):
    if (len(notetype_wordCol_list) == 0):
        return None
    global stemmer
    # wordContentList = []
    new_dict = {}
    CARDTYPE_COL = 1
    TUP_CARDTYPE = 0
    TUP_WORDCOL = 1

    with open(ankiCSVPath, encoding='utf-8') as ankiCSVFile:
        print("opened")
        csv_reader = csv.reader(ankiCSVFile, delimiter='\t')

        for noteWordTup in notetype_wordCol_list:
            print("noteWordTup: {}".format(noteWordTup ))
            for ankiRow in csv_reader:
                if len(ankiRow) <= CARDTYPE_COL:
                    continue
                if ankiRow[CARDTYPE_COL] == noteWordTup[TUP_CARDTYPE]:
                    #ignore if the col we need to look at doesn't exist
                    if len(ankiRow) <= noteWordTup[TUP_WORDCOL]:
                        continue
                    
                    wordFieldContent = ankiRow[noteWordTup[TUP_WORDCOL]]
                    first_stem = get_first_stem(wordFieldContent).lower()
                    
                    if first_stem and first_stem not in new_dict:
                            new_dict[first_stem] = first_stem
                    
                    # wordContentList.append(ankiRow[noteWordTup[TUP_WORDCOL]])
                # else:
                #     print("{} {}".format(ankiRow[CARDTYPE_COL], noteWordTup[TUP_CARDTYPE]))
    return new_dict

def get_additional_stem_dict(CSVPath):
    global stemmer
    new_dict = {}
    with open(CSVPath, encoding='utf-8') as CSVFile:
        csv_reader = csv.reader(CSVFile, delimiter='\t')

        for row in csv_reader:
            first_stem = get_first_stem(row[0]).lower()
            if first_stem and first_stem not in new_dict:
                new_dict[first_stem] = first_stem
    return new_dict
fileDict = {}

#PU == Personal Uniques
OUTPUT_HEADER = "PU"
output_name = "daenerys_3_1"

anki_word_path = r"D:\DocumentsHDD\AnkiOutTest\SpanishVocab.txt"

# Lib files
#cardtypes and where to find the word
noteWordColTups = [("Sp_Vocab", 3), ("Richie_Sp_Gram_Words_New", 3)]
anki_words_dict = get_anki_stem_dict(anki_word_path, notetype_wordCol_list=noteWordColTups)
if anki_word_path not in fileDict:
    fileDict[anki_word_path] = anki_words_dict

# Additional lib files. these are like "fake cards" that I can use to simulate each iteration
addtional_file_paths = [
    # I overwrote the PU of this file by mistake but it doesn't really matter
    r'D:\Users\Richie\PycharmProjects\SpUncommonFinder\GLR_daenerys_2_2.csv',
    r'D:\Users\Richie\PycharmProjects\SpUncommonFinder\PU_daenerys_2_3.csv',
    r'D:\Users\Richie\PycharmProjects\SpUncommonFinder\PU_daenerys_2_4.csv',
    r'D:\Users\Richie\PycharmProjects\SpUncommonFinder\PU_daenerys_2_5.csv',
]

for a_f_path in addtional_file_paths:
    a_f_dict = get_additional_stem_dict(a_f_path)
    if a_f_path not in fileDict:
        fileDict[a_f_path] = a_f_dict

# Input files
words_to_check_path = r'D:\Users\Richie\PycharmProjects\SpUncommonFinder\GLR_daenerys_3_1.csv'
words_to_check = csv_tools.get_content(words_to_check_path, 0)

#the check is going to mean the word that we are comparing the library of words against
res = []
countDict = {}
progCurr = 0.0
progDisplay = 0.0
count = 1

for path in fileDict.keys():
    countDict[path] = 0

print("progress: {}".format(progDisplay))
for check in words_to_check:
    progCurr = round(count / len(words_to_check), 2)
    if (progCurr - progDisplay) >= 0.05:
        progDisplay = progCurr
        print("progress: {}".format(progDisplay))

    #Getting stem of first token
    checkTokenized = nltk.word_tokenize(check.lower())
    checkStem = None
    if checkTokenized:
        checkStem = stemmer.stem(checkTokenized[0])
    else:
        continue
    
    newWord = True
    for path, wordDict in fileDict.items():
        if checkStem in wordDict:
            newWord = False
            countDict[path] += 1
            break
    if newWord:
        res.append(check)

    count += 1

script_directory = os.path.dirname(__file__)
result_path = os.path.join(script_directory, "{}_{}.csv".format(OUTPUT_HEADER, output_name))

with open(result_path, 'w', newline='', encoding='utf-8') as resultFile:
    csvWritter = csv.writer(resultFile, delimiter='\t')
    for resRow in res:
        resultFile.write(resRow + '\n')
    
print(res)
print("")
print("Checks : {} New Words: {}".format(len(words_to_check), len(res)))
catches = len(words_to_check) - len(res)
catchesNonAnki = catches - countDict[anki_word_path]
print("%caught: {} ({})".format(round(catches / len(words_to_check), 2), catches))
print("%caught by \"fake\" anki cards: {} ({})".format(round(1 - (countDict[anki_word_path] / catches), 2), catchesNonAnki))
print("%reduced by \"fake\" cards: {}".format(round(catchesNonAnki / (len(res) + catchesNonAnki), 2)))
print(countDict)
# print(res)











