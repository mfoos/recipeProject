from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

##################
# This crawler gets the most recent "Business and Finance" articles
# from the Brookings Institute, and prints out their title and lede
# (or the first paragraph)
#################

def getArticle(url):
    print("URL: "+url)
    html = urlopen(url)
    articleObj = BeautifulSoup(html.read(), 'html.parser')
    #Get article title. This should have a class name ending in "title"
    title = articleObj.find("h1", {"class":re.compile(".*title")}).get_text()
    print("TITLE: "+title)
    

# url = "http://www.budgetbytes.com/2015/12/slow-cooker-chicken-tikka-masala/"
# getArticle(url)

example = BeautifulSoup(open("testBB.html"), 'html.parser')
title = example.find("h1", {"class":re.compile(".*title")}).get_text()
print("TITLE: "+title)
