# coding=utf8
from nltk.stem import SnowballStemmer
import csv
import os
import finder_tools
import sp_corpus_freq_list
import json

config = None
config_name = "configPersonal.json" if os.path.exists("configPersonal.json") else "config.json"
with open(config_name, "r", encoding='utf-8') as configFile:
    config = json.loads(configFile.read())["SpUncommonFinder"]

# GLR = General Language Rarity
OUTPUT_HEADER = config['output_header']
output_name = config['output_name_w_ext']

SP_GENERAL_FREQ_LIST = sp_corpus_freq_list.SP_CORPUS_LIST
# Initialize the stemmer
stemmer = SnowballStemmer("spanish")

script_directory = os.path.dirname(__file__)
input_path = os.path.join(script_directory, config['input_name_w_ext'])
text = ""
with open(config['input_name_w_ext'], encoding='utf-8') as input_file:
    text = input_file.read()

#Creating data
inputStemToWords = finder_tools.get_stem_dict(text, stemmer)
entries_with_rarity = finder_tools.get_stem_rarity_list(inputStemToWords.keys(), SP_GENERAL_FREQ_LIST)

#Writting files
print("Writing files in {}".format(script_directory))

# Make sure to open the files in write mode
words_out_path = os.path.join(script_directory, "{}_{}".format(OUTPUT_HEADER, output_name))
with open(words_out_path, 'w', newline='', encoding="UTF-8") as wordsOut:
    for tup in entries_with_rarity:
        # print(tup)
        _stem = tup[0]
        # print(_stem)
        wordsOut.write(inputStemToWords[_stem][0] + "\n")
    print("{}_{} created".format(OUTPUT_HEADER, output_name))

details_path = os.path.join(script_directory, "{}_details_{}".format(OUTPUT_HEADER, output_name))
with open(details_path, 'w', newline='', encoding="UTF-8") as details_file:
    writer = csv.writer(details_file,  delimiter='\t')
    # write a row to the csv file
    writer.writerow([r'stem', r'rarity (-1 == wasn\'t in corpora, lower is more rare)', r'total corpora words', r'first word to make stem'])
    for row in entries_with_rarity:
        new_tup = (row[0], row[1], len(SP_GENERAL_FREQ_LIST), inputStemToWords[row[0]][0])
        writer.writerow(new_tup)
    print("{}_details_{} created".format(OUTPUT_HEADER, output_name))

# preview loop
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
