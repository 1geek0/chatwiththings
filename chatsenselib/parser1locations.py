import spacy;
from chatsenselib.responses import getAllScalarQuantities, getAllLocations

def islocation(sr,w):
    print("islocation(" + w + ")?");
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
        for anotherelem in s["modifiers"]:
            anotherword = anotherelem["lemma"].lower();
            #print("debug: matchlocation 2nd case: " + word + " and " + anotherword);
            if (s["POS_fine"] == "NN" and
                anotherelem["POS_fine"] == "NN" and
                islocation(sr,anotherword + " " + word)):
                sr["location"] = anotherword + " " + word;
                return(True);
        return(False);
