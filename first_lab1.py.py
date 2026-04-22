
import requests 
from bs4 import BeautifulSoup
import csv


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


#open a csv file to write the data we will extract from the website in it
with open("test1.csv","w",encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name of the repository", "description of the repository", "number of stars of the repository", "name of the owner of the repository", "date of the last update of the repository"])


# i want to extract the name of the repository, the description of the repository, the number of stars of the repository, the name of the owner of the repository and the date of the last update of the repository
# and put it in a csv file with the name of the repository, the description of the repository, the number of stars of the repository, the name of the owner of the repository and the date of the last update of the repository as header of the csv file

# name of the classe of each post of the repersitory is "result-module_result_Up5vk" 
while True:
    soup = BeautifulSoup(s, "html.parser") 
    repositories = soup.find_all('results-list', className='List-module__List__fNMbL')
    for repository in repositories:
        name = repository.find("div", class_="Result-module__Result__Up5vk").text.strip() 
        name = repository.find("\n", "Header-module__header__sJ0g1").text.strip()
        description = repository.find("p", class_="mb-1").text.strip() 
        stars = repository.find("a", class_="Link--muted").text.strip()
        owner = repository.find("a", class_="mr-1").text.strip()
        date = repository.find("relative-time")["datetime"]
        last_update = repository.find("relative-time").text.strip()
        with open("test1.csv","a",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([name, description, stars, owner, date])
    next_page = soup.find("a", class_="next_page")
    if next_page:
        url = "https://github.com/search?q=mental+health+ai&type=repositories" + next_page["href"]
        page = requests.get(url, headers=header)
        s=page.text
    else:
        break




with open("test1.csv","r",encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)    
