# Sensory Recipe Access

*Update:* Ultimately, the death knell for this project came when The New York
Times published
[this](http://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/)
blog post about how it had taken them 20 years to produce an algorithm to
extract structured data from recipes. This hamstringing stage in my project, 
had I realized it existed, would have fallen between the first and second steps below.

Essentially the goal was to create an engine capable of recommending me a
"cheesy" recipe when I ask for one.

Plan
* Scrape a trusted, curated recipe blog (with permission)
* Create an SQL database to hold the recipe skeleton (title, tags, ingredients)
* Use keyword search & supervised ML to create subjective descriptors (like
  "cheesy") for searching on
* Implement a simple front end for db
* Iterate
