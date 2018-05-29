#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .newsdownload import *
from .newsmake import process_news, sources
from threading import Thread as thread
import sys

def main():
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
            t = thread(target=worker, args=(mode, source), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


def worker(mode, source):
    process_news(mode, source)


if __name__ == "__main__":
    main()