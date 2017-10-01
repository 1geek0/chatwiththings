
def isscalarquantity(sr,w):
    if (w == "temperature" or
        w == "humidity" or
        w == "bubliness"):
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
    
def matchscalarquantityinlist(sr,l):
    for s in l:
        if (matchscalarquantity(sr,s)):
            return(True);
    return(False);

def matchposandlemma(sr,s,expectedpos,expectedlemma):
    if (s["POS_fine"] == expectedpos and
        s["lemma"].lower() == expectedlemma):
        return(True);
    else:
        return(False);
    
def matchposandlemmainlist(sr,l,expectedpos,expectedlemma):
    for s in l:
        if (matchposandlemma(sr,s,expectedpos,expectedlemma)):
            return(True);
    return(False);

def foundrequest(sr,s):
    print("Found a " + sr["type"] + " for " + sr["quantity"] + " in location " + sr["location"]);
    
def lookforrequest(s):
    semanticrepr = { "type": "request", "quantity": "", "location": "" }
    if (matchposandlemma(semanticrepr,s,"VBZ","be") and
        matchposandlemmainlist(semanticrepr,s["modifiers"],"WP","what") and
        matchscalarquantityinlist(semanticrepr,s["modifiers"])):
        foundrequest(semanticrepr,s);
