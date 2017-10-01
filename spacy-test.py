import spacy
from chatsenselib.parser1 import *
from chatsenselib.variables import *

nlp = spacy.load('en')

my_question = "";

try:
    while (my_question != "quit"):
        my_question = unicode(raw_input("How can I help you?\n"),"utf-8")
        if (my_question == "quit"):
            print("Bye!");
        else:
            doc = nlp(my_question)
            response = processrequest(doc)
            print(response+"\n")
except EOFError:
    print("Thank you, bye bye!");



            
