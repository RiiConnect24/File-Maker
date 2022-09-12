#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# FORECAST CHANNEL GENERATION SCRIPT
# VERSION 5.1
# AUTHORS: JOHN PANSERA, LARSEN VALLECILLO
# ***************************************************************************
# Copyright (c) 2015-2022 RiiConnect24, and its (Lead) Developers
# ===========================================================================

import binascii
import calendar
import CloudFlare
import io
import json
import math
import os
import pickle
import queue
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime

import nlzss
import requests
import rsa
from Channels.Forecast_Channel import forecastlists
from datadog import statsd
from utils import setup_log, log, u8, u16, u32, s8

import faulthandler

faulthandler.enable()


class Forecast:
    def __init__(self):
        self.VERSION = 5.1
        self.GLOBE_CONSTANT = 360 / 65536
        self.REFRESH_RATE = 0.15

        self.apirequests = 0  # API Request Counter
        self.bandwidth = 0.0  # Bandwidth
        self.bins = []
        self.bw_usage = 0  # Bandwidth Usage Counter
        self.cache = None
        self.cached = 0  # Count Cached Cities
        self.cities = 0  # City Counter
        self.citycount = 0  # City Progress Counter
        self.constant = None
        self.country_code = 0
        self.currentlist = None
        self.elapsed_time = 0  # Elapsed Time
        self.errors = 0  # Errors
        self.extension = None
        self.forecast_list = None
        self.lists = 0  # Lists Counter
        self.language_code = None
        self.location_keys = None
        self.mode = None
        self.retrycount = 0  # Retry Counter
        self.seek_base = 0  # Base Offset Calculation Location
        self.seek_offset = 0  # Seek Offset Location
        self.shortcount = None
        self.threads = None
        self.threads_run = None
        self.ui_run = None
        self.weather_data = {}

        self.uvindex = {}
        self.wind = {}
        self.times = {}
        self.pollen = {}
        self.today = {}
        self.week = {}
        self.tomorrow = {}
        self.hourly = {}
        self.precipitation = {}
        self.current = {}
        self.globe = {}
        self.weatherloc = {}
        self.cache = {}
        self.laundry = {}
        self.location_keys = {}

        with open("./Channels/Forecast_Channel/config.json", "rb") as f:
            self.config = json.load(f)
        if self.config["production"] and self.config["send_logs"]:
            setup_log(self.config["sentry_url"], False)
        self.location_keys = pickle.load(open("weather.db", "rb"))["location_keys"]
        self.api_key = "6e30dc9ea2aa4d3eb99ad8f6630174cd"
        self.s = requests.Session()  # Use session to speed up requests
        self.s.headers.update(
            {"Host": "api.accuweather.com"}
        )  # using gzip actually seems to slow it down a bit
        self.total_time = time.time()
        self.q = queue.Queue()
        self.q2 = queue.Queue()
        self.threads = []
        self.concurrent = 15 if self.config["multithreaded"] else 1
        self.ui_run = None
        self.threads_run = True
        key = open(self.config["key_path"], "rb")  # Loads the RSA key.
        self.private_key = rsa.PrivateKey.load_pkcs1(key.read(), "PEM")
        key.close()
        self.ui_thread = threading.Thread(target=self.ui)
        self.ui_thread.daemon = True
        self.ui_thread.start()
        self.spawn_threads()

        self.threads = []

        for forecast_list in forecastlists.weathercities:
            self.forecast_list = forecast_list
            self.status = 1
            self.language_code = 1
            self.shortcount = 0
            self.listid = forecastlists.weathercities.index(forecast_list) + 1
            self.currentlist = list(forecast_list.values())[0][2][1]
            self.ui_run = True
            self.weather_data = {}
            self.country_code = forecastlists.bincountries[self.currentlist]
            self.region_flag = self.get_region_flag(self.country_code)
            self.bins = self.get_bins(self.country_code)
            self.populate_international(forecast_list)
            self.generate_locationkeys(forecast_list)
            for key in forecast_list.keys():
                if (
                    not self.matches_country_code(forecast_list, key)
                    or self.get_region(forecast_list, key) == ""
                ):
                    self.shortcount += 1
                if key in self.cache and self.cache[key] == self.get_all(
                    forecast_list, key
                ):
                    self.cached += 1
                else:
                    self.q.put([forecast_list, key])
            self.q.join()
            self.status = 2
            self.parse_data(forecast_list)
            self.cities += self.citycount
            self.status = 3
            data = self.generate_data(forecast_list, self.bins)
            self.status = 4
            self.make_bins(forecast_list, data)
            self.lists += 1

        for t in self.threads:
            t.join()

        time.sleep(self.REFRESH_RATE)
        self.close_threads()
        self.dump_db()

        if self.config["production"]:
            self.purge_cache()

            if self.config["send_stats"]:
                # log stuff to Datadog
                statsd.increment("forecast.api_requests", self.apirequests)
                statsd.increment("forecast.retry_count", self.retrycount)
                statsd.increment("forecast.elapsed_time", self.elapsed_time)
                statsd.increment("forecast.bandwidth_usage", self.bandwidth)
                statsd.increment("forecast.cities", self.cities)
                statsd.increment("forecast.errors", self.errors)
            if self.config["send_webhooks"]:
                # this will use a webhook to log that the script has been ran.
                data = {
                    "username": "Forecast Bot",
                    "content": "Weather Data has been updated!",
                    "avatar_url": "https://rc24.xyz/images/logo-small.png",
                    "attachments": [
                        {
                            "fallback": "Weather Data Update",
                            "color": "#0381D7",
                            "author_name": "RiiConnect24 Forecast Script",
                            "author_icon": "https://rc24.xyz/images/webhooks/forecast/profile.png",
                            "text": "Weather Data has been updated!",
                            "title": "Update!",
                            "fields": [
                                {
                                    "title": "Script",
                                    "value": "Forecast Channel",
                                    "short": "false",
                                }
                            ],
                            "thumb_url": "https://rc24.xyz/images/webhooks/forecast/accuweather.png",
                            "footer": "RiiConnect24 Script",
                            "footer_icon": "https://rc24.xyz/images/logo-small.png",
                            "ts": int(calendar.timegm(datetime.utcnow().timetuple())),
                        }
                    ],
                }
                for url in self.config["webhook_urls"]:
                    self.post_webhook = requests.post(
                        url, json=data, allow_redirects=True
                    )

        print("Completed Successfully")

    def to_celsius(self, temp):
        return int(round((float(temp) - 32) * 5 / 9))

    def to_fahrenheit(self, temp, sub=True):
        return int(round(float(temp) * 9 / 5)) + (32 if sub is True else 0)

    def kmh_mph(self, wind):
        return int(round(float(wind) * 0.621371))

    def mph_kmh(self, wind):
        return int(round(float(wind) * 1.60934))

    def time_convert(self, time):
        return int((time - 946684800) / 60)

    def get_epoch(
        self,
    ):
        return int(time.time())

    def get_city(self, forecast_list, key):
        return forecast_list[key][0][1]

    def get_region(self, forecast_list, key):
        return forecast_list[key][1][1]

    def get_country(self, forecast_list, key):
        return forecast_list[key][2][1]

    def get_all(self, forecast_list, key):
        return ", ".join(
            list(
                filter(
                    None,
                    [
                        self.get_city(forecast_list, key),
                        self.get_region(forecast_list, key),
                        self.get_country(forecast_list, key),
                    ],
                )
            )
        )

    def pad(self, amnt):
        return ("\0" * amnt).encode()

    def get_lat(self, forecast_list, key):
        return forecast_list[key][3][:4]

    def get_lng(self, forecast_list, key):
        return forecast_list[key][3][:8][4:]

    def isJapan(self, forecast_list, key):
        return forecast_list[key][2][1] == "Japan"

    def matches_country_code(self, forecast_list, key):
        v = forecast_list[key]
        if v[2][1] in forecastlists.bincountries:
            return hex(int(str(forecastlists.bincountries[v[2][1]])))[2:].zfill(
                2
            ) == hex(self.country_code)[2:].zfill(2)
        return False

    def check_coords(self, forecast_list, key, lat, lng):
        """Verify Location Coordinates"""
        if (
            abs(lat - self.coord_decode(binascii.hexlify(self.globe[key]["lat"]))) >= 2
            or abs(lng - self.coord_decode(binascii.hexlify(self.globe[key]["lng"])))
            >= 2
        ):
            if self.config["check_coordinates"]:
                log("Coordinate Inaccuracy Detected: %s" % key, "WARNING")
            self.errors += 1
            self.blank_data(forecast_list, key)
            return

        return True

    def get_bins(self, country_code):
        if country_code == 1:
            bins = [0]
        elif 8 <= country_code <= 52:
            bins = [1, 3, 4]
        elif 64 <= country_code <= 110:
            bins = [1, 2, 3, 4, 5, 6]
        else:
            log(
                "Unknown country code %s - generating English only" % country_code,
                "WARNING",
            )
            bins = [1]
        return bins

    def get_region_flag(self, country_code):
        if country_code == 1:
            return 0
        elif country_code in [8, 9, 12, 14, 17, 19, 37, 43, 48, 49, 51]:
            return 1  # Fahrenheit
        else:
            return 2  # Celsius

    def coord_decode(self, value):
        value = int(value, 16)
        if value >= 0x8000:
            value -= 0x10000
        return value * self.GLOBE_CONSTANT

    def validHour(self, hour):
        return True if -1 < hour < 24 else False

    def mode_calc(self, forecast_list):
        if not forecast_list:
            return
        temp = {}
        for i in forecast_list:
            if i not in temp:
                temp[i] = 1
            else:
                temp[i] += 1

        largestValue = 0
        largestKey = None
        duplicate = False
        for k, v in temp.items():
            if v > largestValue:
                largestValue = v
                largestKey = k
                duplicate = False
            elif v == largestValue:
                duplicate = True

        if not duplicate:
            return largestKey

    def populate_international(self, forecast_list):
        for k, v in forecastlists.weathercities_international.items():
            if k not in forecast_list:
                forecast_list[k] = v
            elif v[2][1] is not forecast_list[k][2][1]:
                forecast_list[k + " 2"] = v

    def size(self, data):
        total = 2
        for k, v in data.items():
            total += len(k + v) + 4
        return total

    def get_bandwidth_usage(self, r):
        req = (
            len(r.request.method + r.request.path_url)
            + self.size(r.request.headers)
            + 12
        )
        resp = (
            len(r.reason) + self.size(r.headers) + int(r.headers["Content-Length"]) + 15
        )
        return req + resp

    def worker(self):
        while self.threads_run:
            try:
                item = self.q.get_nowait()
                self.get_data(item[0], item[1])
                self.q.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                raise e
                log("A thread exception has occurred: %s" % e, "CRITICAL")
                self.blank_data(
                    item[0], item[1]
                )  # Since item data is in an unknown state, reset it
                self.q.task_done()
                continue

    def spawn_threads(self):
        for i in range(self.concurrent):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            self.threads.append(t)
            t.start()

    def close_threads(self):
        self.threads_run = False
        for t in self.threads:
            t.join()

        self.ui_run = False
        self.ui_thread.join()

    def refresh(self, type):
        # Uses ANSI escape codes
        if type == 0:
            print("\033[2J")  # Erase display command
        elif type == 1:
            os.system("cls")  # Clear screen
        else:
            print("\033[F\033[K" * 20)  # Clear each line individually

    def ui(self):
        prog = """-\|/"""  # These are characters which will make a spinning effect
        progcount = 0
        bar = 35  # Size of progress bars
        i = 0  # Counter for building progress bar
        if os.name == "nt":  # Windows
            display = "*"
            os.system("title Forecast Downloader - v%s" % self.VERSION)
            ver = sys.getwindowsversion()
            if ver[0] == 6 and ver[1] == 2:
                refresh_type = 0
            else:
                refresh_type = 1
            # os.system('cls')
        else:
            display = "✓"
            refresh_type = 2
            # os.system("clear")
        while not self.ui_run:
            pass  # Wait for main loop to start
        header = "=" * 64 + "\n\n"
        header += "--- RC24 Forecast Downloader [v%s] --- www.rc24.xyz\n" % self.VERSION
        header += "By John Pansera / Larsen Vallecillo --- (C) 2015-2021\n\n"
        if self.config["production"]:
            header += " " * 13 + "*** Production Mode Enabled ***\n"
        else:
            header += " " * 13 + "*** Production Mode Disabled ***\n"
        while self.ui_run:
            # Calculate values to show on screen
            dl = len(self.forecast_list) - self.cached > 0
            elapsed_time = int(round(time.time() - self.total_time))
            bandwidth = float("%.2f" % round(float(self.bw_usage) / 1048576, 2))
            totalpercent = int(
                round(float(self.lists) / float(len(forecastlists.weathercities)) * 100)
            )
            totalfill = int(totalpercent * 35 / 100)
            totalprog = "[" + "#" * totalfill + " " * (35 - totalfill) + "]"
            if self.status == 1:
                percent = (
                    int(
                        round(
                            float(self.citycount)
                            / float(len(self.forecast_list) - self.cached)
                            * 100
                        )
                    )
                    if dl
                    else 0
                )
                fill = int(round(percent * bar / 100))
                progbar = str(percent) + "% [" + "=" * fill + " " * (bar - fill) + "]"
            else:
                i = (i + 1) % (bar - 1)
                progbar = "[" + " " * i + "=" * 5 + (bar - i - 2) * " " + "]"
            # Build output
            out = header
            out += "API Requests: [%s] API Retries: [%s] Time: [%s]\n" % (
                self.apirequests,
                self.retrycount,
                elapsed_time,
            )
            out += "Bandwidth Usage: [%s MiB] Cities: [%s] Errors: [%s]\n" % (
                bandwidth,
                self.cities,
                self.errors,
            )
            out += "\nProcessing List #%s/%s (%s): %s %s\n\n" % (
                self.listid,
                len(forecastlists.weathercities),
                self.country_code,
                self.currentlist,
                "." * progcount,
            )
            if self.status == 1 and dl:
                out += "Downloading Forecasts [%s] %s%%\n" % (prog[progcount], percent)
            else:
                out += "Downloading Forecasts [%s] 100%%\n" % display
            if self.status == 2:
                out += "Parsing Data [%s]\n" % prog[progcount]
            elif self.status == 1:
                out += "Parsing Data [-]\n"
            else:
                out += "Parsing Data [%s]" % display + "\n"
            if self.status == 3:
                out += "Generating Data [%s]\n" % prog[progcount]
            elif self.status == 4:
                out += "Generating Data [%s]" % display + "\n"
            else:
                out += "Generating Data [-]\n"
            if self.status == 4:
                out += "Building Files [%s]\n\n" % prog[progcount]
            else:
                out += "Building Files [-]\n\n"
            out += "List Progress:  %s" % progbar
            out += "\nTotal Progress: %s%% " % totalpercent + totalprog
            out += "\n\n" + "=" * 64
            progcount = (progcount + 1) % 4

            self.refresh(refresh_type)
            sys.stdout.write(out)
            sys.stdout.flush()
            time.sleep(self.REFRESH_RATE)
        print("\n")

    def get_icon(self, icon, forecast_list, key):
        if icon == -1:
            return "FFFF"
        if self.isJapan(forecast_list, key):
            return forecastlists.weatherconditions[icon][3]
        else:
            return forecastlists.weatherconditions[icon][1]

    """Resets bin-specific values for next generation."""

    def reset_data(self):
        self.seek_offset = 0
        self.seek_base = 0
        self.cached = 0
        self.citycount = 0

    """This requests data from AccuWeather's API. It also retries the request if it fails."""

    def request_data(self, url):
        self.apirequests += 1
        i = 0
        c = False
        while not c:
            if i == 3:
                self.errors += 1
                return -1
            if i > 0:
                self.retrycount += 1
            try:
                data = self.s.get(url)
                self.bw_usage += self.get_bandwidth_usage(data)
                status_code = data.status_code
                if status_code == 200:
                    c = True
                i += 1
            except:
                i += 1
        return data.json()

    def timestamps(self, mode, key=None):
        time = self.time_convert(self.get_epoch())
        if key:
            citytime = self.time_convert(self.globe[key]["time"])
        if mode == 0:
            timestamp = time
        elif mode == 1:
            timestamp = citytime
        elif mode == 2:
            timestamp = time + 63
        return timestamp

    def get_locationkey(self, forecast_list, key):
        country = self.get_country(forecast_list, key)
        region = self.get_region(forecast_list, key)
        city = self.get_city(forecast_list, key)
        listid = forecastlists.weathercities.index(forecast_list)
        if region == "" and (
            country not in forecastlists.bincountries
            or self.matches_country_code(forecast_list, key)
        ):
            a = hex(self.weatherloc[listid]["null"][city])[2:].zfill(4)
            b = "FE"
            c = "FE"
        elif region == "" and not self.matches_country_code(forecast_list, key):
            a = hex(self.weatherloc[listid]["no-region"][country][city])[2:].zfill(4)
            if self.weatherloc[listid]["count"][country][region] > 1:
                b = "FE"
            else:
                b = "01"
            c = hex(forecastlists.bincountries[country])[2:].zfill(2)
        else:
            a = hex(self.weatherloc[listid][country][region][city])[2:].zfill(4)
            b = hex(self.weatherloc[listid]["regions"][country][region])[2:].zfill(2)
            c = hex(forecastlists.bincountries[country])[2:].zfill(2)
        return "".join([c, b, a])

    def zoom(self, forecast_list, key, mode):
        if mode == 1:
            return forecast_list[key][3][8:][:2]
        if mode == 2:
            return forecast_list[key][3][10:][:2]

    def generate_locationkeys(self, forecast_list):
        listid = forecastlists.weathercities.index(forecast_list)
        self.weatherloc[listid] = {}
        self.weatherloc[listid]["null"] = {}
        self.weatherloc[listid]["no-region"] = {}
        self.weatherloc[listid]["regions"] = {}
        self.weatherloc[listid]["count"] = {}
        for k, v in forecast_list.items():
            if v[1][1] == "" and (
                v[2][1] not in forecastlists.bincountries
                or self.matches_country_code(forecast_list, k)
            ):
                self.weatherloc[listid]["null"].setdefault(
                    v[0][1], len(self.weatherloc[listid]["null"]) + 1
                )
            elif v[1][1] == "" and not self.matches_country_code(forecast_list, k):
                self.weatherloc[listid]["no-region"].setdefault(v[2][1], {})
                self.weatherloc[listid]["no-region"][v[2][1]].setdefault(
                    v[0][1], len(self.weatherloc[listid]["no-region"][v[2][1]]) + 1
                )
            else:
                self.weatherloc[listid].setdefault(v[2][1], {})
                self.weatherloc[listid][v[2][1]].setdefault(v[1][1], {})
                self.weatherloc[listid][v[2][1]][v[1][1]].setdefault(
                    v[0][1], len(self.weatherloc[listid][v[2][1]][v[1][1]]) + 1
                )
                self.weatherloc[listid]["regions"].setdefault(v[2][1], {})
                self.weatherloc[listid]["regions"][v[2][1]].setdefault("", 1)
                self.weatherloc[listid]["regions"][v[2][1]].setdefault(
                    v[1][1], len(self.weatherloc[listid]["regions"][v[2][1]]) + 1
                )
            self.weatherloc[listid]["count"].setdefault(v[2][1], {})
            self.weatherloc[listid]["count"][v[2][1]].setdefault(v[1][1], 0)
            self.weatherloc[listid]["count"][v[2][1]][v[1][1]] += 1

    """If the script was unable to get forecast for a city, it's filled with this blank data."""

    def blank_data(self, forecast_list, key):
        self.wind[key] = {}
        self.uvindex[key] = {}
        self.precipitation[key] = {}
        self.week[key] = {}
        self.hourly[key] = {}
        self.today[key] = {}
        self.tomorrow[key] = {}
        self.current[key] = {}
        self.globe[key] = {}
        self.wind[key][0] = 0
        self.wind[key][1] = 0
        self.wind[key][2] = "N"
        self.wind[key][3] = 0
        self.wind[key][4] = 0
        self.wind[key][5] = "N"
        self.current[key][0] = "N"
        self.current[key][1] = 0
        self.current[key][2] = 0
        self.current[key][3] = -128
        self.current[key][4] = -128
        self.uvindex[key] = 255
        if self.isJapan(forecast_list, key):
            self.pollen[key] = 231  # Missing/No Data
            self.laundry[key] = 231  # Missing/No Data
        else:
            self.pollen[key] = 255
            self.laundry[key] = 255
        self.current[key][5] = "FFFF"
        self.times[key] = self.get_epoch()
        for k in range(0, 15):
            self.precipitation[key][k] = 255
        for k in range(0, 28):
            self.week[key][k] = -128  # Week Temperature Values
        for k in range(30, 37):
            self.week[key][k] = "FFFF"  # Week Forecast Icons
        for k in range(0, 8):
            self.hourly[key][k] = "FFFF"  # Hourly Weather Icons
        for k in range(1, 9):
            self.today[key][k] = -128  # Today Temperature Values
        for k in range(1, 9):
            self.tomorrow[key][k] = -128  # Tomorrow Temperature Values
        self.today[key][0] = "FFFF"
        self.tomorrow[key][0] = "FFFF"
        self.globe[key]["lat"] = binascii.unhexlify(self.get_lat(forecast_list, key))
        self.globe[key]["lng"] = binascii.unhexlify(self.get_lng(forecast_list, key))
        self.globe[key]["time"] = self.get_epoch()

    def get_accuweather_api(self, forecast_list, key):
        accuapi = self.weather_data[key]
        data_current = accuapi["current"][0]
        data_quarters = accuapi["quarters"]
        data_10day = accuapi["10day"]
        localdatetime = data_current["LocalObservationDateTime"]
        day = 0
        if data_10day["DailyForecasts"][0]["Date"][:10] != localdatetime[:10]:
            day = 1
        self.current[key][3] = int(data_current["Temperature"]["Imperial"]["Value"])
        self.current[key][4] = int(data_current["Temperature"]["Metric"]["Value"])
        self.current[key][5] = self.get_icon(
            int(data_current["WeatherIcon"]), forecast_list, key
        )
        self.current[key][0] = data_current["Wind"]["Direction"]["English"]
        self.current[key][2] = int(data_current["Wind"]["Speed"]["Imperial"]["Value"])
        self.current[key][1] = int(data_current["Wind"]["Speed"]["Metric"]["Value"])
        self.today[key][1] = int(
            data_10day["DailyForecasts"][day]["Temperature"]["Minimum"]["Value"]
        )
        self.today[key][2] = int(
            data_10day["DailyForecasts"][day]["Temperature"]["Maximum"]["Value"]
        )
        self.today[key][3] = self.to_celsius(self.today[key][1])
        self.today[key][4] = self.to_celsius(self.today[key][2])
        self.today[key][0] = self.get_icon(
            int(data_10day["DailyForecasts"][day]["Day"]["Icon"]), forecast_list, key
        )
        self.tomorrow[key][1] = int(
            data_10day["DailyForecasts"][day + 1]["Temperature"]["Minimum"]["Value"]
        )
        self.tomorrow[key][2] = int(
            data_10day["DailyForecasts"][day + 1]["Temperature"]["Maximum"]["Value"]
        )
        self.tomorrow[key][3] = self.to_celsius(self.tomorrow[key][1])
        self.tomorrow[key][4] = self.to_celsius(self.tomorrow[key][2])
        self.tomorrow[key][0] = self.get_icon(
            int(data_10day["DailyForecasts"][day + 1]["Day"]["Icon"]),
            forecast_list,
            key,
        )
        self.uvindex[key] = int(
            data_10day["DailyForecasts"][day]["AirAndPollen"][5]["Value"]
        )
        if self.uvindex[key] > 12:
            self.uvindex[key] = 12
        self.wind[key][0] = self.mph_kmh(
            int(data_10day["DailyForecasts"][day]["Day"]["Wind"]["Speed"]["Value"])
        )
        self.wind[key][1] = int(
            data_10day["DailyForecasts"][day]["Day"]["Wind"]["Speed"]["Value"]
        )
        self.wind[key][2] = data_10day["DailyForecasts"][day]["Day"]["Wind"][
            "Direction"
        ]["English"]
        self.wind[key][3] = self.mph_kmh(
            int(data_10day["DailyForecasts"][day + 1]["Day"]["Wind"]["Speed"]["Value"])
        )
        self.wind[key][4] = int(
            data_10day["DailyForecasts"][day + 1]["Day"]["Wind"]["Speed"]["Value"]
        )
        self.wind[key][5] = data_10day["DailyForecasts"][day + 1]["Day"]["Wind"][
            "Direction"
        ]["English"]
        try:
            grass = forecastlists.pollen_api[
                data_10day["DailyForecasts"][day]["AirAndPollen"][1]["Value"]
            ]
            tree = forecastlists.pollen_api[
                data_10day["DailyForecasts"][day]["AirAndPollen"][4]["Value"]
            ]
            ragweed = forecastlists.pollen_api[
                data_10day["DailyForecasts"][day]["AirAndPollen"][3]["Value"]
            ]
        except:
            grass = 2
            tree = 2
            ragweed = 2
        avg = int(round((grass + tree + ragweed) / 3))
        self.pollen[key] = avg

        quarter_offset = 0
        right_day = False

        while not right_day:
            try:
                hourly_start = math.floor(
                    int(data_quarters[quarter_offset]["EffectiveDate"][11:13]) / 6
                )
                if (
                    data_quarters[quarter_offset]["EffectiveDate"][:10]
                    == localdatetime[:10]
                ):
                    right_day = True
                else:
                    quarter_offset += 1
            except:
                self.blank_data(forecast_list, key)
                return

        j = 0
        for i in range(hourly_start, 8):
            self.precipitation[key][i] = int(
                data_quarters[quarter_offset + j]["PrecipitationProbability"]
            )
            j += 1
        for i in range(8, 15):
            self.precipitation[key][i] = int(
                data_10day["DailyForecasts"][i - 8 + day]["Day"][
                    "PrecipitationProbability"
                ]
            )
        # lat = float(accuapi[1].find(aw+"lat").text)
        # lng = float(accuapi[1].find(aw+"lon").text)
        self.globe[key]["offset"] = float(localdatetime[20:22]) + float(
            int(localdatetime[23:25]) / 60
        )
        if data_current["LocalObservationDateTime"][19] == "-":
            self.globe[key]["offset"] *= -1
        self.globe[key]["time"] = int(
            self.get_epoch() + self.globe[key]["offset"] * 3600
        )

        j = 1
        for i in range(0, 14, 2):
            self.week[key][i] = int(
                data_10day["DailyForecasts"][j + day]["Temperature"]["Maximum"]["Value"]
            )
            j += 1
        j = 1
        for i in range(1, 14, 2):
            self.week[key][i] = int(
                data_10day["DailyForecasts"][j + day]["Temperature"]["Minimum"]["Value"]
            )
            j += 1
        for i in range(0, 14):
            self.week[key][i + 14] = self.to_celsius(self.week[key][i])
        for i in range(0, 8):
            try:
                self.week[key][i + 30] = self.get_icon(
                    int(data_10day["DailyForecasts"][i + 1 + day]["Day"]["Icon"]),
                    forecast_list,
                    key,
                )
            except:
                self.blank_data(forecast_list, key)
                return

        j = 0
        for i in range(hourly_start, 8):
            self.hourly[key][i] = self.get_icon(
                int(data_quarters[quarter_offset + j]["Icon"]), forecast_list, key
            )
            j += 1

        """if check_coords(forecast_list,key,lat,lng):
            globe[key]['lat'] = s16(int(lat / self.GLOBE_CONSTANT))
            globe[key]['lng'] = s16(int(lng / self.GLOBE_CONSTANT))"""

    def parse_data(self, forecast_list):
        for k, v in self.weather_data.items():
            if self.weather_data[k]:
                self.get_accuweather_api(forecast_list, k)
            else:
                log(
                    "Unable to retrieve forecast data for %s - using blank data" % k,
                    "INFO",
                )

    def hex_write(self, file, loc, data):
        file.seek(loc)
        file.write(u32(data))

    def offset_write(self, file, value, post=True):
        self.seek_offset += 4
        file.seek(self.seek_offset)
        file.write(u32(value))
        if post:
            self.seek_offset += 4

    def make_bins(self, forecast_list, data):
        for j in self.bins:
            language_code = j
            self.make_forecast_bin(language_code, forecast_list, data)
            self.make_short_bin(language_code, forecast_list, data)
            if self.config["production"] and self.config["packVFF"]:
                self.packVFF(j, self.country_code)
            self.reset_data()

    def generate_data(self, forecast_list, bins):
        long_forecast_tables = dict.fromkeys([1, 2])
        short_japan_tables = dict.fromkeys([1, 2])
        short_forecast_tables = dict.fromkeys([1, 2])
        uvindex_text_tables = dict.fromkeys(bins)
        weathervalue_text_tables = dict.fromkeys(bins)
        text_tables = dict.fromkeys(bins)
        uvindex_table = self.make_uvindex_table()
        pollenindex_table = self.make_pollenindex_table()
        pollen_text_table = self.make_pollen_text_table()
        laundryindex_table = self.make_laundryindex_table()
        laundry_text_table = self.make_laundry_text_table()
        location_table = self.make_location_table(forecast_list)
        weathervalue_offset_table = self.make_weather_offset_table()
        for i in [1, 2]:
            self.mode = i
            long_forecast_tables[i] = self.make_long_forecast_table(forecast_list)
            short_japan_tables[i] = self.make_forecast_short_table(forecast_list)
            short_forecast_tables[i] = self.make_short_forecast_table(forecast_list)
        for language in bins:
            self.language_code = language
            uvindex_text_tables[language] = self.make_uvindex_text_table()
            text_tables[language] = self.make_forecast_text_table(forecast_list)
            weathervalue_text_tables[language] = self.make_weather_value_table()
        return [
            long_forecast_tables,
            uvindex_table,
            uvindex_text_tables,
            short_japan_tables,
            pollenindex_table,
            pollen_text_table,
            laundryindex_table,
            laundry_text_table,
            location_table,
            text_tables,
            weathervalue_offset_table,
            weathervalue_text_tables,
            short_forecast_tables,
        ]

    def make_forecast_bin(self, language_code, forecast_list, data):
        constant = 0
        count = {}
        header = self.make_header_forecast(forecast_list)
        long_forecast_table = data[0][self.mode]
        uvindex_table = data[1]
        uvindex_text_table = data[2][language_code]
        short_japan_tables = data[3][self.mode]
        pollenindex_table = data[4]
        pollen_text_table = data[5]
        laundryindex_table = data[6]
        laundry_text_table = data[7]
        location_table = data[8]
        text_table = data[9][language_code]
        weathervalue_offset_table = data[10]
        weathervalue_text_table = data[11][language_code]
        dictionaries = [
            header,
            long_forecast_table,
            short_japan_tables,
            weathervalue_offset_table,
            uvindex_table,
            laundryindex_table,
            pollenindex_table,
            location_table,
            weathervalue_text_table,
            uvindex_text_table,
            laundry_text_table,
            pollen_text_table,
            text_table,
        ]
        self.extension = "bin"
        file = io.BytesIO()
        file1 = "forecast.{}.{}_{}".format(
            self.extension, str(self.country_code).zfill(3), str(language_code)
        )
        file2 = "forecast.{}".format(self.extension)
        file.write(self.pad(12))
        file.write(u32(self.timestamps(0)))
        file.write(u32(self.timestamps(2)))
        for i in dictionaries:
            for v in i.values():
                file.write(v)
            count[constant] = file.tell()
            constant += 1
        file.write(self.pad(16))
        file.write(
            "RIICONNECT24".encode("ASCII")
        )  # This can be used to identify that we made this file.
        file.seek(0)
        self.hex_write(file, 36, count[0])
        if self.shortcount > 0:
            self.hex_write(file, 44, count[1])
        self.hex_write(file, 52, count[2])
        self.hex_write(file, 60, count[3])
        self.hex_write(file, 68, count[4])
        self.hex_write(file, 76, count[5])
        self.hex_write(file, 84, count[6])
        self.seek_offset = count[2]
        self.seek_base = count[7]
        for i in [
            list(forecastlists.weatherconditions.values())[j // 2]
            for j in range(len(forecastlists.weatherconditions.values()) * 2)
        ]:
            self.offset_write(file, self.seek_base)
            self.seek_base += len(i[0][language_code].encode("utf-16be")) + 2
        """UV Index"""
        self.seek_offset = count[3]
        self.seek_base = count[8]
        for i in forecastlists.uvindex.values():
            self.offset_write(file, self.seek_base)
            self.seek_base += len(i[language_code].encode("utf-16be")) + 2
        """Laundry Table"""
        self.seek_offset = count[4]
        self.seek_base = count[9]
        for i in forecastlists.laundry.values():
            self.offset_write(file, self.seek_base)
            self.seek_base += len(i.encode("utf-16be")) + 2
        """Pollen Table"""
        self.seek_offset = count[5]
        self.seek_base = count[10]
        for i in forecastlists.pollen.values():
            self.offset_write(file, self.seek_base)
            self.seek_base += len(i.encode("utf-16be")) + 2
        """Location Text"""
        self.seek_offset = count[6]
        self.seek_base = count[11]
        for key in forecast_list.keys():
            self.offset_write(file, self.seek_base, False)
            self.seek_base += (
                len(forecast_list[key][0][language_code].encode("utf-16be")) + 2
            )
            if len(forecast_list[key][1][language_code]) > 0:
                self.offset_write(file, self.seek_base, False)
                self.seek_base += (
                    len(forecast_list[key][1][language_code].encode("utf-16be")) + 2
                )
            else:
                self.offset_write(file, 0, False)
            if len(forecast_list[key][2][language_code]) > 0:
                self.offset_write(file, self.seek_base, False)
                self.seek_base += (
                    len(forecast_list[key][2][language_code].encode("utf-16be")) + 2
                )
            else:
                self.offset_write(file, 0, False)
            self.seek_offset += 12
        file.seek(0)
        f = file.read()[12:]
        file.close()
        if self.config["production"]:
            self.sign_file(f, language_code, file1, file2, False)
            if self.config["wii_u_generation"]:
                self.sign_file(f, language_code, file1, file2, True)

    def make_short_bin(self, language_code, forecast_list, data):
        short_forecast_header = self.make_header_short(forecast_list)
        short_forecast_table = data[12][self.mode]
        file1 = "short.{}.{}_{}".format(
            self.extension, str(self.country_code).zfill(3), str(language_code)
        )
        file2 = "short.{}".format(self.extension)
        file = io.BytesIO()
        file.write(u32(self.timestamps(0)))
        file.write(u32(self.timestamps(2)))
        for v in short_forecast_header.values():
            file.write(v)
        count = file.tell()
        for v in short_forecast_table.values():
            file.write(v)
        file.seek(count - 4)
        file.write(u32(count + 12))
        file.seek(0)
        f = file.read()
        file.close()
        if self.config["production"]:
            self.sign_file(f, language_code, file1, file2, False)
            if self.config["wii_u_generation"]:
                self.sign_file(f, language_code, file1, file2, True)

    def sign_file(self, file, language_code, local_name, server_name, wiiu):
        if wiiu:
            local_name = local_name.replace("bin", "alt")
            server_name = server_name.replace("bin", "alt")
            file = u32(0) + u32(4294967295) + file[8:]
        log("Processing " + local_name + " ...", "VERBOSE")
        crc32 = format(binascii.crc32(file) & 0xFFFFFFFF, "08x")
        size = len(file) + 12
        dest = open(local_name, "wb")
        dest.write(u32(0))
        dest.write(u32(size))
        dest.write(binascii.unhexlify(crc32))
        dest.write(file)
        dest.close()
        log("Compressing ...", "VERBOSE")
        nlzss.encode_file(local_name, local_name)
        file = open(local_name, "rb")
        new = file.read()
        file.close()
        dest = open(local_name, "wb")
        log("RSA Signing ...", "VERBOSE")
        signature = rsa.sign(
            new, self.private_key, "SHA-1"
        )  # Makes a SHA1 with ASN1 padding. Beautiful.
        dest.write(
            self.pad(64)
        )  # Padding. This is where data for an encrypted WC24 file would go (such as the header and IV), but this is not encrypted so it's blank.
        dest.write(signature)
        dest.write(new)
        dest.close()
        # Create directory if it does not exist
        path = "{}/{}/{}".format(
            self.config["file_path"],
            language_code,
            str(self.country_code).zfill(3),
        )
        os.makedirs(path, exist_ok=True)
        try:
            shutil.copy2(local_name, path + "/" + server_name)
        except:
            pass
        os.remove(local_name)

    def packVFF(self, language_code, country_code):
        log("Packing VFF ...", "VERBOSE")
        path = "{}/{}/{}/".format(
            self.config["file_path"], language_code, str(country_code).zfill(3)
        )
        os.makedirs(path + "wc24dl", exist_ok=True)
        with open(path + "forecast.alt", "rb") as source:
            with open(path + "wc24dl/3.BIN", "wb") as dest:
                dest.write(source.read()[320:])
        with open(path + "short.alt", "rb") as source:
            with open(path + "wc24dl/4.BIN", "wb") as dest:
                dest.write(source.read()[320:])
        if os.path.exists(path + "wc24dl.vff"):
            os.remove(path + "wc24dl.vff")
        subprocess.call(
            ["vfftool", "create", path + "wc24dl.vff", path + "wc24dl", "204800"],
            stdout=subprocess.DEVNULL,
        )  # Pack VFF
        os.remove(path + "wc24dl/3.BIN")
        os.remove(path + "wc24dl/4.BIN")
        os.rmdir(path + "wc24dl")

    def purge_cache(self):
        if self.config["production"]:
            if self.config["cloudflare_cache_purge"]:
                print("Purging cache...")

                for forecast_list in forecastlists.weathercities:
                    purge_list = []

                    self.currentlist = list(forecast_list.values())[0][2][1]
                    country_code = forecastlists.bincountries[self.currentlist]

                    for language_code in self.get_bins(country_code):
                        url = "http://{}/{}/{}/".format(
                            self.config["cloudflare_hostname"],
                            language_code,
                            str(country_code).zfill(3),
                        )

                        purge_list.append(url + "forecast.bin")
                        purge_list.append(url + "forecast.bi2")
                        purge_list.append(url + "short.bin")
                        purge_list.append(url + "short.bi2")
                        purge_list.append(url + "wc24dl.vff")

                    cf = CloudFlare.CloudFlare(token=self.config["cloudflare_token"])

                    cf.zones.purge_cache.post(
                        self.config["cloudflare_zone_name"],
                        data={"files": purge_list},
                    )

    def get_data(self, forecast_list, key):
        self.citycount += 1
        self.cache[key] = self.get_all(forecast_list, key)
        self.blank_data(forecast_list, key)
        lat = self.coord_decode(self.get_lat(forecast_list, key))
        lon = self.coord_decode(self.get_lng(forecast_list, key))
        if self.config["download_locations"]:
            location_key = self.request_data(
                "https://api.accuweather.com/locations/v1/cities/geoposition/search.json?q={},{}&apikey={}".format(
                    lat, lon, self.api_key
                )
            )["Key"]
            self.location_keys["{},{}".format(lat, lon)] = location_key
        else:
            location_key = self.location_keys["{},{}".format(lat, lon)]
        self.weather_data[key] = {}
        self.weather_data[key]["current"] = self.request_data(
            "https://api.accuweather.com/currentconditions/v1/{}?apikey={}&details=true".format(
                location_key, self.api_key
            )
        )
        self.weather_data[key]["quarters"] = self.request_data(
            "https://api.accuweather.com/forecasts/v1/daily/5day/quarters/{}?apikey={}".format(
                location_key, self.api_key
            )
        )
        self.weather_data[key]["10day"] = self.request_data(
            "https://api.accuweather.com/forecasts/v1/daily/10day/{}?apikey={}&details=true".format(
                location_key, self.api_key
            )
        )

    def make_header_short(self, forecast_list):
        header = {}
        header["country_code"] = u8(self.country_code)  # Wii Country Code.
        header["language_code"] = u32(self.language_code)  # Wii Language Code.
        header["region_flag"] = u8(self.region_flag)  # Region Flag.
        header["unknown_2"] = u8(0)  # Unknown.
        header["padding_1"] = u8(0)  # Padding.
        header["short_forecast_number"] = u32(
            len(forecast_list)
        )  # Number of short forecast entries.
        header["start_offset"] = u32(0)

        return header

    def make_header_forecast(self, forecast_list):
        header = {}
        header["country_code"] = u8(self.country_code)  # Wii Country Code.
        header["language_code"] = u32(self.language_code)  # Wii Language Code.
        header["region_flag"] = u8(self.region_flag)  # Region Flag.
        header["unknown_2"] = u8(1)  # Unknown.
        header["padding_1"] = u8(0)  # Padding.
        header["message_offset"] = u32(0)  # Offset for a message.
        header["long_forecast_number"] = u32(
            len(forecast_list) - self.shortcount
        )  # Number of long forecast entries.
        header["long_forecast_offset"] = u32(
            0
        )  # Offset for the long forecast entry table.
        header["short_forecast_number"] = u32(
            self.shortcount
        )  # Number of short forecast entries.
        header["short_forecast_offset"] = u32(
            0
        )  # Offset for the short forecast entry table.
        header["weather_condition_codes_number"] = u32(
            len(forecastlists.weatherconditions) * 2
        )  # Number of weather condition code entries.
        header["weather_condition_codes_offset"] = u32(
            0
        )  # Offset for the weather condition code table.
        header["uv_index_number"] = u32(
            len(forecastlists.uvindex)
        )  # Number of UV Index entries.
        header["uv_index_offset"] = u32(0)  # Offset for the UV Index table.
        header["laundry_index_number"] = u32(
            len(forecastlists.laundry)
        )  # Number of Laundry Index entries.
        header["laundry_index_offset"] = u32(0)  # Offset for the Laundry Index table.
        header["pollen_count_number"] = u32(
            len(forecastlists.pollen)
        )  # Number of Pollen Count entries.
        header["pollen_count_offset"] = u32(0)  # Offset for the Pollen Count table.
        header["location_number"] = u32(
            len(forecast_list)
        )  # Number of location entries.
        header["location_offset"] = u32(0)  # Offset for the location table.

        return header

    def make_long_forecast_table(self, forecast_list):
        long_forecast_table = {}
        for key in forecast_list.keys():
            if (
                self.matches_country_code(forecast_list, key)
                and self.get_region(forecast_list, key) != ""
            ):
                keyIndex = list(forecast_list).index(key)
                long_forecast_table["location_code_%s" % keyIndex] = binascii.unhexlify(
                    self.get_locationkey(forecast_list, key)
                )  # Wii Location Code.
                long_forecast_table["timestamp_1_%s" % keyIndex] = u32(
                    self.timestamps(1, key)
                )  # 1st timestamp.
                long_forecast_table["timestamp_2_%s" % keyIndex] = u32(
                    self.timestamps(0, key)
                )  # 2nd timestamp.
                long_forecast_table["unknown_1_%s" % keyIndex] = u32(
                    0
                )  # Unknown. (0xC-0xF)
                long_forecast_table[
                    "today_forecast_%s" % keyIndex
                ] = binascii.unhexlify(
                    self.today[key][0]
                )  # Today's forecast.
                for p in range(0, 4):
                    long_forecast_table[
                        "today_hourly_forecast_%s_%s" % (p, keyIndex)
                    ] = binascii.unhexlify(
                        self.hourly[key][p]
                    )  # Tomorrow's hourly forecast.
                long_forecast_table["today_tempc_high_%s" % keyIndex] = s8(
                    self.today[key][4]
                )  # Today's high temperature in Celsius
                long_forecast_table["today_tempc_high_difference_%s" % keyIndex] = s8(
                    self.today[key][8]
                )  # Today's high temperature difference in Celsius
                long_forecast_table["today_tempc_low_%s" % keyIndex] = s8(
                    self.today[key][3]
                )  # Today's low temperature in Celsius
                long_forecast_table["today_tempc_low_difference_%s" % keyIndex] = s8(
                    self.today[key][7]
                )  # Today's low temperature difference in Celsius
                long_forecast_table["today_tempf_high_%s" % keyIndex] = s8(
                    self.today[key][2]
                )  # Today's high temperature in Fahrenheit
                long_forecast_table["today_tempf_high_difference_%s" % keyIndex] = s8(
                    self.today[key][6]
                )  # Today's high Fahrenheit difference
                long_forecast_table["today_tempf_low_%s" % keyIndex] = s8(
                    self.today[key][1]
                )  # Today's low temperature in Fahrenheit
                long_forecast_table["today_tempf_low_difference_%s" % keyIndex] = s8(
                    self.today[key][5]
                )  # Today's low Fahrenheit difference
                for p in range(0, 4):
                    long_forecast_table[
                        "today_precipitation_%s_%s" % (p, keyIndex)
                    ] = u8(
                        self.precipitation[key][p]
                    )  # Today's precipitation
                long_forecast_table["today_winddirection_%s" % keyIndex] = u8(
                    int(self.get_wind_direction(self.wind[key][2]))
                )  # Today's wind direction
                long_forecast_table["today_windkm_%s" % keyIndex] = u8(
                    self.wind[key][0]
                )  # Today's wind speed in km/hr
                long_forecast_table["today_windmph_%s" % keyIndex] = u8(
                    self.wind[key][1]
                )  # Today's wind speed in mph
                long_forecast_table["uv_index_%s" % keyIndex] = u8(
                    self.uvindex[key]
                )  # UV Index
                long_forecast_table["laundry_index_%s" % keyIndex] = u8(
                    self.laundry[key]
                )  # Laundry Index
                long_forecast_table["pollen_index_%s" % keyIndex] = u8(
                    self.pollen[key]
                )  # Pollen Index
                long_forecast_table[
                    "tomorrow_forecast_%s" % keyIndex
                ] = binascii.unhexlify(
                    self.tomorrow[key][0]
                )  # Tomorrow's forecast.
                for p in range(4, 8):
                    long_forecast_table[
                        "tomorrow_hourly_forecast_%s_%s" % (p, keyIndex)
                    ] = binascii.unhexlify(
                        self.hourly[key][p]
                    )  # Tomorrow's hourly forecast.
                long_forecast_table["tomorrow_tempc_high_%s" % keyIndex] = s8(
                    self.tomorrow[key][4]
                )  # Tomorrow's temperature in Celsius
                long_forecast_table[
                    "tomorrow_tempc_high_difference_%s" % keyIndex
                ] = s8(
                    self.tomorrow[key][8]
                )  # Tomorrow's temperature mean in Celsius
                long_forecast_table["tomorrow_tempc_low_%s" % keyIndex] = s8(
                    self.tomorrow[key][3]
                )  # Tomorrow's Celsius globe value
                long_forecast_table["tomorrow_tempc_low_difference_%s" % keyIndex] = s8(
                    self.tomorrow[key][7]
                )  # Tomorrow's Celsius globe value
                long_forecast_table["tomorrow_tempf_high_%s" % keyIndex] = s8(
                    self.tomorrow[key][2]
                )  # Tomorrow's temperature in Fahrenheit
                long_forecast_table[
                    "tomorrow_tempf_high_difference_%s" % keyIndex
                ] = s8(
                    self.tomorrow[key][6]
                )  # Tomorrow's Celsius globe value
                long_forecast_table["tomorrow_tempf_low_%s" % keyIndex] = s8(
                    self.tomorrow[key][1]
                )  # Tomorrow's temperature mean in Fahrenheit
                long_forecast_table["tomorrow_tempf_low_difference_%s" % keyIndex] = s8(
                    self.tomorrow[key][5]
                )  # Tomorrow's Fahrenheit globe value
                for p in range(4, 8):
                    long_forecast_table[
                        "tomorrow_precipitation_%s_%s" % (p, keyIndex)
                    ] = u8(
                        self.precipitation[key][p]
                    )  # Tomorrow's's precipitation
                long_forecast_table["tomorrow_winddirection_%s" % keyIndex] = u8(
                    int(self.get_wind_direction(self.wind[key][5]))
                )  # Tomorrow's wind direction
                long_forecast_table["tomorrow_windkm_%s" % keyIndex] = u8(
                    self.wind[key][3]
                )  # Tomorrow's wind speed in km/hr
                long_forecast_table["tomorrow_windmph_%s" % keyIndex] = u8(
                    self.wind[key][4]
                )  # Tomorrow's wind speed in mph
                long_forecast_table["uvindex_2_%s" % keyIndex] = u8(
                    self.uvindex[key]
                )  # UV Index (Unknown)
                long_forecast_table["laundry_index_2_%s" % keyIndex] = u8(
                    self.laundry[key]
                )  # Laundry Index (Unknown)
                long_forecast_table["pollen_index_2_%s" % keyIndex] = u8(
                    self.pollen[key]
                )  # Pollen Index (Unknown)
                for p in range(0, 7):
                    long_forecast_table[
                        "5day_forecast_%s_%s" % (p, keyIndex)
                    ] = binascii.unhexlify(
                        self.week[key][30 + p]
                    )  # 5-Day forecast weather icon
                    long_forecast_table["5day_tempc_high_%s_%s" % (p, keyIndex)] = s8(
                        self.week[key][14 + (p * 2)]
                    )  # 5-Day forecast high temperature in Celsius
                    long_forecast_table["5day_tempc_low_%s_%s" % (p, keyIndex)] = s8(
                        self.week[key][15 + (p * 2)]
                    )  # 5-Day forecast low temperature in Celsius
                    long_forecast_table["5day_tempf_high_%s_%s" % (p, keyIndex)] = s8(
                        self.week[key][p * 2]
                    )  # 5-Day forecast high temperature in Fahrenheit
                    long_forecast_table["5day_tempf_low_%s_%s" % (p, keyIndex)] = s8(
                        self.week[key][1 + (p * 2)]
                    )  # 5-Day forecast low temperature in Fahrenheit
                    long_forecast_table[
                        "5day_precipitation_%s_%s" % (p, keyIndex)
                    ] = u8(
                        self.precipitation[key][8 + p]
                    )  # 5-Day precipitation percentage
                    long_forecast_table[
                        "5day_forecast_padding_%s_%s" % (p, keyIndex)
                    ] = u8(
                        0
                    )  # Padding

        return long_forecast_table

    def make_short_forecast_table(self, forecast_list):
        short_forecast_table = {}
        for key in forecast_list.keys():
            keyIndex = list(forecast_list).index(key)
            short_forecast_table["location_code_%s" % keyIndex] = binascii.unhexlify(
                self.get_locationkey(forecast_list, key)
            )  # Wii location code for city
            short_forecast_table["timestamp_1_%s" % keyIndex] = u32(
                self.timestamps(1, key)
            )  # Timestamp 1
            short_forecast_table["timestamp_2_%s" % keyIndex] = u32(
                self.timestamps(0, key)
            )  # Timestamp 2
            short_forecast_table["current_forecast_%s" % keyIndex] = binascii.unhexlify(
                self.current[key][5]
            )  # Current forecast
            short_forecast_table["unknown_%s" % keyIndex] = u8(0)  # 0xE unknown
            short_forecast_table["current_tempc_%s" % keyIndex] = s8(
                self.current[key][4]
            )  # Current temperature in Celsius
            short_forecast_table["current_tempf_%s" % keyIndex] = s8(
                self.current[key][3]
            )  # Current temperature in Fahrenheit
            short_forecast_table["current_winddirection_%s" % keyIndex] = u8(
                int(self.get_wind_direction(self.current[key][0]))
            )  # Current wind direction
            short_forecast_table["current_windkm_%s" % keyIndex] = u8(
                self.current[key][1]
            )  # Current wind in km/hr
            short_forecast_table["current_windmph_%s" % keyIndex] = u8(
                self.current[key][2]
            )  # Current wind in mph
            short_forecast_table["unknown_2_%s" % keyIndex] = u16(0)  # 00?
            short_forecast_table["unknown_3_%s" % keyIndex] = binascii.unhexlify(
                "FFFF"
            )  # FFFF?

        return short_forecast_table

    def make_forecast_short_table(self, forecast_list):
        short_forecast_table = {}
        for key in forecast_list.keys():
            if (
                not self.matches_country_code(forecast_list, key)
                or self.get_region(forecast_list, key) == ""
            ):
                keyIndex = list(forecast_list).index(key)
                short_forecast_table[
                    "location_code_%s" % keyIndex
                ] = binascii.unhexlify(
                    self.get_locationkey(forecast_list, key)
                )  # Wii Location Code.
                short_forecast_table["timestamp_1_%s" % keyIndex] = u32(
                    self.timestamps(1, key)
                )  # 1st timestamp.
                short_forecast_table["timestamp_2_%s" % keyIndex] = u32(
                    self.timestamps(0, key)
                )  # 2nd timestamp.
                short_forecast_table["padding_%s" % keyIndex] = u32(0)
                short_forecast_table[
                    "today_forecast_%s" % keyIndex
                ] = binascii.unhexlify(
                    self.today[key][0]
                )  # Today's forecast.
                for p in range(0, 4):
                    short_forecast_table[
                        "today_hourly_forecast_%s_%s" % (p, keyIndex)
                    ] = binascii.unhexlify(
                        self.hourly[key][p]
                    )  # Today's hourly forecast.
                short_forecast_table["today_tempc_high_%s" % keyIndex] = s8(
                    self.today[key][4]
                )  # Today's high temperature in Celsius
                short_forecast_table["today_tempc_high_difference_%s" % keyIndex] = s8(
                    self.today[key][8]
                )  # Today's high temperature difference in Celsius
                short_forecast_table["today_tempc_low_%s" % keyIndex] = s8(
                    self.today[key][3]
                )  # Today's low temperature in Celsius
                short_forecast_table["today_tempc_low_difference_%s" % keyIndex] = s8(
                    self.today[key][7]
                )  # Today's low temperature difference in Celsius
                short_forecast_table["today_tempf_high_%s" % keyIndex] = s8(
                    self.today[key][2]
                )  # Today's high temperature in Fahrenheit
                short_forecast_table["today_tempf_high_difference_%s" % keyIndex] = s8(
                    self.today[key][6]
                )  # Today's high Fahrenheit difference
                short_forecast_table["today_tempf_low_%s" % keyIndex] = s8(
                    self.today[key][1]
                )  # Today's low temperature in Fahrenheit
                short_forecast_table["today_tempf_low_difference_%s" % keyIndex] = s8(
                    self.today[key][5]
                )  # Today's low Fahrenheit difference
                for p in range(0, 4):
                    short_forecast_table[
                        "today_precipitation_%s_%s" % (p, keyIndex)
                    ] = u8(
                        self.precipitation[key][p]
                    )  # Today's precipitation
                short_forecast_table["today_winddirection_%s" % keyIndex] = u8(
                    int(self.get_wind_direction(self.wind[key][2]))
                )  # Today's wind direction
                short_forecast_table["today_windkm_%s" % keyIndex] = u8(
                    self.wind[key][0]
                )  # Today's wind speed in km/hr
                short_forecast_table["today_windmph_%s" % keyIndex] = u8(
                    self.wind[key][1]
                )  # Today's wind speed in mph
                for p in range(1, 4):
                    short_forecast_table["unknown_value_%s_%s" % (p, keyIndex)] = u8(
                        255
                    )  # ??
                short_forecast_table[
                    "tomorrow_forecast_%s" % keyIndex
                ] = binascii.unhexlify(
                    self.tomorrow[key][0]
                )  # Tomorrow's forecast.
                for p in range(4, 8):
                    short_forecast_table[
                        "tomorrow_hourly_forecast_%s_%s" % (p, keyIndex)
                    ] = binascii.unhexlify(
                        self.hourly[key][p]
                    )  # Tomorrow's hourly forecast.
                short_forecast_table["tomorrow_tempc_high_%s" % keyIndex] = s8(
                    self.tomorrow[key][4]
                )  # Tomorrow's temperature in Celsius
                short_forecast_table[
                    "tomorrow_tempc_high_difference_%s" % keyIndex
                ] = s8(
                    self.tomorrow[key][8]
                )  # Tomorrow's temperature mean in Celsius
                short_forecast_table["tomorrow_tempc_low_%s" % keyIndex] = s8(
                    self.tomorrow[key][3]
                )  # Tomorrow's Celsius globe value
                short_forecast_table[
                    "tomorrow_tempc_low_difference_%s" % keyIndex
                ] = s8(
                    self.tomorrow[key][7]
                )  # Tomorrow's Celsius globe value
                short_forecast_table["tomorrow_tempf_high_%s" % keyIndex] = s8(
                    self.tomorrow[key][2]
                )  # Tomorrow's temperature in Fahrenheit
                short_forecast_table[
                    "tomorrow_tempf_high_difference_%s" % keyIndex
                ] = s8(
                    self.tomorrow[key][6]
                )  # Tomorrow's Celsius globe value
                short_forecast_table["tomorrow_tempf_low_%s" % keyIndex] = s8(
                    self.tomorrow[key][1]
                )  # Tomorrow's temperature mean in Fahrenheit
                short_forecast_table[
                    "tomorrow_tempf_low_difference_%s" % keyIndex
                ] = s8(
                    self.tomorrow[key][5]
                )  # Tomorrow's Fahrenheit globe value
                for p in range(4, 8):
                    short_forecast_table[
                        "tomorrow_precipitation_%s_%s" % (p, keyIndex)
                    ] = u8(
                        self.precipitation[key][p]
                    )  # Today's precipitation
                short_forecast_table["tomorrow_winddirection_%s" % keyIndex] = u8(
                    int(self.get_wind_direction(self.wind[key][5]))
                )  # Tomorrow's wind direction
                short_forecast_table["tomorrow_windkm_%s" % keyIndex] = u8(
                    self.wind[key][3]
                )  # Tomorrow's wind speed in km/hr
                short_forecast_table["tomorrow_windmph_%s" % keyIndex] = u8(
                    self.wind[key][4]
                )  # Tomorrow's wind speed in mph
                short_forecast_table["uvindex_%s" % keyIndex] = u8(
                    self.uvindex[key]
                )  # Today's UV Index
                short_forecast_table["laundry_index_%s" % keyIndex] = u8(
                    self.laundry[key]
                )  # Today's Laundry Index
                short_forecast_table["pollen_index_%s" % keyIndex] = u8(
                    self.pollen[key]
                )  # Today's Pollen Index

        return short_forecast_table

    """Database of UV index values."""

    def make_uvindex_table(self):
        uvindex = {}
        for i in forecastlists.uvindex:
            uvindex["uv_%s_number" % i] = u8(i)
            uvindex["uv_%s_padding" % i] = self.pad(3)
            uvindex["uv_%s_offset" % i] = u32(0)

        return uvindex

    """Database of laundry index values."""

    def make_laundryindex_table(self):
        laundry = {}
        for i in forecastlists.laundry:
            laundry["laundry_%s_number" % i] = u8(i)
            laundry["laundry_%s_padding" % i] = self.pad(3)
            laundry["laundry_%s_offset" % i] = u32(0)

        return laundry

    """Database of pollen index values."""

    def make_pollenindex_table(self):
        pollen = {}
        for i in forecastlists.pollen:
            pollen["pollen_%s_number" % i] = u8(i)
            pollen["pollen_%s_padding" % i] = self.pad(3)
            pollen["pollen_%s_offset" % i] = u32(0)

        return pollen

    def make_location_table(self, forecast_list):
        location_table = {}
        for key in forecast_list.keys():
            keyIndex = list(forecast_list).index(key)
            location_table["location_code_%s" % keyIndex] = binascii.unhexlify(
                self.get_locationkey(forecast_list, key)
            )  # Wii Location Code.
            location_table["city_text_offset_%s" % keyIndex] = u32(
                0
            )  # Offset for location's city text
            location_table["region_text_offset_%s" % keyIndex] = u32(
                0
            )  # Offset for location's region text
            location_table["country_text_offset_%s" % keyIndex] = u32(
                0
            )  # Offset for location's country text
            location_table["latitude_coordinates_%s" % keyIndex] = binascii.unhexlify(
                self.get_lat(forecast_list, key)
            )  # Latitude coordinates for location on globe
            location_table["longitude_coordinates_%s" % keyIndex] = binascii.unhexlify(
                self.get_lng(forecast_list, key)
            )  # Longitude coordinates for location on globe
            for p in range(1, 3):
                location_table[
                    "location_zoom_%s_%s" % (p, keyIndex)
                ] = binascii.unhexlify(
                    self.zoom(forecast_list, key, p)
                )  # Location zoom for location on globe
            location_table["padding_%s" % keyIndex] = u16(0)

        return location_table

    def make_forecast_text_table(self, forecast_list):
        text_table = {}
        for key in forecast_list.keys():
            keyIndex = list(forecast_list).index(key)
            text_table[keyIndex] = "\0".join(
                list(
                    filter(
                        None,
                        [
                            forecast_list[key][0][self.language_code],
                            forecast_list[key][1][self.language_code],
                            forecast_list[key][2][self.language_code],
                        ],
                    )
                )
            )
            text_table[keyIndex] = text_table[keyIndex].encode("utf-16be") + self.pad(2)
        return text_table

    def make_weather_value_table(self):
        weathervalue_text_table = {}
        for k, v in forecastlists.weatherconditions.items():
            keyIndex = list(forecastlists.weatherconditions).index(k)
            for i in range(2):
                weathervalue_text_table["weather_text_%s_%s" % (keyIndex, i)] = v[0][
                    self.language_code
                ].encode("utf-16be") + self.pad(2)
        return weathervalue_text_table

    def make_weather_offset_table(self):
        weathervalue_offset_table = {}
        for k, v in forecastlists.weatherconditions.items():
            keyIndex = list(forecastlists.weatherconditions).index(k)
            for p in range(1, 3):
                weathervalue_offset_table[
                    "condition_code_%s_international_%s" % (p, keyIndex)
                ] = binascii.unhexlify(v[p])
            weathervalue_offset_table["padding_1_%s" % keyIndex] = u32(0)
            for p in range(3, 5):
                weathervalue_offset_table[
                    "condition_code_%s_japan_%s" % (p, keyIndex)
                ] = binascii.unhexlify(v[p])
            weathervalue_offset_table["padding_2_%s" % keyIndex] = u32(0)
        return weathervalue_offset_table

    def make_uvindex_text_table(self):
        uvindex_text_table = {}
        uvindexlist = []
        for v in forecastlists.uvindex.values():
            uvindexlist.append(v[self.language_code])
        uvindex_text_table[0] = "\0".join(uvindexlist).encode("utf-16be") + self.pad(2)
        return uvindex_text_table

    def make_laundry_text_table(self):
        laundry = {}
        for k, v in forecastlists.laundry.items():
            keyIndex = list(forecastlists.laundry).index(k)
            laundry[keyIndex] = v.encode("utf-16be") + self.pad(2)
        return laundry

    def make_pollen_text_table(self):
        pollen = {}
        for k, v in forecastlists.pollen.items():
            keyIndex = list(forecastlists.pollen).index(k)
            pollen[keyIndex] = v.encode("utf-16be") + self.pad(2)
        return pollen

    def get_wind_direction(self, degrees):
        return forecastlists.winddirection[degrees]

    def dump_db(self):
        # db = {"update_time": time.time(), "location_keys": weatherloc, "local_times": times, "laundry_indexes": laundry,
        #      "pollen_indexes": pollen, "globe_data": globe, "wind_speed": wind, "uvindexes": uvindex,
        #      "current_forecast": current, "precipitation": precipitation, "hourly_forecast": hourly,
        #      "tomorrow_forecast": tomorrow, "week_forecast": week, "today_forecast": today, "key_cache": cache}
        db = {"location_keys": self.location_keys}
        with open("weather.db", "wb") as f:
            pickle.dump(db, f)


Forecast()
