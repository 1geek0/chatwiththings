import spacy
from chatsenselib.parser1 import *
from chatsenselib.variables import *

nlp = spacy.load('en')

my_question = "";

while (my_question != "quit"):

    my_question = input("How can I help you?\n")

    if (my_question != "quit"):
        doc = nlp(my_question)
        response = processrequest(doc)
        print(response)
        
            
