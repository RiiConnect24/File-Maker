# News Channel

Thanks for your interest in helping out with RiiConnect24's File Maker.

Please read on to learn how to add your own news source (and PR it to us).

## Files

### Scripts

+ newsdownload.py downloads the news from the news site.
+ newsmake.py parses the news data into a data file the News Channel loads.
+ news.py calls newsdownload and newsmake with the news source to download from.

The "logos" folder contains the news source logos that will show up on the News Channel.

## How to Contribute

If you want to add your own news source (if you have a valid reason to do so) here are some instructions.

NOTE: The way we download and parse the news might not be the best Pythonic way to do so, but it gets the job done. Sorry if you think my instructions are poorly written, this is just some raw instructions. And adding a news source will be tricky and I recommend you have a little bit of Python experience before you go any further.

First, go in newsdownload.py and make a function that will call another function to download the news. Put as many categories as you want.

+ The key in topics_name is what the topic name will internally be called when downloading the news and making the file.
+ The value in topics_name is what the topic will be called on the Wii.
+ The key in topics should be the same as topics_name.
+ The value in topics should be a list of RSS feeds to use. If a source uses the same URL format, just put something the URL will be identified by. So if the URL for national news is http://mcnxne.ws/rss/national and the URL for international news is http://mcnxne.ws/rss/international, just put "national" or "international" for this value.

Let's say our news source is called MCNX News.

```python
def download_mcnx_news():
	print "Downloading from MCNX News (English)...\n"

	topics_name = collections.OrderedDict()

	topics_name["national"] = "National News"

	topics = collections.OrderedDict()

	topics["national"] = ["USHEADS"]

	return download_mcnx_news(topics_name, topics, "en")
```

Then make the function for that news source that will go through each news article in an RSS feed and parse it with something like this:

```python
def download_efe(mode, topics_name):
	data = collections.OrderedDict()

	numbers = 0

  for rss_category in topics.items():
		numbers = 0

		print "Downloading %s..." % topics_name[rss_category[0]]

		print "\n"

		for rss in rss_category[1]:
			rss_feed = feedparser.parse(requests.get("http://mcnxne.ws/rss/%s").text)

    	for items in rss_feed.entries:
    		try:
      		updated = parser.parse(items.updated)
      		updated = updated.astimezone(tz.tzutc())

      		updated = (int(time.mktime(updated.timetuple()) - 946684800) / 60)

      		time_current = (int(time.mktime(datetime.utcnow().timetuple())) - 946684800) / 60

      		if updated >= time_current - 60:
      			numbers += 1

      			print "Downloading News Article %s..." % (str(numbers))

      			parsedata = parsedata_mcnx_news(items["link"], items["title"], updated)

      			if parsedata != None: data[category + str(numbers)] = parsedata
        except: print "Failed".

    	return data
```

Now make a function to parse the data. You can look how we did it in the newsdownload code, **it might not be the best way to do it** but it gets the job done.

The function should return a list in this order:

1. Published time. In all cases, we've just used the updated time. (Make sure you're packing it in a u32)
1. Updated time. (Also make sure it's being packed in a u32)
1. Article.
1. Headline. We've got the headline in most cases by passing it to this function from the title in the RSS feed.
1. Picture. It should be ran through the `shrink_image` function. It can be set to None.
1. Credits (for the image).
1. Caption (for the image).
1. Location. We try to use sources which have the location associated with the article, and we extract that from the article.
1. Source name. We've been using `mcnx_news` for the source name all this time, so make sure you use exactly the same name.
1. Category the news falls under. It needs to match the key in topics_name and topics.

Nice! You have got the hardest part out of the way if you've made it this far, now let's add code for it to be parsed in newsmake.

Find the if/else statement in `make_news_bin` and add an entry there for your news source. Like this:

```python
if mode == "mcnx_news":
		topics_news = collections.OrderedDict()

		topics_news["National News"] = "national"

		languages = [1, 3, 4]

		language_code = 1

		country_code = 49
```

topics_news should just be like topics_name in the first function you made, just switch the values with the key to make it.

Don't worry about languages and country_code much.

The language code should match the language you're making a news source for:

+ 0 - Japanese
+ 1 - English
+ 2 - German
+ 3 - French
+ 4 - Spanish
+ 5 - Italian
+ 6 - Dutch

Now look at the `make_source_table` function. Add the source name you have been using as a key.

The first value in the list you'll get has to be what logo you're gonna use.

Number|Value
:-----:|:-----:
0 |Custom Logo
1 |Mainichi
2 |News24
3 |Associated Press
4 |AFP
5 |ANP
6 |ANSA

The second value has to be the position the logo should correspond to how you want it to look:

Number|Result
:-----:|:-----:
1 |http://imgur.com/I3H59qp
2 |http://imgur.com/uzwwgsy
3 |http://imgur.com/heqzeTz
4 |http://imgur.com/AJAQndN
5 |http://imgur.com/3rQxpVJ
6 |http://imgur.com/f1O8VjS

OK, that's done. You're probably gonna be using a custom logo for your news source, so find a good picture of the logo you want to use and make it really small. How small? See how small the logos are by browsing the "logos" folder. If you're going to use "1" or "2" you're probably going to have to make it a bit smaller than the rest of them.

The picture you got needs to be saved in a baseline JPEG. Remove the metadata by playing with the `shrink_image` function and make the quality be decent but the smaller the logo filesize, the better. Put your logo in the "logos" folder with the source name.

Since you're probably using your own logo, add the source name to the `sources` list in `make_source_pictures`.

You're almost done! Add a copyright to the `copyrights` dictionary in the `make_source_name_copyright` function, using the source name as the key, as with everything else.

Now go into `news.py` and add a function call to the news download function:

`elif sys.argv[1] == "mcnx_news": download_source("MCNX News", "mcnx_news", 1, ["018"], download_mcnx_news())`

The `download_source` function call should have the arguments in this order:

+ Source name (this time, use the full name of the news source if you aren't already)
+ The source name you've been using for everything else
+ Language Code
+ List of country codes to copy the file to. [You can get the country codes here.](http://wiibrew.org/wiki/Country_Codes)

Also add the news source name to the "Invalid argument" text below this.

Now remove the "elif" statement" and put it in the same order in the "else" statement below that where the function calls are again.

You're done! If you figured everything out and got it working, I think you're smart! It's not like I expected you to follow all these steps...
