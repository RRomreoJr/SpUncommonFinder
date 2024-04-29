import nltk
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer("spanish")

words = ['encargar(se)', 'listimar      ', 'encargarse', '', ' ']
'''
    I need to make sure that I get rid of white space before I tokenize

    encargar and encargarse both became encarg so that's nice I guess
'''
for word in words:
    tokenized = nltk.word_tokenize(word)
    print(tokenized)
    if tokenized:
        print(stemmer.stem(tokenized[0]))
        # for token in tokenized:
        #     print(stemmer.stem(token))