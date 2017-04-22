require 'nokogiri'
require 'open-uri'
# Or change to any other page
document = Nokogiri::HTML(open(ARGV[0]))
File.write("temp_mainichi", document)