import datetime
import sys


def main():
    wii_to_timestamp = (int(sys.argv[1]) * 60) + 946684800
    date = datetime.datetime.utcfromtimestamp(wii_to_timestamp).strftime('%Y-%m-%d %H:%M')
    print "Timestamp: %s" % wii_to_timestamp
    print "Date: %s" % date


if __name__ == "__main__":
    main()
