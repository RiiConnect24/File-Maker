#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections

"""List of countries the EVC uses."""

countries = collections.OrderedDict()

countries["Japan"] = ["日本", "Japan", "Japan", "Japon", "Japón", "Giappone", "Japan"]
countries["Argentina"] = ["アルゼンチン", "Argentina", "Argentinien", "Argentine", "Argentina", "Argentina", "Argentinië"]
countries["Brazil"] = ["ブラジル", "Brazil", "Brasilien", "Brésil", "Brasil", "Brasile", "Brazilië"]
countries["Canada"] = ["カナダ", "Canada", "Kanada", "Canada", "Canadá", "Canada", "Canada"]
countries["Chile"] = ["チリ", "Chile", "Chile", "Chili", "Chile", "Cile", "Chili"]
countries["Colombia"] = ["コロンビア", "Colombia", "Kolumbien", "Colombie", "Colombia", "Colombia", "Colombia"]
countries["Costa Rica"] = ["コスタリカ", "Costa Rica", "Costa Rica", "Costa Rica", "Costa Rica", "Costa Rica", "Costa Rica"]
countries["Ecuador"] = ["エクアドル", "Ecuador", "Ecuador", "Equateur", "Ecuador", "Ecuador", "Ecuador"]
countries["Guatemala"] = ["グアテマラ", "Guatemala", "Guatemala", "Guatemala", "Guatemala", "Guatemala", "Guatemala"]
countries["Mexico"] = ["メキシコ", "Mexico", "Mexiko", "Mexique", "México", "Messico", "Mexico"]
countries["Panama"] = ["パナマ", "Panama", "Panama", "Panama", "Panamá", "Panamá", "Panama"]
countries["Peru"] = ["ペルー", "Peru", "Peru", "Pérou", "Perú", "Perù", "Peru"]
countries["United States"] = ["アメリカ", "United States", "Vereinigte Staaten", "Etats-Unis d’Amérique", "Estados Unidos de América", "Stati Uniti d'America", "Verenigde Staten"]
countries["Venezuela"] = ["ベネズエラ", "Venezuela", "Venezuela", "Venezuela", "Venezuela", "Venezuela", "Venezuela"]
countries["Australia"] = ["オーストラリア", "Australia", "Australien", "Australie", "Australia", "Australia", "Australië"]
countries["Austria"] = ["オーストリア", "Austria", "Österreich", "Autriche", "Austria", "Austria", "Oostenrijk"]
countries["Belgium"] = ["ベルギー", "Belgium", "Belgien", "Belgique", "Bélgica", "Belgio", "België"]
countries["Denmark"] = ["デンマーク", "Denmark", "Dänemark", "Danemark", "Dinamarca", "Danimarca", "Denemarken"]
countries["Finland"] = ["フィンランド", "Finland", "Finnland", "Finlande", "Finlandia", "Finlandia", "Finland"]
countries["France"] = ["フランス", "France", "Frankreich", "France", "Francia", "Francia", "Frankrijk"]
countries["Germany"] = ["ドイツ", "Germany", "Deutschland", "Allemagne", "Alemania", "Germania", "Duitsland"]
countries["Greece"] = ["ギリシャ", "Greece", "Griechenland", "Grèce", "Grecia", "Grecia", "Griekenland"]
countries["Ireland"] = ["アイルランド", "Ireland", "Irland", "Irlande", "Irlanda", "Irlanda", "Ierland"]
countries["Italy"] = ["イタリア", "Italy", "Italien", "Italie", "Italia", "Italia", "Italië"]
countries["Luxembourg"] = ["ルクセンブルク", "Luxembourg", "Luxemburg", "Luxembourg", "Luxemburgo", "Lussemburgo", "Luxemburg"]
countries["Netherlands"] = ["オランダ", "Netherlands", "Niederlande", "Pays-Bas", "Países Bajos", "Paesi Bassi", "Nederland"]
countries["New Zealand"] = ["ニュージーランド", "New Zealand", "Neuseeland", "Nouvelle-Zélande", "Nueva Zelanda", "Nuova Zelanda", "Nieuw-Zeeland"]
countries["Norway"] = ["ノルウェー", "Norway", "Norwegen", "Norvège", "Noruega", "Norvegia", "
countries["Poland"] = ["ポーランド", "Poland", "Polen", "Pologne", "Polonia", "Polonia", "Polen"]
countries["Portugal"] = ["ポルトガル", "Portugal", "Portugal", "Portugal", "Portugal", "Portogallo", "Portugal"]
countries["Spain"] = ["スペイン", "Spain", "Spanien", "Espagne", "España", "Spagna", "Spanje"]
countries["Sweden"] = ["スウェーデン", "Sweden", "Schweden", "Suède", "Suecia", "Svezia", "Zweden"]
countries["Switzerland"] = ["スイス", "Switzerland", "Schweiz", "Suisse", "Suiza", "Svizzera", "Zwitserland"]
countries["United Kingdom"] = ["イギリス", "United Kingdom", "Großbritannien", "Royaume-Uni", "Reino Unido", "Regno Unito", "Verenigd Koninkrijk"]

"""List of country codes."""

country_codes = [1, 10, 16, 18, 20, 21, 22, 25, 30, 36, 40, 42, 49, 52, 65, 66, 67, 74, 76, 77, 78, 79, 82, 83, 88, 94, 95, 96, 98, 105, 107, 108, 110]

"""These lists tell the script how many entries are used for the position tables."""
"""(if it's more than 1, that must mean the region is split up into multiple parts)"""

position_table = collections.OrderedDict()

position_table[1] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
position_table[16] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1]
position_table[18] = [1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 4, 3]
position_table[21] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
position_table[36] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
position_table[40] = [2, 0, 1, 1, 1, 0, 0, 1, 1, 2]
position_table[49] = [1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
position_table[77] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
position_table[78] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
position_table[83] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
position_table[94] = [1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1]
position_table[105] = [1, 1, 1, 1, 3, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
position_table[110] = [1, 2, 2, 1, 1]

"""Data for the position table. Nintendo mixed these up to match the order votes were submitted in (I think)."""
"""That would be more effort to re-arrange the data in the position table, so I just made it read the values only if there is any votes for the region."""

position_data = collections.OrderedDict()

position_data[1] = "A2A4C828AF52B964B478AA64AA73AA87AD9BA5969B96A09EADA5A2A987947F8E78A096A5919B9B8782A591AF82AF7AB978AA6EAA6DB364AF73B96BC05AA546AA55AF4BB437B95FC358BA46C350C82DBE26C623CD2DD237C837D728E14849395A"
position_data[16] = "A4862664E8648E1E4141C873D746CD9E7DA0B4467878B99B8746E35385BEC855C2AEE94D82DC4B6996C8A5AAE3699687E15AA064"
position_data[18] = "87BE3CA009981EA064AAC8C3F0A8E1AAC89BD7C3D4BDAAAA50AF1E695C405649505A3C787841647D8E89"
position_data[21] = "7C7D78739BC8695AAA5A71247D468D6B6E6E579887326946969BC896649B9119782D8C8C4BA58D4864B2677B647328194E19875A733E6E825A87"
position_data[36] = "37508FB0786914465A5A69A54B7D98B69B9E8AAF9687E6A07DAF82918C787DA2649B91B476988BA1EBAA5F7D8CBE91A52B6F67B2A5C8C8C899AE738CC8B9D7B4"
position_data[40] = "A05DAF7B1E7373737D5A739BAA5250823AA0"
position_data[49] = "D25E78D252E748E1AA87917D3C7819645A64E04EDC5FC8A0BE872EE628DF18D98C5A3C46A064AA5F7869B46C9191E249DC64EB37A53FAF5087419169A08C5037D2737337735AE440DC55557D2D5AD746E254B95D7D7D2341CD55E84CC87D714BAA7878914164CD69DC3F272F9B46C3645550F0BE"
position_data[77] = "8246DC465AB49196463CA06E28467864AA46E6E6C86E6E3296C87896C84678C88C14505A8C2D508CC8C8BE96"
position_data[78] = "B95A64966EDC9BC8C86E5F417837AF2D7350467841AA3CBEBE919664781E8C8C"
position_data[83] = "7D822328283C324B463264196432821E64466464786E82649682A08CA0A0BE96B9AABEBE96E63CB4"
position_data[94] = "645AC8418C6496288214B40AAA82D223BE08A0C882B4B46E32C8788232C8"
position_data[105] = "6E5F64E6A03C3C1EF852E65FCA739AD9A7E6B4E1C8E6EBE1641E7878503CC832AA73468C1E32A0968C28781E7832"
position_data[110] = "B4B4738732E67846D71E82B4507D"

"""Number of regions for each country."""

region_number = collections.OrderedDict()

region_number[1] = 47
region_number[10] = 24
region_number[16] = 27
region_number[18] = 13
region_number[20] = 13
region_number[21] = 33
region_number[22] = 7
region_number[25] = 22
region_number[30] = 22
region_number[36] = 32
region_number[40] = 10
region_number[42] = 25
region_number[49] = 52
region_number[52] = 25
region_number[65] = 8
region_number[66] = 9
region_number[67] = 3
region_number[74] = 17
region_number[76] = 6
region_number[77] = 26
region_number[78] = 16
region_number[79] = 13
region_number[82] = 8
region_number[83] = 20
region_number[88] = 3
region_number[94] = 12
region_number[95] = 13
region_number[96] = 5
# region_number[97] = 16
region_number[98] = 7
region_number[105] = 17
region_number[107] = 21
region_number[108] = 23
region_number[110] = 5

language_num = collections.OrderedDict()

language_num[0] = "Japanese"
language_num[1] = "English"
language_num[2] = "German"
language_num[3] = "French"
language_num[4] = "Spanish"
language_num[5] = "Italian"
language_num[6] = "Dutch"
language_num[7] = "Portuguese"
language_num[8] = "French Canada"

"""Languages each country uses. The numbers correspond to the ones in the dictionary above."""

country_language = collections.OrderedDict()

country_language[1] = [0]
country_language[10] = [1, 4, 8]
country_language[16] = [1, 4, 7, 8]
country_language[18] = [1, 4, 8]
country_language[20] = [1, 4, 8]
country_language[21] = [1, 4, 8]
country_language[22] = [1, 4, 8]
country_language[25] = [1, 4, 8]
country_language[30] = [1, 4, 8]
country_language[36] = [1, 4, 8]
country_language[40] = [1, 4, 8]
country_language[42] = [1, 4, 8]
country_language[49] = [1, 4, 8]
country_language[52] = [1, 4, 8]
country_language[65] = [1]
country_language[66] = [2, 3, 5, 6]
country_language[67] = [2, 3, 5, 6]
country_language[74] = [1]
country_language[76] = [1]
country_language[77] = [3]
country_language[78] = [2]
country_language[79] = [1, 4, 7]
country_language[82] = [1]
country_language[83] = [5]
country_language[88] = [2, 3, 5, 6]
country_language[94] = [6]
country_language[95] = [1]
country_language[96] = [1]
country_language[98] = [1, 4, 7]
country_language[105] = [4]
country_language[107] = [1]
country_language[108] = [2, 3, 5, 6]
country_language[110] = [1]

category_text = collections.OrderedDict()

category_text[0] = "Thoughts"
category_text[1] = "Personality"
category_text[2] = "Surroundings"
category_text[3] = "Experience"
category_text[4] = "Knowledge"

"""Poll categories. The keys correspond to the ones above."""

categories = collections.OrderedDict()

categories[0] = 3
categories[1] = 5
categories[2] = 7
categories[3] = 9
categories[4] = 10
