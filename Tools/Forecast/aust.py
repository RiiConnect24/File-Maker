import collections
import json
import googlemaps

dict = collections.OrderedDict()

dict["Canberra"] = ["Australian Capital Territory", "Australia", "e6dd69fc09030000"]
dict["Sydney"] = ["New South Wales", "Australia", "e7e76b8c07030000"]
dict["Wollongong"] = ["New South Wales", "Australia", "e7856b4903030000"]
dict["Newcastle"] = ["New South Wales", "Australia", "e8966be703030000"]
dict["Albury"] = ["New South Wales", "Australia", "e65b687a03030000"]
dict["Coffs Harbour"] = ["New South Wales", "Australia", "ea746ce203030000"]
dict["Wagga Wagga"] = ["New South Wales", "Australia", "e70668c803030000"]
dict["Lismore"] = ["New South Wales", "Australia", "eb836d0103030000"]
dict["Tamworth"] = ["New South Wales", "Australia", "e9e36b5203030000"]
dict["Dubbo"] = ["New South Wales", "Australia", "e91169ac03030000"]
dict["Orange"] = ["New South Wales", "Australia", "e8556a0703030000"]
dict["Bega"] = ["New South Wales", "Australia", "e5eb6a8d03030000"]
dict["Griffith"] = ["New South Wales", "Australia", "e79f67d903030000"]
dict["Armidale"] = ["New South Wales", "Australia", "ea4d6bda03030000"]
dict["Broken Hill"] = ["New South Wales", "Australia", "e947649503030000"]
dict["Katoomba"] = ["New South Wales", "Australia", "e8076ae503030000"]
dict["Darwin"] = ["Northern Territory", "Australia", "f7295d0b08030000"]
dict["Alice Springs"] = ["Northern Territory", "Australia", "ef275f3203030000"]
dict["Katherine"] = ["Northern Territory", "Australia", "f5b65e0d03030000"]
dict["Tennant Creek"] = ["Northern Territory", "Australia", "f2075f6b03030000"]
dict["Uluru"] = ["Northern Territory", "Australia", "edfb5d2d07030000"]
dict["Brisbane"] = ["Queensland", "Australia", "ec7b6cd107030000"]
dict["Gold Coast"] = ["Queensland", "Australia", "ec136d1907030000"]
dict["Sunshine Coast"] = ["Queensland", "Australia", "ed126cc603030000"]
dict["Mackay"] = ["Queensland", "Australia", "f0f66a1603030000"]
dict["Cairns"] = ["Queensland", "Australia", "f3f867a607030000"]
dict["Toowoomba"] = ["Queensland", "Australia", "ec676c0f03030000"]
dict["Townsville"] = ["Queensland", "Australia", "f24b686303030000"]
dict["Rockhampton"] = ["Queensland", "Australia", "ef616b0703030000"]
dict["Bundaberg"] = ["Queensland", "Australia", "ee506c5603030000"]
dict["Maryborough"] = ["Queensland", "Australia", "edd76c9903030000"]
dict["Mount Isa"] = ["Queensland", "Australia", "f142633003030000"]
dict["Longreach"] = ["Queensland", "Australia", "ef55669303030000"]
dict["Charleville"] = ["Queensland", "Australia", "ed3967fc03030000"]
dict["Adelaide"] = ["South Australia", "Australia", "e72c629107030000"]
dict["Maitland"] = ["South Australia", "Australia", "e78f61e603030000"]
dict["Port Pirie"] = ["South Australia", "Australia", "e866622103030000"]
dict["Mount Gambier"] = ["South Australia", "Australia", "e519641b03030000"]
dict["Whyalla"] = ["South Australia", "Australia", "e88361d303030000"]
dict["Port Lincoln"] = ["South Australia", "Australia", "e74f609c03030000"]
dict["Renmark"] = ["South Australia", "Australia", "e7b2641303030000"]
dict["Ceduna"] = ["South Australia", "Australia", "e9275f0e03030000"]
dict["Coober Pedy"] = ["South Australia", "Australia", "eb5f5fd103030000"]
dict["Clare"] = ["South Australia", "Australia", "e7f0629003030000"]
dict["Keith"] = ["South Australia", "Australia", "e65463ce03030000"]
dict["Hobart"] = ["Tasmania", "Australia", "e18868bd02030000"]
dict["Launceston"] = ["Tasmania", "Australia", "e28868a103030000"]
dict["Devonport"] = ["Tasmania", "Australia", "e2b8681103030000"]
dict["Strahan"] = ["Tasmania", "Australia", "e206675603030000"]
dict["Melbourne"] = ["Victoria", "Australia", "e51d671607030000"]
dict["Geelong"] = ["Victoria", "Australia", "e4e166a203030000"]
dict["Ballarat"] = ["Victoria", "Australia", "e54b664a03030000"]
dict["Bendigo"] = ["Victoria", "Australia", "e5dd669903030000"]
dict["Latrobe Valley"] = ["Victoria", "Australia", "e4d4682803030000"]
dict["Mildura"] = ["Victoria", "Australia", "e7b0651703030000"]
dict["Warrnambool"] = ["Victoria", "Australia", "e4b5655103030000"]
dict["Wangaratta"] = ["Victoria", "Australia", "e625680903030000"]
dict["Horsham"] = ["Victoria", "Australia", "e5e5651d03030000"]
dict["Sale"] = ["Victoria", "Australia", "e4e6689403030000"]
dict["Perth"] = ["Western Australia", "Australia", "e94b526408030000"]
dict["Albany"] = ["Western Australia", "Australia", "e71953d303030000"]
dict["Bunbury"] = ["Western Australia", "Australia", "e849523c03030000"]
dict["Kalgoorlie"] = ["Western Australia", "Australia", "ea23566004030000"]
dict["Geraldton"] = ["Western Australia", "Australia", "eb8a517e03030000"]
dict["Augusta"] = ["Western Australia", "Australia", "e78f51df03030000"]
dict["Broome"] = ["Western Australia", "Australia", "f33a56ea03030000"]
dict["Port Hedland"] = ["Western Australia", "Australia", "f18e545707030000"]
dict["Karratha"] = ["Western Australia", "Australia", "f141531603030000"]
dict["Northam"] = ["Western Australia", "Australia", "e97d52f603030000"]
dict["Exmouth"] = ["Western Australia", "Australia", "f067512703030000"]
dict["Kununurra"] = ["Western Australia", "Australia", "f4ca5b8b03030000"]

gmaps = googlemaps.Client(key="AIzaSyD8ouvQPlFAdVrThJ_wvmA6QZh-Y4whGzY")

for k, v in dict.items():
    langs = ["ja", "en", "de", "fr", "es", "it", "nl"]

    list = ""

    for l in langs:
        if l != "en":
            geocode_result = gmaps.geocode(k + ", " + v[0] + ", " + v[1], language=l)
            name = geocode_result[0]["address_components"][0]["long_name"]
            list += name
            if l != "nl":
                list += ", "
        else:
            list += k
            list += ", "

    print list