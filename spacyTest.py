import spacy

def get_dictionary_forms(words):
    nlp = spacy.load("es_core_news_sm")
    dictionary_forms = []
    for word in words:
        doc = nlp(word)
        # Extract the lemma for each word
        lemma = doc[0].lemma_
        dictionary_forms.append(lemma)
    return dictionary_forms

# words = ['Los', 'jinetes', 'vestían', 'armaduras', 'de', 'escamas', 'de', 'cobre', ',',
#          'y', 'yelmos', 'con', 'hocicos', 'de', 'jabalí', 'y', 'colmillos', 'también',
#          'de', 'cobre', ',', 'rematados', 'por', 'largos', 'penachos', 'de', 'seda', 'negra']
words = ['apodo', 'apoda', 'apodan', 'apodas', 'apodaste', 'pintado']
# becomes ['apodo', 'apodar', 'apodar', 'apoda', 'apodastir']
dictionary_forms = get_dictionary_forms(words)
print(dictionary_forms)