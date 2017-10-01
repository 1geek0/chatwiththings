import spacy
from chatsenselib.parser1 import *
from chatsenselib.variables import *

my_question = input("How can I help you?\n")
nlp = spacy.load('en')
doc1 = nlp(u'This is a sentence.')
doc2 = nlp(str(my_question))
s2 = doc2.print_tree()[0]

print("Looking for requests in " + doc2.text);
        
for s in doc2.print_tree():
    lookforrequest(s)
