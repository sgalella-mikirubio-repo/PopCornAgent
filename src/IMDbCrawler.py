"""
Project: PopCornAgent
Name: IMDbCrawler.py
Authors: mikirubio & sgalella
Description: crawl IMDb to retrieve information about the recommended film
"""

from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import rdflib
import rdflib.plugins.sparql as sparql
import os

def retrieveData(movie_name):
    
    g = rdflib.Graph()
    g.parse("../data/PopCornOntology.owl")
    
    q = g.query("""
        PREFIX mov: <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
        SELECT ?code
        WHERE {?movie mov:URLcode ?code .
               ?movie mov:Name ?name .
               FILTER (str(?name) = '"""+movie_name+"""')}
        """)
    for row in q:
        URLcode = row[0].rsplit('#')[-1]
                     
    q = g.query("""
        PREFIX mov: <http://www.semanticweb.org/sgalella/ontologies/2018/11/movieAgent#>
        SELECT ?netflix
        WHERE {?movie mov:inNetflix ?netflix .
               ?movie mov:Name ?name .
               FILTER (str(?name) = '"""+movie_name+"""')}
        """)
    for row in q:
        inNetflix = row[0].rsplit('#')[-1]
    
    quote_page = 'https://www.imdb.com/title/tt'+URLcode
    page = urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    
    ## Retrieve image
    imgs = soup.findAll("div", {"class":"poster"})
    for img in imgs:
        for a in img.find_all('img', alt=True):
            link = a['src']
         
    
    urlretrieve(link, "image.png")
    
    q=mpimg.imread("image.png",0)
    imgplot = plt.imshow(q)
    plt.axis('off')
    plt.show()
    

    
    tdTags = soup.find_all("div", {"class": "title_wrapper"})
    for tag in tdTags:
        a = tag.find_all("h1")
        for i in a:
            name = i.text
    
    name = name.split()
    name = ' '.join(name[0:len(name)-1])
    
    
    print("Name: "+name+'\n')
    
    rate_box = soup.find('span', attrs={'itemprop': 'ratingValue'})
    rate = rate_box.text.strip()
    
    year_box = soup.find('span', attrs={'id': 'titleYear'})
    year = year_box.text.strip()
    
    print("Rate: "+rate+'\n')
    print("Year: "+year[1:5]+'\n')    

    i = 0
    labels = ['Director: ','Writers: ','Actors: ']
    tdTags = soup.find_all("div", {"class": "credit_summary_item"})
    for tag in tdTags:
        tdTags = tag.find_all("a", href=True)
        if i==0:
            print(labels[i],end="")
        else:
            print("\n\n"+labels[i],end="")
        i+=1
        j = 0
        for foo in tdTags:
            if foo.text == 'See full cast & crew' or foo.text == '1 more credit' or \
            foo.text == '2 more credit' or foo.text == '3 more credits':
                continue
            if j == 0:
                print(foo.text, end="")
                j+=1
            else:
                print(", "+foo.text, end="")
    print("\n")
    tdTags = soup.find_all("div", {"class": "inline canwrap"})
    for tag in tdTags:
        a = tag.find_all("span")
        for i in a:
            description = i.text
    
    if inNetflix == 1:
        print("Available in Netflix: Yes")
    else:
        print("Available in Netflix: No")
            
    print("\nDescription: "+' '.join(description.split()))
    
    print("\nIf you want more information, you can go to "+quote_page+'\n')
    
    os.remove("image.png")

