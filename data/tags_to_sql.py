import sqlite3
import xmltodict

connection = sqlite3.connect("tags.db")
c = connection.cursor()
# need tags table, recipe table, tags to recipe table

c.execute('DROP TABLE IF EXISTS recipe')
c.execute("CREATE TABLE recipe (id INTEGER PRIMARY KEY, title TEXT, url TEXT NOT NULL)")
c.execute('DROP TABLE IF EXISTS tags')
c.execute("CREATE TABLE tags (id INTEGER PRIMARY KEY, tag TEXT UNIQUE NOT NULL)")
#c.execute('DROP TABLE IF EXISTS recipe_has_tag')
#c.execute("CREATE TABLE recipe_has_tag (recipe_id INTEGER FOREIGN KEY, tag_id INTEGER FOREIGN KEY)")
connection.commit()

with open("Budget_Bytes_scraping_2016-01-21_220058.xml","r") as f:
    indoc = f.read()
    recp_dict = xmltodict.parse(indoc)

for i in range(10):
    title = recp_dict['library']['recipe'][i]['title']
    url = recp_dict['library']['recipe'][i]['url']
    # unique key will self-generate in SQLite, injection return ID
    c.execute('INSERT INTO RECIPE (title, url) VALUES (?, ?)', [title, url])
    connection.commit()

    for tag in recp_dict['library']['recipe'][i]['tags']['tag']:
        # kick out first tag as title?
        print(tag)
        # unique key self-generates, return ID
        # check against existing tags - keep dict or SQL struct?

        # create entry linking title:tag




