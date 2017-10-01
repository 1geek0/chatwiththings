import spacy
from chatsenselib.variables import mLangMapDB
from chatsenselib.responses import *
from chatsenselib.parser1sensors import *
from chatsenselib.parser1locations import *

def matchscalarquantityinlist(sr,l):
    answer = False;
    for s in l:
        if (matchscalarquantity(sr,s)):
            answer = True;
        if (matchscalarquantityinlist(sr,s["modifiers"])):
            answer = True;
    return(answer);

def matchlocationinlist(sr,l):
    answer = False;
    for s in l:
        if (matchlocation(sr,s)):
            answer = True;
        if (matchlocationinlist(sr,s["modifiers"])):
            answer = True;
    return(answer);

def matchposandlemma(sr,s,expectedpos,expectedlemma):
    if (s["POS_fine"] == expectedpos and
        s["lemma"].lower() == expectedlemma):
        return(True);
    else:
        return(False);
    
def matchposandlemmainlist(sr,l,expectedpos,expectedlemma):
    answer = False
    for s in l:
        if (matchposandlemma(sr,s,expectedpos,expectedlemma)):
            answer = True
        matchposandlemmainlist(sr,s["modifiers"],expectedpos,expectedlemma);
    return(answer);

def foundrequestfull(sr,s):
    # print("debug: Found a " + sr["type"] + " for " + sr["quantity"] + " in location " + sr["location"]);
    if (sr["type"] == "request for information"):
        val = str(getSensorValue(sr["quantity"],sr["location"]));
        return("The " + sr["quantity"] + " is " + val + ".");
    else:
        return("Sorry, I cannot do that (yet).");

def foundrequestnolocation(sr,s):
    # print("debug: Found a " + sr["type"] + " for " + sr["quantity"] + " in unspecified location");
    if (sr["type"] == "request for information"):
        return("You would like to get " + sr["quantity"] + ", but for what? Can you specify where?");
    else:
        return("You would like to change something in " + sr["quantity"] + ", but can you specify where?");

def foundrequestnosensor(sr,s):
    # print("debug: Found a " + sr["type"] + " but not clear for what");
    if (sr["location"] == ""):
        return("I'm sorry, you are talking about a " + sr["type"] + " but what for?");
    else:
        return("I'm sorry, you are talking about a " + sr["type"] + " but what for? What do you want to know about the " + sr["location"] + "?");
    
def foundnorequest(sr,s):
    # print("debug: Found no request");
    return("I'm sorry, I did not understand. What do you want?");
    
def lookforrequest(s):
    semanticrepr = { "type": "", "quantity": "", "location": "" }
    #print("debug: first pos and lemma: " + s["POS_fine"] + ", " + s["lemma"]);
    #if (len(s["modifiers"]) > 0):
    #   print("debug: second pos and lemma: " + s["modifiers"][0]["POS_fine"] + ", " + s["modifiers"][0]["lemma"]);
    if (semanticrepr["type"] == "" and
        matchposandlemma(semanticrepr,s,"VBZ","be") and
        matchposandlemmainlist(semanticrepr,s["modifiers"],"WP","what")):
        semanticrepr["type"] = "request for information";
    if (semanticrepr["type"] == "" and
        matchposandlemma(semanticrepr,s,"VB","show") and
        matchposandlemmainlist(semanticrepr,s["modifiers"],"PRP","me")):
        semanticrepr["type"] = "request for information";
    if (semanticrepr["type"] == "" and
        matchposandlemma(semanticrepr,s,"VB","show")):
        semanticrepr["type"] = "request for information";
    if (semanticrepr["type"] == "" and
        matchposandlemma(semanticrepr,s,"VB","give") and
        matchposandlemmainlist(semanticrepr,s["modifiers"],"PRP","me")):
        semanticrepr["type"] = "request for information";
    if (semanticrepr["type"] == "" and
        matchposandlemma(semanticrepr,s,"VB","give")):
        semanticrepr["type"] = "request for information";
    if (semanticrepr["type"] == "" and
        matchposandlemma(semanticrepr,s,"VB","display")):
        semanticrepr["type"] = "request for information";
    if (semanticrepr["type"] == "" and
        matchposandlemma(semanticrepr,s,"VB","set")):
        semanticrepr["type"] = "command to change";
    if (semanticrepr["type"] != ""):
        if (matchscalarquantityinlist(semanticrepr,s["modifiers"])):
            if (matchlocationinlist(semanticrepr,s["modifiers"])):
                return(foundrequestfull(semanticrepr,s));
            else:
                return(foundrequestnolocation(semanticrepr,s));
        else:
            matchlocationinlist(semanticrepr,s["modifiers"])
            return(foundrequestnosensor(semanticrepr,s));
    else:
        return(foundnorequest(semanticrepr,s));

def processrequest(doc):
    result = "";
    # print("debug: Looking for requests in " + doc.text + "...");
    for s in doc.print_tree():
        if (result != ""):
            result = result + " ";
        result = result + lookforrequest(s);
    return(result)
