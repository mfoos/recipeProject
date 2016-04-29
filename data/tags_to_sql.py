import sqlite3
import xmltodict
#import unicodedata # gotta remember module name

connection = sqlite3.connect("tags.db")
c = connection.cursor()
# need tags table, recipe table, tags to recipe table

c.execute('BEGIN')
c.execute('DROP TABLE IF EXISTS recipe')
c.execute("CREATE TABLE recipe (id INTEGER PRIMARY KEY, title TEXT, url TEXT NOT NULL)")
c.execute('DROP TABLE IF EXISTS tag')
c.execute("CREATE TABLE tag (id INTEGER PRIMARY KEY, tag TEXT UNIQUE NOT NULL)")
c.execute('DROP TABLE IF EXISTS recipe_has_tag')
c.execute('''CREATE TABLE recipe_has_tag (recipe_id INTEGER, tag_id INTEGER, 
    FOREIGN KEY(recipe_id) REFERENCES recipe(id), 
    FOREIGN KEY(tag_id) REFERENCES tag(id))''')
connection.commit()

with open("Budget_Bytes_scraping_2016-01-21_220058.xml","r") as f:
    indoc = f.read()
    recp_dict = xmltodict.parse(indoc)

for i in range(len(recp_dict['library']['recipe'])):
    c.execute('BEGIN')
    title = recp_dict['library']['recipe'][i]['title']
    url = recp_dict['library']['recipe'][i]['url']
    # unique key will self-generate in SQLite, injection return ID
    c.execute('INSERT INTO RECIPE (title, url) VALUES (?, ?)', [title, url])
    recipe_id = c.lastrowid

    for tag in recp_dict['library']['recipe'][i]['tags']['tag'][1:]:
        # kick out first tag as title
        c.execute("SELECT rowid FROM tag WHERE tag = ?",[tag]) 
        tag_id = c.fetchone()
        # check against existing tags
        # error handle better here
        
        if tag_id:
            tag_id = tag_id[0]
            # contains tag key
            # error handle better here
        else:
            c.execute("INSERT INTO tag (tag) VALUES (?)",[tag])
            tag_id = c.lastrowid

        print("rec id",recipe_id,"tag",tag_id)
        c.execute("INSERT INTO recipe_has_tag (recipe_id, tag_id) VALUES (?,?)",[recipe_id, tag_id])
        # create entry linking title:tag

    connection.commit()

connection.close()
