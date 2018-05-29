#!/usr/bin/python3
# -*- coding: utf-8 -*-

if __name__ is not "__main__":
    print("This is a module. Go to File-Maker and run \"python3 -m Channels.News_Channel.news\".")
    exit()

import sys
from .newsmake import process_news, sources
from threading import Thread as thread


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
        t = thread(target=process_news, args=(mode, source), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()