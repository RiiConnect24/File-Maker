# News Channel

These are the scripts we use to run the News Channel.

## Files

### Scripts

+ newsdownload.py downloads the news from the news site.
+ newsmake.py parses the news data into a data file the News Channel loads.
+ news.py calls newsdownload and newsmake with the news source to download from.

The "logos" folder contains the news source logos that will show up on the News Channel.

## How to Add Your Own News Source

If you want to add your own news source (if you have a valid reason to do so) here are some instructions.

NOTE: I recommend you have a little bit of Python experience before you go any further.

First, go in newsdownload.py and take a look at the `sources` dictionary:

+ Key: ID used for the news source.
+ Values:
    + name: Name of the news source. If using a custom logo for the news source, it needs to use the same name for the JPEG.
    + url: Base URL for the RSS feeds. We use `%s` substitutions for the categories (will be explained later)
    + lang: Language that the news is in. It's used for the newspaper module in order for it to know what language to get the news in. You can find the list of available languages with the `newspaper.languages()` command, but we only support 7 (Japanese, English, German, French, Spanish, Italian, and Dutch).
    + cat: Categories for the news:
        + Key: RSS feed name to substitute in url.
        + Value: ID used internally for the news category.

Next, jump to the `Parse` class. In the `__init__` function, add an entry:

+ Key: Needs to match the key used for the `sources` dictionary (the news source ID).
+ Value: Name of the function we will define to manage special things for the news source.

Now define the function for the `Parse` class. The two main things you usually have to manage in this function are:

+ Caption. newspaper unfortunately doesn't automatically parse captions, so normally you can grab it from the HTML with BeautifulSoup.
+ Location. Hopefully you are using a news source that has the location at the start of the article.

Confused? Look at the other functions to see how it's done.

Now for newsmake.py, take a look at the `sources` dictionary there:

+ Key: Needs to match the key used for the other `sources` dictionary (the news source ID).
+ Values:
    + topics_news: News topics used.
        + Key: Topic name used in the actual News Channel.
        + Value: Needs to match the value used in the `cat` dictionary inside the other `sources` dictionary.
    + languages: List of languages that is used for a hidden language selection screen that can only be toggled with an integer in the file. The way we do it is have it be [0] if the source is to be used in Japan, [1, 3, 4] for America, and [1, 2, 3, 4, 5, 6] for Europe.
    + language_code: Used to indicate the language used for the source.
        + 0: Japanese
        + 1: English
        + 2: German
        + 3: French
        + 4: Spanish
        + 5: Italian
        + 6: Dutch
    + country_code: Used to indicate the country code for the file. Since the news files we make are identical per country in a region, we just set it to 1 for Japan, 49 for America, and 110 for Europe.

A couple more things, and you're done:

In the `source_nums` dictionary in the `make_source_nums` function, you need to add an entry:

+ Key: Needs to match the key used for the `sources` dictionary from newsdownload.py (the news source ID).
+ Value: This needs to be an array:
    + 1st Entry: Logo to use.
        + 0: Custom Logo
        + 1: Mainichi
        + 2: News24
        + 3: Associated Press
        + 4: AFP
        + 5: ANP
        + 6: ANSA
    + 2nd Entry: Position for the logo to use.
        + 1: https://imgur.com/I3H59qp
        + 2: https://imgur.com/uzwwgsy
        + 3: https://imgur.com/heqzeTz
        + 4: https://imgur.com/AJAQndN
        + 5: https://imgur.com/3rQxpVJ
        + 6: https://imgur.com/f1O8VjS

If using a custom logo, add the ID that matches the one used in `sources` from newsdownload.py to the `sources` array in the `make_source_pictures` function

That's it! If you made it this far, I'd give you a few cookies if I could, unless you just skipped all the way to the end of here.