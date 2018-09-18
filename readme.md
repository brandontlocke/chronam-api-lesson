# Quickly Getting Plain Text from the Chronicling America API

Right-click on the Desktop and create a folder called "chronam" — we'll come back to this.

Let’s check out the [ChronAm advanced search web interface for the newspapers](https://chroniclingamerica.loc.gov/#tab=tab_advanced_search). 

Let’s search for the words “labor” or “union” in the Dearborn Independent newspaper while Henry Ford owned it:

- In ‘State’ select Michigan (this shouldn’t matter since we’re selecting an individual paper, but it seems to)
- In ‘Select Newspaper(s)’, find “Dearborn Independent. (Dearborn, Mich.)” (you can click in the box and start typing)
- For ‘Select Year(s)’, put in 1919-1927
- In the search, we’ll do “...with all of the words…” and put in “labor union”
- Click Search

This should bring up 149 results that include both labor and union in the results.

Let’s take a quick look at the URL for the results page - it shows us exactly what’s going on if we know what to look for:

https://chroniclingamerica.loc.gov/search/pages/results/?state=Michigan&lccn=2013218776&dateFilterType=yearRange&date1=1919&date2=1927&language=&ortext=&andtext=labor+union&phrasetext=&proxtext=&proxdistance=5&rows=20&searchType=advanced

Let's add `&format=json` to the end of that URL. This will bring our results back in json format instead of links to page images.

Check the results: [https://chroniclingamerica.loc.gov/search/pages/results/?state=Michigan&lccn=2013218776&dateFilterType=yearRange&date1=1919&date2=1927&language=&ortext=&andtext=labor+union&phrasetext=&proxtext=&proxdistance=5&rows=20&searchType=advanced&format=json](https://chroniclingamerica.loc.gov/search/pages/results/?state=Michigan&lccn=2013218776&dateFilterType=yearRange&date1=1919&date2=1927&language=&ortext=&andtext=labor+union&phrasetext=&proxtext=&proxdistance=5&rows=20&searchType=advanced&format=json)

Depending on your browser, it may or may not be easy to see the results. Scroll down a bit and you’ll see all kinds of metadata for the paper and the specific page that we’re looking at. Take note of the ‘ocr_eng’ field, which has all of the text for the page. (The ‘\n’ marks are new line markers—it makes it hard to read here, but we don’t really need to worry about them.) So now we know we can access information about each page, as well as the text of the page. There's just one more thing to deal with. 

It says that each page only returns 20 results...we'll need to add one more thing to the url to get all of the results in one page: `&rows=149`

[https://chroniclingamerica.loc.gov/search/pages/results/?state=Michigan&lccn=2013218776&dateFilterType=yearRange&date1=1919&date2=1927&language=&ortext=&andtext=labor+union&phrasetext=&proxtext=&proxdistance=5&rows=20&searchType=advanced&format=json&rows=149](https://chroniclingamerica.loc.gov/search/pages/results/?state=Michigan&lccn=2013218776&dateFilterType=yearRange&date1=1919&date2=1927&language=&ortext=&andtext=labor+union&phrasetext=&proxtext=&proxdistance=5&rows=20&searchType=advanced&format=json&rows=149)

Right click on the results page, select ‘save as,’ name it ‘fordlaborunion.json,’ and save it to the Desktop/chronam folder.

So, we now have everything in one json file, but we can’t really analyze it very well. We’ll want to split it out into individual files based on each page. We can do that if we [download this fairly short Python script](https://gist.githubusercontent.com/brandontlocke/f4cf37c38ad000bcd86cdf5769f31466/raw/fd0a7a99ca03697710edb3dbd82999d78dbfc2df/neh-chronam.py) (right click on an empty part of the page, click save as, and put it in your Desktop/chronam folder (it needs to be in the same folder as your json file) and make sure it’s called ‘neh-chronam.py'.

**On Windows**: Double-click on the ‘neh-chronam.py’ icon in the Desktop/chronam folder.

**On Macs**:
Open Terminal
`$ cd Desktop/chronam`
`$ python neh-chronam.py`

Now, using Windows Explorer/Finder, open up the Desktop/chronam folder and see what’s there.


---

## URL Breakdown

We’ll break this down:
`https://chroniclingamerica.loc.gov/search/pages/results/`
this is the main search results site for the project - there aren’t any fields specified, so it will bring up all 13.5 million results if we were to go to that address

`?`
this signifies that a query is coming-everything after this is the search material

`state=Michigan`
there are sets of keys and values; the first word tells us what field we’re searching and the second tells us what information we’re looking for. This is searching for papers in the state of Michigan

`&`
this appends another pair of keys and values; we’ll see it used a bunch here in the URL

`lccn=2013218776`
this is the unique identifier for the Dearborn Independent newspaper

`dateFilterType=yearRange&date1=1919&date2=1927`
this shows that the filter is years (not month/date/year) and searches for things between 1919 (date1) & 1927 (date2)

`language=&ortext=`
for some reason, LC leaves in all the blank fields; we left language and ‘any word’ blank

`andtext=labor+union`
this is the ‘all word’ field that we entered - it’s looking for only papers with both words

`phrasetext=&proxtext=&proxdistance=5&rows=20&searchType=advanced` 
more blank fields that are kept in the URL

## Python Script Breakdown

#!/usr/bin/env python

`import json`

```
with open('fordlaborunion.json') as json_file:  
    data = json.load(json_file)
```

```
    for p in data['items']:
        filename = p['date']+'_'+p['title']+'_'+"pg"+p['page']
```

```
        file = open(filename.replace(" ", "").replace(".", "")+".txt", "w")
        file.write(p['ocr_eng'])
```

`file.close()`