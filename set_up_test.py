# coding=utf8
'''
GLF = General language frequency

Generates a list of tuples and orders them based on the frequency in the
"general language" which I'm defining as whatever is in cess_esp.words()
'''
import sys
import os
import nltk
print("nltk imported")
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("spanish")
print("Snowball stemmer good")
from nltk.corpus import cess_esp

words = cess_esp.words()
print("corpora good")


