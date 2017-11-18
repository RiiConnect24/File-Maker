"""Example config.py"""

webhook_urls = ["DISCORD WEBHOOK", "DISCORD WEBHOOK"] # Used to update webhooks on Discord
key_path = "/path/to/key/in/format/of/file.pem" # Private key to sign the file
file_path = "/path/to/folder" # Path to save the file to
lzss_path = "/path/to/lzss" # Path to lzss
production = None # Use production mode
cachet_url = "http://status.domain.tld/api/v1" # URL for Cachet
cachet_key = "api_key" # API Key for Cachet
sentry_url = "http://status.domain.tld/" # URL for Sentry

"""News Channel only"""

force_all = False # Force the script to replace all news files
google_maps_api_key = "api_key" # API Key for Google Maps geocoding API
geoparser_keys = ["GEOPARSER KEY", "GEOPARSER KEY"] # API Key for Geoparser

"""Forecast Channel only"""

import forecastlists

useVerbose = None # Print more verbose messages
useMultithreaded = None # Use multithreading
weathercities = ["CITY LIST", "CITY LIST"] # Lists of cities to use
cachet_elapsed_time = None # ID of the Cachet point to log elapsed time.

"""Everybody Votes Channel only"""

evc_mysql_user = "user" # MySQL username
evc_mysql_password = "password" # MySQL password
evc_mysql_database = "database" # MySQL database
