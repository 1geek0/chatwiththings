import spacy
from chatsenselib.variables import mLangMapDB
from chatsenselib.parser1sensors import *
from chatsenselib.parser1locations import *

def matchscalarquantityinlist(sr,l):
    answer = False;
    for s in l:
        if (matchscalarquantity(sr,s)):
            answer = True;
        matchscalarquantityinlist(sr,s["modifiers"]);
    return(answer);

def matchlocationinlist(sr,l):
    answer = False;
    for s in l:
        if (matchlocation(sr,s)):
            answer = True;
        matchlocationinlist(sr,s["modifiers"]);
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
    print("debug: Found a " + sr["type"] + " for " + sr["quantity"] + " in location " + sr["location"]);

def foundrequestnolocation(sr,s):
    print("debug: Found a " + sr["type"] + " for " + sr["quantity"] + " in unspecified location");

def foundrequestnosensor(sr,s):
    print("debug: Found a " + sr["type"] + " but not clear for what");
    
def foundnorequest(sr,s):
    print("debug: Found no request");
    
def lookforrequest(s):
    semanticrepr = { "type": "", "quantity": "", "location": "" }
    if (matchposandlemma(semanticrepr,s,"VBZ","be") and
        matchposandlemmainlist(semanticrepr,s["modifiers"],"WP","what")):
        semanticrepr["type"] = "request for information";
    if (matchposandlemma(semanticrepr,s,"VB","show") and
        matchposandlemmainlist(semanticrepr,s["modifiers"],"PRP","me")):
        semanticrepr["type"] = "request for information";
    if (matchposandlemma(semanticrepr,s,"VB","give") and
        matchposandlemmainlist(semanticrepr,s["modifiers"],"PRP","me")):
        semanticrepr["type"] = "request for information";
    if (matchposandlemma(semanticrepr,s,"VB","display")):
        semanticrepr["type"] = "request for information";
    if (matchposandlemma(semanticrepr,s,"VB","set")):
        semanticrepr["type"] = "command to change";
    if (semanticrepr["type"] != ""):
        if (matchscalarquantityinlist(semanticrepr,s["modifiers"])):
            if (matchlocationinlist(semanticrepr,s["modifiers"])):
                foundrequestfull(semanticrepr,s);
            else:
                foundrequestnolocation(semanticrepr,s);
        else:
            foundrequestnosensor(semanticrepr,s);
    else:
        foundnorequest(semanticrepr,s);
