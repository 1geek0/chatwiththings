import spacy;
from chatsenselib.responses import getAllScalarQuantities, getAllLocations

def islocation(sr,w):
    # print("debug: islocation(" + w + ")?");
    # print("debug: all locations = " + (" ".join(getAllLocations())));
    for x in getAllLocations():
        # print("debug:   comparing " + w + " to " + x);
        if (w == x):
            # print("debug:   found match");
            return(True);
    # print("debug: no match");
    return(False);
    
def matchlocation(sr,s):
    word = s["lemma"].lower()
    if (s["POS_fine"] == "NN" and
        islocation(sr,word)):
        sr["location"] = word
        # print("debug: setting location to " + word);
        return(True);
    else:
        for anotherelem in s["modifiers"]:
            anotherword = anotherelem["lemma"].lower();
            # print("debug: matchlocation 2nd case: " + word + " and " + anotherword);
            if (s["POS_fine"] == "NN" and
                anotherelem["POS_fine"] == "NN" and
                islocation(sr,anotherword + " " + word)):
                sr["location"] = anotherword + " " + word;
                # print("debug: setting location in case 2 to " + sr["location"]);
                return(True);
        return(False);
