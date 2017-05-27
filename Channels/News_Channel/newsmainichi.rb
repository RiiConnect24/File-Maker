# Don't know how to get Mainichi working in Python, so we're using Ruby to parse it for now.
require 'nokogiri'
require 'open-uri'
# Or change to any other page
document = Nokogiri::HTML(open(ARGV[0]))
File.write("temp_mainichi", document)
