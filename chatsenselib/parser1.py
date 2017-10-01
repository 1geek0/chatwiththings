import spacy

def isscalarquantity(sr,w):
    if (w == "temperature" or
        w == "humidity" or
        w == "bubliness"):
        return(True);
    else:
        return(False);
        
def islocation(sr,w):
    if (w == "sauna" or
        w == "bathtub" or
        w == "outside"):
        return(True);
    else:
        return(False);
        
def matchscalarquantity(sr,s):
    word = s["lemma"].lower()
    if (s["POS_fine"] == "NN" and
        isscalarquantity(sr,word)):
        sr["quantity"] = word
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

def foundrequest(sr,s):
    if (sr["location"] != ""):
        print("Found a " + sr["type"] + " for " + sr["quantity"] + " in location " + sr["location"]);
    else:
        print("Found a " + sr["type"] + " for " + sr["quantity"] + " in unspecified location");
    
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
    if (semanticrepr["type"] != "" and
        matchscalarquantityinlist(semanticrepr,s["modifiers"])):
        matchlocationinlist(semanticrepr,s["modifiers"]);
        foundrequest(semanticrepr,s);
