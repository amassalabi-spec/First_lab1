
import requests
"""commentaire
before starting web scraping we create once an virtuale environnement for this project
after we import the requests environment 
the variable url get take a link of the url of the serveur(which contain the web) that will be scraped
and after it we have the header, it is important in the sense that , it notice to the serveur that
it is not an robot but an requet and give it some information in his host, connection user-Agent the most
important thing in this header because it give it some information on the type of system on the sender computer,
the name of the web acces navigator and also all necessaire information to recognize th computer.
and finally there the variable which receive the request and write it with print if it's done successful or not.
and also to write it in an text file.
"""

url="https://github.com/search?q=mental+health+ai&type=repositories"


header = {
    "Host" :"github.com",
    "connection" :"keep-alive",
    "Accept" :"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Referrer" : "https://www/google/com/",
    "Accept-Encoding" :"gzip, deflate, sdch",
    "Accept-Language" : "en -US, en; q=0.8"
}

page = requests.get(url, headers=header)

print(page)
s=page.text
with open("test1.txt","w",encoding="utf-8") as f:
    f.write(s)

import os
print("Le fichier est ici :", os.getcwd())