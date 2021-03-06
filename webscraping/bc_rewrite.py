from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import time
from lxml import etree
import unicodedata
from datetime import datetime
import pickle
import os

##################
# This script goes through the Budget Bytes archive by month and retrieves
# ingredients and tags for each recipe, ignoring non-recipes. Data gets stored
# in an XML file for later use.
#
# DO NOT USE THIS SCRIPT TO SCRAPE BUDGET BYTES WITHOUT PERMISSION
#################

def getRecipe(url):
    print("URL: "+url)
    time.sleep(1)
    response = requests.get(url)
    if not response.status_code < 400:
        return
    html = urlopen(url)
    recipeObj = BeautifulSoup(html.read(), 'html.parser')

    title = recipeObj.find("h1", {"class":re.compile(".*title")}).get_text()
    ingredients = [i.get_text() for i in recipeObj.find_all("li",{"class":"ingredient"})]
    if not ingredients:
        # no ingredients means a non-recipe post (news, how-to, etc)
        return
    tags = recipeObj.findAll(attrs={"name":"shareaholic:keywords"})[0]['content'].split(',')
    writeXML(url, title, ingredients, tags)    


def getIndivUrls(baseUrl):
    if os.path.isfile("cacheLinks"):
        with open("cacheLinks","rb") as f:
            return pickle.load(f)
    else: 
        allLinks = []
        for yr in range(2009, 2017):
           for mon in range(1,13):
                if (yr > 2009) | (mon > 4):
                # some (?!) of the non-existant months redirect, so going manual
                    archivUrl = baseUrl + str(yr) + "/" + str(format(mon,'02d')) + "/"
                    print("month page: " + archivUrl)
                    response = requests.get(archivUrl)
                    if not response.status_code < 400:
                        break
                    time.sleep(1)
                    html = urlopen(archivUrl)
                    recipeObj = BeautifulSoup(html.read(), 'html.parser')
                    allUrls = recipeObj.findAll("a",{"rel":"bookmark"})
                    allLinks.extend([i.get('href') for i in allUrls])
        with open("cacheLinks","wb") as f:
            pickle.dump(allLinks, f)
        return allLinks


def writeXML(url, title, ingreds, tags):
    root = etree.Element("recipe")
    # top level brackets for each recipe
    xurl = etree.SubElement(root, "url")
    xurl.text = url

    xtitle = etree.SubElement(root, "title")
    xtitle.text = title

    xingreds = etree.SubElement(root, "ingredients")
    for i in ingreds:
        # reads in wackadoo vulgar fractions
        etree.SubElement(xingreds, "ingredient").text = i
    
    xtags = etree.SubElement(root, "tags")
    for t in tags:
        etree.SubElement(xtags, "tag").text = t.strip()

    ofile.write(etree.tostring(root, pretty_print = False).decode('utf-8'))
    # in current setup tostring creates a bytes object

                    
baseUrl = "http://www.budgetbytes.com/"
links = getIndivUrls(baseUrl)
filename = "Budget_Bytes_scraping_" + datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".xml"
with open(filename, 'w') as ofile:
    ofile.write("<library>")
    for url in links:
        getRecipe(url)
    ofile.write("</library>")
