import spacy
from chatsenselib.parser1 import *

nlp = spacy.load('en')
doc1 = nlp(u'This is a sentence.')
doc2 = nlp(u'What is the temperature in the living room?')
s2 = doc2.print_tree()[0]

print("Looking for requests in " + doc2.text);
        
for s in doc2.print_tree():
    lookforrequest(s)
