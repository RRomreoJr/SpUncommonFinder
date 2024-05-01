# coding=utf8
'''
GLF = General language frequency

Generates a list of tuples and orders them based on the frequency in the
"general language" which I'm defining as whatever is in cess_esp.words()
'''
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import cess_esp
import regex

def GetStemFreqDict(wordList):
    _stemDict = {}
    _stemmer = SnowballStemmer("spanish")
    
    count = 0
    countPercent = 0.0

    print("progress..." + str(countPercent))
    for w in wordList:
        if ((count / len(wordList)) >= countPercent + 0.05):
            countPercent = round(count / len(wordList), 2)
            print("progress..." + str(countPercent))

        # It seems like word_tokenize won't get rid of underscores like in for ex.,
        # poco_a_poco. For now I'll just relace anything that isn't a unicode letter
        # with spaces so it tokenizes better.

        # In the future I may want to keep these "underscore phrases" I won't for now
        modidied_word = regex.sub(r'[^\p{L} ]', r' ', w)
        tokenized = nltk.word_tokenize(modidied_word)
        
        if(tokenized):
            # for testing purposes
            # if(w != '*0*' and len(tokenized) > 1):
            #     print(w)
            #     print(tokenized)
            for token in tokenized:
                #removing special charaters
                token = regex.sub(r'[^\p{L} ]', r'', token)

                if len(token) == 0:
                    continue
                # if(len(tokenized) > 1):
                #     print("multi token word {} is adding token: {}".format(w, token))
                stem = _stemmer.stem(token)
                if(stem in _stemDict):
                    _stemDict[stem] += 1
                else:
                    _stemDict[stem] = 1
        count += 1
    return _stemDict
print("Getting words..")
words = cess_esp.words()
# Was used to generate a list of words for testing ---
# if len(words) <= 0:
#     print("No words to print. closing without writting")
# with open("GL_words.txt", "a", encoding='utf-8') as gl_words_file:

#     first = True
#     for thing in cess_esp.words():
#         if first:
#             gl_words_file.write("[\'{}\'".format(thing))
#             first = False
#         else:
#             gl_words_file.write(", \'{}\'".format(thing))
    
#     gl_words_file.write("]")
# -------------------------------------------------------------------
print('total words: ' + str(len(words)))

freqDict = GetStemFreqDict(words)
GLF_list = list(freqDict.items())
print("Sorting based on freqency...")
GLF_list.sort(reverse=True, key= lambda x: x[1])

assert len(freqDict) == len(GLF_list), "The len of the freqDict doesn't matach the len of generated list version"
# print('freqDict: ' + str(len(freqDict)))
print('Length of GLF_list: ' + str(len(GLF_list)))
f = open("GLF_list.txt", "w", encoding='utf-8')
# f = open("GLF_list.txt", "a", encoding='utf-8')
f.write(str(GLF_list))
f.close()