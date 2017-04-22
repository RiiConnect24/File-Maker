#!/usr/bin/python
# -*- coding: utf-8 -*-

# ===========================================================================
# NEWS CHANNEL GENERATION SCRIPT
# AUTHORS: LARSEN VALLECILLO
# ****************************************************************************
# Copyright (c) 2015-2017 RiiConnect24, and it's (Lead) Developers
# ===========================================================================

import binascii
import collections
import feedparser
import googlemaps # Used to parse the Google Maps API.
import json # Used for JSON parsing.
import jsonp2json
import os
import pytz # Used to find time zones.
import requests
import subprocess
import struct
import time # Used to get time stuff.
import unidecode
import urllib2 # Needed to download a few things for the news.
import tempfile # For resizing images etc
from bs4 import BeautifulSoup # Used to parse HTML.
from datetime import timedelta, datetime, date # Used to get time stuff.
from dateutil import tz, parser
from newspaper import * # Used to parse news articles.
from PIL import Image # Used to work with images.
from resizeimage import resizeimage # Used to resize images.

"""This will pack the integers."""

def u8(data):
	if data < 0 or data > 255:
		print "[SEVERE] Value Pack Failure: %s" % data
		data = 0
	return struct.pack(">B", data)

def u16(data):
	if data < 0 or data > 65535:
		print "[SEVERE] Value Pack Failure: %s" % data
		data = 0
	return struct.pack(">H", data)

def u32(data):
	if data < 0 or data > 4294967295:
		print "[SEVERE] Value Pack Failure: %s" % data
		data = 0
	return struct.pack(">I", data)

def u32_littleendian(data):
	if data < 0 or data > 4294967295:
		print "[SEVERE] Value Pack Failure: %s" % data
		data = 0
	return struct.pack("<I", data)
	
"""This is to replace characters."""
	
replace_chars = collections.OrderedDict()
		
replace_chars["\x01\x0c"] = "\x00\x43"
replace_chars["\x01\x0d"] = "\x00\x63"
replace_chars["\x02\xdd"] = "\x00\xbd"
replace_chars["\x00\x26\x00\x61\x00\x6d\x00\x70\x00\x3b"] = "\x00\x26"
replace_chars["\x20\x10"] = "\x00\x2d"
replace_chars["\x20\x11"] = "\x00\x2d"
replace_chars["\x20\x12"] = "\x00\x2d"
replace_chars["\x20\x13"] = "\x00\x2d"
replace_chars["\x20\x14"] = "\x00\x2d"
replace_chars["\x20\x15"] = "\x00\x2d"
replace_chars["\x20\x18"] = "\x00\x27"
replace_chars["\x20\x19"] = "\x02\xdd"
replace_chars["\x20\x1a"] = "\x00\x2c"
replace_chars["\x20\x1b"] = "\x00\x27"
replace_chars["\x20\x1c"] = "\x00\x22"
replace_chars["\x20\x1d"] = "\x00\x22"

"""This is a list of locations."""

japanese_locations = ["東京", "八丈島", "大島", "父島", "三宅島", "札幌市", "稚内市", "旭川市", "留萌市", "岩見沢市", "倶知安町", "網走市", "北見市", "紋別市", "根室市", "釧路市", "帯広市", "室蘭市", "浦河町", "函館市", "江差町", "枝幸町", "羽幌町", "小樽市", "寿都町", "雄武町", "広尾町", "苫小牧市", "青森市", "むつ市", "八戸市", "深浦町", "盛岡市", "宮古市", "大船渡市", "仙台市", "白石市", "石巻市", "秋田市", "横手市", "山形市", "米沢市", "酒田市", "新庄市", "福島市", "小名浜", "会津若松市", "白河市", "水戸市", "つくば市", "宇都宮市", "大田原市", "日光市", "前橋市", "みなかみ町", "さいたま市", "熊谷市", "秩父市", "千葉市", "銚子市", "勝浦市", "館山市", "横浜市", "小田原市", "富山市", "伏木", "金沢市", "輪島市", "福井市", "敦賀市", "甲府市", "河口湖", "長野市", "松本市", "飯田市", "軽井沢町", "諏訪市", "新潟市", "長岡市", "上越市", "相川", "岐阜市", "高山市", "静岡市", "網代", "三島市", "浜松市", "富士山", "御前崎市", "石廊崎", "名古屋市", "豊橋市", "伊良湖", "津市", "尾鷲市", "四日市市", "上野", "大津市", "彦根市", "京都市", "舞鶴市", "大阪市", "神戸市", "豊岡市", "姫路市", "洲本市", "奈良市", "風屋", "和歌山市", "潮岬", "鳥取市", "米子市", "境港市", "松江市", "浜田市", "西郷", "岡山市", "津山市", "広島市", "庄原市", "福山市", "呉市", "山口市", "下関市", "柳井市", "萩市", "宇部市", "徳島市", "美波町", "高松市", "多度津町", "松山市", "新居浜市", "宇和島市", "高知市", "室戸岬", "宿毛市", "土佐清水市", "福岡市", "八幡", "飯塚市", "久留米市", "佐賀市", "伊万里市", "長崎市", "厳原", "福江", "平戸市", "大村市", "佐世保市", "熊本市", "牛深", "人吉市", "阿蘇山", "大分市", "中津市", "日田市", "佐伯市", "宮崎市", "延岡市", "都城市", "高千穂町", "油津", "鹿児島市", "名瀬", "鹿屋市", "阿久根市", "溝辺", "枕崎市", "種子島", "屋久島", "喜界島", "沖永良部", "与論島", "那覇市", "名護市", "久米島町", "南大東島", "宮古島市", "石垣島", "与那国島", "西表島", "ザ・バレー", "セント・ジョン", "ブエノスアイレス", "コモドロ・リバダビア", "コルドバ", "コリエンテス", "オラニェスタード", "ナッソー", "ブリッジタウン", "ベルモパン", "ラパス", "ブラジリア", "マナウス", "サルバドール", "フォルタレザ", "リオデジャネイロ", "サンパウロ", "レシフェ", "ロードタウン", "オタワ", "トロント", "エドモントン", "カルガリー", "バンクーバー", "ウィニペグ", "チャーチル", "ケベック", "モントリオール", "イエローナイフ", "イカルイット", "ジョージタウン", "サンティアゴ", "イースター島", "ホーン岬", "ボゴタ", "レティシア", "サンホセ", "ロゾー", "サントドミンゴ", "キト", "サンサルバドル", "セントジョージ", "グアテマラ", "ポルトープランス", "テグシガルパ", "キングストン", "メキシコシティ", "サンルーカス岬", "アカプルコ", "プエルト・バヤルタ", "テオティワカン", "モンテレー", "カンクン", "プリマス", "ウィレムスタット", "マナグア", "パナマ", "アスンシオン", "リマ", "マチュ・ピチュ", "ナスカ", "バセテール", "カストリーズ", "キングスタウン", "パラマリボ", "ポートオブスペイン", "グランドターク", "ワシントン", "アンカレジ", "ロサンゼルス", "サンフランシスコ", "デンバー", "マイアミ", "オーランド", "アトランタ", "ホノルル", "シカゴ", "ニュー・オリンズ", "ボストン", "デトロイト", "ミネアポリス", "カンザスシティ", "セントルイス", "シャーロット", "ラスベガス", "ニューヨーク", "ナイアガラ", "シンシナティ", "オクラホマシティ", "ポートランド", "ピッツバーグ", "メンフィス", "ダラス", "エル・パソ", "ヒューストン", "ソルトレークシティ", "シアトル", "ペンシルベニア州", "サイパン", "モンテビデオ", "シャーロット・アマリエ", "カラカス", "ティラナ", "キャンベラ", "シドニー", "ダーウィン", "ウルル", "ブリスベン", "ゴールドコースト", "ケアンズ", "アデレード", "メルボルン", "パース", "クリスマス島", "ウィーン", "ブリュッセル", "サラエボ", "ハボローネ", "ソフィア", "ザグレブ", "ニコシア", "プラハ", "コペンハーゲン", "ヌーク", "タリン", "ヘルシンキ", "パリ", "ボルドー", "トゥールーズ", "ナント", "マルセイユ", "ニース", "ベルリン", "フランクフルト", "ミュンヘン", "ハンブルク", "デュッセルドルフ", "ボン", "アテネ", "ロードス", "ブダペスト", "レイキャビク", "ダブリン", "ローマ", "トリノ", "ミラノ", "ベネチア", "フィレンツェ", "ナポリ", "パレルモ", "シラクサ", "リガ", "マセル", "ファドゥーツ", "ビリニュス", "ルクセンブルク", "スコピエ", "バレッタ", "ポドゴリツァ", "マプト", "ウィントフーク", "アムステルダム", "ウェリントン", "オークランド", "クライストチャーチ", "オスロ", "ワルシャワ", "クラクフ", "リスボン", "ブカレスト", "モスクワ", "ハバロフスク", "ウラジオストク", "ユジノ・サハリンスク", "サンクトペテルブルク", "イルクーツク", "グロズヌイ", "ベオグラード", "ブラチスラヴァ", "リュブリャナ", "プレトリア", "ヨハネスバーグ", "ケープタウン", "マドリード", "トレド", "バルセロナ", "バレンシア", "ムババネ", "ストックホルム", "ベルン", "ジュネーブ", "ローザンヌ", "チューリヒ", "アンカラ", "イスタンブール", "ロンドン", "ケンブリッジ", "マンチェスター", "リバプール", "エジンバラ", "ベルファスト", "ルサカ", "ハラレ", "台北", "カオシュン", "ソウル", "プサン", "香港", "マカオ", "ジャカルタ", "デンパサル", "シンガポール", "バンコク", "プーケット", "マニラ", "セブ", "クアラルンプール", "北京", "上海", "広州", "ハルビン", "大連", "成都", "桂林", "アブダビ", "ドバイ", "ニューデリー", "ムンバイ", "カイロ", "ルクソール", "マスカット", "ドーハ", "クウェート", "リヤド", "メッカ", "ジッダ", "ダマスカス", "マナマ", "アンマン", "バクー", "カブール", "アルジェ", "アンド・ラ・ラベリャ", "ルアンダ", "エレバン", "ダッカ", "ミンスク", "ポルト・ノボ", "ティンプー", "バンダル・スリ・ブガワン", "ワガドゥグー", "ヤンゴン", "ブジュンブラ", "プノンペン", "アンコール・ワット", "ヤウンデ", "プライア", "バンギ", "ンジャメナ", "モロニ", "ブラザビル", "キンシャサ", "ヤムスクロ", "ハバナ", "ジブチ", "ディリ", "マラボ", "アスマラ", "アディス・アベバ", "スバ", "ナンディ", "パペーテ", "リーブルビル", "トビリシ", "アクラ", "コナクリ", "ビサオ", "テヘラン", "バグダッド", "エルサレム", "アスタナ", "ナイロビ", "タラワ", "ビシュケク", "ビエンチャン", "ベイルート", "モンロビア", "トリポリ", "アンタナナリボ", "リロングウェ", "マレ", "バマコ", "マジュロ", "ヌアクショット", "ポート・ルイス", "パリキール", "キシニョフ", "モナコ", "ウランバートル", "ラバト", "カサブランカ", "ヤレン", "カトマンズ", "ヌメア", "ニアメ", "アブジャ", "ピョンヤン", "イスラマバード", "カラチ", "コロール", "ラマッラ", "ポート・モレスビー", "アシガバット", "キガリ", "アピア", "サンマリノ", "サントメ", "ダカール", "ビクトリア", "フリータウン", "ホニアラ", "モガディシュ", "スリ・ジャヤワルダナプラ・コッテ", "ハルツーム", "ドゥシャンベ", "ドドマ", "バンジュール", "南極点", "ロメ", "ヌクアロファ", "チュニス", "フナフティ", "カンパラ", "キエフ", "タシケント", "ポート・ビラ", "ハノイ", "ホー・チミン", "サヌア", "テル・アビブ", "エロマンガ島", "セントルシア", "スリナム", "タークス・カイコス諸島", "エリトリア", "ニュージーランド", "リヒテンシュタイン", "ドミニカ共和国", "日本", "マケドニア", "エジプト", "ロシア", "ジャマイカ", "ブラジル", "ニジェール", "韓国", "ナミビア", "モントセラト", "ベリーズ", "ルーマニア", "スウェーデン", "ラトビア", "アルゼンチン", "レソト", "ブルガリア", "モザンビーク", "アラブ首長国連邦", "オランダ", "チェコ", "マリ", "オマーン", "イタリア", "カタール", "ボスニア・ヘルツェゴビナ", "イギリス", "キプロス", "カナダ", "ホンジュラス", "スロベニア", "インド", "セルビア", "デンマーク", "スロバキア", "コスタリカ", "ガイアナ", "エルサルバドル", "ボリビア", "アンティグア・バーブーダ", "ポルトガル", "ホンコン", "グアドループ", "インドネシア", "アイルランド", "コロンビア", "アンギラ", "グレナダ", "モーリタニア", "アルバニア", "オランダ領アンティル", "フィリピン", "トリニダード・トバゴ", "台湾", "フランス領ギアナ", "ペルー", "ジンバブエ", "バーレーン", "セントキッツ・ネイビス", "サウジアラビア", "ギリシャ", "モンテネグロ", "ボツワナ", "ザンビア", "ポーランド", "マルタ", "マルティニーク", "リトアニア", "ドイツ", "タイ", "アイスランド", "ケイマン諸島", "スイス", "シリア", "ベルギー", "バハマ", "クロアチア", "アゼルバイジャン", "スーダン", "南アフリカ", "エストニア", "メキシコ", "ウルグアイ", "エクアドル", "ハイチ", "スワジランド", "バルバドス", "アメリカ", "中国", "ノルウェー", "ニカラグア", "フィンランド", "チャド", "セントビンセント・グレナディーン", "トルコ", "フランス", "マレーシア", "オーストラリア", "ハンガリー", "英領ヴァージン諸島", "ベネズエラ", "スペイン", "ヨルダン", "米領バージン諸島", "アルバ", "オーストリア", "ドミニカ国", "パラグアイ", "ソマリア", "チリ", "コロンビア特別区", "アラスカ州", "アラバマ州", "アーカンソー州", "アリゾナ州", "カリフォルニア州", "コロラド州", "コネティカット州", "デラウェア州", "フロリダ州", "ジョージア州", "ハワイ州", "アイオワ州", "アイダホ州", "イリノイ州", "インディアナ州", "カンザス州", "ケンタッキー州", "ルイジアナ州", "マサチューセッツ州", "メリーランド州", "メーン州", "ミシガン州", "ミネソタ州", "ミズーリ州", "ミシシッピ州", "モンタナ州", "ノースカロライナ州", "ノースダコタ州", "ネブラスカ州", "ニューハンプシャー州", "ニュージャージー州", "ニューメキシコ州", "ネバダ州", "ニューヨーク州", "オハイオ州", "オクラホマ州", "オレゴン州", "ロードアイランド州", "サウスカロライナ州", "サウスダコタ州", "テネシー州", "テキサス州", "ユタ州", "バージニア州", "バーモント州", "ワシントン州", "ウィスコンシン州", "ウェストバージニア州", "ワイオミング州", "東京都", "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "神奈川県", "富山県", "石川県", "福井県", "山梨県", "長野県", "新潟県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県"]
dutch_locations = ["Assen", "Coevorden", "Emmen", "Hoogeveen", "Meppel", "Almere", "Lelystad", "Emmeloord", "Biddinghuizen", "Bolsward", "Dokkum", "Drachten", "Franeker", "Harlingen", "Heerenveen", "Leeuwarden", "Sloten", "Sneek", "Stavoren", "Workum", "Apeldoorn", "Arnhem", "Buren", "Culemborg", "Deil", "Dieren", "Doetinchem", "Ede", "Enspijk", "Gendt", "Groenlo", "Harderwijk", "Hattem", "Heukelum", "Huissen", "Nijkerk", "Nijmegen", "Tiel", "Wageningen", "Wijchen", "Winterswijk", "Zaltbommel", "Zevenaar", "Zutphen", "Appingedam", "Delfzijl", "Groningen", "Hoogezand-Sappemeer", "Stadskanaal", "Winschoten", "Veendam", "Geleen", "Gennep", "Heerlen", "Kerkrade", "Kessel", "Landgraaf", "Maastricht", "Montfort", "Nieuwstadt", "Roermond", "Sittard", "Schin op Geul", "Stein", "Thorn", "Valkenburg", "Venlo", "Weert", "Bergen op Zoom", "Breda", "'s-Hertogenbosch", "Eindhoven", "Geertruidenberg", "Grave", "Helmond", "Heusden", "Klundert", "Oosterhout", "Oss", "Ravenstein", "Roosendaal", "Sint-Oedenrode", "Tilburg", "Valkenswaard", "Veldhoven", "Waalwijk", "Willemstad", "Woudrichem", "Alkmaar", "Amstelveen", "Amsterdam", "Enkhuizen", "Haarlem", "Heerhugowaard", "Hilversum", "Hoofddorp", "Hoorn", "Laren", "Purmerend", "Medemblik", "Monnickendam", "Muiden", "Naarden", "Schagen", "Velsen", "Weesp", "Zaanstad", "Almelo", "Blokzijl", "Deventer", "Enschede", "Genemuiden", "Hasselt", "Hengelo", "Kampen", "Oldenzaal", "Steenwijk", "Vollenhove", "Zwolle", "Alphen aan den Rijn", "Delft", "Dordrecht", "Gorinchem", "Gouda", "Leiden", "Rotterdam", "Spijkenisse", "Zoetermeer", "Amersfoort", "Nieuwegein", "Utrecht", "Veenendaal", "Arnemuiden", "Goes", "Hulst", "Middelburg", "Sluis", "Terneuzen", "Veere", "Vlissingen", "Zierikzee", "Afghanistan", "Algerije", "Andorra", "Angola", "Antigua en Barbuda", "Azerbeidzjan", "Bahama's", "Bahrein", "Bangladesh", "Barbados", "Belize", "Benin", "Bhutan", "Bolivia", "Botswana", "Brunei", "Bulgarije", "Burundi", "Cambodja", "Canada", "Centraal-Afrikaanse Republiek", "Chili", "China", "Colombia", "Comoren", "Congo-Brazzaville", "Costa Rica", "Cuba", "Cyprus", "Denemarken", "Djibouti", "Dominica", "Dominicaanse Republiek", "Duitsland", "Ecuador", "Egypte", "El Salvador", "Equatoriaal-Guinea", "Eritrea", "Estland", "Fiji", "Filipijnen", "Finland", "Frankrijk", "Gabon", "Gambia", "Ghana", "Grenada", "Griekenland", "Guatemala", "Guinee", "Guinee-Bissau", "Guyana", "Honduras", "Hongarije", "Ierland", "IJsland", "India", "Irak", "Iran", "Ivoorkust", "Jamaica", "Japan", "Jemen", "Kameroen", "Kazachstan", "Kenia", "Kiribati", "Koeweit", "Kosovo", "Laos", "Lesotho", "Letland", "Libanon", "Liberia", "Liechtenstein", "Litouwen", "Luxemburg", "Madagaskar", "Malawi", "Maldiven", "Mali", "Malta", "Marokko", "Marshalleilanden", "Mauritius", "Mexico", "Micronesia", "Monaco", "Montenegro", "Mozambique", "Myanmar", "Nauru", "Nederland", "Nepal", "Nicaragua", "Nieuw-Zeeland", "Niger", "Nigeria", "Noord-Korea", "Noorwegen", "Oeganda", "Oezbekistan", "Oman", "Oostenrijk", "Oost-Timor", "Pakistan", "Palestina", "Panama", "Paraguay", "Peru", "Polen", "Portugal", "Qatar", "Rusland", "Rwanda", "Salomonseilanden", "Samoa", "San Marino", "Senegal", "Seychellen", "Sierra Leone", "Singapore", "Slowakije", "Soedan", "Spanje", "Sri Lanka", "Suriname", "Swaziland", "Tadzjikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad en Tobago", "Tsjaad", "Turkije", "Turkmenistan", "Tuvalu", "Uruguay", "Vanuatu", "Vaticaanstad", "Venezuela", "Verenigde Arabische Emiraten", "Verenigde Staten", "Vietnam", "Wit-Rusland", "Zambia", "Zimbabwe", "Zuid-Afrika", "Zuid-Korea", "Zuid-Soedan", "Zweden", "Zwitserland", "Noord-Holland", "Drenthe", "Flevoland", "Friesland", "Gelderland", "Limburg", "Noord-Brabant", "Overijssel", "Zuid-Holland", "Zeeland", "Alaska", "Alabama", "Arkansas", "Arizona", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "Nebraska", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming", "Tokio", "Kyoto", "Osaka", "Fukuoka", "Buenos Aires", "Oranjestad", "Manaus", "Salvador", "Fortaleza", "Rio de Janeiro", "Ottawa", "Toronto", "Edmonton", "Calgary", "Vancouver", "Winnipeg", "Churchill", "Santiago", "Paaseiland", "Bogota", "Santo Domingo", "San Salvador", "Georgetown", "Port-au-Prince", "Tegucigalpa", "Kingston", "Mexico-stad", "Acapulco", "Monterrey", "Plymouth", "Lima", "Machu Picchu", "Paramaribo", "Washington D.C.", "Los Angeles", "San Francisco", "Denver", "Miami", "Orlando", "Atlanta", "Honolulu", "Chicago", "New Orleans", "Boston", "Detroit", "Minneapolis", "Kansas City", "Saint Louis", "Charlotte", "Las Vegas", "Niagara Falls", "Cincinnati", "Oklahoma City", "Portland", "Pittsburgh", "Memphis", "Dallas", "El Paso", "Houston", "Salt Lake City", "Seattle", "Guam", "Caracas", "Canberra", "Sydney", "Darwin", "Uluru", "Brisbane", "Gold Coast", "Cairns", "Adelaide", "Melbourne", "Perth", "Wenen", "Brussel", "Sarajevo", "Sofia", "Zagreb", "Nicosia", "Praag", "Kopenhagen", "Tallinn", "Helsinki", "Parijs", "Bordeaux", "Toulouse", "Nantes", "Marseille", "Nice", "Berlijn", "Frankfurt", "Hamburg", "Bonn", "Athene", "Rhodos", "Boedapest", "Reykjavik", "Dublin", "Rome", "Turijn", "Milaan", "Florence", "Napels", "Palermo", "Riga", "Skopje", "Podgorica", "Wellington", "Auckland", "Christchurch", "Oslo", "Warschau", "Lissabon", "Boekarest", "Moskou", "Sint-Petersburg", "Grozny", "Belgrado", "Bratislava", "Pretoria", "Johannesburg", "Kaapstad", "Madrid", "Barcelona", "Valencia", "Stockholm", "Bern", "Lausanne", "Ankara", "Istanbul", "Londen", "Cambridge", "Manchester", "Liverpool", "Edinburgh", "Belfast", "Lusaka", "Taipei", "Kaohsiung", "Seoul", "Busan", "Hongkong", "Macau", "Jakarta", "Bangkok", "Phuket", "Manilla", "Kuala Lumpur", "Beijing", "Sjanghai", "Harbin", "Chengdu", "Abu Dhabi", "Dubai", "New Delhi", "Mumbai", "Luxor", "Doha", "Riyad", "Mekka", "Djedda", "Damascus", "Amman", "Algiers", "Luanda", "Dhaka", "Minsk", "Ouagadougou", "Angkor Wat", "Bangui", "Brazzaville", "Kinshasa", "Havana", "Dili", "Tbilisi", "Accra", "Conakry", "Teheran", "Bagdad", "Jeruzalem", "Astana", "Nairobi", "Beiroet", "Tripoli", "Bamako", "Port Louis", "Rabat", "Casablanca", "Kathmandu", "Abuja", "Pyongyang", "Islamabad", "Karachi", "Ramallah", "Dakar", "Victoria", "Mogadishu", "Khartoem", "Tunis", "Kampala", "Kiev", "Hanoi", "Sanaa", "Tel Aviv", "Mosul", "Phoenix", "Sacramento", "Dover", "Tallahassee", "Springfield", "Indianapolis", "Topeka", "Baton Rouge", "Augusta", "Saint Paul", "Jackson", "Lincoln", "Albany", "Raleigh", "Columbus", "Salem", "Columbia", "Nashville", "Austin", "Richmond", "Olympia", "Charleston", "Madison", "Cheyenne", "Kabul", "Jerevan", "Phnom Penh", "Peking", "Asuncion", "Decatur", "Dothan", "Hoover", "Mobile", "Birmingham", "Flagstaff", "Tucson", "Yuma", "Anaheim", "Fresno", "Oakland", "Palm Springs", "Redding", "Riverside", "San Bernardino", "San Diego", "San Jose", "Santa Barbara", "Santa Cruz", "Colorado Springs", "Bristol", "Wilmington", "Fort Lauderdale", "Hollywood", "Miami Beach", "Naples", "Panama City", "Tampa", "Athens", "Brunswick", "Waterloo", "Aurora", "Mount Vernon", "Anderson", "Elkhart", "Evansville", "Gary", "Lafayette", "Hutchinson", "Manhattan", "Wichita", "Bowling Green", "Lexington", "Alexandria", "Monroe", "Lowell", "Worcester", "Baltimore", "Bethesda", "Flint", "Grand Rapids", "Holland", "Kalamazoo", "Midland", "Rochester", "Joplin", "St. Louis", "Hattiesburg", "Bozeman", "Durham", "Greenville", "Fargo", "Omaha", "Edison", "Newark", "Albuquerque", "Henderson", "Reno", "Binghamton", "Buffalo", "Ithaca", "Southampton", "Akron", "Cleveland", "Dayton", "Mansfield", "Portsmouth", "Lawton", "Tulsa", "Ontario", "Philadelphia", "Reading", "Newport", "Chattanooga", "Knoxville", "Amarillo", "Corpus Christi", "Odessa", "Paris", "San Antonio", "Tyler", "Waco", "Logan", "Moab", "Arlington", "Charlottesville", "Burlington", "Tacoma", "Yakima", "Milwaukee", "Casper"]

"""Replace categories in French news with these."""

lobs_categories = collections.OrderedDict()

lobs_categories["TopNews"] = "topnews"
lobs_categories["Société"] = "society"
lobs_categories["Monde"] = "world"
lobs_categories["Politique"] = "politics"

"""Categories for ZEIT."""

zeit_sports_categories = ["Eishockey", "Fußball", "Tennis", "Basketball", "Wintersport", "Sport Allgemein", "Motorsport", "Ski nordisch", "Handball", "Golf"]

zeit_categories = collections.OrderedDict()

zeit_categories["General"] = "general"
zeit_categories["Politik"] = "politics"
zeit_categories["Wirtschaft"] = "economy"
zeit_categories["Gesellschaft"] = "society"
zeit_categories["Kultur"] = "culture"
zeit_categories["Wissen"] = "knowledge"
zeit_categories["Digital"] = "digital"
zeit_categories["Sport"] = "sports"

"""Function to replace characters."""

def replace(item):
	if item != 0:
		for characters in replace_chars.items():
			if characters[0] in item:
				item = item.replace(characters[0], characters[1])
				
	return item
			
"""Get the location data."""

def locations_download(language_code, data):
	locations = collections.OrderedDict()
	locations_return = collections.OrderedDict()
	gmaps = googlemaps.Client(key="AIzaSyCOHZJ1mZmaz6A5r6kpv2gQPOe6l0OLT4A")
	
	"""This dictionary is used to determine languages."""
	
	languages = {
		0: "ja",
		1: "en",
		2: "de",
		3: "fr",
		4: "es",
		5: "it",
		6: "nl",
	}
	
	"""This dictionary is used to get the right location with Google Maps."""
	
	corrections = {
		"UNITED NATIONS": ["1cf0cb780000000006000000", "United Nations"],
		"WASHINGTON": ["1ba2c94a0000000006000000", "Washington"],
	}
	
	for keys,values in data.items():
		location = values[8]
		
		if location > 0:
			if location not in locations:
				locations[location] = []
				
			locations[location].append(keys)
	
	for name in locations.keys():
		read = 1
		
		if name not in corrections:
			try:
				read = gmaps.geocode(name.decode("utf-8"), language=languages[language_code])
			except:
				pass
			
		if read == 1:
			if name in corrections:
				coordinates = binascii.unhexlify(corrections[name][0])
				new_name = corrections[name][1]
				
				for filenames in locations[name]:
					if new_name not in locations_return:
						locations_return[new_name] = [coordinates, []]
					
					locations_return[new_name][1].append(filenames)
	
		elif read != 1:
			try:
				new_name = replace(read[0]["address_components"][0]["long_name"])
			
				"""Not doing anything with these at this time."""
			
				country = u8(0)
				region = u8(0)
				location = u16(0)
				zoom_factor = u32_littleendian(6)
			
				coordinates = u16(int(read[0]["geometry"]["location"]["lat"] / 0.0055) & 0xFFFF) + u16(int(read[0]["geometry"]["location"]["lng"] / 0.0055) & 0xFFFF) + country + region + u16(0) + zoom_factor
				
				for filenames in locations[name]:
					if new_name not in locations_return:
						locations_return[new_name] = [coordinates, []]
					
					locations_return[new_name][1].append(filenames)
			except:
				pass
	
	return locations_return

def download_ap_english():
	print "Downloading from the Associated Press (English)..."
	
	print "\n"
	
	topics_name = collections.OrderedDict()
	
	topics_name["national"] = "National News"
	topics_name["world"] = "International News"
	topics_name["sports"] = "Sports"
	topics_name["entertainment"] = "Arts/Entertainment"
	topics_name["business"] = "Business"
	topics_name["science"] = "Science/Health"
	topics_name["technology"] = "Technology"
	
	topics = collections.OrderedDict()
	
	topics["national"] = ["USHEADS"]
	topics["world"] = ["WORLDHEADS"]
	topics["sports"] = ["SPORTSHEADS"]
	topics["entertainment"] = ["ENTERTAINMENTHEADS"]
	topics["business"] = ["BUSINESSHEADS"]
	topics["science"] = ["SCIENCEHEADS", "HEALTHHEADS"]
	topics["technology"] = ["TECHHEADS"]
	
	return download_ap(topics_name, topics, "en")
	
def download_ap_spanish():
	print "Downloading from the Associated Press (Spanish)..."
	
	print "\n"
	
	topics_name = collections.OrderedDict()
	
	topics_name["general"] = "Generales"
	topics_name["finance"] = "Financieras"
	topics_name["sports"] = "Deportivas"
	topics_name["shows"] = "Espectáculos"
	
	topics = collections.OrderedDict()
	
	topics["general"] = ["NOTICIAS_GENERALES"]
	topics["finance"] = ["NOTICIAS_FINANCIERAS"]
	topics["sports"] = ["NOTICIAS_DEPORTIVAS"]
	topics["shows"] = ["NOTICIAS_ENTRETENIMIENTOS"]
	
	return download_ap(topics_name, topics, "es")
	
def download_reuters_english():
	print "Downloading from Reuters (English)..."
	
	print "\n"
	
	topics_name = collections.OrderedDict()
	
	topics_name["world"] = "World"
	topics_name["uk"] = "UK"
	topics_name["health"] = "Health"
	topics_name["science"] = "Science"
	topics_name["technology"] = "Technology"
	topics_name["offbeat"] = "Oddly Enough"
	topics_name["entertainment"] = "Entertainment"
	topics_name["sports"] = "Sports"
	
	topics = collections.OrderedDict()
	
	topics["world"] = ["UKWorldNews"]
	topics["uk"] = ["UKdomesticNews"]
	topics["health"] = ["UKHealthNews"]
	topics["science"] = ["UKScienceNews"]
	topics["technology"] = ["technologyNews"]
	topics["offbeat"] = ["UKOddlyEnoughNews"]
	topics["entertainment"] = ["UKEntertainment"]
	topics["sports"] = ["UKSportsNews"]
	
	return download_reuters(topics_name, topics)
	
def download_lobs_french():
	print "Downloading from L'Obs (French)..."
	
	print "\n"
	
	topics_name = collections.OrderedDict()
	
	topics_name["topnews"] = "Top News"
	topics_name["society"] = "Société"
	topics_name["world"] = "Monde"
	topics_name["politique"] = "Politique"
	
	return download_lobs(topics_name)
	
def download_zeit_german():
	print "Downloading from ZEIT (German)..."
	
	print "\n"
	
	topics_name = collections.OrderedDict()
	
	topics_name["general"] = "General"
	topics_name["politics"] = "Politik"
	topics_name["economy"] = "Wirtschaft"
	topics_name["society"] = "Gesellschaft"
	topics_name["culture"] = "Kultur"
	topics_name["knowledge"] = "Wissen"
	topics_name["digital"] = "Digital"
	topics_name["sports"] = "Sport"
	
	return download_zeit(topics_name)
	
def download_ansa_italian():
	print "Downloading from ANSA (Italian)..."
	
	print "\n"
	
	topics_name = collections.OrderedDict()
	
	topics_name["world"] = "Dal mondo"
	topics_name["italy"] = "Dall'Italia"
	topics_name["sports"] = "Sport"
	topics_name["economy"] = "Economia"
	topics_name["culture"] = "Cultura"
	
	topics = collections.OrderedDict()
	
	topics["world"] = ["mondo"]
	topics["italy"] = ["abruzzo", "basilicata", "calabria", "campania", "emiliaromagna", "friuliveneziagiulia", "lazio", "liguria", "lombardia", "marche", "molise", "piemonte", "puglia", "sardegna", "sicilia", "toscana", "trentino", "umbria", "valledaosta", "veneto"]
	topics["sports"] = ["sport"]
	topics["economy"] = ["economia"]
	topics["culture"] = ["cultura"]
	
	return download_ansa(topics_name, topics)
	
def download_anp_dutch():
	print "Downloading from ANP (Dutch)..."
	
	print "\n"
	
	topics_name = collections.OrderedDict()
	
	topics_name["general"] = "Algemeen"
	topics_name["economy"] = "Economie"
	topics_name["sports"] = "Sport"
	topics_name["technology"] = "Tech"
	topics_name["entertainment"] = "Entertainment"
	topics_name["lifestyle"] = "Lifestyle"
	topics_name["noteworthy"] = "Opmerkelijk"
	
	topics = collections.OrderedDict()
	
	topics["general"] = ["algemeen"]
	topics["economy"] = ["economie"]
	topics["sports"] = ["sport"]
	topics["technology"] = ["tech"]
	topics["entertainment"] = ["entertainment"]
	topics["lifestyle"] = ["lifestyle"]
	topics["noteworthy"] = ["opmerkelijk"]
	
	return download_anp(topics_name, topics)
	
def download_news24_mainichi_japanese():
	print "Downloading from News24 and Mainichi (Japanese)..."
	
	print "\n"
	
	topics_name = collections.OrderedDict()
	
	topics_name["politics"] = "政治"
	topics_name["economy"] = "経済"
	topics_name["international"] = "国際"
	topics_name["society"] = "社会"
	topics_name["sports"] = "スポーツ"
	topics_name["entertainment"] = "芸能文化"
	
	topics = collections.OrderedDict()
	
	topics["politics"] = ["politics"]
	topics["economy"] = ["economy"]
	topics["international"] = ["international"]
	topics["society"] = ["society"]
	topics["sports"] = ["sports"]
	topics["entertainment"] = ["entertainment"]
	
	return download_news24_mainichi(topics_name, topics)

def download_news24_mainichi(topics_name, topics):
	picture_number = 0
	
	data = collections.OrderedDict()
	
	for rss_category in topics.items():
		numbers = 0
		
		print "Downloading %s..." % topics_name[rss_category[0]]
		
		print "\n"
		
		for rss in rss_category[1]:
			numbers_category = 0
			
			rss_feed = urllib2.urlopen("http://news24.jp/sitemap_%s.xml" % rss).read()
			
			soup = BeautifulSoup(rss_feed, "lxml")
			
			occurrences = 0
			
			format = "%Y-%m-%dT%H:%M:%SZ+09:00"
			
			for items in soup.findAll("url"):
				updated = parser.parse(soup.findAll("news:publication_date")[occurrences].contents[0])
				updated = updated.astimezone(tz.tzutc())
				
				updated = (int(time.mktime(updated.timetuple()) - 946684800) / 60)
				
				time_current = (int(time.mktime(datetime.utcnow().timetuple())) - 946684800) / 60
				
				if updated >= time_current - 60:
					numbers += 1
						
					print "Downloading News Article %s..." % (str(numbers))
					
					parsedata = parsedata_news24(soup.findAll("loc")[occurrences].contents[0].replace("html", "jsonp"), soup.findAll("news:title")[occurrences].contents[0], updated, picture_number)
					
					if parsedata > 0:
						picture_number += parsedata[7]
						data[rss_category[0] + str(numbers)] = parsedata
				
				occurrences += 1
				
		print "\n"
						
	print "Downloading Breaking News..."
		
	print "\n"
		
	rss_feed = feedparser.parse(urllib2.urlopen("http://rss.rssad.jp/rss/mainichi/flash.rss").read())
		
	for items in rss_feed.entries:
		updated = parser.parse(items.updated)
		updated = updated.astimezone(tz.tzutc())
				
		updated = (int(time.mktime(updated.timetuple()) - 946684800) / 60)
				
		time_current = (int(time.mktime(datetime.utcnow().timetuple())) - 946684800) / 60
				
		if updated >= time_current - 60:
			if "/ad/" not in items["link"]:
				numbers += 1
						
				print "Downloading News Article %s..." % (str(numbers))
					
				parsedata = parsedata_mainichi(items["link"], items["title"], updated, picture_number)
						
				if parsedata > 0:
					picture_number += parsedata[7]
					data[rss_category[0] + str(numbers)] = parsedata
	
	return data

def parsedata_mainichi(url, title, updated, picture_number):
	subprocess.call(["ruby", "newsmainichi.rb", url])

	with open("temp_mainichi", "rb") as source_file:
		html = source_file.read()

	os.remove("temp_mainichi")
	
	soup = BeautifulSoup(html, "lxml")
	
	headline = title.encode("utf-16be") # Parse the headline.
	
	article = ""
	
	for text in soup.findAll("p", {"class": "txt"}):
		article += " " + text.getText().strip() + "\n\n"
		
	article = article.encode("utf-16be")
	
	location_list = collections.OrderedDict()
	
	for location in japanese_locations:
		if location.encode("utf-16be") in article:
			location_list[location] = article.count(location.encode("utf-16be"))
	
	try:
		location = max(location_list, key=location_list.get)
	except:
		location = 0
	
	try:
		if picture_number <= 5:
			"""Parse the pictures."""
		
			picture = urllib2.urlopen(soup.find("img", {"alt", "vertical-photo"})["src"]).read()
		
			picture_number = 1
		else:
			picture_number = 0
			picture = 0
	except:
		picture_number = 0
		picture = 0
			
	if len(headline) == 0:
		print "Headline is 0."
		print url
		return 0
	elif len(article) == 0:
		print "Article is 0."
		print url
		return 0
	else:
		return [u32(updated), u32(updated), replace(article), replace(headline), picture, 0, 0, picture_number, replace(location), "mainichi"]

def parsedata_news24(url, title, updated, picture_number):
	json_data = json.loads(jsonp2json.convert(urllib2.urlopen(url).read()))
	
	headline = title.encode("utf-16be") # Parse the headline.

	article = json_data["article"]["newsBody"].replace("<br />", "\n").encode("utf-16be")
	
	location_list = collections.OrderedDict()
	
	for location in japanese_locations:
		if location.encode("utf-16be") in article:
			location_list[location] = article.count(location.encode("utf-16be"))
	
	try:
		location = max(location_list, key=location_list.get)
	except:
		location = 0
	
	try:
		if picture_number <= 5:
			"""Parse the pictures."""
		
			picture = urllib2.urlopen("http://news24.jp/" + json_data["article"]["imageList"][2]["distributePath"] + json_data["article"]["imageList"][2]["imageFileName"]).read()
		
			picture_number = 1
		else:
			picture_number = 0
			picture = 0
	except:
		picture_number = 0
		picture = 0
			
	if len(headline) == 0:
		print "Headline is 0."
		print url
		return 0
	elif len(article) == 0:
		print "Article is 0."
		print url
		return 0
	else:
		return [u32(updated), u32(updated), replace(article), replace(headline), picture, 0, 0, picture_number, replace(location), "news24"]
	
def download_reuters(topics_name, topics):
	picture_number = 0
	
	data = collections.OrderedDict()
	
	for rss_category in topics.items():
		numbers = 0
		
		print "Downloading %s..." % topics_name[rss_category[0]]
		
		print "\n"
		
		for rss in rss_category[1]:
			numbers_category = 0
			
			rss_feed = feedparser.parse(urllib2.urlopen("http://feeds.reuters.com/reuters/%s.rss" % rss).read())
			
			for items in rss_feed.entries:
				updated = parser.parse(items.updated)
				updated = updated.astimezone(tz.tzutc())
				
				updated = (int(time.mktime(updated.timetuple()) - 946684800) / 60)
				
				time_current = (int(time.mktime(datetime.utcnow().timetuple())) - 946684800) / 60
				
				if updated >= time_current - 60:
					numbers += 1
						
					print "Downloading News Article %s..." % (str(numbers))
					
					parsedata = parsedata_reuters(items["link"], items["title"], updated, picture_number)
					
					if parsedata > 0:
						picture_number += parsedata[7]
						data[rss_category[0] + str(numbers)] = parsedata
						
		print "\n"
	
	return data
	
def parsedata_reuters(url, title, updated, picture_number):
	utc = pytz.utc
	
	data1 = Article(url, language="en")
	data1.download()
	data1.parse()
	html = data1.html
	soup = BeautifulSoup(html, "lxml")
	
	soup2 = BeautifulSoup(html, "lxml")
	
	for s in soup2("div", {"class": "module-meta group"}):
		s.extract()
	
	data2 = Article(url, language="en")
	data2.set_html(str(soup2))
	data2.parse()
	
	headline = title.encode("utf-16be") # Parse the headline.
	
	try:
		location = soup.find("span", {"class": "articleLocation"}).contents[0]
		
		if "/" in location:
			location = location.split("/", 1)[0]
	except:
		location = 0
	
	try:
		article = (data2.text + "\n" + "\n" + soup.find("span", {"class": "author"}).get_text()).encode("utf-16be")
	except:
		article = data2.text.encode("utf-16be") # Parse the article.
		
	try:
		if picture_number <= 5:
			"""Parse the pictures."""
		
			picture = urllib2.urlopen(data1.top_image + "&w=200").read()
		
			picture_number = 1
		
			"""Parse the picture credits."""
	
			credits = soup.find("span", {"class": "module-credit"}).get_text().strip().encode("utf-16be")
			
			"""Parse the picture captions."""
	
			caption = soup.find("div", {"class": "module-caption"}).contents[0].strip().encode("utf-16be")
		else:
			picture_number = 0
			picture = 0
			credits = 0
			caption = 0
	except:
		picture_number = 0
		picture = 0
		credits = 0
		caption = 0
			
	if len(headline) == 0:
		print "Headline is 0."
		print url
		return 0
	elif len(article) == 0:
		print "Article is 0."
		print url
		return 0
	else:
		return [u32(updated), u32(updated), replace(article), replace(headline), picture, replace(credits), replace(caption), picture_number, replace(location), "reuters"]
	
def download_anp(topics_name, topics):
	picture_number = 0
	
	data = collections.OrderedDict()
	
	for rss_category in topics.items():
		numbers = 0
		
		print "Downloading %s..." % topics_name[rss_category[0]]
		
		print "\n"
		
		for rss in rss_category[1]:
			numbers_category = 0
			
			rss_feed = feedparser.parse(urllib2.urlopen("http://nu.nl/rss/%s" % rss).read())
			
			for items in rss_feed.entries:
				updated = parser.parse(items.updated)
				try:
					updated = updated.astimezone(tz.tzutc())
				
					updated = (int(time.mktime(updated.timetuple()) - 946684800) / 60)
				
					time_current = (int(time.mktime(datetime.utcnow().timetuple())) - 946684800) / 60
				
					if updated >= time_current - 60:
						if items.author == "NU.nl" or "ANP":
							numbers += 1
						
							print "Downloading News Article %s..." % (str(numbers))
							
							if items.author == "NU.nl/Reuters" or "NU.nl/Reuters/ANP" or "NU.nl/ANP/Reuters" or "NU.nl/ANP":
								parsedata = parsedata_anp(items["link"], items["title"], "NU.nl", updated, picture_number)
							else:
								parsedata = parsedata_anp(items["link"], items["title"], items.author, updated, picture_number)
						
							if parsedata > 0:
								picture_number += parsedata[7]
								data[rss_category[0] + str(numbers)] = parsedata
				except:
					print "Failed."
		
		print "\n"
	
	return data
						
def parsedata_anp(url, title, source, updated, picture_number):
	data1 = Article(url, language="nl")
	data1.download()
	data1.parse()
	html = data1.html
	soup = BeautifulSoup(html, "lxml")
	
	headline = title.encode("utf-16be") # Parse the headline.
	
	try:
		article = (soup.find("div", {"class": "item-excerpt"}).contents[0].replace("        ", "") + "\n" + data1.text).encode("utf-16be") # Parse the article.
	except:
		article = data1.text.encode("utf-16be") # Parse the article.
	
	try:
		if picture_number <= 5:
			"""Parse the pictures."""
			
			with tempfile.NamedTemporaryFile(dir=None, delete=True, prefix="jpg") as tmpfile:
				with open(tmpfile.name, "w+") as dest_file:
					picture = urllib2.urlopen(data1.top_image).read()
					dest_file.write(picture)

				with Image.open(tmpfile.name) as picture:
					picture = resizeimage.resize_width(picture, 200)
					picture.save(tmpfile.name, picture.format)

				with open(tmpfile.name, "rb") as source_file:
					picture = source_file.read()
			
			picture_number = 1
			
			"""Parse the caption."""
			
			credits = soup.find("span", {"class": "photographer"}).contents[0].encode("utf-16be")
		else:
			picture_number = 0
			picture = 0
			credits = 0
	except:
		picture_number = 0
		picture = 0
		credits = 0
	
	location = 0
		
	for tag in soup.find("meta", {"name": "keywords"})["content"].split(","):
		if tag in dutch_locations:
			location = tag
			break
			
	if len(headline) == 0:
		print "Headline is 0."
		print url
		return 0
	elif len(article) == 0:
		print "Article is 0."
		print url
		return 0
	else:
		return [u32(updated), u32(updated), replace(article), replace(headline), picture, replace(credits), 0, picture_number, replace(location), source]
	
def download_ansa(topics_name, topics):
	picture_number = 0
	
	data = collections.OrderedDict()
	
	for rss_category in topics.items():
		numbers = 0
		
		print "Downloading %s..." % topics_name[rss_category[0]]
		
		print "\n"
		
		for rss in rss_category[1]:
			numbers_category = 0
			
			if rss_category[0] == "italy":
				rss_feed = feedparser.parse(urllib2.urlopen("http://ansa.it/%s/notizie/%s_rss.xml" % (rss, rss)).read())
			else:
				rss_feed = feedparser.parse(urllib2.urlopen("http://ansa.it/sito/notizie/%s/%s_rss.xml" % (rss, rss)).read())
			
			for items in rss_feed.entries:
				try:
					updated = parser.parse(items.updated)
					updated = updated.astimezone(tz.tzutc())
					
					updated = (int(time.mktime(updated.timetuple()) - 946684800) / 60)
				
					time_current = (int(time.mktime(datetime.utcnow().timetuple())) - 946684800) / 60
					
					if updated >= time_current - 60:
						numbers_category += 1
					
						if numbers_category > 1:
							if rss_category[0] == "italy":
								pass
						else:
							numbers += 1
						
							print "Downloading News Article %s..." % (str(numbers))
					
							parsedata = parsedata_ansa(items["link"], items["title"], updated, picture_number)
					
							if parsedata > 0:
								picture_number += parsedata[7]
								data[rss_category[0] + str(numbers)] = parsedata
				except:
					print "Failed."

	return data

def parsedata_ansa(url, title, updated, picture_number):
	data1 = Article(url, language="it")
	data1.download()
	data1.parse()
	html = data1.html
	soup = BeautifulSoup(html, "lxml")
	
	headline = title.encode("utf-16be") # Parse the headline.
	article = data1.text.encode("utf-16be") # Parse the article.
	
	try:
		if picture_number <= 5:
			"""Parse the pictures."""

			with tempfile.NamedTemporaryFile(dir=None, delete=True, prefix="jpg") as tmpfile:
				with open(tmpfile.name, "w+") as dest_file:
					picture = urllib2.urlopen(data1.top_image).read()
					dest_file.write(picture)

				with Image.open(tmpfile.name) as picture:
					picture = resizeimage.resize_width(picture, 200)
					picture.save(tmpfile.name, picture.format)

				with open(tmpfile.name, "rb") as source_file:
					picture = source_file.read()
			
			picture_number = 1
		
			"""Parse the picture credits."""
			
			credits = soup.find("div", {"class": "news-caption hidden-phone"}).find("em").contents[0].encode("utf-16be")
		else:
			picture_number = 0
			picture = 0
			credits = 0
	except:
		picture_number = 0
		picture = 0
		credits = 0
		
	try:
		location = soup.find("span", {"itemprop": "dateline"}, {"class": "location"}).contents[0]
	except:
		location = 0
			
	if len(headline) == 0:
		print "Headline is 0."
		print url
		return 0
	elif len(article) == 0:
		print "Article is 0."
		print url
		return 0
	else:
		return [u32(updated), u32(updated), replace(article), replace(headline), picture, replace(credits), 0, picture_number, replace(location), "ansa"]
	
def download_lobs(topics_name):
	picture_number = 0
	
	data = collections.OrderedDict()
	
	numbers = 0
		
	print "Downloading News..."
		
	print "\n"
		
	rss_feed = feedparser.parse(urllib2.urlopen("http://tempsreel.nouvelobs.com/depeche/rss.xml").read())
			
	for items in rss_feed.entries:
		category = lobs_categories[items["tags"][0]["term"].encode("utf-8")]
		
		updated = parser.parse(items.updated)
		updated = updated.astimezone(tz.tzutc())
		
		updated = (int(time.mktime(updated.timetuple()) - 946684800) / 60)
				
		time_current = (int(time.mktime(datetime.utcnow().timetuple())) - 946684800) / 60
				
		if updated >= time_current - 60:
			numbers += 1
					
			print "Downloading News Article %s..." % (str(numbers))
					
			parsedata = parsedata_lobs(items["link"], items["title"], updated, picture_number)
					
			if parsedata > 0:
				picture_number += parsedata[7]
				data[category + str(numbers)] = parsedata
	
	return data
						
def parsedata_lobs(url, title, updated, picture_number):
	data1 = Article(url, language="fr")
	data1.download()
	data1.parse()
	html = data1.html
	soup = BeautifulSoup(html, "lxml")
	
	headline = title.encode("utf-16be") # Parse the headline.
	article = data1.text.encode("utf-16be") # Parse the article.
	
	try:
		if picture_number <= 5:
			if data1.top_image != "http://referentiel.nouvelobs.com/logos/og/logo-nobstr.jpg":
				"""Parse the pictures."""

				with tempfile.NamedTemporaryFile(dir=None, delete=True, prefix="jpg") as tmpfile:
					with open(tmpfile.name, "w+") as dest_file:
						picture = urllib2.urlopen(data1.top_image).read()
						dest_file.write(picture)

					with Image.open(tmpfile.name) as picture:
						picture = resizeimage.resize_width(picture, 200)
						picture.save(tmpfile.name, picture.format)

					with open(tmpfile.name, "rb") as source_file:
						picture = source_file.read()
			
				picture_number = 1
		
				"""Parse the picture captions."""
		
				try:
					caption = soup.find("figcaption", {"class": "obs-legend"}).contents[0].encode("utf-16be")
				except:
					caption = 0
			else:
				picture_number = 0
				picture = 0
				caption = 0
		else:
			picture_number = 0
			picture = 0
			caption = 0
	except:
		picture_number = 0
		picture = 0
		caption = 0
	
	if " (AFP)" in article.decode("utf-16be"):
		location = article.decode("utf-16be").split(" (AFP)", 1)[0]
	else:
		location = 0
			
	if len(headline) == 0:
		print "Headline is 0."
		print url
		return 0
	elif len(article) == 0:
		print "Article is 0."
		print url
		return 0
	else:
		return [u32(updated), u32(updated), replace(article), replace(headline), picture, 0, replace(caption), picture_number, replace(location), "AFP"]
		
def download_zeit(topics_name):
	picture_number = 0
	
	data = collections.OrderedDict()
	
	numbers = 0
		
	print "Downloading News..."
		
	print "\n"
	
	soup = BeautifulSoup(urllib2.urlopen("http://www.zeit.de/news/index").read(), "lxml")
			
	for items in soup.findAll("article", {"class": "newsteaser"}):
		updated = parser.parse(items.find("time", {"class": "newsteaser__time"}).contents[0].strip() + " +0100")
		updated = updated.astimezone(tz.tzutc())
		
		updated = (int(time.mktime(updated.timetuple()) - 946684800) / 60)
		
		time_current = (int(time.mktime(datetime.utcnow().timetuple())) - 946684800) / 60
		
		link = items.find("a", {"class": "newsteaser__combined-link"})["href"]
		source = items.find("span", {"class": "newsteaser__product"}).contents[0]
					
		if updated >= time_current - 60:
			numbers += 1
			
			print "Downloading News Article %s..." % (str(numbers))
				
			parsedata = parsedata_zeit(link, updated, source, picture_number)
					
			if parsedata > 0:
				picture_number += parsedata[7]
				data[parsedata[10] + str(numbers)] = parsedata
				
	return data
	
def parsedata_zeit(url, updated, source, picture_number):
	data1 = Article(url, language="de")
	data1.download()
	data1.parse()
	html = data1.html
	soup = BeautifulSoup(html, "lxml")
	
	headline = data1.title.encode("utf-16be") # Parse the headline.
	article = data1.text.encode("utf-16be") # Parse the article.
	
	headline_category = headline.decode("utf-16be").split(": ", 1)[0]
	category = "general"
	
	if headline_category in zeit_categories:
		category = zeit_categories[headline_category]
			
	if headline_category in zeit_sports_categories:
		category = "sports"
	
	try:
		if picture_number <= 3:
			"""Parse the pictures."""
					
			with tempfile.NamedTemporaryFile(dir=None, delete=True, prefix="jpg") as tmpfile:
				with open(tmpfile.name, "w+") as dest_file:
					picture = urllib2.urlopen(data1.top_image).read()
					dest_file.write(picture)

				with Image.open(tmpfile.name) as picture:
					picture = resizeimage.resize_width(picture, 200)
					picture.save(tmpfile.name, picture.format)

				with open(tmpfile.name, "rb") as source_file:
					picture = source_file.read()
				
			picture_number = 1
		
			"""Parse the picture captions."""
		
			try:
				caption = soup.find("span", {"class": "figure__text"}).contents[0].encode("utf-16be")
			except:
				caption = 0
				
			"""Parse the picture credits."""
			
			try:
				credits = soup.find("span", {"class": "figure__copyright"}).get_text().encode("utf-16be")
			except:
				credits = 0
		else:
			picture_number = 0
			picture = 0
			caption = 0
			credits = 0
	except:
		picture_number = 0
		picture = 0
		caption = 0
		credits = 0
	
	if source == "ZEIT ONLINE":
		try:
			credits = soup.find("div", {"class": "byline"}).get_text().strip().encode("utf-16be")
				
			if ", " in credits.decode("utf-16be"):
				location = credits.decode("utf-16be").split(", ", 1)[1]
			else:
				location = 0
				
			article += "\n" + "\n" + credits
		except:
			location = 0
			
	elif source == "SID":
		if " (SID)" in article.decode("utf-16be"):
			location = article.decode("utf-16be").split(" (SID)", 1)[0]
		else:
			location = 0
		category = "sports"
			
	elif source == "dpa":
		if " (dpa)" in article.decode("utf-16be"):
			location = article.decode("utf-16be").split(" (dpa)", 1)[0]
		else:
			location = 0
			
	elif source == "AFP":
		if " (AFP)" in article.decode("utf-16be"):
			location = article.decode("utf-16be").split(" (AFP)", 1)[0]
		else:
			location = 0
	
	else:
		location = 0
			
	if len(headline) == 0:
		print "Headline is 0."
		print url
		return 0
	elif len(article) == 0:
		print "Article is 0."
		print url
		return 0
	else:
		return [u32(updated), u32(updated), replace(article), replace(headline), picture, 0, replace(caption), picture_number, replace(location), source, category]

def download_ap(topics_name, topics, language):
	picture_number = 0
	
	data = collections.OrderedDict()
	
	for rss_category in topics.items():
		numbers = 0
		
		print "Downloading %s..." % topics_name[rss_category[0]]
		
		print "\n"
		
		for rss in rss_category[1]:
			rss_feed = feedparser.parse(urllib2.urlopen("http://hosted.ap.org/lineups/%s-rss_2.0.xml?SITE=AP&SECTION=HOME" % rss).read())
	
			for items in rss_feed.entries:
				format = "%Y-%m-%dT%H:%M:%SZ"
	
				try:
					updated_utc = datetime.strptime(items["date"], format)
				
					updated_utc = updated_utc.strftime(format)
				
					updated = (int(time.mktime(datetime.strptime(updated_utc, format).timetuple()) - 946684800) / 60)
				
					time_current = (int(time.mktime(datetime.utcnow().timetuple())) - 946684800) / 60

					if updated >= time_current - 60:
						numbers += 1
					
						print "Downloading News Article %s..." % (str(numbers))
				
						parsedata = parsedata_ap(items["link"], items["title"], updated_utc, updated, format, picture_number, language)	
						
						if parsedata > 0:
							picture_number += parsedata[7]
							data[rss_category[0] + str(numbers)] = parsedata
				except:
					print "Failed."
		
		print "\n"
		
	return data
		
def parsedata_ap(url, title, updated_utc, updated, format, picture_number, language):
	utc = pytz.utc
	
	data1 = Article(url, language=language)
	data1.download()
	data1.parse()
	html = data1.html
	soup = BeautifulSoup(html, "lxml")
	
	headline = title.encode("utf-16be") # Parse the headline.
	
	try:
		article = (data1.text + "\n" + "\n" + "By " + soup.find("span", {"class": "fn"}).contents[0] + ", " + soup.find("span", {"class": "bylinetitle"}).contents[0]).encode("utf-16be") # Parse the article.
	except:
		article = data1.text.encode("utf-16be") # Parse the article.
		
	if "ap-smallphoto-img" in html:
		if picture_number <= 5:
			"""Parse the pictures."""
		
			picture = urllib2.urlopen("http://hosted.ap.org/" + soup.find("img", {"class": "ap-smallphoto-img"})["src"][:-10] + "-small.jpg").read()
		
			picture_number = 1
		
			"""Parse the picture credits."""
	
			credits = soup.find("span", {"class": "apCaption"}).contents[0].encode("utf-16be")
		
			"""Parse the picture captions."""
	
			url_captions = urllib2.urlopen("http://hosted.ap.org/" + soup.find("a", {"class": "ap-smallphoto-a"})['href']).read()
			soup = BeautifulSoup(url_captions, "lxml")
			caption = soup.find("font", {"class": "photo"}).contents[0].encode("utf-16be")
		else:
			picture_number = 0
			picture = 0
			credits = 0
			caption = 0
	else:
		picture_number = 0
		picture = 0
		credits = 0
		caption = 0
	
	if " (AP)" in article.decode("utf-16be"):
		location = article.decode("utf-16be").split(" (AP)", 1)[0]
	else:
		location = 0
			
	if len(headline) == 0:
		print "Headline is 0."
		print url
		return 0
	elif len(article) == 0:
		print "Article is 0."
		print url
		return 0
	else:
		return [u32(updated), u32(updated), replace(article), replace(headline), picture, replace(credits), replace(caption), picture_number, replace(location), "ap"]