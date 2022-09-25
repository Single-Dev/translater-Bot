
import requests
import json
app_id = "d3efc512"
app_key = "ed12860d963de6f07e7cb2a5e22e51f2"
language = "en-gb"
word_id = "Uzbekistan"
url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
r = requests.get(url, headers={"app_id": app_id, "app_key": app_key}) 
res = r.json()
print(res)
