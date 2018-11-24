import json, urllib

API_LINK = "http://yerkee.com/api/fortune"

def getQuote():
    x = urllib.request.urlopen(API_LINK);
    d = json.loads( x.read() )
    txt = d['fortune']
    i = txt.rfind("--")
    if i == -1:
        return [txt, "Anonymous"]
    quote = txt[: i]
    cite = txt[i + 3: ]
    return [quote, cite];
