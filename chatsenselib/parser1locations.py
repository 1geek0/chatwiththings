import spacy;
from chatsenselib.responses import getAllScalarQuantities, getAllLocations

def islocation(sr,w):
    if w in getAllLocations():
        return(True);
    else:
        return(False);
    
def matchlocation(sr,s):
    word = s["lemma"].lower()
    if (s["POS_fine"] == "NN" and
        islocation(sr,word)):
        sr["location"] = word
        return(True);
    else:
        return(False);
    
