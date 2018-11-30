import json
import urllib.request

API_LINK = "http://yerkee.com/api/fortune"

def getQuote():
    raw = urllib.request.urlopen(API_LINK);
    json_data = json.loads( raw.read() )
    txt = json_data['fortune']
    name = txt.rfind("--")
    if name == -1:
        return [txt, "Anonymous"]
    quote = txt[: name]
    cite = txt[name + 3: ]
    return [quote, cite];
