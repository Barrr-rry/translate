import spacy


def similarity(sentence1, sentence2):
    nlp = spacy.load('en_core_web_sm')
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)
    return doc1.similarity(doc2)
