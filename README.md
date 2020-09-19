# Articles_scraper_api
scraping bbc articles with scrapy and provide API

### This will crawl bbc and save the data in Mongo Data base :
```
scrapy crawl bbc
```

### Save the data in a json file :

This will crawl bbc and save the data in a file called bbc.json.
```
scrapy crawl bbc -o bbc.json
```



# The structure of bbc spider
This spider can mainly scrape the articles  from the home page of bbc, in this form: 

```
{
  "title": "", 
  "url": "", 
  "related_topics": : "", 
  "aricle_text": "", 
}

```

### to show result :

Run app.py in Command prompt.
```
python app.py
```

Our local web server is running in the port 5000 by default.
