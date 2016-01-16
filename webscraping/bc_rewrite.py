from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import time
import lxml

##################
# This script goes through the Budget Bytes archive by month and retrieves
# ingredients and tags for each recipe, ignoring non-recipes. Data gets stored
# in an XML file for later use.
#################

def getRecipe(url):
    print("URL: "+url)
    time.sleep(1)
    html = urlopen(url)
    recipeObj = BeautifulSoup(html.read(), 'html.parser')
    #recipeObj = BeautifulSoup(open("testBB.html"), 'html.parser')

    title = recipeObj.find("h1", {"class":re.compile(".*title")}).get_text()
    ingredients = [i.get_text() for i in recipeObj.find_all("li",{"class":"ingredient"})]
    if not ingredients:
        return
    tags = recipeObj.findAll(attrs={"name":"shareaholic:keywords"})[0]['content'].split(',')
    print(title) 


def getIndivUrls(baseUrl):
    #for yr in range(2009, 2017):
       #for mon in range(1,13):
            #if (yr > 2009) | (mon > 4):
                yr = 2015
                mon = 6
                archivUrl = baseUrl + str(yr) + "/" + str(format(mon,'02d')) + "/"
                html = urlopen(archivUrl)
                recipeObj = BeautifulSoup(html.read(), 'html.parser')
                allUrls = recipeObj.findAll("a",{"rel":"bookmark"})
                allLinks = [i.get('href') for i in allUrls]
                for link in allLinks:
                    getRecipe(link)

def writeXML(url, title, ingreds, tags):
    
                    
baseUrl = "http://www.budgetbytes.com/"
getIndivUrls(baseUrl)