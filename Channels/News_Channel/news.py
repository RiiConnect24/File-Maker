#!/usr/bin/python3
# -*- coding: utf-8 -*-

if __name__ is not "__main__":
    print("This is a module. Go to File-Maker and run \"python3 -m Channels.News_Channel.news\".")
    exit()

import sys
import json
from .newsmake import process_news, sources
from threading import Thread as thread
import time
from datetime import datetime
import requests

with open("./Channels/News_Channel/config.json", "rb") as f:
    config = json.load(f)


# Store results (plain text of generated article titles) in order for Discord Webhooks (pretty messy)
webhook_information = [None]*len(sources)


def process_news_ordered(mode, source):
    webhook_information[list(sources.values()).index(source)] = {"username": "News Bot", "content": "News Data has been updated!",
                  "avatar_url": "https://rc24.xyz/images/logo-small.png", "attachments": [
                {"fallback": "News Data Update", "color": "#1B691E", "author_name": "RiiConnect24 News Script",
                "author_icon": "https://rc24.xyz/images/webhooks/news/profile.png", "text": process_news(mode, source),
                 "title": "Update!",
                 "fields": [{"title": "Script", "value": "News Channel (" + source["name"] + ")", "short": "false"}],
                 "thumb_url": "https://rc24.xyz/images/webhooks/news/%s.png" % mode,
                 "footer": "RiiConnect24 Script",
                "footer_icon": "https://rc24.xyz/images/logo-small.png",
                "ts": int(time.mktime(datetime.utcnow().timetuple()))}]}


print("-=" * 22 + "\n" + " " * 9 + "News Channel Data Generator\n" + " " * 6 + "By and only by Larsen Vallecillo\n" + " " * 17 + "rc24.xyz\n" + "-=" * 22)

if len(sys.argv) > 1:
    try:
        mode = sys.argv[1]
        source = sources[mode]
        process_news(mode, source)
    except KeyError:
        print("No such source: %s" % sys.argv[1])
else:
    threads = []

    for mode, source in sources.items():
        t = thread(target=(process_news_ordered if config["production"] else process_news), args=(mode, source), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    for webhook_json in webhook_information:  # No need to check if production again, array will be empty if not
        for url in config["webhook_urls"]:
            if requests.post(url, json=webhook_json, allow_redirects=True).status_code is not 200:
                print("Failed to call Discord Webhook %s" % url)
            time.sleep(5)  # Account for ratelimiting
