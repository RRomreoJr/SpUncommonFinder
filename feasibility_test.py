'''
GOAL: To check a list of words to see if they are alredy cards in my 
        anki deck(s)
'''
import csv
import csv_tools
import nltk
from nltk.stem import SnowballStemmer
import os
import json
INVAILD_ANKI_PATHS = set(['' , "C:\\Example\\Please\\Use\\Double\\Backslashes\\LikeThis.csv"])
stemmer = SnowballStemmer("spanish")

def get_first_stem(inp):
    global stemmer

    inpTokenized = nltk.word_tokenize(inp)
    if not inpTokenized:
        return None

    return stemmer.stem(inpTokenized[0])
    
def get_anki_stem_dict(ankiCSVPath, notetype_wordCol_list=[]): # --check
    if (len(notetype_wordCol_list) == 0):
        return None
    global stemmer
    # wordContentList = []
    new_dict = {}
    CARDTYPE_COL = 1
    TUP_CARDTYPE = 0
    TUP_WORDCOL = 1

    with open(ankiCSVPath, encoding='utf-8') as ankiCSVFile:
        # print("opened")
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

config = None
# Made a personal version so I don't have to push out my personal settings
config_name = "configPersonal.json" if os.path.exists("configPersonal.json") else "config.json"
with open(config_name, "r", encoding='utf-8') as configFile:
    config = json.loads(configFile.read())["unique_finder"]
script_directory = os.path.dirname(__file__)

#PU == Personal Uniques
OUTPUT_HEADER = config["output_header"]
output_name = config["output_name_w_ext"]

fileDict = {}
if(config["anki_path"] not in INVAILD_ANKI_PATHS):
    anki_word_path = r"D:\DocumentsHDD\AnkiOutTest\SpanishVocab.txt"

    # Lib files
    #cardtypes and where to find the word
    noteWordColTups = [("Sp_Vocab", 3), ("Richie_Sp_Gram_Words_New", 3)]
    anki_words_dict = get_anki_stem_dict(anki_word_path, notetype_wordCol_list=noteWordColTups)
    if anki_word_path not in fileDict:
        fileDict[anki_word_path] = anki_words_dict

# Additional lib files. these are like "fake cards" that I can use to simulate each iteration
additional_file_paths = []
for input_file in config["input_names_w_ext"]:
    additional_file_paths.append(os.path.join(script_directory, input_file))

for a_f_path in additional_file_paths:
    a_f_dict = get_additional_stem_dict(a_f_path)
    if a_f_path not in fileDict:
        fileDict[a_f_path] = a_f_dict

if(len(fileDict) <= 0):
    print("No libraries found to check against. Please check config.json and add some filenames to unique_finder.input_names_w_ext")
    quit()
# Input files
words_to_check_path = os.path.join(script_directory, config["check_filename_w_ext"])
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
for check in words_to_check: # --check
    #Progess tracker
    progCurr = round(count / len(words_to_check), 2)
    if (progCurr - progDisplay) >= 0.05:
        progDisplay = progCurr
        print("progress: {}".format(progDisplay))

    #Getting stem of first token
    checkStem = get_first_stem(check.lower())
    if not checkStem:
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

#Writting out results
result_path = os.path.join(script_directory, "{}_{}.csv".format(OUTPUT_HEADER, output_name))

with open(result_path, 'w', newline='', encoding='utf-8') as resultFile:
    csvWritter = csv.writer(resultFile, delimiter='\t')
    for resRow in res:
        resultFile.write(resRow + '\n')
    
catches = len(words_to_check) - len(res)
# print(res)
print("")
print("Checks : {} New Words: {}".format(len(words_to_check), len(res)))
print("%caught: {} ({})".format(round(catches / len(words_to_check), 2), catches))
if(config["anki_path"] in INVAILD_ANKI_PATHS):
    print("No Anki search")
else:
    catchesNonAnki = catches - countDict[anki_word_path]
    print("%caught by \"fake\" anki cards: {} ({})".format(round(1 - (countDict[anki_word_path] / catches), 2), catchesNonAnki)) # I should catchesNonAnki to make the %
    print("%reduced by \"fake\" cards: {}".format(round(catchesNonAnki / (len(res) + catchesNonAnki), 2)))
print(countDict)
# print(res)











