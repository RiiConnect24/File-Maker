#!/usr/bin/python
# -*- coding: utf-8 -*-

"""These were taken from Nintendo's servers, these are for a region select screen."""
"""In rare cases, the region data might be outdated because Nintendo never actively updated this list."""

regioninfo_001 = {
	1: [0, 0, ["日本", "Japan", "Japan", "Japon", "Japón", "Giappone", "Japan"]],
	2: [35.687, 139.765, ["東京都", "Tokyo", "Tokio", "Tokyo", "Tokio", "Tokyo", "Tokio"]],
	3: [43.058, 141.332, ["北海道", "Hokkaido", "Hokkaido", "Hokkaido", "Hokaido", "Hokkaido", "Hokkaido"]],
	4: [40.818, 140.772, ["青森県", "Aomori", "Aomori", "Aomori", "Aomori", "Aomori", "Aomori"]],
	5: [39.695, 141.168, ["岩手県", "Iwate", "Iwate", "Iwate", "Iwate", "Iwate", "Iwate"]],
	6: [38.258, 140.9, ["宮城県", "Miyagi", "Miyagi", "Miyagi", "Miyagi", "Miyagi", "Miyagi"]],
	7: [39.715, 140.103, ["秋田県", "Akita", "Akita", "Akita", "Akita", "Akita", "Akita"]],
	8: [38.253, 140.348, ["山形県", "Yamagata", "Yamagata", "Yamagata", "Yamagata", "Yamagata", "Yamagata"]],
	9: [37.757, 140.475, ["福島県", "Fukushima", "Fukushima", "Fukushima", "Fukushima", "Fukushima", "Fukushima"]],
	10: [36.378, 140.472, ["茨城県", "Ibaraki", "Ibaraki", "Ibaraki", "Ibaraki", "Ibaraki", "Ibaraki"]],
	11: [36.547, 139.872, ["栃木県", "Tochigi", "Tochigi", "Tochigi", "Tochigi", "Tochigi", "Tochigi"]],
	12: [36.402, 139.065, ["群馬県", "Gunma", "Gunma", "Gunma", "Gunma", "Gunma", "Gunma"]],
	13: [35.873, 139.59, ["埼玉県", "Saitama", "Saitama", "Saitama", "Saitama", "Saitama", "Saitama"]],
	14: [35.6, 140.107, ["千葉県", "Chiba", "Chiba", "Chiba", "Chiba", "Chiba", "Chiba"]],
	15: [35.437, 139.657, ["神奈川県", "Kanagawa", "Kanagawa", "Kanagawa", "Kanagawa", "Kanagawa", "Kanagawa"]],
	16: [36.707, 137.205, ["富山県", "Toyama", "Toyama", "Toyama", "Toyama", "Toyama", "Toyama"]],
	17: [36.587, 136.637, ["石川県", "Ishikawa", "Ishikawa", "Ishikawa", "Ishikawa", "Ishikawa", "Ishikawa"]],
	18: [36.053, 136.227, ["福井県", "Fukui", "Fukui", "Fukui", "Fukui", "Fukui", "Fukui"]],
	19: [35.665, 138.557, ["山梨県", "Yamanashi", "Yamanashi", "Yamanashi", "Yamanashi", "Yamanashi", "Yamanashi"]],
	20: [36.66, 138.195, ["長野県", "Nagano", "Nagano", "Nagano", "Nagano", "Nagano", "Nagano"]],
	21: [37.91, 139.052, ["新潟県", "Niigata", "Niigata", "Niigata", "Niigata", "Niigata", "Niigata"]],
	22: [35.397, 136.765, ["岐阜県", "Gifu", "Gifu", "Gifu", "Gifu", "Gifu", "Gifu"]],
	23: [34.973, 138.407, ["静岡県", "Shizuoka", "Shizuoka", "Shizuoka", "Shizuoka", "Shizuoka", "Shizuoka"]],
	24: [35.167, 136.968, ["愛知県", "Aichi", "Aichi", "Aichi", "Aichi", "Aichi", "Aichi"]],
	25: [34.73, 136.523, ["三重県", "Mie", "Mie", "Mie", "Mie", "Mie", "Mie"]],
	26: [34.988, 135.915, ["滋賀県", "Shiga", "Shiga", "Shiga", "Shiga", "Shiga", "Shiga"]],
	27: [35.012, 135.735, ["京都府", "Kyoto", "Kyoto", "Kyoto", "Kioto", "Kyoto", "Kyoto"]],
	28: [34.678, 135.522, ["大阪府", "Osaka", "Osaka", "Osaka", "Osaka", "Osaka", "Osaka"]],
	29: [34.693, 135.215, ["兵庫県", "Hyogo", "Hyogo", "Hyogo", "Hiogo", "Hyogo", "Hyogo"]],
	30: [34.692, 135.832, ["奈良県", "Nara", "Nara", "Nara", "Nara", "Nara", "Nara"]],
	31: [34.227, 135.167, ["和歌山県", "Wakayama", "Wakayama", "Wakayama", "Wakayama", "Wakayama", "Wakayama"]],
	32: [35.485, 134.24, ["鳥取県", "Tottori", "Tottori", "Tottori", "Totori", "Tottori", "Tottori"]],
	33: [35.455, 133.068, ["島根県", "Shimane", "Shimane", "Shimane", "Shimane", "Shimane", "Shimane"]],
	34: [34.658, 133.918, ["岡山県", "Okayama", "Okayama", "Okayama", "Okayama", "Okayama", "Okayama"]],
	35: [34.395, 132.465, ["広島県", "Hiroshima", "Hiroshima", "Hiroshima", "Hiroshima", "Hiroshima", "Hiroshima"]],
	36: [34.157, 131.458, ["山口県", "Yamaguchi", "Yamaguchi", "Yamaguchi", "Yamaguchi", "Yamaguchi", "Yamaguchi"]],
	37: [34.065, 134.577, ["徳島県", "Tokushima", "Tokushima", "Tokushima", "Tokushima", "Tokushima", "Tokushima"]],
	38: [34.313, 134.057, ["香川県", "Kagawa", "Kagawa", "Kagawa", "Kagawa", "Kagawa", "Kagawa"]],
	39: [33.84, 132.78, ["愛媛県", "Ehime", "Ehime", "Ehime", "Ehime", "Ehime", "Ehime"]],
	40: [33.565, 133.552, ["高知県", "Kochi", "Kochi", "Kochi", "Kochi", "Kochi", "Kochi"]],
	41: [33.58, 130.377, ["福岡県", "Fukuoka", "Fukuoka", "Fukuoka", "Fukuoka", "Fukuoka", "Fukuoka"]],
	42: [33.242, 130.305, ["佐賀県", "Saga", "Saga", "Saga", "Saga", "Saga", "Saga"]],
	43: [32.732, 129.87, ["長崎県", "Nagasaki", "Nagasaki", "Nagasaki", "Nagasaki", "Nagasaki", "Nagasaki"]],
	44: [32.81, 130.71, ["熊本県", "Kumamoto", "Kumamoto", "Kumamoto", "Kumamoto", "Kumamoto", "Kumamoto"]],
	45: [33.232, 131.62, ["大分県", "Oita", "Oita", "Oita", "Oita", "Oita", "Oita"]],
	46: [31.935, 131.417, ["宮崎県", "Miyazaki", "Miyazaki", "Miyazaki", "Miyazaki", "Miyazaki", "Miyazaki"]],
	47: [31.552, 130.552, ["鹿児島県", "Kagoshima", "Kagoshima", "Kagoshima", "Kagoshima", "Kagoshima", "Kagoshima"]],
	48: [26.203, 127.688, ["沖縄県", "Okinawa", "Okinawa", "Okinawa", "Okinawa", "Okinawa", "Okinawa"]]
}

regioninfo_008 = {
	1: [18.2166667, -63.05, ["アンギラ", "Anguilla", "Anguilla", "Anguilla", "Anguila", "Anguilla", "Anguilla"]]
}

regioninfo_009 = {
	1: [0, 0, ["アンティグア・バーブーダ", "Antigua and Barbuda", "Antigua und Barbuda", "Antigua-et-Barbuda", "Antigua y Barbuda", "Antigua e Barbuda", "Antigua en Barbuda"]],
	2: [17.1166667, -61.85, ["セント・ジョン", "Saint John", "Saint John", "Saint-Jean", "Saint John", "Saint John", "Saint John"]],
	3: [17.6333333, -61.8333333, ["バーブーダ島", "Barbuda", "Barbuda", "Barbuda", "Barbuda", "Barbuda", "Barbuda"]],
	4: [17.1333333, -61.8, ["セント・ジョージ", "Saint George", "Saint George", "Saint-Georges", "Saint George", "Saint George", "Saint George"]],
	5: [17.0333333, -61.8833333, ["セント・メアリー", "Saint Mary", "Saint Mary", "Sainte-Marie", "Saint Mary", "Saint Mary", "Saint Mary"]],
	6: [17.0333333, -61.7833333, ["セント・ポール", "Saint Paul", "Saint Paul", "Saint-Paul", "Saint Paul", "Saint Paul", "Saint Paul"]],
	7: [17.0833333, -61.7666667, ["セント・ピーター", "Saint Peter", "Saint Peter", "Saint-Pierre", "Saint Peter", "Saint Peter", "Saint Peter"]],
	8: [17.05, -61.7, ["セント・フィリップ", "Saint Philip", "Saint Philip", "Saint-Philippe", "Saint Philip", "Saint Philip", "Saint Philip"]]
}

regioninfo_010 = {
	1: [0, 0, ["アルゼンチン", "Argentina", "Argentinien", "Argentine", "Argentina", "Argentina", "Argentinië"]],
	2: [-34.5875, -58.6725, ["特別区", "Distrito Federal", "Bundesdistrikt", "District Fédéral", "Distrito Federal", "Distretto Federale", "Federaal District"]],
	3: [-34.9313889, -57.9488889, ["ブエノスアイレス州", "Buenos Aires", "Buenos Aires", "Buenos Aires", "Buenos Aires", "Buenos Aires", "Buenos Aires"]],
	4: [-28.4666667, -65.7833333, ["カタマルカ州", "Catamarca", "Catamarca", "Catamarca", "Catamarca", "Catamarca", "Catamarca"]],
	5: [-27.45, -58.9833333, ["チャコ州", "Chaco", "Chaco", "Chaco", "Chaco", "Chaco", "Chaco"]],
	6: [-43.3, -65.1, ["チュブト州", "Chubut", "Chubut", "Chubut", "Chubut", "Chubut", "Chubut"]],
	7: [-31.4, -64.1833333, ["コルドバ州", "Córdoba", "Córdoba", "Córdoba", "Córdoba", "Córdoba", "Córdoba"]],
	8: [-27.4666667, -58.8333333, ["コリエンテス州", "Corrientes", "Corrientes", "Corrientes", "Corrientes", "Corrientes", "Corrientes"]],
	9: [-31.7333333, -60.5333333, ["エントレ・リオス州", "Entre Ríos", "Entre Ríos", "Entre Ríos", "Entre Ríos", "Entre Ríos", "Entre Ríos"]],
	10: [-26.1833333, -58.1833333, ["フォルモサ州", "Formosa", "Formosa", "Formosa", "Formosa", "Formosa", "Formosa"]],
	11: [-24.1833333, -65.3, ["フフイ州", "Jujuy", "Jujuy", "Jujuy", "Jujuy", "Jujuy", "Jujuy"]],
	12: [-36.6166667, -64.2833333, ["ラ・パンパ州", "La Pampa", "La Pampa", "La Pampa", "La Pampa", "La Pampa", "La Pampa"]],
	13: [-29.4333333, -66.85, ["ラ・リオハ州", "La Rioja", "La Rioja", "La Rioja", "La Rioja", "La Rioja", "La Rioja"]],
	14: [-32.8833333, -68.8166667, ["メンドーサ州", "Mendoza", "Mendoza", "Mendoza", "Mendoza", "Mendoza", "Mendoza"]],
	15: [-27.3833333, -55.8833333, ["ミシオネス州", "Misiones", "Misiones", "Misiones", "Misiones", "Misiones", "Misiones"]],
	16: [-38.95, -68.0666667, ["ネウケン州", "Neuquén", "Neuquén", "Neuquén", "Neuquén", "Neuquén", "Neuquén"]],
	17: [-40.8, -63, ["リオネグロ州", "Río Negro", "Río Negro", "Río Negro", "Río Negro", "Río Negro", "Río Negro"]],
	18: [-24.7833333, -65.4166667, ["サルタ州", "Salta", "Salta", "Salta", "Salta", "Salta", "Salta"]],
	19: [-31.5375, -68.5363889, ["サン・フアン州", "San Juan", "San Juan", "San Juan", "San Juan", "San Juan", "San Juan"]],
	20: [-33.3, -66.35, ["サン・ルイス州", "San Luis", "San Luis", "San Luis", "San Luis", "San Luis", "San Luis"]],
	21: [-51.6333333, -69.2166667, ["サンタ・クルス州", "Santa Cruz", "Santa Cruz", "Santa Cruz", "Santa Cruz", "Santa Cruz", "Santa Cruz"]],
	22: [-31.6333333, -60.7, ["サンタ・フェ州", "Santa Fe", "Santa Fe", "Santa Fe", "Santa Fe", "Santa Fe", "Santa Fe"]],
	23: [-27.7833333, -64.2666667, ["サンティアゴ・デル・エステロ州", "Santiago del Estero", "Santiago del Estero", "Santiago del Estero", "Santiago del Estero", "Santiago del Estero", "Santiago del Estero"]],
	24: [-54.8, -68.3, ["ティエラ・デル・フエゴ州", "Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Feuerland", "Terre de Feu", "Tierra del Fuego, Antártida e Islas del Atlántico Sur", "Terra del Fuoco, Antartide e Isole dell'Atlantico Sud ", "Vuurland, Antarctica en Zuid-Atlantische eilanden"]],
	25: [-26.8166667, -65.2166667, ["トゥクマン州", "Tucumán", "Tucumán", "Tucuman", "Tucumán", "Tucumán", "Tucumán"]]
}

regioninfo_011 = {
	1: [12.5166667, -70.0333333, ["アルバ", "Aruba", "Aruba", "Aruba", "Aruba", "Aruba", "Aruba"]]
}

regioninfo_012 = {
	1: [25.0833333, -77.35, ["バハマ", "Bahamas", "Bahamas", "Bahamas", "Bahamas", "Bahamas", "Bahama's"]]
}

regioninfo_013 = {
	1: [13.1, -59.6166667, ["バルバドス", "Barbados", "Barbados", "Barbade", "Barbados", "Barbados", "Barbados"]]
}

regioninfo_014 = {
	1: [0, 0, ["ベリーズ", "Belize", "Belize", "Belize", "Belice", "Belize", "Belize"]],
	2: [17.25, -88.7666667, ["カヨー州", "Cayo", "Cayo", "Cayo", "Cayo", "Cayo", "Cayo"]],
	3: [17.4833333, -88.1833333, ["ベリーズ州", "Belize", "Belize", "Belize", "Belice", "Belize", "Belize"]],
	4: [18.3833333, -88.3833333, ["コロサル州", "Corozal", "Corozal", "Corozal", "Corozal", "Corozal", "Corozal"]],
	5: [18.0666667, -88.55, ["オレンジウォーク州", "Orange Walk", "Orange Walk", "Orange Walk", "Orange Walk", "Orange Walk", "Orange Walk"]],
	6: [16.9666667, -88.2166667, ["スタンクリーク州", "Stann Creek", "Stann Creek", "Stann Creek", "Stann Creek", "Stann Creek", "Stann Creek"]],
	7: [16.1, -88.8, ["トレド州", "Toledo", "Toledo", "Toledo", "Toledo", "Toledo", "Toledo"]]
}

regioninfo_015 = {
	1: [0, 0, ["ボリビア", "Bolivia", "Bolivien", "Bolivie", "Bolivia", "Bolivia", "Bolivia"]],
	2: [-16.5, -68.15, ["ラパス県", "La Paz", "La Paz", "La Paz", "La Paz", "La Paz", "La Paz"]],
	3: [-19.0430556, -65.2591667, ["チュキサカ県", "Chuquisaca", "Chuquisaca", "Chuquisaca", "Chuquisaca", "Chuquisaca", "Chuquisaca"]],
	4: [-17.3833333, -66.15, ["コチャバンバ県", "Cochabamba", "Cochabamba", "Cochabamba", "Cochabamba", "Cochabamba", "Cochabamba"]],
	5: [-14.8333333, -64.9, ["ベニ県", "El Beni", "Beni", "Beni", "El Beni", "El Beni", "Beni"]],
	6: [-17.9833333, -67.15, ["オルロ県", "Oruro", "Oruro", "Oruro", "Oruro", "Oruro", "Oruro"]],
	7: [-11.0333333, -68.7333333, ["パンド県", "Pando", "Pando", "Pando", "Pando", "Pando", "Pando"]],
	8: [-19.5836111, -65.7530556, ["ポトシ県", "Potosí", "Potosí", "Potosí", "Potosí", "Potosí", "Potosí"]],
	9: [-17.8, -63.1666667, ["サンタ・クルス県", "Santa Cruz", "Santa Cruz", "Santa Cruz", "Santa Cruz", "Santa Cruz", "Santa Cruz"]],
	10: [-21.5166667, -64.75, ["タリハ県", "Tarija", "Tarija", "Tarija", "Tarija", "Tarija", "Tarija"]]
}

regioninfo_016 = {
	1: [0, 0, ["ブラジル", "Brazil", "Brasilien", "Brésil", "Brasil", "Brasile", "Brazilië"]],
	2: [-15.7833333, -47.9166667, ["ディストリト・フェデラル州", "Distrito Federal", "Bundesdistrikt", "District Fédéral", "Distrito Federal", "Distretto Federale", "Federaal District"]],
	3: [-9.9666667, -67.8, ["アクレ州", "Acre", "Acre", "Acre", "Acre", "Acre", "Acre"]],
	4: [-9.6666667, -35.7166667, ["アラゴアス州", "Alagoas", "Alagoas", "Alagoas", "Alagoas", "Alagoas", "Alagoas"]],
	5: [0.0333333, -51.05, ["アマパー州", "Amapá", "Amapá", "Amapá", "Amapá", "Amapá", "Amapá"]],
	6: [-3.1133333, -60.0252778, ["アマゾナス州", "Amazonas", "Amazonas", "Amazonas", "Amazonas", "Amazonas", "Amazonas"]],
	7: [-12.9833333, -38.5166667, ["バイア州", "Bahia", "Bahia", "Bahia", "Bahía", "Bahia", "Bahia"]],
	8: [-3.7737, -38.5748, ["セアラ州", "Ceará", "Ceará", "Ceará", "Ceará", "Ceará", "Ceará"]],
	9: [-20.3166667, -40.35, ["エスピリト・サント州", "Espírito Santo", "Espírito Santo", "Espírito Santo", "Espírito Santo", "Espírito Santo", "Espírito Santo"]],
	10: [-20.45, -54.6166667, ["マット・グロッソ・ド・スル州", "Mato Grosso do Sul", "Mato Grosso do Sul", "Mato Grosso do Sul", "Mato Grosso do Sul", "Mato Grosso del Sud", "Mato Grosso do Sul"]],
	11: [-2.5166667, -44.2666667, ["マラニョン州", "Maranhão", "Maranhão", "Maranhao", "Maranhão", "Maranhão", "Maranhão"]],
	12: [-15.5833333, -56.0833333, ["マット・グロッソ州", "Mato Grosso", "Mato Grosso", "Mato Grosso", "Mato Grosso", "Mato Grosso", "Mato Grosso"]],
	13: [-19.9166667, -43.9333333, ["ミナス・ジェライス州", "Minas Gerais", "Minas Gerais", "Minas Gerais", "Minas Gerais", "Minas Gerais", "Minas Gerais"]],
	14: [-1.45, -48.4833333, ["パラー州", "Pará", "Pará", "Pará", "Pará", "Pará", "Pará"]],
	15: [-7.1166667, -34.8666667, ["パライーバ州", "Paraíba", "Paraíba", "Paraíba", "Paraíba", "Paraíba", "Paraíba"]],
	16: [-25.4166667, -49.25, ["パラナ州", "Paraná", "Paraná", "Paraná", "Paraná", "Paraná", "Paraná"]],
	17: [-5.0833333, -42.8166667, ["ピアウイー州", "Piauí", "Piauí", "Piaui", "Piauí", "Piauí", "Piauí"]],
	18: [-22.9, -43.2333333, ["リオ・デ・ジャネイロ州", "Rio de Janeiro", "Rio de Janeiro", "Etat de Rio de Janeiro", "Río de Janeiro", "Rio de Janeiro", "Rio de Janeiro"]],
	19: [-5.7833333, -35.2166667, ["リオ・グランデ・ド・ノルテ州", "Rio Grande do Norte", "Rio Grande do Norte", "Rio Grande do Norte", "Rio Grande do Norte", "Rio Grande del Nord", "Rio Grande do Norte"]],
	20: [-30.0333333, -51.2, ["リオ・グランデ・ド・スル州", "Rio Grande do Sul", "Rio Grande do Sul", "Rio Grande do Sul", "Rio Grande do Sul", "Rio Grande do Sul", "Rio Grande do Sul"]],
	21: [-8.7666667, -63.9, ["ロンドニア州", "Rondônia", "Rondônia", "Rondônia", "Rondônia", "Rondônia", "Rondônia"]],
	22: [2.8166667, -60.6666667, ["ロライマ州", "Roraima", "Roraima", "Roraima", "Roraima", "Roraima", "Roraima"]],
	23: [-27.5833333, -48.5666667, ["サンタ・カタリーナ州", "Santa Catarina", "Santa Catarina", "Santa Catarina", "Santa Catarina", "Santa Catarina", "Santa Catarina"]],
	24: [-23.5333333, -46.6166667, ["サン・パウロ州", "São Paulo", "São Paulo", "Etat de São Paulo", "São Paulo", "San Paolo", "São Paulo"]],
	25: [-10.9166667, -37.0666667, ["セルジッペ州", "Sergipe", "Sergipe", "Sergipe", "Sergipe", "Sergipe", "Sergipe"]],
	26: [-16.66758366, -49.26460505, ["ゴイアス州", "Goiás", "Goiás", "Goias", "Goiás", "Goiás", "Goiás"]],
	27: [-8.05, -34.9, ["ペルナンブコ州", "Pernambuco", "Pernambuco", "Pernambouc", "Pernambuco", "Pernambuco", "Pernambuco"]],
	28: [-10.2227778, -48.2777778, ["トカンティンス州", "Tocantins", "Tocantins", "Tocantins", "Tocantins", "Tocantins", "Tocantins"]]
}

regioninfo_017 = {
	1: [18.4166667, -64.6166667, ["英領ヴァージン諸島", "British Virgin Islands", "Britische Jungferninseln", "Iles Vierges britanniques", "Islas Vírgenes Británicas", "Isole Vergini Britanniche", "Britse Maagdeneilanden"]]
}

regioninfo_018 = {
	1: [0, 0, ["カナダ", "Canada", "Kanada", "Canada", "Canadá", "Canada", "Canada"]],
	2: [45.26680278, -75.74934996, ["オンタリオ州", "Ontario", "Ontario", "Ontario", "Ontario", "Ontario", "Ontario"]],
	3: [53.55013594, -113.4687122, ["アルバータ州", "Alberta", "Alberta", "Alberta", "Alberta", "Alberta", "Alberta"]],
	4: [48.43293574, -123.3692997, ["ブリティッシュ・コロンビア州", "British Columbia", "Britisch-Kolumbien", "Colombie-Britannique", "Columbia Británica", "Columbia Britannica", "Brits-Columbia"]],
	5: [49.88439862, -97.14704472, ["マニトバ州", "Manitoba", "Manitoba", "Manitoba", "Manitoba", "Manitoba", "Manitoba"]],
	6: [45.94541477, -66.6655816, ["ニュー・ブランズウィック州", "New Brunswick", "Neubraunschweig", "Nouveau-Brunswick", "Nuevo Brunswick", "Nuovo Brunswick", "Nieuw-Brunswijk"]],
	7: [47.56658838, -52.73134462, ["ニューファンドランド・ラブラドール州", "Newfoundland and Labrador", "Neufundland und Labrador", "Terre-Neuve-et-Labrador", "Terranova y Labrador", "Terranova e Labrador", "Newfoundland en Labrador"]],
	8: [44.9, -63.5, ["ノバ・スコシア州", "Nova Scotia", "Neuschottland", "Nouvelle-Écosse", "Nueva Escocia", "Nuova Scozia", "Nova Scotia"]],
	9: [46.24041836, -63.1333861, ["プリンス・エドワード・アイランド州", "Prince Edward Island", "Prinz-Edward-Insel", "Île-du-Prince-Édouard", "Isla del Príncipe Eduardo", "Isola del Principe Edoardo", "Prins Edwardeiland"]],
	10: [46.8069, -71.2118, ["ケベック州", "Quebec", "Québec", "Québec", "Quebec", "Québec", "Québec"]],
	11: [50.45008005, -104.6177979, ["サスカチュワン州", "Saskatchewan", "Saskatchewan", "Saskatchewan", "Saskatchewan", "Saskatchewan", "Saskatchewan"]],
	12: [60.71611478, -135.0537476, ["ユーコン準州", "Yukon", "Yukon-Territorium", "Territoire du Yukon", "Yukón", "Yukon", "Yukon"]],
	13: [62.45599511, -114.352546, ["ノースウェスト準州", "Northwest Territories", "Nordwest-Territorien", "Territoires du Nord-Ouest", "Territorios del Noroeste", "Territori del Nord-Ovest", "Northwest Territories"]],
	14: [63.75059349, -68.51448958, ["ヌナブト準州", "Nunavut", "Nunavut", "Territoire du Nunavut", "Nunavut", "Nunavut", "Nunavut"]]
}

regioninfo_019 = {
	1: [19.3, -81.3833333, ["ケイマン諸島", "Cayman Islands", "Kaimaninseln", "Iles Caïmans", "Islas Caimán", "Isole Cayman", "Kaaimaneilanden"]]
}

regioninfo_020 = {
	1: [0, 0, ["チリ", "Chile", "Chile", "Chili", "Chile", "Cile", "Chili"]],
	2: [-33.45, -70.6666667, ["レジョン・メトロポリタナ州", "Región Metropolitana", "Región Metropolitana", "Région Métropolitaine de Santiago", "Región Metropolitana", "Regione Metropolitana di Santiago", "Región Metropolitana"]],
	3: [-33.0477778, -71.6011111, ["バルパライソ州", "Valparaíso", "Valparaíso (Region V)", "Valparaiso", "Valparaíso", "Valparaíso", "Valparaíso"]],
	4: [-45.5666667, -72.0666667, ["アイセン・デル・Ｇ・カルロス・イバニェス・デル・カンポ州", "Aisén del General Carlos Ibáñez del Campo", "Aisén (Region XI)", "Aisén del General Carlos Ibánez del Campo", "Aisén del General Carlos Ibáñez del Campo", "Aysen", "Aysén del General Carlos Ibáñez del Campo"]],
	5: [-23.65, -70.4, ["アントファガスタ州", "Antofagasta", "Antofagasta (Region II)", "Antofagasta", "Antofagasta", "Antofagasta", "Antofagasta"]],
	6: [-38.7333333, -72.6, ["アラウカニア州", "Araucanía", "Araukanien (Region IX)", "Araucanie", "Araucanía", "Araucanía", "Araucanía"]],
	7: [-27.3666667, -70.3333333, ["アタカマ州", "Atacama", "Atacama (Region III)", "Atacama", "Atacama", "Atacama", "Atacama"]],
	8: [-36.8333333, -73.05, ["ビオビオ州", "Bío-Bío", "Bío-Bío (Region VIII)", "Biobío", "Bío-Bío", "Bío-Bío", "Bío-Bío"]],
	9: [-29.9533333, -71.3436111, ["コキンボ州", "Coquimbo", "Coquimbo (Region IV)", "Coquimbo", "Coquimbo", "Coquimbo", "Coquimbo"]],
	10: [-34.1666667, -70.75, ["L・ベルナルド・オヒギンス州", "Libertador General Bernardo O'Higgins", "Libertador General Bernardo O'Higgins (Region VI)", "Libertador General Bernardo O'Higgins", "Libertador General Bernardo O'Higgins", "O'Higgins", "Libertador General Bernardo O'Higgins"]],
	11: [-41.4716667, -72.9369444, ["ロス・ラゴス州", "Los Lagos", "Los Lagos (Region X)", "Los Lagos", "Los Lagos", "Los Lagos", "Los Lagos"]],
	12: [-53.15, -70.9166667, ["マガリャネス州", "Magallanes y Antártica Chilena", "Magallanes (Region XII) und Chilenische Antarktis", "Magellan et Antarctique Chilienne", "Magallanes y Antártica Chilena", "Magellane e Antartide Cilena", "Magallanes y de la Antártica Chilena"]],
	13: [-35.4333333, -71.6666667, ["マウレ州", "Maule", "Maule (Region VII)", "Maule", "Maule", "Maule", "Maule"]],
	14: [-20.2166667, -70.1666667, ["タラパカ州", "Tarapacá", "Tarapacá (Region I)", "Tarapacá", "Tarapacá", "Tarapacá", "Tarapacá"]]
}

regioninfo_021 = {
	1: [0, 0, ["コロンビア", "Colombia", "Kolumbien", "Colombie", "Colombia", "Colombia", "Colombia"]],
	2: [4.25, -74.1833333, ["ディストリト・キャピタル", "Distrito Capital", "Distrito Capital", "District Capital de Santa Fe de Bogotá", "Distrito Capital", "Distrito Capital", "Hoofdstedelijk District"]],
	3: [4.6, -74.0833333, ["クンディナマルカ県", "Cundinamarca", "Cundinamarca", "Cundinamarca", "Cundinamarca", "Cundinamarca", "Cundinamarca"]],
	4: [-4.2152778, -69.9405556, ["アマソナス県", "Amazonas", "Amazonas", "Amazone", "Amazonas", "Amazonas", "Amazonas"]],
	5: [6.2913889, -75.5361111, ["アンティオキア県", "Antioquia", "Antioquia", "Antioquia", "Antioquia", "Antioquia", "Antioquia"]],
	6: [7.0902778, -70.7616667, ["アラウカ県", "Arauca", "Arauca", "Arauca", "Arauca", "Arauca", "Arauca"]],
	7: [10.9638889, -74.7963889, ["アトランティコ県", "Atlántico", "Atlántico", "Atlantique", "Atlántico", "Atlántico", "Atlántico"]],
	8: [10.3997222, -75.5144444, ["ボリーバル県", "Bolívar", "Bolívar", "Bolívar", "Bolívar", "Bolívar", "Bolívar"]],
	9: [5.5352778, -73.3677778, ["ボヤカ県", "Boyacá", "Boyacá", "Boyaca", "Boyacá", "Boyacá", "Boyacá"]],
	10: [5.07, -75.5205556, ["カルダス県", "Caldas", "Caldas", "Caldas", "Caldas", "Caldas", "Caldas"]],
	11: [1.6175, -75.6175, ["カケタ県", "Caquetá", "Caquetá", "Caqueta", "Caquetá", "Caquetá", "Caquetá"]],
	12: [2.4861, -76.5814, ["カウカ県", "Cauca", "Cauca", "Cauca", "Cauca", "Cauca", "Cauca"]],
	13: [10.4769444, -73.2505556, ["セサル県", "Cesar", "Cesar", "Cesar", "Cesar", "Cesar", "Cesar"]],
	14: [5.6947222, -76.6611111, ["チョコ県", "Chocó", "Chocó", "Chocó", "Chocó", "Chocó", "Chocó"]],
	15: [8.7575, -75.89, ["コルドバ県", "Córdoba", "Córdoba", "Córdoba", "Córdoba", "Córdoba", "Córdoba"]],
	16: [2.5683333, -72.6416667, ["グアビアレ県", "Guaviare", "Guaviare", "Guaviare", "Guaviare", "Guaviare", "Guaviare"]],
	17: [3.8652778, -67.9238889, ["グアイニア県", "Guainía", "Guainía", "Guainía", "Guainía", "Guainía", "Guainía"]],
	18: [2.9305556, -75.3302778, ["ウィラ県", "Huila", "Huila", "Huila", "Huila", "Huila", "Huila"]],
	19: [11.5444444, -72.9072222, ["グアヒーラ県", "La Guajira", "La Guajira", "La Guajira", "La Guajira", "La Guajira", "Guajira"]],
	20: [11.2472222, -74.2016667, ["マグダレーナ県", "Magdalena", "Magdalena", "Magdalena", "Magdalena", "Magdalena", "Magdalena"]],
	21: [4.1533333, -73.635, ["メタ県", "Meta", "Meta", "Meta", "Meta", "Meta", "Meta"]],
	22: [1.2136111, -77.2811111, ["ナリーニョ県", "Nariño", "Nariño", "Nariño", "Nariño", "Nariño", "Nariño"]],
	23: [7.8833333, -72.5052778, ["ノルテ・デ・サンタンデル県", "Norte de Santander", "Norte de Santander", "Norte de Santander", "Norte de Santander", "Norte de Santander", "Norte de Santander"]],
	24: [1.1488889, -76.6477778, ["プトゥマイオ県", "Putumayo", "Putumayo", "Putumayo", "Putumayo", "Putumayo", "Putumayo"]],
	25: [4.5338889, -75.6811111, ["キンディオ県", "Quindío", "Quindío", "Quindío", "Quindío", "Quindío", "Quindío"]],
	26: [4.8133333, -75.6961111, ["リサラルダ県", "Risaralda", "Risaralda", "Risaralda", "Risaralda", "Risaralda", "Risaralda"]],
	27: [12.5847222, -81.7005556, ["サン・アンドレス・イ・プロビデンシア県", "Archipiélago de San Andrés, Providencia y Santa Catalina", "San Andrés und Providencia", "Îles de San Andrés, Providencia et Santa Cataline", "Archipiélago de San Andrés, Providencia y Santa Catalina", "San Andrés e Providencia", "San Andrés en Providencia"]],
	28: [7.1297222, -73.1258333, ["サンタンデル県", "Santander", "Santander", "Santander", "Santander", "Santander", "Santander"]],
	29: [9.3047222, -75.3977778, ["スクレ県", "Sucre", "Sucre", "Sucre", "Sucre", "Sucre", "Sucre"]],
	30: [4.4388889, -75.2322222, ["トリマ県", "Tolima", "Tolima", "Tolima", "Tolima", "Tolima", "Tolima"]],
	31: [3.4372222, -76.5225, ["バジェ・デル・カウカ県", "Valle del Cauca", "Valle del Cauca", "Valle del Cauca", "Valle del Cauca", "Valle del Cauca", "Valle del Cauca"]],
	32: [1.1983333, -70.1733333, ["バウペス県", "Vaupés", "Vaupés", "Vaupés", "Vaupés", "Vaupés", "Vaupés"]],
	33: [6.1877778, -67.4730556, ["ビチャダ県", "Vichada", "Vichada", "Vichada", "Vichada", "Vichada", "Vichada"]],
	34: [5.3394444, -72.3941667, ["カサナレ県", "Casanare", "Casanare", "Casanare", "Casanare", "Casanare", "Casanare"]]
}

regioninfo_022 = {
	1: [0, 0, ["コスタリカ", "Costa Rica", "Costa Rica", "Costa Rica", "Costa Rica", "Costa Rica", "Costa Rica"]],
	2: [9.9333333, -84.0833333, ["サン・ホセ州", "San José", "San José", "San José", "San José", "San José", "San José"]],
	3: [10.0166667, -84.2166667, ["アラフエラ州", "Alajuela", "Alajuela", "Alajuela", "Alajuela", "Alajuela", "Alajuela"]],
	4: [9.8666667, -83.9166667, ["カルタゴ州", "Cartago", "Cartago", "Cartago", "Cartago", "Cartago", "Cartago"]],
	5: [10.6333333, -85.4333333, ["グアナカステ州", "Guanacaste", "Guanacaste", "Guanacaste", "Guanacaste", "Guanacaste", "Guanacaste"]],
	6: [10, -84.1166667, ["エレディア州", "Heredia", "Heredia", "Heredia", "Heredia", "Heredia", "Heredia"]],
	7: [10, -83.0333333, ["リモン州", "Limón", "Limón", "Limón", "Limón", "Limón", "Limón"]],
	8: [9.9666667, -84.8333333, ["プンタレナス州", "Puntarenas", "Puntarenas", "Puntarenas", "Puntarenas", "Puntarenas", "Puntarenas"]]
}

regioninfo_023 = {
	1: [15.3, -61.4, ["ドミニカ国", "Dominica", "Dominica", "Dominique", "Dominica", "Dominica", "Dominica"]]
}

regioninfo_024 = {
	1: [0, 0, ["ドミニカ共和国", "Dominican Republic", "Dominikanische Republik", "République dominicaine", "República Dominicana", "Repubblica Dominicana", "Dominicaanse Replubliek"]],
	2: [18.4666667, -69.9, ["ディストリト・ナショナル首都圏", "Distrito Nacional", "Distrito Nacional", "District National", "Distrito Nacional", "Distretto Nazionale", "Distrito Nacional"]],
	3: [18.45, -70.7333333, ["アスア", "Azua", "Azua", "Azua", "Azua", "Azua", "Azua"]],
	4: [18.4666667, -71.4166667, ["バオルコ", "Baoruco", "Baoruco", "Baoruco", "Baoruco", "Baoruco", "Baoruco"]],
	5: [18.2, -71.1, ["バラオナ", "Barahona", "Barahona", "Barahona", "Barahona", "Barahona", "Barahona"]],
	6: [19.55, -71.7, ["ダハボン", "Dajabón", "Dajabón", "Dajabón", "Dajabón", "Dajabón", "Dajabón"]],
	7: [19.3, -70.25, ["ドゥアルテ", "Duarte", "Duarte", "Duarte", "Duarte", "Duarte", "Duarte"]],
	8: [19.4, -70.5166667, ["Espaillat", "Espaillat", "Espaillat", "Espaillat", "Espaillat", "Espaillat", "Espaillat"]],
	9: [18.4908333, -71.8508333, ["インデペンデンシア", "Independencia", "Independencia", "Independencia", "Independencia", "Independencia", "Independencia"]],
	10: [18.7, -68.6666667, ["ラアルタグラシア", "La Altagracia", "La Altagracia", "La Altagracia", "La Altagracia", "La Altagracia", "La Altagracia"]],
	11: [18.8775, -71.7027778, ["Elías Piña", "Elías Piña", "Elías Piña", "Elías Piña", "Elías Piña", "Elías Piña", "Elías Piña"]],
	12: [18.4166667, -68.9666667, ["ラ・ロマナ", "La Romana", "La Romana", "La Romana", "La Romana", "La Romana", "La Romana"]],
	13: [19.3833333, -69.8333333, ["María Trinidad Sánchez", "María Trinidad Sánchez", "María Trinidad Sánchez", "María Trinidad Sánchez", "María Trinidad Sánchez", "María Trinidad Sánchez", "María Trinidad Sánchez"]],
	14: [19.6666667, -71.6666667, ["Monte Cristi", "Monte Cristi", "Monte Cristi", "Monte Cristi", "Monte Cristi", "Monte Cristi", "Monte Cristi"]],
	15: [18.0333333, -71.75, ["Pedernales", "Pedernales", "Pedernales", "Pedernales", "Pedernales", "Pedernales", "Pedernales"]],
	16: [18.2833333, -70.3333333, ["Peravia", "Peravia", "Peravia", "Peravia", "Peravia", "Peravia", "Peravia"]],
	17: [19.8, -70.6833333, ["プエルト・プラタ", "Puerto Plata", "Puerto Plata", "Puerto Plata", "Puerto Plata", "Puerto Plata", "Puerto Plata"]],
	18: [19.4, -70.35, ["Salcedo", "Salcedo", "Salcedo", "Salcedo", "Salcedo", "Salcedo", "Salcedo"]],
	19: [19.2166667, -69.3166667, ["Samaná", "Samaná", "Samaná", "Samaná", "Samaná", "Samaná", "Samaná"]],
	20: [19.05, -70.15, ["Sánchez Ramírez", "Sánchez Ramírez", "Sánchez Ramírez", "Sánchez Ramírez", "Sánchez Ramírez", "Sánchez Ramírez", "Sánchez Ramírez"]],
	21: [18.8, -71.2333333, ["サン・フアン", "San Juan", "San Juan", "San Juan", "San Juan", "San Juan", "San Juan"]],
	22: [18.45, -69.3, ["サン・ペドロ・デ・マコリス", "San Pedro de Macorís", "San Pedro de Macorís", "San Pedro de Macorís", "San Pedro de Macorís", "San Pedro de Macorís", "San Pedro de Macorís"]],
	23: [19.45, -70.7, ["サンティアゴ", "Santiago", "Santiago", "Santiago", "Santiago", "Santiago", "Santiago"]],
	24: [19.4666667, -71.3333333, ["Santiago Rodríguez", "Santiago Rodríguez", "Santiago Rodríguez", "Santiago Rodríguez", "Santiago Rodríguez", "Santiago Rodríguez", "Santiago Rodríguez"]],
	25: [19.5666667, -71.0833333, ["Valverde", "Valverde", "Valverde", "Valverde", "Valverde", "Valverde", "Valverde"]],
	26: [18.7666667, -69.0333333, ["El Seíbo", "El Seíbo", "El Seíbo", "El Seibo", "El Seíbo", "El Seíbo", "El Seibo"]],
	27: [18.7666667, -69.25, ["Hato Mayor", "Hato Mayor", "Hato Mayor", "Hato Mayor", "Hato Mayor", "Hato Mayor", "Hato Mayor"]],
	28: [19.2166667, -70.5166667, ["La Vega", "La Vega", "La Vega", "La Vega", "La Vega", "La Vega", "La Vega"]],
	29: [18.9333333, -70.4166667, ["Monseñor Nouel", "Monseñor Nouel", "Monseñor Nouel", "Monseñor Nouel", "Monseñor Nouel", "Monseñor Nouel", "Monseñor Nouel"]],
	30: [18.8, -69.7833333, ["Monte Plata", "Monte Plata", "Monte Plata", "Monte Plata", "Monte Plata", "Monte Plata", "Monte Plata"]],
	31: [18.4166667, -70.1, ["San Cristóbal", "San Cristóbal", "San Cristóbal", "San Cristóbal", "San Cristóbal", "San Cristóbal", "San Cristóbal"]]
}

regioninfo_025 = {
	1: [0, 0, ["エクアドル", "Ecuador", "Ecuador", "Equateur", "Ecuador", "Ecuador", "Ecuador"]],
	2: [-0.2166667, -78.5, ["ピチンチャ", "Pichincha", "Pichincha", "Pichincha", "Pichincha", "Pichincha", "Pichincha"]],
	3: [-0.9, -89.6, ["ガラパゴス", "Galápagos", "Galapagosinseln", "Galápagos", "Galápagos", "Galapagos", "Galápagos"]],
	4: [-2.8833333, -78.9833333, ["アスアイ", "Azuay", "Azuay", "Azuay", "Azuay", "Azuay", "Azuay"]],
	5: [-1.6, -79, ["ボリーバル", "Bolívar", "Bolívar", "Bolívar", "Bolívar", "Bolívar", "Bolívar"]],
	6: [-2.7333333, -78.8333333, ["カニャル", "Cañar", "Cañar", "Cañar", "Cañar", "Cañar", "Cañar"]],
	7: [0.8, -77.7333333, ["カルチ", "Carchi", "Carchi", "Carchi", "Carchi", "Carchi", "Carchi"]],
	8: [-1.6666667, -78.6333333, ["チンボラソ", "Chimborazo", "Chimborazo", "Chimborazo", "Chimborazo", "Chimborazo", "Chimborazo"]],
	9: [-0.9333333, -78.6166667, ["コトパクシ", "Cotopaxi", "Cotopaxi", "Cotopaxi", "Cotopaxi", "Cotopaxi", "Cotopaxi"]],
	10: [-3.2666667, -79.9666667, ["エル・オロ", "El Oro", "El Oro", "El Oro", "El Oro", "El Oro", "El Oro"]],
	11: [0.9833333, -79.7, ["エスメラルダス", "Esmeraldas", "Esmeraldas", "Esmeraldas", "Esmeraldas", "Esmeraldas", "Esmeraldas"]],
	12: [-2.1666667, -79.9, ["グアヤス", "Guayas", "Guayas", "Guayas", "Guayas", "Guayas", "Guayas"]],
	13: [0.35, -78.1166667, ["インバブラ", "Imbabura", "Imbabura", "Imbabura", "Imbabura", "Imbabura", "Imbabura"]],
	14: [-4, -79.2166667, ["ロハ", "Loja", "Loja", "Loja", "Loja", "Loja", "Loja"]],
	15: [-1.8166667, -79.5166667, ["ロス・リオス", "Los Ríos", "Los Ríos", "Los Rios", "Los Ríos", "Los Ríos", "Los Ríos"]],
	16: [-1.05, -80.45, ["マナビ", "Manabí", "Manabí", "Manabi", "Manabí", "Manabí", "Manabí"]],
	17: [-2.3166667, -78.1166667, ["モロナ・サンティアゴ", "Morona-Santiago", "Morona Santiago", "Morona Santiago", "Morona-Santiago", "Morona-Santiago", "Morona-Santiago"]],
	18: [-1.4666667, -77.9833333, ["パスタサ", "Pastaza", "Pastaza", "Pastaza", "Pastaza", "Pastaza", "Pastaza"]],
	19: [-1.25, -78.6166667, ["トゥングラワ", "Tungurahua", "Tungurahua", "Tungurahua", "Tungurahua", "Tungurahua", "Tungurahua"]],
	20: [-4.0691667, -78.9566667, ["サモラ・チンチペ", "Zamora-Chinchipe", "Zamora Chinchipe", "Zamora Chinchipe", "Zamora-Chinchipe", "Zamora-Chinchipe", "Zamora-Chinchipe"]],
	21: [0.0847222, -76.8827778, ["スクンビオス", "Sucumbios", "Sucumbios", "Sucumbíos", "Sucumbíos", "Sucumbíos", "Sucumbíos"]],
	22: [-0.9833333, -77.8166667, ["ナポ", "Napo", "Napo", "Napo", "Napo", "Napo", "Napo"]],
	23: [-0.8, -76.36666667, ["オレリャナ", "Orellana", "Orellana", "Orellana", "Orellana", "Orellana", "Orellana"]]
}

regioninfo_026 = {
	1: [0, 0, ["エルサルバドル", "El Salvador", "El Salvador", "Salvador", "El Salvador", "El Salvador", "El Salvador"]],
	2: [13.7086111, -89.2030556, ["サン・サルバドル県", "San Salvador", "San Salvador", "San Salvador", "San Salvador", "San Salvador", "San Salvador"]],
	3: [13.9213889, -89.845, ["アワチャパン県", "Ahuachapán", "Ahuachapán", "Ahuachapán", "Ahuachapán", "Ahuachapán", "Ahuachapán"]],
	4: [13.8666667, -88.6333333, ["カバニャス県", "Cabañas", "Cabañas", "Cabañas", "Cabañas", "Cabañas", "Cabañas"]],
	5: [14.0333333, -88.9333333, ["チャラテナンゴ県", "Chalatenango", "Chalatenango", "Chalatenango", "Chalatenango", "Chalatenango", "Chalatenango"]],
	6: [13.7166667, -88.9333333, ["クスカトラン県", "Cuscatlán", "Cuscatlán", "Cuscatlán", "Cuscatlán", "Cuscatlán", "Cuscatlán"]],
	7: [13.6769444, -89.2797222, ["ラ・リベルター県", "La Libertad", "La Libertad", "La Libertad", "La Libertad", "La Libertad", "La Libertad"]],
	8: [13.5, -88.8666667, ["ラパス県", "La Paz", "La Paz", "La Paz", "La Paz", "La Paz", "La Paz"]],
	9: [13.3369444, -87.8438889, ["ラ・ウニオン県", "La Unión", "La Unión", "La Unión", "La Unión", "La Unión", "La Unión"]],
	10: [13.7, -88.1, ["モラサン県", "Morazán", "Morazán", "Morazán", "Morazán", "Morazán", "Morazán"]],
	11: [13.4833333, -88.1833333, ["サン・ミゲル県", "San Miguel", "San Miguel", "San Miguel", "San Miguel", "San Miguel", "San Miguel"]],
	12: [13.9941667, -89.5597222, ["サンタ・アナ県", "Santa Ana", "Santa Ana", "Santa Ana", "Santa Ana", "Santa Ana", "Santa Ana"]],
	13: [13.6333333, -88.8, ["サンビセンテ県", "San Vicente", "San Vicente", "San Vicente", "San Vicente", "San Vicente", "San Vicente"]],
	14: [13.7188889, -89.7241667, ["ソンソナテ県", "Sonsonate", "Sonsonate", "Sonsonate", "Sonsonate", "Sonsonate", "Sonsonate"]],
	15: [13.35, -88.45, ["ウスルタン県", "Usulután", "Usulután", "Usulután", "Usulután", "Usulután", "Usulután"]]
}

regioninfo_027 = {
	1: [4.9333333, -52.3333333, ["フランス領ギアナ", "French Guiana", "Guayana", "Guyane française", "Guayana Francesa", "Guayana Francese", "Frans-Guyana"]]
}

regioninfo_028 = {
	1: [12.05, -61.75, ["グレナダ", "Grenada", "Grenada", "Grenade", "Granada", "Grenada", "Grenada"]]
}

regioninfo_029 = {
	1: [16, -61.7166667, ["グアドループ", "Guadeloupe", "Guadeloupe", "Guadeloupe", "Guadalupe", "Guadalupa", "Guadeloupe"]]
}

regioninfo_030 = {
	1: [0, 0, ["グアテマラ", "Guatemala", "Guatemala", "Guatemala", "Guatemala", "Guatemala", "Guatemala"]],
	2: [14.6211111, -90.5269444, ["グアテマラ県", "Guatemala", "Guatemala", "Guatemala", "Guatemala", "Guatemala", "Guatemala"]],
	3: [15.4833333, -90.3666667, ["アルタ・べラパス県", "Alta Verapaz", "Alta Verapaz", "Alta Verapaz", "Alta Verapaz", "Alta Verapaz", "Alta Verapaz"]],
	4: [15.1, -90.2666667, ["バハ・べラパス県", "Baja Verapaz", "Baja Verapaz", "Baja Verapaz", "Baja Verapaz", "Baja Verapaz", "Baja Verapaz"]],
	5: [14.6686111, -90.8166667, ["チマルテナンゴ県", "Chimaltenango", "Chimaltenango", "Chimaltenango", "Chimaltenango", "Chimaltenango", "Chimaltenango"]],
	6: [14.8, -89.55, ["チキムラ県", "Chiquimula", "Chiquimula", "Chiquimula", "Chiquimula", "Chiquimula", "Chiquimula"]],
	7: [14.8538889, -90.0647222, ["エル・プログレソ県", "El Progreso", "El Progreso", "El Progreso", "El Progreso", "El Progreso", "El Progreso"]],
	8: [14.305, -90.785, ["エスクィントラ県", "Escuintla", "Escuintla", "Escuintla", "Escuintla", "Escuintla", "Escuintla"]],
	9: [15.3197222, -91.4708333, ["ウェウェテナンゴ県", "Huehuetenango", "Huehuetenango", "Huehuetenango", "Huehuetenango", "Huehuetenango", "Huehuetenango"]],
	10: [15.7166667, -88.6, ["イザバル県", "Izabal", "Izabal", "Izabal", "Izabal", "Izabal", "Izabal"]],
	11: [14.6333333, -89.9833333, ["ハラパ県", "Jalapa", "Xalapa", "Jalapa", "Jalapa", "Jalapa", "Jalapa"]],
	12: [14.2833333, -89.9, ["フティアパ県", "Jutiapa", "Jutiapa", "Jutiapa", "Jutiapa", "Jutiapa", "Jutiapa"]],
	13: [16.9333333, -89.8833333, ["エル・ペテン県", "Petén", "El Petén", "El Petén", "Petén", "El Petén", "Petén"]],
	14: [14.8333333, -91.5166667, ["ケツァルテナンゴ県", "Quetzaltenango", "Quetzaltenango", "Quetzaltenango", "Quetzaltenango", "Quetzaltenango", "Quetzaltenango"]],
	15: [15.0305556, -91.1488889, ["エル・キチェ県", "Quiché", "El Quiché", "El Quiché", "Quiché", "El Quiché", "Quiché"]],
	16: [14.5333333, -91.6833333, ["レタルーレウ県", "Retalhuleu", "Retalhuleu", "Retalhuleu", "Retalhuleu", "Retalhuleu", "Retalhuleu"]],
	17: [14.5611111, -90.7344444, ["サカテペケス県", "Sacatepéquez", "Sacatepéquez", "Sacatepéquez", "Sacatepéquez", "Sacatepéquez", "Sacatepéquez"]],
	18: [14.9666667, -91.8, ["サン・マルコス県", "San Marcos", "San Marcos", "San Marcos", "San Marcos", "San Marcos", "San Marcos"]],
	19: [14.2763889, -90.3002778, ["サンタ・ローサ県", "Santa Rosa", "Santa Rosa", "Santa Rosa", "Santa Rosa", "Santa Rosa", "Santa Rosa"]],
	20: [14.7666667, -91.1833333, ["ソロラ県", "Sololá", "Sololá", "Sololá", "Sololá", "Sololá", "Sololá"]],
	21: [14.5333333, -91.5, ["スチテペケス県", "Suchitepéquez", "Suchitepéquez", "Suchitepéquez", "Suchitepéquez", "Suchitepéquez", "Suchitepéquez"]],
	22: [14.9166667, -91.3666667, ["トトニカパン県", "Totonicapán", "Totonicapán", "Totonicapán", "Totonicapán", "Totonicapán", "Totonicapán"]],
	23: [14.9666667, -89.5333333, ["サカパ県", "Zacapa", "Zacapa", "Zacapa", "Zacapa", "Zacapa", "Zacapa"]]
}

regioninfo_031 = {
	1: [0, 0, ["ガイアナ", "Guyana", "Guyana", "République Coopérative de Guyane", "Guyana", "Guyana", "Guyana"]],
	2: [6.8, -58.1666667, ["デメララ", "Demerara-Mahaica", "Demerara-Mahaica", "Demerara-Mahaica", "Demerara-Mahaica", "Demerara-Mahaica", "Demerara-Mahaica"]],
	3: [8.2, -59.7833333, ["Barima-Waini", "Barima-Waini", "Barima-Waini", "Nord-Ouest", "Barima-Waini", "Barima-Waini", "Barima-Waini"]],
	4: [6.4, -58.6166667, ["Cuyuni-Mazaruni", "Cuyuni-Mazaruni", "Cuyuni-Mazaruni", "Marazuni-Potaro", "Cuyuni-Mazaruni", "Cuyuni-Mazaruni", "Cuyuni-Mazaruni"]],
	5: [6.25, -57.5166667, ["East Berbice-Corentyne", "East Berbice-Corentyne", "East Berbice-Corentyne", "Berbice-Est et Corentyne", "Berbice Oriental-Corentyne", "East Berbice-Corentyne", "East Berbice-Corentyne"]],
	6: [6.8666667, -58.4166667, ["Essequibo Islands-West Demerara", "Essequibo Islands-West Demerara", "Essequibo Islands-West Demerara", "Iles Essequibo et Demerara-Ouest", "Islas Essequibo-Demerara Occidental", "Essequibo Islands-West Demerara", "Essequibo Islands-West Demerara"]],
	7: [6.4, -57.6, ["Mahaica-Berbice", "Mahaica-Berbice", "Mahaica-Berbice", "Mahaica-Berbice", "Mahaica-Berbice", "Mahaica-Berbice", "Mahaica-Berbice"]],
	8: [7.2666667, -58.5, ["Pomeroon-Supenaam", "Pomeroon-Supenaam", "Pomeroon-Supenaam", "Pomeroon-Supenaam", "Pomeroon-Supenaam", "Pomeroon-Supenaam", "Pomeroon-Supenaam"]],
	9: [5.2666667, -59.15, ["Potaro-Siparuni", "Potaro-Siparuni", "Potaro-Siparuni", "Potaro-Siparuni", "Potaro-Siparuni", "Potaro-Siparuni", "Potaro-Siparuni"]],
	10: [6, -58.3, ["Upper Demerara-Berbice", "Upper Demerara-Berbice", "Upper Demerara-Berbice", "Haut-Demerara et Berbice", "Alto Demerara-Berbice", "Upper Demerara-Berbice", "Upper Demerara-Berbice"]],
	11: [3.3833333, -59.8, ["Upper Takutu-Upper Essequibo", "Upper Takutu-Upper Essequibo", "Upper Takutu-Upper Essequibo", "Haut-Takutu et Haut-Essequibo", "Alto Takutu-Alto Essequibo", "Upper Takutu-Upper Essequibo", "Upper Takutu-Upper Essequibo"]]
}

regioninfo_032 = {
	1: [0, 0, ["ハイチ", "Haiti", "Haiti", "Haïti", "Haití", "Haiti", "Haïti"]],
	2: [18.5391667, -72.335, ["西県", "Ouest", "Ouest", "Ouest", "Oeste", "Ouest", "Ouest"]],
	3: [19.95, -72.8333333, ["北西県", "Nord-Ouest", "Nord-Ouest", "Nord-Ouest", "Noroeste", "Nord-Ouest", "Nord-Ouest"]],
	4: [19.45, -72.6833333, ["アルティボニット県", "Artibonite", "Artibonite", "Artibonite", "Artibonito", "Artibonite", "Artibonite"]],
	5: [19.15, -72.0166667, ["中央県", "Centre", "Centre", "Centre", "Centro", "Centre", "Centre"]],
	6: [18.65, -74.1166667, ["湾岸県", "Grand'Anse", "Grand'Anse", "Grande-Anse", "Grand'Anse", "Grand'Anse", "Grand'Anse"]],
	7: [19.7577778, -72.2041667, ["北県", "Nord", "Nord", "Nord", "Norte", "Nord", "Nord"]],
	8: [19.6677778, -71.8397222, ["北東県", "Nord-Est", "Nord-Est", "Nord-Est", "Noreste", "Nord-Est", "Nord-Est"]],
	9: [18.2, -73.75, ["南県", "Sud", "Sud", "Sud", "Sur", "Sud", "Sud"]],
	10: [18.2341667, -72.5347222, ["南東県", "Sud-Est", "Sud-Est", "Sud-Est", "Sureste", "Sud-Est", "Sud-Est"]]
}

regioninfo_033 = {
	1: [0, 0, ["ホンジュラス", "Honduras", "Honduras", "Honduras", "Honduras", "Honduras", "Honduras"]],
	2: [14.1, -87.2166667, ["フランシスコ・モラサン", "Francisco Morazán", "Francisco Morazán", "Francisco Morazán", "Francisco Morazán", "Francisco Morazán", "Francisco Morazán"]],
	3: [15.7833333, -86.8, ["アトランティダ", "Atlántida", "Atlántida", "Atlántida", "Atlántida", "Atlántida", "Atlántida"]],
	4: [13.3166667, -87.2166667, ["チョルテカ", "Choluteca", "Choluteca", "Choluteca", "Choluteca", "Choluteca", "Choluteca"]],
	5: [15.9166667, -86, ["コロン", "Colón", "Colón", "Colón", "Colón", "Colón", "Colón"]],
	6: [14.45, -87.6333333, ["コマヤグア", "Comayagua", "Comayagua", "Comayagua", "Comayagua", "Comayagua", "Comayagua"]],
	7: [14.7666667, -88.7833333, ["コパン", "Copán", "Copán", "Copán", "Copán", "Copán", "Copán"]],
	8: [15.5, -88.0333333, ["コルテス", "Cortés", "Cortés", "Cortés", "Cortés", "Cortés", "Cortés"]],
	9: [13.9333333, -86.85, ["エル・パライソ", "El Paraíso", "El Paraíso", "El Paraíso", "El Paraíso", "El Paraíso", "El Paraíso"]],
	10: [15.2666667, -83.7666667, ["グラシアス・ア・ディオス", "Gracias a Dios", "Gracias a Dios", "Gracias a Dios", "Gracias a Dios", "Gracias a Dios", "Gracias a Dios"]],
	11: [14.3, -88.1833333, ["インティブカ", "Intibucá", "Intibucá", "Intibuca", "Intibucá", "Intibucá", "Intibucá"]],
	12: [16.3, -86.55, ["イスラス・デ・ラ・バイア", "Islas de la Bahía", "Islas de la Bahía", "Islas de la Bahía", "Islas de la Bahía", "Islas de la Bahía", "Baai Eilanden"]],
	13: [14.3166667, -87.6833333, ["ラ・パス", "La Paz", "La Paz", "La Paz", "La Paz", "La Paz", "La Paz"]],
	14: [14.5833333, -88.5833333, ["レンピラ", "Lempira", "Lempira", "Lempira", "Lempira", "Lempira", "Lempira"]],
	15: [14.4333333, -89.1833333, ["オコテペケ", "Ocotepeque", "Ocotepeque", "Ocotepeque", "Ocotepeque", "Ocotepeque", "Ocotepeque"]],
	16: [14.65, -86.2, ["オランチョ", "Olancho", "Olancho", "Olancho", "Olancho", "Olancho", "Olancho"]],
	17: [14.9166667, -88.2333333, ["サンタ・バルバラ", "Santa Bárbara", "Santa Bárbara", "Santa Bárbara", "Santa Bárbara", "Santa Bárbara", "Santa Bárbara"]],
	18: [13.5361111, -87.4875, ["バジェ", "Valle", "Valle", "Valle", "Valle", "Valle", "Valle"]],
	19: [15.1333333, -87.1333333, ["ヨロ", "Yoro", "Yoro", "Yoro", "Yoro", "Yoro", "Yoro"]]
}

regioninfo_034 = {
	1: [0, 0, ["ジャマイカ", "Jamaica", "Jamaika", "Jamaïque", "Jamaica", "Giamaica", "Jamaica"]],
	2: [18, -76.8, ["セント・トーマス", "Saint Thomas", "Saint Thomas", "Saint-Thomas", "Saint Thomas", "Saint Thomas", "Saint Thomas"]],
	3: [17.9666667, -77.2333333, ["クラレンドン", "Clarendon", "Clarendon", "Clarendon", "Clarendon", "Clarendon", "Clarendon"]],
	4: [18.45, -78.1666667, ["ハノーバー", "Hanover", "Hanover", "Hanover", "Hanover", "Hanover", "Hanover"]],
	5: [18.0333333, -77.5, ["マンチェスター", "Manchester", "Manchester", "Manchester", "Manchester", "Manchester", "Manchester"]],
	6: [18.1833333, -76.4666667, ["ポートランド", "Portland", "Portland", "Portland", "Portland", "Portland", "Portland"]],
	7: [18, -76.8, ["セント・アンドリュー", "Saint Andrew", "Saint Andrew", "Saint-Andrew", "Saint Andrew", "Saint Andrew", "Saint Andrew"]],
	8: [18.4333333, -77.2, ["セント・アン", "Saint Ann", "Saint Ann", "Sainte-Anne", "Saint Ann", "Saint Ann", "Saint Ann"]],
	9: [17.9833333, -76.95, ["セント・キャサリン", "Saint Catherine", "Saint Catherine", "Sainte-Catherine", "Saint Catherine", "Saint Catherine", "Saint Catherine"]],
	10: [18.0166667, -77.85, ["セント・エリザベス", "Saint Elizabeth", "Saint Elizabeth", "Sainte-Elizabeth", "Saint Elizabeth", "Saint Elizabeth", "Saint Elizabeth"]],
	11: [18.4666667, -77.9166667, ["セント・ジェームズ", "Saint James", "Saint James", "Saint-James", "Saint James", "Saint James", "Saint James"]],
	12: [18.3666667, -76.9, ["セント・メアリー", "Saint Mary", "Saint Mary", "Sainte-Marie", "Saint Mary", "Saint Mary", "Saint Mary"]],
	13: [18.5, -77.65, ["トレローニー", "Trelawny", "Trelawny", "Trelawny", "Trelawny", "Trelawny", "Trelawny"]],
	14: [18.2166667, -78.1333333, ["ウェストモアランド", "Westmoreland", "Westmoreland", "Westmoreland", "Westmoreland", "Westmoreland", "Westmoreland"]],
	15: [17.95, -76.78333333, ["キングストン", "Kingston-Saint John", "Kingston", "Kingston - Saint-John", "Kingston-Saint John", "Kingston-Saint John", "Kingston-Saint John"]]
}

regioninfo_035 = {
	1: [14.6, -61.0833333, ["マルティニーク", "Martinique", "Martinique", "Martinique", "Martinica", "Martinica", "Martinique"]]
}

regioninfo_036 = {
	1: [0, 0, ["メキシコ", "Mexico", "Mexiko", "Mexique", "México", "Messico", "Mexico"]],
	2: [19.4341667, -99.1386111, ["ディストリト・フェデラル連邦区", "Distrito Federal", "Bundesdistrikt", "District Fédéral", "Distrito Federal", "Distretto Federale", "Federaal District"]],
	3: [21.8833333, -102.3, ["アグアスカリエンテス州", "Aguascalientes", "Aguascalientes", "Aguascalientes", "Aguascalientes", "Aguascalientes", "Aguascalientes"]],
	4: [32.6519444, -115.4683333, ["バハ・カリフォルニア州", "Baja California", "Niederkalifornien", "Basse-Californie", "Baja California", "Bassa California", "Neder-Californië"]],
	5: [24.1666667, -110.3, ["バハ・カリフォルニア・スル州", "Baja California Sur", "Süd-Niederkalifornien", "Basse-Californie du Sud", "Baja California Sur", "Bassa California del Sud", "Zuid-Neder-Californië"]],
	6: [19.85, -90.5333333, ["カンペチェ州", "Campeche", "Campeche", "Campeche", "Campeche", "Campeche", "Campeche"]],
	7: [16.75, -93.1166667, ["チアパス州", "Chiapas", "Chiapas", "Chiapas", "Chiapas", "Chiapas", "Chiapas"]],
	8: [28.6333333, -106.0833333, ["チワワ州", "Chihuahua", "Chihuahua", "Chihuahua", "Chihuahua", "Chihuahua", "Chihuahua"]],
	9: [25.4166667, -101, ["コアウイラ州", "Coahuila de Zaragoza", "Coahuila de Zaragoza", "Coahuila", "Coahuila de Zaragoza", "Coahuila", "Coahuila de Zaragoza"]],
	10: [19.2333333, -103.7166667, ["コリマ州", "Colima", "Colima", "Colima", "Colima", "Colima", "Colima"]],
	11: [24.0333333, -104.6666667, ["ドゥランゴ州", "Durango", "Durango", "Durango", "Durango", "Durango", "Durango"]],
	12: [21.0166667, -101.25, ["グアナフアト州", "Guanajuato", "Guanajuato", "Guanajuato", "Guanajuato", "Guanajuato", "Guanajuato"]],
	13: [17.55, -99.5, ["ゲレロ州", "Guerrero", "Guerrero", "Guerrero", "Guerrero", "Guerrero", "Guerrero"]],
	14: [20.1166667, -98.7333333, ["イダルゴ州", "Hidalgo", "Hidalgo", "Hidalgo", "Hidalgo", "Hidalgo", "Hidalgo"]],
	15: [20.6666667, -103.3333333, ["ハリスコ州", "Jalisco", "Jalisco", "Jalisco", "Jalisco", "Jalisco", "Jalisco"]],
	16: [19.2883333, -99.6672222, ["メヒコ州", "México", "México", "Mexico", "México", "Messico", "Mexico"]],
	17: [19.7, -101.1166667, ["ミチョアカン州", "Michoacán de Ocampo", "Michoacán", "Michoacán", "Michoacán de Ocampo", "Michoacán", "Michoacán de Ocampo"]],
	18: [18.9166667, -99.25, ["モレロス州", "Morelos", "Morelos", "Morelos", "Morelos", "Morelos", "Morelos"]],
	19: [21.5, -104.9, ["ナヤリット州", "Nayarit", "Nayarit", "Nayarit", "Nayarit", "Nayarit", "Nayarit"]],
	20: [25.6666667, -100.3166667, ["ヌエボ・レオン州", "Nuevo León", "Nuevo León", "Nuevo León", "Nuevo León", "Nuevo León", "Nieuw-León"]],
	21: [17.05, -96.7166667, ["オアハカ州", "Oaxaca", "Oaxaca", "Oaxaca", "Oaxaca", "Oaxaca", "Oaxaca"]],
	22: [19.05, -98.2, ["プエブラ州", "Puebla", "Puebla", "Puebla", "Puebla", "Puebla", "Puebla"]],
	23: [20.6, -100.3833333, ["ケレタロ州", "Querétaro de Arteaga", "Querétaro", "Querétaro", "Querétaro de Arteaga", "Querétaro", "Querétaro de Arteaga"]],
	24: [18.5, -88.3, ["キンタナ・ロー州", "Quintana Roo", "Quintana Roo", "Quintana Roo", "Quintana Roo", "Quintana Roo", "Quintana Roo"]],
	25: [22.15, -100.9833333, ["サン・ルイス・ポトシ州", "San Luis Potosí", "San Luis Potosí", "San Luis Potosí", "San Luis Potosí", "San Luis Potosí", "San Luis Potosí"]],
	26: [24.7994444, -107.3897222, ["シナロア州", "Sinaloa", "Sinaloa", "Sinaloa", "Sinaloa", "Sinaloa", "Sinaloa"]],
	27: [29.0666667, -110.9666667, ["ソノラ州", "Sonora", "Sonora", "Sonora", "Sonora", "Sonora", "Sonora"]],
	28: [17.9833333, -92.9166667, ["タバスコ州", "Tabasco", "Tabasco", "Tabasco", "Tabasco", "Tabasco", "Tabasco"]],
	29: [23.7333333, -99.1333333, ["タマウリパス州", "Tamaulipas", "Tamaulipas", "Tamaulipas", "Tamaulipas", "Tamaulipas", "Tamaulipas"]],
	30: [19.3138889, -98.2416667, ["トラスカラ州", "Tlaxcala", "Tlaxcala", "Tlaxcala", "Tlaxcala", "Tlaxcala", "Tlaxcala"]],
	31: [19.5333333, -96.9166667, ["ベラクルス州", "Veracruz-Llave", "Veracruz", "Veracruz", "Veracruz-Llave", "Veracruz", "Veracruz"]],
	32: [20.9666667, -89.6166667, ["ユカタン州", "Yucatán", "Yukatan", "Yucatán", "Yucatán", "Yucatán", "Yucatán"]],
	33: [22.7833333, -102.5833333, ["サカテカス州", "Zacatecas", "Zacatecas", "Zacatecas", "Zacatecas", "Zacatecas", "Zacatecas"]]
}

regioninfo_037 = {
	1: [16.7, -62.2166667, ["モントセラト", "Montserrat", "Montserrat", "Montserrat", "Montserrat", "Montserrat", "Montserrat"]]
}

regioninfo_038 = {
	1: [12.1, -68.9166667, ["オランダ領アンティル", "Netherlands Antilles", "Niederländische Antillen", "Antilles néerlandaises", "Antillas Neerlandesas", "Antille Olandesi", "Nederlandse Antillen"]]
}

regioninfo_039 = {
	1: [0, 0, ["ニカラグア", "Nicaragua", "Nicaragua", "Nicaragua", "Nicaragua", "Nicaragua", "Nicaragua"]],
	2: [12.1508333, -86.2683333, ["マナグア", "Managua", "Managua", "Managua", "Managua", "Managua", "Managua"]],
	3: [12.4666667, -85.6666667, ["ボアコ", "Boaco", "Boaco", "Boaco", "Boaco", "Boaco", "Boaco"]],
	4: [11.85, -86.2, ["カラソ", "Carazo", "Carazo", "Carazo", "Carazo", "Carazo", "Carazo"]],
	5: [12.6166667, -87.15, ["チナンデガ", "Chinandega", "Chinandega", "Chinandega", "Chinandega", "Chinandega", "Chinandega"]],
	6: [12.0833333, -85.4, ["チョンタレス", "Chontales", "Chontales", "Chontales", "Chontales", "Chontales", "Chontales"]],
	7: [13.0833333, -86.35, ["エステリ", "Estelí", "Estelí", "Estelí", "Estelí", "Estelí", "Estelí"]],
	8: [11.9333333, -85.95, ["グラナダ", "Granada", "Granada", "Granada", "Granada", "Granada", "Granada"]],
	9: [13.1, -86, ["ヒノテガ", "Jinotega", "Jinotega", "Jinotega", "Jinotega", "Jinotega", "Jinotega"]],
	10: [12.4355556, -86.8794444, ["レオン", "León", "León", "León", "León", "León", "León"]],
	11: [13.4833333, -86.5833333, ["マドリス", "Madriz", "Madriz", "Madriz", "Madriz", "Madriz", "Madriz"]],
	12: [11.9666667, -86.1, ["マサヤ", "Masaya", "Masaya", "Masaya", "Masaya", "Masaya", "Masaya"]],
	13: [12.9166667, -85.9166667, ["マタガルパ", "Matagalpa", "Matagalpa", "Matagalpa", "Matagalpa", "Matagalpa", "Matagalpa"]],
	14: [13.6333333, -86.4833333, ["ヌエバ・セゴビア", "Nueva Segovia", "Nueva Segovia", "Nueva Segovia", "Nueva Segovia", "Nueva Segovia", "Nueva Segovia"]],
	15: [11.1166667, -84.7833333, ["リオ・サン・フアン", "Río San Juan", "Río San Juan", "Río San Juan", "Río San Juan", "Río San Juan", "Río San Juan"]],
	16: [11.4333333, -85.8333333, ["リバス", "Rivas", "Rivas", "Rivas", "Rivas", "Rivas", "Rivas"]],
	17: [14.0333333, -83.3833333, ["北アトランティコ自治地域", "Atlántico Norte", "Región Autónoma del Atlántico Norte", "Atlantique-Nord", "Atlántico Norte", "Regione Autonoma dell'Atlantico del Nord", "Atlántico Norte"]],
	18: [12, -83.75, ["南アトランティコ自治地域", "Atlántico Sur", "Región Autónoma del Atlántico Sur", "Atlantique-Sud", "Atlántico Sur", "Regione Autonoma dell'Atlantico del Sud", "Atlántico Sur"]]
}

regioninfo_040 = {
	1: [0, 0, ["パナマ", "Panama", "Panama", "Panama", "Panamá", "Panamá", "Panama"]],
	2: [8.9666667, -79.5333333, ["パナマ", "Panamá", "Panama", "Panama", "Panamá", "Panamá", "Panama"]],
	3: [9.3333333, -82.25, ["ボカズ・デル・トーロ", "Bocas del Toro", "Bocas del Toro", "Bocas del Toro", "Bocas del Toro", "Bocas del Toro", "Bocas del Toro"]],
	4: [8.4333333, -82.4333333, ["チリキ", "Chiriquí", "Chiriquí", "Chiriqui", "Chiriquí", "Chiriquí", "Chiriquí"]],
	5: [8.5166667, -80.3666667, ["コクレ", "Coclé", "Coclé", "Coclé", "Coclé", "Coclé", "Coclé"]],
	6: [9.3591667, -79.9013889, ["コロン", "Colón", "Colón", "Colón", "Colón", "Colón", "Colón"]],
	7: [8.4027778, -78.1452778, ["ダリエン", "Darién", "Darién", "Darién", "Darién", "Darién", "Darién"]],
	8: [7.9666667, -80.4333333, ["エレーラ", "Herrera", "Herrera", "Herrera", "Herrera", "Herrera", "Herrera"]],
	9: [7.7666667, -80.2833333, ["ロス・サントス", "Los Santos", "Los Santos", "Los Santos", "Los Santos", "Los Santos", "Los Santos"]],
	10: [9.5652778, -78.9533333, ["サンブラス諸島", "San Blas", "Kuna Yala", "San Blas", "San Blas", "San Blas", "San Blas-eilanden"]],
	11: [8.1, -80.9833333, ["ベラグアス", "Veraguas", "Veraguas", "Veraguas", "Veraguas", "Veraguas", "Veraguas"]]
}

regioninfo_041 = {
	1: [0, 0, ["パラグアイ", "Paraguay", "Paraguay", "Paraguay", "Paraguay", "Paraguay", "Paraguay"]],
	2: [-25.2666667, -57.6666667, ["セントラル県", "Central", "Central", "Central", "Central", "Central", "Central"]],
	3: [-25.5, -54.8333333, ["アルト・パラナ県", "Alto Paraná", "Alto Paraná", "Haut-Paraná", "Alto Paraná", "Alto Paraná", "Alto Paraná"]],
	4: [-23, -56, ["アマンバイ県", "Amambay", "Amambay", "Amambay", "Amambay", "Amambay", "Amambay"]],
	5: [-25.4166667, -56.45, ["カアグアスー県", "Caaguazú", "Caaguazú", "Caaguazú", "Caaguazú", "Caaguazú", "Caaguazú"]],
	6: [-26.1666667, -56, ["カアサパ県", "Caazapá", "Caazapá", "Caazapá", "Caazapá", "Caazapá", "Caazapá"]],
	7: [-23.4063889, -57.4344444, ["コンセプシオン県", "Concepción", "Concepción", "Concepción", "Concepción", "Concepción", "Concepción"]],
	8: [-25.3833333, -57.15, ["コルディリェラ県", "Cordillera", "Cordillera", "Cordillera", "Cordillera", "Cordillera", "Cordillera"]],
	9: [-25.75, -56.4333333, ["グアイラー県", "Guairá", "Guairá", "Guairá", "Guairá", "Guairá", "Guairá"]],
	10: [-27.3333333, -55.9, ["イタプア県", "Itapúa", "Itapúa", "Itapua", "Itapúa", "Itapúa", "Itapúa"]],
	11: [-27, -57, ["ミシオネス県", "Misiones", "Misiones", "Misiones", "Misiones", "Misiones", "Misiones"]],
	12: [-27, -58, ["ニェエンブク県", "Ñeembucú", "Ñeembucú", "Ñeembucú", "Ñeembucú", "Ñeembucú", "Ñeembucú"]],
	13: [-25.6333333, -57.15, ["パラグアリ県", "Paraguarí", "Paraguarí", "Paraguari", "Paraguarí", "Paraguarí", "Paraguarí"]],
	14: [-23.5, -58.8333333, ["プレジデンテ・アエス県", "Presidente Hayes", "Presidente Hayes", "Presidente Hayes", "Presidente Hayes", "Presidente Hayes", "Presidente Hayes"]],
	15: [-24.1, -57.0833333, ["サン・ペドロ県", "San Pedro", "San Pedro", "San Pedro", "San Pedro", "San Pedro", "San Pedro"]],
	16: [-24.05, -54.35, ["カニンデジュ県", "Canindeyú", "Canindeyú", "Canindeyú", "Canindeyú", "Canindeyú", "Canindeyú"]],
	17: [-25.2666667, -57.6666667, ["アスンシオン市", "Asunción", "Distrito Capital", "Asunción", "Asunción", "Asunción", "Asunción"]],
	18: [-21.0333333, -57.9, ["アルト・パラグアイ県", "Alto Paraguay", "Alto Paraguay", "Haut-Paraguay", "Alto Paraguay", "Alto Paraguay", "Alto Paraguay"]],
	19: [-22.35, -60.0333333, ["ボケロン県", "Boquerón", "Boquerón", "Boquerón", "Boquerón", "Boquerón", "Boquerón"]]
}

regioninfo_042 = {
	1: [0, 0, ["ペルー", "Peru", "Peru", "Pérou", "Perú", "Perù", "Peru"]],
	2: [-12.05, -77.05, ["リマ", "Lima", "Lima Metropolitana", "Province de Lima", "Lima", "Provincia di Lima", "Lima"]],
	3: [-6.2166667, -77.85, ["アマソナス", "Amazonas", "Amazonas", "Amazone", "Amazonas", "Amazonas", "Amazonas"]],
	4: [-9.5333333, -77.5333333, ["アンカッシュ", "Ancash", "Ancash", "Ancash", "Ancash", "Ancash", "Ancash"]],
	5: [-13.6338889, -72.8813889, ["アプリマック", "Apurímac", "Apurímac", "Apurímac", "Apurímac", "Apurímac", "Apurímac"]],
	6: [-16.3988889, -71.535, ["アレキパ", "Arequipa", "Arequipa", "Arequipa", "Arequipa", "Arequipa", "Arequipa"]],
	7: [-13.1583333, -74.2238889, ["アヤクーチョ", "Ayacucho", "Ayacucho", "Ayacucho", "Ayacucho", "Ayacucho", "Ayacucho"]],
	8: [-7.1666667, -78.5166667, ["カハマルカ", "Cajamarca", "Cajamarca", "Cajamarca", "Cajamarca", "Cajamarca", "Cajamarca"]],
	9: [-12.0666667, -77.15, ["カヤオ", "Callao", "Callao", "Callao", "Callao", "Callao", "Callao"]],
	10: [-13.5183333, -71.9780556, ["クスコ", "Cuzco", "Cusco", "Cuzco", "Cuzco", "Cusco", "Cuzco"]],
	11: [-12.7666667, -74.9833333, ["ワンカベリカ", "Huancavelica", "Huancavelica", "Huancavelica", "Huancavelica", "Huancavelica", "Huancavelica"]],
	12: [-9.9166667, -76.2333333, ["ワヌコ", "Huánuco", "Huánuco", "Huanuco", "Huánuco", "Huánuco", "Huánuco"]],
	13: [-14.0680556, -75.7255556, ["イカ", "Ica", "Ica", "Ica", "Ica", "Ica", "Ica"]],
	14: [-12.0666667, -75.2333333, ["フニン", "Junín", "Junín", "Junín", "Junín", "Junín", "Junín"]],
	15: [-8.1119444, -79.0255556, ["ラ・リベルター", "La Libertad", "La Libertad", "La Libertad", "La Libertad", "La Libertad", "La Libertad"]],
	16: [-6.7736111, -79.8416667, ["ランバイェケ", "Lambayeque", "Lambayeque", "Lambayeque", "Lambayeque", "Lambayeque", "Lambayeque"]],
	17: [-3.7480556, -73.2472222, ["ロレト", "Loreto", "Loreto", "Loreto", "Loreto", "Loreto", "Loreto"]],
	18: [-12.6, -69.1833333, ["マドレ・デ・ディオス", "Madre de Dios", "Madre de Dios", "Madre de Dios", "Madre de Dios", "Madre de Dios", "Madre de Dios"]],
	19: [-17.1955556, -70.9352778, ["モケグア", "Moquegua", "Moquegua", "Moquegua", "Moquegua", "Moquegua", "Moquegua"]],
	20: [-10.6833333, -76.2666667, ["パスコ", "Pasco", "Pasco", "Pasco", "Pasco", "Pasco", "Pasco"]],
	21: [-5.2, -80.6333333, ["ピウラ", "Piura", "Piura", "Piura", "Piura", "Piura", "Piura"]],
	22: [-15.8333333, -70.0333333, ["プーノ", "Puno", "Puno", "Puno", "Puno", "Puno", "Puno"]],
	23: [-6.05, -76.9666667, ["サン・マルティン", "San Martín", "San Martín", "San Martín", "San Martín", "San Martín", "San Martín"]],
	24: [-18.0055556, -70.2483333, ["タクナ", "Tacna", "Tacna", "Tacna", "Tacna", "Tacna", "Tacna"]],
	25: [-3.5666667, -80.4413889, ["トゥンベス", "Tumbes", "Tumbes", "Tumbes", "Tumbes", "Tumbes", "Tumbes"]],
	26: [-8.3825, -74.5380556, ["ウカヤリ", "Ucayali", "Ucayali", "Ucayali", "Ucayali", "Ucayali", "Ucayali"]]
}

regioninfo_043 = {
	1: [0, 0, ["セントキッツ・ネイビス", "St. Kitts and Nevis", "St. Kitts und Nevis", "Saint-Kitts-et-Nevis", "San Cristóbal y Nieves", "Saint Kitts e Nevis", "Saint Kitts en Nevis"]],
	2: [17.3, -62.7166667, ["セント・ジョージ・バセテール", "Saint George Basseterre", "Saint George Basseterre", "Saint-George Basseterre", "Saint George Basseterre", "Saint George Basseterre", "Saint George Basseterre"]],
	3: [17.3666667, -62.75, ["クライスト・チャーチ・ニコラタウン", "Christ Church Nichola Town", "Christ Church Nichola Town", "Christ Church Nichola Town", "Christ Church Nichola Town", "Christ Church Nichola Town", "Christ Church Nichola Town"]],
	4: [17.35, -62.8333333, ["セント・アン・サンディ・ポイント", "Saint Anne Sandy Point", "Saint Anne Sandy Point", "Sainte-Anne Sandy Point", "Saint Anne Sandy Point", "Saint Anne Sandy Point", "Saint Anne Sandy Point"]],
	5: [17.1333333, -62.55, ["セント・ジョージ・ジンジャーランド", "Saint George Gingerland", "Saint George Gingerland", "Saint-George Gingerland", "Saint George Gingerland", "Saint George Gingerland", "Saint George Gingerland"]],
	6: [17.2, -62.5833333, ["セント・ジェームズ・ウィンドワード", "Saint James Windward", "Saint James Windward", "Saint-Jacques Windward", "Saint James Windward", "Saint James Windward", "Saint James Windward"]],
	7: [17.4, -62.7833333, ["セント・ジョン・カピステール", "Saint John Capesterre", "Saint John Capesterre", "Saint-Jean Capisterre", "Saint John Capesterre", "Saint John Capesterre", "Saint John Capesterre"]],
	8: [17.1166667, -62.6, ["セント・ジョン・フィッグトリー", "Saint John Figtree", "Saint John Figtree", "Saint-Jean Figtree", "Saint John Figtree", "Saint John Figtree", "Saint John Figtree"]],
	9: [17.35, -62.7333333, ["セント・メリー・ケーヨン", "Saint Mary Cayon", "Saint Mary Cayon", "Sainte-Marie Cayon", "Saint Mary Cayon", "Saint Mary Cayon", "Saint Mary Cayon"]],
	10: [17.4, -62.8166667, ["セント・ポール・カピステール", "Saint Paul Capesterre", "Saint Paul Capesterre", "Saint-Paul Capisterre", "Saint Paul Capesterre", "Saint Paul Capesterre", "Saint Paul Capesterre"]],
	11: [17.1333333, -62.6166667, ["セント・ポール・チャールズタウン", "Saint Paul Charlestown", "Saint Paul Charlestown", "Saint-Paul Charlestown", "Saint Paul Charlestown", "Saint Paul Charlestown", "Saint Paul Charlestown"]],
	12: [17.3166667, -62.7166667, ["セント・ピーター・バセテール", "Saint Peter Basseterre", "Saint Peter Basseterre", "Saint-Pierre Basseterre", "Saint Peter Basseterre", "Saint Peter Basseterre", "Saint Peter Basseterre"]],
	13: [17.1666667, -62.6166667, ["セント・トーマス・ロウランド", "Saint Thomas Lowland", "Saint Thomas Lowland", "Saint-Thomas Lowland", "Saint Thomas Lowland", "Saint Thomas Lowland", "Saint Thomas Lowland"]],
	14: [17.3166667, -62.8166667, ["セント・トーマス・ミドルアイランド", "Saint Thomas Middle Island", "Saint Thomas Middle Island", "Saint-Thomas Middle Island", "Saint Thomas Middle Island", "Saint Thomas Middle Island", "Saint Thomas Middle Island"]],
	15: [17.2833333, -62.7666667, ["トリニティ・パルメット・ポイント", "Trinity Palmetto Point", "Trinity Palmetto Point", "Trinity Palmetto Point", "Trinity Palmetto Point", "Trinity Palmetto Point", "Trinity Palmetto Point"]]
}

regioninfo_044 = {
	1: [14, -61, ["セントルシア", "St. Lucia", "St. Lucia", "Sainte-Lucie", "Santa Lucía", "Santa Lucia", "Saint Lucia"]]
}

regioninfo_045 = {
	1: [13.1333333, -61.2166667, ["セントビンセント・グレナディーン", "St. Vincent and the Grenadines", "St. Vincent und die Grenadinen", "Saint-Vincent-et-les-Grenadines", "San Vicente y las Granadinas", "Saint Vincent e Grenadine", "Saint Vincent en de Grenadines"]]
}

regioninfo_046 = {
	1: [0, 0, ["スリナム", "Suriname", "Suriname", "Suriname", "Surinam", "Suriname", "Suriname"]],
	2: [5.8333333, -55.1666667, ["パラマリボ", "Paramaribo", "Paramaribo", "Paramaribo", "Paramaribo", "Paramaribo", "Paramaribo"]],
	3: [5.0666667, -54.9666667, ["ブロコポンド", "Brokopondo", "Brokopondo", "Brokopondo", "Brokopondo", "Brokopondo", "Brokopondo"]],
	4: [5.8833333, -55.0833333, ["コメウィネ", "Commewijne", "Commewijne", "Commewijne", "Commewijne", "Commewijne", "Commewijne"]],
	5: [5.8833333, -56.3166667, ["コロニー", "Coronie", "Coronie", "Coronie", "Coronie", "Coronie", "Coronie"]],
	6: [5.5, -54.05, ["マロウィネ", "Marowijne", "Marowijne", "Marowijne", "Marowijne", "Marowijne", "Marowijne"]],
	7: [5.95, -56.9833333, ["ニッケリー", "Nickerie", "Nickerie", "Nickerie", "Nickerie", "Nickerie", "Nickerie"]],
	8: [5.5833333, -55.1833333, ["パラ", "Para", "Para", "Para", "Para", "Para", "Para"]],
	9: [5.8, -55.4666667, ["サラマッカ", "Saramacca", "Saramacca", "Saramacca", "Saramacca", "Saramacca", "Saramacca"]],
	10: [5.2, -57.1666667, ["シパリウィニ", "Sipaliwini", "Sipaliwini", "Sipaliwini", "Sipaliwini", "Sipaliwini", "Sipaliwini"]],
	11: [5.7, -55.2333333, ["ワニカ", "Wanica", "Wanica", "Wanica", "Wanica", "Wanica", "Wanica"]]
}

regioninfo_047 = {
	1: [0, 0, ["トリニダード・トバゴ", "Trinidad and Tobago", "Trinidad und Tobago", "Trinité-et-Tobago", "Trinidad y Tobago", "Trinidad e Tobago", "Trinidad en Tobago"]],
	2: [10.65, -61.5166667, ["ポート・オブ・スペイン", "Port-of-Spain", "Port-of-Spain", "Port d'Espagne", "Puerto España", "Port of Spain", "Port of Spain"]],
	3: [10.6333333, -61.2833333, ["アリマ", "Arima", "Arima", "Arima", "Arima", "Arima", "Arima"]],
	4: [10.5166667, -61.4166667, ["カロニ州", "Caroni", "Caroni", "Caroni", "Caroni", "Caroni", "Caroni"]],
	5: [10.21666667, -61, ["マジャロ州", "Mayaro", "Mayaro", "Mayaro", "Mayaro", "Mayaro", "Mayaro"]],
	6: [10.3, -61.1833333, ["ナリバ州", "Nariva", "Nariva", "Nariva", "Nariva", "Nariva", "Nariva"]],
	7: [10.5833333, -61.1166667, ["セント・アンドリュー州", "Saint Andrew", "Saint Andrew", "Saint Andrew", "Saint Andrew", "Saint Andrew", "Saint Andrew"]],
	8: [10.8, -61.01666667, ["セント・デビッド州", "Saint David", "Saint David", "Saint David", "Saint David", "Saint David", "Saint David"]],
	9: [10.6333333, -61.3833333, ["セント・ジョージ州", "Saint George", "Saint George", "Saint George", "Saint George", "Saint George", "Saint George"]],
	10: [10.1833333, -61.6833333, ["セント・パトリック州", "Saint Patrick", "Saint Patrick", "Saint Patrick", "Saint Patrick", "Saint Patrick", "Saint Patrick"]],
	11: [10.2833333, -61.4666667, ["サン・フェルナンド", "San Fernando", "San Fernando", "San Fernando", "San Fernando", "San Fernando", "San Fernando"]],
	12: [11.1833333, -60.7333333, ["トバゴ島", "Tobago", "Tobago", "Tobago", "Tobago", "Tobago", "Tobago"]],
	13: [10.2666667, -61.3833333, ["ビクトリア州", "Victoria", "Victoria", "Victoria", "Victoria", "Victoria", "Victoria"]]
}

regioninfo_048 = {
	1: [21.4666667, -71.1333333, ["タークス・カイコス諸島", "Turks and Caicos Islands", "Turks- und Caicosinseln", "Iles Turques et Caïques", "Islas Turcas y Caicos", "Isole Turks e Caicos", "Turks- en Caicoseilanden"]]
}

regioninfo_049 = {
	1: [0, 0, ["アメリカ", "United States", "Vereinigte Staaten", "Etats-Unis d’Amérique", "Estados Unidos de América", "Stati Uniti d'America", "Verenigde Staten"]],
	2: [38.895, -77.03667, ["コロンビア特別区", "District of Columbia", "District of Columbia", "District Fédéral de Washington D.C.", "Distrito de Columbia", "Distretto di Columbia", "District of Columbia"]],
	3: [58.30194, -134.41972, ["アラスカ州", "Alaska", "Alaska", "Alaska", "Alaska", "Alaska", "Alaska"]],
	4: [32.36667, -86.3, ["アラバマ州", "Alabama", "Alabama", "Alabama", "Alabama", "Alabama", "Alabama"]],
	5: [34.74639, -92.28944, ["アーカンソー州", "Arkansas", "Arkansas", "Arkansas", "Arkansas", "Arkansas", "Arkansas"]],
	6: [33.44833, -112.07333, ["アリゾナ州", "Arizona", "Arizona", "Arizona", "Arizona", "Arizona", "Arizona"]],
	7: [38.58167, -121.49333, ["カリフォルニア州", "California", "Kalifornien", "Californie", "California", "California", "Californië"]],
	8: [39.73917, -104.98417, ["コロラド州", "Colorado", "Colorado", "Colorado", "Colorado", "Colorado", "Colorado"]],
	9: [41.76361, -72.68556, ["コネティカット州", "Connecticut", "Connecticut", "Connecticut", "Connecticut", "Connecticut", "Connecticut"]],
	10: [39.15806, -75.52472, ["デラウェア州", "Delaware", "Delaware", "Delaware", "Delaware", "Delaware", "Delaware"]],
	11: [30.43806, -84.28083, ["フロリダ州", "Florida", "Florida", "Floride", "Florida", "Florida", "Florida"]],
	12: [33.74889, -84.38806, ["ジョージア州", "Georgia", "Georgia", "Géorgie", "Georgia", "Georgia", "Georgia"]],
	13: [21.30694, -157.85833, ["ハワイ州", "Hawaii", "Hawaii", "Hawaï", "Hawai", "Hawaii", "Hawaï"]],
	14: [41.60056, -93.60889, ["アイオワ州", "Iowa", "Iowa", "Iowa", "Iowa", "Iowa", "Iowa"]],
	15: [43.61361, -116.2025, ["アイダホ州", "Idaho", "Idaho", "Idaho", "Idaho", "Idaho", "Idaho"]],
	16: [39.80167, -89.64361, ["イリノイ州", "Illinois", "Illinois", "Illinois", "Illinois", "Illinois", "Illinois"]],
	17: [39.76833, -86.15806, ["インディアナ州", "Indiana", "Indiana", "Indiana", "Indiana", "Indiana", "Indiana"]],
	18: [39.04833, -95.67778, ["カンザス州", "Kansas", "Kansas", "Kansas", "Kansas", "Kansas", "Kansas"]],
	19: [38.20083, -84.87333, ["ケンタッキー州", "Kentucky", "Kentucky", "Kentucky", "Kentucky", "Kentucky", "Kentucky"]],
	20: [30.45056, -91.15444, ["ルイジアナ州", "Louisiana", "Louisiana", "Louisiane", "Luisiana", "Louisiana", "Louisiana"]],
	21: [42.35833, -71.06028, ["マサチューセッツ州", "Massachusetts", "Massachusetts", "Massachusetts", "Massachusetts", "Massachusetts", "Massachusetts"]],
	22: [38.97833, -76.4925, ["メリーランド州", "Maryland", "Maryland", "Maryland", "Maryland", "Maryland", "Maryland"]],
	23: [44.31056, -69.78, ["メーン州", "Maine", "Maine", "Maine", "Maine", "Maine", "Maine"]],
	24: [42.7325, -84.55556, ["ミシガン州", "Michigan", "Michigan", "Michigan", "Michigan", "Michigan", "Michigan"]],
	25: [44.94444, -93.09306, ["ミネソタ州", "Minnesota", "Minnesota", "Minnesota", "Minnesota", "Minnesota", "Minnesota"]],
	26: [38.57667, -92.17333, ["ミズーリ州", "Missouri", "Missouri", "Missouri", "Misuri", "Missouri", "Missouri"]],
	27: [32.29861, -90.18472, ["ミシシッピ州", "Mississippi", "Mississippi", "Mississippi", "Mississippi", "Mississippi", "Mississippi"]],
	28: [46.59278, -112.03528, ["モンタナ州", "Montana", "Montana", "Montana", "Montana", "Montana", "Montana"]],
	29: [35.77194, -78.63889, ["ノースカロライナ州", "North Carolina", "Nordkarolina", "Caroline du Nord", "Carolina del Norte", "Carolina del Nord", "Noord-Carolina"]],
	30: [46.80833, -100.78333, ["ノースダコタ州", "North Dakota", "Norddakota", "Dakota du Nord", "Dakota del Norte", "Dakota del Nord", "Noord-Dakota"]],
	31: [40.8, -96.66667, ["ネブラスカ州", "Nebraska", "Nebraska", "Nebraska", "Nebraska", "Nebraska", "Nebraska"]],
	32: [43.20806, -71.53806, ["ニューハンプシャー州", "New Hampshire", "New Hampshire", "New Hampshire", "Nuevo Hampshire", "New Hampshire", "New Hampshire"]],
	33: [40.21694, -74.74333, ["ニュージャージー州", "New Jersey", "New Jersey", "New Jersey", "Nueva Jersey", "New Jersey", "New Jersey"]],
	34: [35.68694, -105.93722, ["ニューメキシコ州", "New Mexico", "New Mexico", "Nouveau-Mexique", "Nuevo México", "Nuovo Messico", "New Mexico"]],
	35: [39.16389, -119.76639, ["ネバダ州", "Nevada", "Nevada", "Nevada", "Nevada", "Nevada", "Nevada"]],
	36: [42.6525, -73.75667, ["ニューヨーク州", "New York", "New York", "New York", "Nueva York", "New York", "New York"]],
	37: [39.96111, -82.99889, ["オハイオ州", "Ohio", "Ohio", "Ohio", "Ohio", "Ohio", "Ohio"]],
	38: [35.4675, -97.51611, ["オクラホマ州", "Oklahoma", "Oklahoma", "Oklahoma", "Oklahoma", "Oklahoma", "Oklahoma"]],
	39: [44.94306, -123.03389, ["オレゴン州", "Oregon", "Oregon", "Oregon", "Oregón", "Oregon", "Oregon"]],
	40: [40.27361, -76.88472, ["ペンシルベニア州", "Pennsylvania", "Pennsylvania", "Pennsylvanie", "Pensilvania", "Pennsylvania", "Pennsylvania"]],
	41: [41.82389, -71.41333, ["ロードアイランド州", "Rhode Island", "Rhode Island", "Rhode Island", "Rhode Island", "Rhode Island", "Rhode Island"]],
	42: [34.00056, -81.035, ["サウスカロライナ州", "South Carolina", "Südkarolina", "Caroline du Sud", "Carolina del Sur", "Carolina del Sud", "Zuid-Carolina"]],
	43: [44.36833, -100.35056, ["サウスダコタ州", "South Dakota", "Süddakota", "Dakota du Sud", "Dakota del Sur", "Dakota del Sud", "Zuid-Dakota"]],
	44: [36.16583, -86.78444, ["テネシー州", "Tennessee", "Tennessee", "Tennessee", "Tennessee", "Tennessee", "Tennessee"]],
	45: [30.26694, -97.74278, ["テキサス州", "Texas", "Texas", "Texas", "Texas", "Texas", "Texas"]],
	46: [40.76083, -111.89028, ["ユタ州", "Utah", "Utah", "Utah", "Utah", "Utah", "Utah"]],
	47: [37.55361, -77.46056, ["バージニア州", "Virginia", "Virginia", "Virginie", "Virginia", "Virginia", "Virginia"]],
	48: [44.26, -72.57583, ["バーモント州", "Vermont", "Vermont", "Vermont", "Vermont", "Vermont", "Vermont"]],
	49: [47.03806, -122.89944, ["ワシントン州", "Washington", "Washington", "Washington", "Washington", "Washington", "Washington"]],
	50: [43.07306, -89.40111, ["ウィスコンシン州", "Wisconsin", "Wisconsin", "Wisconsin", "Wisconsin", "Wisconsin", "Wisconsin"]],
	51: [38.34972, -81.63278, ["ウェストバージニア州", "West Virginia", "West Virginia", "Virginie Occidentale", "Virginia Occidental", "Virginia Occidentale", "West Virginia"]],
	52: [41.14, -104.81972, ["ワイオミング州", "Wyoming", "Wyoming", "Wyoming", "Wyoming", "Wyoming", "Wyoming"]],
	53: [18.46833, -66.10611, ["プエルトリコ", "Puerto Rico", "Puerto Rico", "Porto Rico", "Puerto Rico", "Porto Rico", "Puerto Rico"]]
}

regioninfo_050 = {
	1: [0, 0, ["ウルグアイ", "Uruguay", "Uruguay", "Uruguay", "Uruguay", "Uruguay", "Uruguay"]],
	2: [-34.8580556, -56.1708333, ["モンテビデオ", "Montevideo", "Montevideo", "Montevideo", "Montevideo", "Montevideo", "Montevideo"]],
	3: [-30.4, -56.4666667, ["アルティガス", "Artigas", "Artigas", "Artigas", "Artigas", "Artigas", "Artigas"]],
	4: [-34.5227778, -56.2777778, ["カネロネス", "Canelones", "Canelones", "Canelones", "Canelones", "Canelones", "Canelones"]],
	5: [-32.3666667, -54.1833333, ["セロ・ラルゴ", "Cerro Largo", "Cerro Largo", "Cerro Largo", "Cerro Largo", "Cerro Largo", "Cerro Largo"]],
	6: [-34.4666667, -57.85, ["コロニア", "Colonia", "Colonia", "Colonia", "Colonia", "Colonia", "Colonia"]],
	7: [-33.4130556, -56.5005556, ["ドゥラスノ", "Durazno", "Durazno", "Durazno", "Durazno", "Durazno", "Durazno"]],
	8: [-33.5388889, -56.8886111, ["フロレス", "Flores", "Flores", "Flores", "Flores", "Flores", "Flores"]],
	9: [-34.0955556, -56.2141667, ["フロリダ", "Florida", "Florida", "Florida", "Florida", "Florida", "Florida"]],
	10: [-34.37, -55.225, ["ラバジェハ", "Lavalleja", "Lavalleja", "Lavalleja", "Lavalleja", "Lavalleja", "Lavalleja"]],
	11: [-34.9, -54.95, ["マルドナド", "Maldonado", "Maldonado", "Maldonado", "Maldonado", "Maldonado", "Maldonado"]],
	12: [-32.3213889, -58.0755556, ["パイサンドゥ", "Paysandú", "Paysandú", "Paysandú", "Paysandú", "Paysandú", "Paysandú"]],
	13: [-33.1325, -58.2955556, ["リオ・ネグロ", "Río Negro", "Río Negro", "Río Negro", "Río Negro", "Río Negro", "Río Negro"]],
	14: [-30.9, -55.5166667, ["リベラ", "Rivera", "Rivera", "Rivera", "Rivera", "Rivera", "Rivera"]],
	15: [-34.4833333, -54.3333333, ["ロチャ", "Rocha", "Rocha", "Rocha", "Rocha", "Rocha", "Rocha"]],
	16: [-31.3833333, -57.9666667, ["サルト", "Salto", "Salto", "Salto", "Salto", "Salto", "Salto"]],
	17: [-34.3375, -56.7136111, ["サン・ホセ", "San José", "San José", "San José", "San José", "San José", "San José"]],
	18: [-33.2558333, -58.0191667, ["ソリアノ", "Soriano", "Soriano", "Soriano", "Soriano", "Soriano", "Soriano"]],
	19: [-31.7333333, -55.9833333, ["タクアレンボ", "Tacuarembó", "Tacuarembó", "Tacuarembo", "Tacuarembó", "Tacuarembó", "Tacuarembó"]],
	20: [-33.2333333, -54.3833333, ["トレインタ・イ・トレス", "Treinta y Tres", "Treinta y Tres", "Treinta y Tres", "Treinta y Tres", "Treinta y Tres", "Treinta y Tres"]]
}

regioninfo_051 = {
	1: [18.34389, -64.93111, ["米領バージン諸島", "US Virgin Islands", "Amerikanische Jungferninseln", "Iles Vierges américaines", "Islas Vírgenes Americanas", "Isole Vergini Statunitensi", "Amerikaanse Maagdeneilanden"]]
}

regioninfo_052 = {
	1: [0, 0, ["ベネズエラ", "Venezuela", "Venezuela", "Venezuela", "Venezuela", "Venezuela", "Venezuela"]],
	2: [10.5, -66.9166667, ["ディストリト首都地区", "Distrito Federal", "Bundesdistrikt", "District Fédéral", "Distrito Federal", "Distretto Federale", "Hoofdstedelijk District"]],
	3: [5.6638889, -67.6236111, ["アマソナス", "Amazonas", "Amazonas", "Amazone", "Amazonas", "Amazonas", "Amazonas"]],
	4: [10.1333333, -64.7, ["アンソアテギ", "Anzoátegui", "Anzoátegui", "Anzoategui", "Anzoátegui", "Anzoátegui", "Anzoátegui"]],
	5: [7.8966667, -67.4672222, ["アプレ", "Apure", "Apure", "Apure", "Apure", "Apure", "Apure"]],
	6: [10.2469444, -67.5958333, ["アラグア", "Aragua", "Aragua", "Aragua", "Aragua", "Aragua", "Aragua"]],
	7: [8.6291667, -70.2072222, ["バリナス", "Barinas", "Barinas", "Barinas", "Barinas", "Barinas", "Barinas"]],
	8: [8.1222222, -63.5497222, ["ボリーバル", "Bolívar", "Bolívar", "Bolívar", "Bolívar", "Bolívar", "Bolívar"]],
	9: [10.1805556, -68.0038889, ["カラボボ", "Carabobo", "Carabobo", "Carabobo", "Carabobo", "Carabobo", "Carabobo"]],
	10: [9.6666667, -68.6, ["コヘデス", "Cojedes", "Cojedes", "Cojedes", "Cojedes", "Cojedes", "Cojedes"]],
	11: [9.0686111, -62.0491667, ["デルタ・アマクロ", "Delta Amacuro", "Delta Amacuro", "Delta Amacuro", "Delta Amacuro", "Delta Amacuro", "Delta Amacuro"]],
	12: [11.4091667, -69.6672222, ["ファルコン", "Falcón", "Falcón", "Falçon", "Falcón", "Falcón", "Falcón"]],
	13: [9.9111111, -67.3583333, ["グアリコ", "Guárico", "Guárico", "Guárico", "Guárico", "Guárico", "Guárico"]],
	14: [10.0738889, -69.3227778, ["ララ", "Lara", "Lara", "Lara", "Lara", "Lara", "Lara"]],
	15: [8.5983333, -71.145, ["メリダ", "Mérida", "Mérida", "Mérida", "Mérida", "Mérida", "Mérida"]],
	16: [10.34214, -67.040329, ["ミランダ", "Miranda", "Miranda", "Miranda", "Miranda", "Miranda", "Miranda"]],
	17: [9.75, -63.1766667, ["モナガス", "Monagas", "Monagas", "Monagas", "Monagas", "Monagas", "Monagas"]],
	18: [11.0333333, -63.8627778, ["ヌエバエスパルタ", "Nueva Esparta", "Nueva Esparta", "Nueva Esparta", "Nueva Esparta", "Nueva Esparta", "Nueva Esparta"]],
	19: [9.05, -69.75, ["ポルトゥゲサ", "Portuguesa", "Portuguesa", "Portuguesa", "Portuguesa", "Portuguesa", "Portuguesa"]],
	20: [10.4666667, -64.1666667, ["スクレ", "Sucre", "Sucre", "Sucre", "Sucre", "Sucre", "Sucre"]],
	21: [7.7669444, -72.225, ["タチラ", "Táchira", "Táchira", "Táchira", "Táchira", "Táchira", "Táchira"]],
	22: [9.3666667, -70.4333333, ["トルヒーヨ", "Trujillo", "Trujillo", "Trujillo", "Trujillo", "Trujillo", "Trujillo"]],
	23: [10.3405556, -68.7372222, ["ヤラクイ", "Yaracuy", "Yaracuy", "Yaracuy", "Yaracuy", "Yaracuy", "Yaracuy"]],
	24: [10.6316667, -71.6405556, ["スリア", "Zulia", "Zulia", "Zulia", "Zulia", "Zulia", "Zulia"]],
	25: [12, -66, ["連邦保護領", "Dependencias Federales", "Dependencias Federales", "Dépendances Fédérales", "Dependencias Federales", "Dependencias Federales", "Federale gebieden"]],
	26: [10.6, -66.9333333, ["バルガス", "Vargas", "Vargas", "Vargas", "Vargas", "Vargas", "Vargas"]]
}

regioninfo_064 = {
	1: [0, 0, ["アルバニア", "Albania", "Albanien", "Albanie", "Albania", "Albania", "Albanië"]],
	2: [41.32583333, 19.82516667, ["ティラナ州", "Tirana", "Tirana", "Tirana", "Tirana", "Tirana", "Tiranë"]],
	3: [40.70583333, 19.9685, ["ベラト州", "Berat", "Berat", "Berat", "Berat", "Berat", "Berat"]],
	4: [41.684, 20.44316667, ["ディブラ州", "Dibër", "Dibra", "Dibër", "Dibër", "Dibër", "Dibër"]],
	5: [41.324, 19.45233333, ["デュラス州", "Durrës", "Durrës", "Durrës", "Durrës", "Durazzo", "Durrës"]],
	6: [41.045, 19.998, ["エルバサン州", "Elbasan", "Elbasan", "Elbasan", "Elbasan", "Elbasan", "Elbasan"]],
	7: [40.72516667, 19.56983333, ["フィエル州", "Fier", "Fier", "Fier", "Fier", "Fier", "Fier"]],
	8: [40.077, 20.148, ["ギロカストラ州", "Gjirokastër", "Gjirokastra", "Gjirokastër", "Gjirokastra", "Argirocastro", "Gjirokastër"]],
	9: [40.61766667, 20.787, ["コルチャ州", "Korcë", "Korça", "Korçë", "Korcë", "Coriza", "Korcë"]],
	10: [42.083, 20.434, ["クケス州", "Kukës", "Kukës", "Kukës", "Kukës", "Kukës", "Kukës"]],
	11: [41.78566667, 19.65216667, ["レジャ州", "Lezhë", "Lezha", "Lezhë", "Lezhë", "Alessio", "Lezhë"]],
	12: [42.074, 19.526, ["シュコドラ州", "Shkodër", "Shkodra", "Shkodër", "Shkodër", "Scutari", "Shkodër"]],
	13: [40.47016667, 19.48683333, ["ヴロラ州", "Vlorë", "Vlora", "Vlorë", "Vlorë", "Valona", "Vlorë"]]
}

regioninfo_065 = {
	1: [0, 0, ["オーストラリア", "Australia", "Australien", "Australie", "Australia", "Australia", "Australië"]],
	2: [-35.34993, 149.041595, ["オーストラリア首都特別地域", "Australian Capital Territory", "Australisches Hauptstadtterritorium", "Territoire de la capitale australienne", "Territorio de la Capital Australiana", "Australian Capital Territory", "Australisch Hoofdstedelijk Territorium"]],
	3: [-33.89158, 151.2417, ["ニューサウスウェールズ州", "New South Wales", "Neusüdwales", "Nouvelle-Galles-du-Sud", "Nueva Gales del Sur", "Nuovo Galles del Sud", "Nieuw-Zuid-Wales"]],
	4: [-12.433, 130.8425, ["ノーザンテリトリー", "Northern Territory", "Nördliches Territorium", "Territoire du Nord", "Territorio del Norte", "Territorio del Nord", "Noordelijk Territorium"]],
	5: [-27.4539, 153.0265, ["クィーンズランド州", "Queensland", "Queensland", "Queensland", "Queensland", "Queensland", "Queensland"]],
	6: [-34.9185, 138.613, ["南オーストラリア州", "South Australia", "Südaustralien", "Australie-Méridionale", "Australia Meridional", "Australia Meridionale", "Zuid-Australië"]],
	7: [-42.8509, 147.291, ["タスマニア州", "Tasmania", "Tasmanien", "Tasmanie", "Tasmania", "Tasmania", "Tasmanië"]],
	8: [-37.8095, 144.965, ["ヴィクトリア州", "Victoria", "Victoria", "Victoria", "Victoria", "Victoria", "Victoria"]],
	9: [-31.933, 115.862, ["西オーストラリア州", "Western Australia", "Westaustralien", "Australie-Occidentale", "Australia Occidental", "Australia Occidentale", "West-Australië"]]
}

regioninfo_066 = {
	1: [0, 0, ["オーストリア", "Austria", "Österreich", "Autriche", "Austria", "Austria", "Oostenrijk"]],
	2: [48.205, 16.3705, ["ウィーン", "Vienna", "Wien", "Vienne", "Viena", "Vienna", "Wenen"]],
	3: [47.85, 16.51666667, ["ブルゲンラント州", "Burgenland", "Burgenland", "Burgenland", "Burgenland", "Burgenland", "Burgenland"]],
	4: [46.61733333, 14.30333333, ["ケルンテン州", "Carinthia", "Kärnten", "Carinthie", "Carintia", "Carinzia", "Karinthië"]],
	5: [48.2, 15.62166667, ["ニーダー・エスターライヒ州", "Lower Austria", "Niederösterreich", "Basse-Autriche", "Baja Austria", "Bassa Austria", "Neder-Oostenrijk"]],
	6: [48.30092, 14.291035, ["オーバー・エスターライヒ州", "Upper Austria", "Oberösterreich", "Haute-Autriche", "Alta Austria", "Alta Austria", "Opper-Oostenrijk"]],
	7: [47.8, 13.03333333, ["ザルツブルク州", "Salzburg", "Salzburg", "Salzbourg", "Salzburgo", "Salisburghese", "Salzburg"]],
	8: [47.06883333, 15.43666667, ["シュタイアーマルク州", "Styria", "Steiermark", "Styrie", "Estiria", "Stiria", "Stiermarken"]],
	9: [47.26666667, 11.38333333, ["ティロル州", "Tyrol", "Tirol", "Tyrol", "Tirol", "Tirolo", "Tirol"]],
	10: [47.504, 9.748, ["フォアアールベルク州", "Vorarlberg", "Vorarlberg", "Vorarlberg", "Vorarlberg", "Vorarlberg", "Vorarlberg"]]
}

regioninfo_067 = {
	1: [0, 0, ["ベルギー", "Belgium", "Belgien", "Belgique", "Bélgica", "Belgio", "België"]],
	2: [50.83983333, 4.37, ["ブリュッセル首都地域圏", "Brussels Region", "Region Brüssel-Hauptstadt", "Région de Bruxelles-Capitale", "Región de Bruselas-Capital", "Regione di Bruxelles", "Brusselse Gewest"]],
	3: [50.83983333, 4.37, ["フランデレン地域圏", "Flanders", "Flandern", "Flandre", "Región de Flandes", "Fiandre", "Vlaanderen"]],
	4: [50.466, 4.866, ["ワロン地域圏", "Wallonia", "Wallonien", "Wallonie", "Región de Valonia", "Vallonia", "Wallonië"]]
}

regioninfo_068 = {
	1: [0, 0, ["ボスニア・ヘルツェゴビナ", "Bosnia & Herzegovina", "Bosnien-Herzegowina", "Bosnie-Herzégovine", "Bosnia-Herzegovina", "Bosnia-Erzegovina", "Bosnië en Herzegovina"]],
	2: [43.85383333, 18.408, ["ボスニア・ヘルツェゴビナ連邦", "Fed. of Bosnia and Herzegovina", "Föderation Bosnien und Herzegowina", "Fédération de Bosnie-Herzégovine", "Federación de Bosnia-Herzegovina", "Federazione di Bosnia-Erzegovina", "Moslim-Kroatische Federatie"]],
	3: [44.771, 17.197, ["セルビア人共和国", "Republika Srpska", "Serbische Republik", "République serbe de Bosnie", "República Serbia", "Repubblica Serba", "Servische Republiek"]],
	4: [44.87016667, 18.80583333, ["ブルチュコ", "Brcko Distrikt", "Brcko-Distrikt", "District de Brcko", "Distrito de Brcko", "Distretto di Brcko", "Brcko-District"]]
}

regioninfo_069 = {
	1: [0, 0, ["ボツワナ", "Botswana", "Botswana", "Botswana", "Botsuana", "Botswana", "Botswana"]],
	2: [-24.65233333, 25.90516667, ["南東地方", "South-East", "South-East", "Sud Est", "Sureste", "Sud-Est", "South-East"]],
	3: [-22.38916667, 26.7065, ["中部地方", "Central", "Central", "Centre", "Central", "Centrale", "Central"]],
	4: [-21.70266667, 21.64116667, ["ガンジ地方", "Ghanzi", "Ghanzi", "Ghanzi", "Ghanzi", "Ghanzi", "Ghanzi"]],
	5: [-26.01666667, 22.397, ["カラガディ地方", "Kgalagadi", "Kgalagadi", "Kgalagadi", "Kgalagadi", "Kgalagadi", "Kgalagadi"]],
	6: [-24.376, 26.152, ["カトレング地方", "Kgatleng", "Kgatleng", "Kgatleng", "Kgatleng", "Kgatleng", "Kgatleng"]],
	7: [-24.40833333, 25.518, ["クウェネング地方", "Kweneng", "Kweneng", "Kweneng", "Kweneng", "Kweneng", "Kweneng"]],
	8: [-21.16933333, 27.5, ["北東地方", "North-East", "North-East", "Nord-Est", "Noreste", "Nord-Est", "North-East"]],
	9: [-19.98983333, 23.41766667, ["ノースウェスト", "North-West", "North-West", "Nord-Ouest", "Noroeste", "Nord-Ovest", "North-West"]],
	10: [-24.97316667, 25.33883333, ["南部地方", "Southern", "Southern", "Southern", "Meridional", "Sud", "Southern"]]
}

regioninfo_070 = {
	1: [0, 0, ["ブルガリア", "Bulgaria", "Bulgarien", "Bulgarie", "Bulgaria", "Bulgaria", "Bulgarije"]],
	2: [42.70783333, 23.30666667, ["ソフィア市", "Sofia City", "Sofia Stadt", "Sofia-Grad", "Ciudad de Sofía", "Sofia", "Sofia-Stad"]],
	3: [42.70783333, 23.30666667, ["ソフィア州", "Sofia Province", "Sofia Region", "Oblast de Sofia", "Provincia de Sofía", "Regione di Sofia", "Sofia (oblast)"]],
	4: [42.02033333, 23.099, ["ブラゴエブグラト州", "Blagoevgrad", "Blagoewgrad", "Blagoevgrad", "Blagoevgrad", "Blagoevgrad", "Blagoevgrad"]],
	5: [43.41816667, 24.62466667, ["プレベン州", "Pleven", "Plewen", "Pleven", "Pleven", "Pleven", "Pleven"]],
	6: [43.992, 22.87566667, ["ビディン州", "Vidin", "Widin", "Vidin", "Vidin", "Vidin", "Vidin"]],
	7: [43.20583333, 27.90216667, ["バルナ州", "Varna", "Warna", "Varna", "Varna", "Varna", "Varna"]],
	8: [42.526, 27.45783333, ["ブルガス州", "Burgas", "Burgas", "Bourgas", "Burgas", "Burgas", "Boergas"]],
	9: [43.57283333, 27.83466667, ["ドブリチ州", "Dobric", "Dobritsch", "Dobritch", "Dobrich", "Dobrich", "Dobritsj"]],
	10: [42.894, 25.312, ["ガブロボ州", "Gabrovo", "Gabrowo", "Gabrovo", "Gabrovo", "Gabrovo", "Gabrovo"]],
	11: [41.936, 25.559, ["ハスコボ州", "Haskovo", "Chaskowo", "Khaskovo", "Haskovo", "Haskovo", "Chaskovo"]],
	12: [42.48883333, 26.5185, ["ヤンボル州", "Yambol", "Jambol", "Yambol", "Yambol", "Yambol", "Jambol"]],
	13: [41.642, 25.38, ["クルジャリ州", "Kardzhali", "Kardschali", "Kardjali", "Kardzhali", "Kardzhali", "Kurdzjali"]],
	14: [42.2875, 22.68983333, ["キュステンディル州", "Kyustendil", "Kjustendil", "Kyoustendil", "Kyustendil", "Kyustendil", "Kjoestendil"]],
	15: [43.1365, 24.717, ["ロベチ州", "Lovech", "Lowetsch", "Lovetch", "Lovech", "Lovech", "Lovetsj"]],
	16: [43.413, 23.237, ["モンタナ州", "Montana", "Montana", "Montana", "Montana", "Montana", "Montana"]],
	17: [42.19166667, 24.33683333, ["パザルジク州", "Pazardzhik", "Pazardschik", "Pazardjik", "Pazardzhik", "Pazardzhik", "Pazardzjik"]],
	18: [42.58766667, 23.00866667, ["ペルニク州", "Pernik", "Pernik", "Pernik", "Pernik", "Pernik", "Pernik"]],
	19: [42.13683333, 24.75916667, ["プロブディフ州", "Plovdiv", "Plowdiw", "Plovdiv", "Plovdiv", "Plovdiv", "Plovdiv"]],
	20: [43.5335, 26.53466667, ["ラズグラド州", "Razgrad", "Rasgrad", "Razgrad", "Razgrad", "Razgrad", "Razgrad"]],
	21: [43.8515, 25.9695, ["ルセ州", "Ruse", "Russe", "Roussé", "Ruse", "Ruse", "Roese"]],
	22: [44.08583333, 27.25266667, ["シリストラ州", "Silistra", "Silistra", "Silistra", "Silistra", "Silistra", "Silistra"]],
	23: [42.69, 26.332, ["スリベン州", "Sliven", "Sliwen", "Sliven", "Sliven", "Sliven", "Sliven"]],
	24: [41.58783333, 24.70083333, ["スモリャン州", "Smolyan", "Smoljan", "Smolyan", "Smolyan", "Smolyan", "Smoljan"]],
	25: [42.42466667, 25.63766667, ["スタラ・ザゴラ州", "Stara Zagora", "Stara Sagora", "Stara Zagora", "Stara Zagora", "Stara Zagora", "Stara Zagora"]],
	26: [43.2745, 26.923, ["シュメン州", "Shumen", "Schumen", "Choumen", "Shumen", "Shumen", "Sjoemen"]],
	27: [43.25066667, 26.5755, ["トゥルゴビシュテ州", "Targovishte", "Targowischte", "Targovichte", "Targovishte", "Targovishte", "Turgovishte"]],
	28: [43.0855, 25.6335, ["ベリコ・トゥルノボ州", "Veliko Tarnovo", "Weliko Tarnowo", "Veliko Tarnovo", "Veliko Tarnovo", "Veliko Tarnovo", "Veliko Turnovo"]],
	29: [43.20716667, 23.55466667, ["ブラツァ州", "Vratsa", "Wraza", "Vratsa", "Vratsa", "Vratsa", "Vratsa"]]
}

regioninfo_071 = {
	1: [0, 0, ["クロアチア", "Croatia", "Kroatien", "Croatie", "Croacia", "Croazia", "Kroatië"]],
	2: [45.807, 15.964, ["ザグレブ", "Zagreb Region", "Region Zagreb", "Région de Zagreb", "Región de Zagreb", "Regione di Zagabria", "Zagreb-regio"]],
	3: [46.30016667, 16.33416667, ["中央クロアチア", "Central Croatia", "Zentralkroatien", "Croatie centrale", "Croacia Central", "Croazia Centrale", "Centraal Kroatië"]],
	4: [44.8705, 13.85116667, ["アドリア海岸", "Adriatic Croatia", "Adriatisches Kroatien", "Croatie Adriatique", "Croacia Adriática", "Croazia Adriatica", "Adriatisch Kroatië"]],
	5: [45.55083333, 18.6755, ["東クロアチア", "East Croatia", "Ostkroatien", "Est de la Croatie", "Croacia del Este", "Croazia Orientale", "Oost-Kroatë"]]
}

regioninfo_072 = {
	1: [0, 0, ["キプロス", "Cyprus", "Zypern", "Chypre", "Chipre", "Cipro", "Cyprus"]],
	2: [35.167, 33.373, ["ニコシア", "Nicosia", "Nikosia", "Nicosie", "Nicosia", "Nicosia", "Nicosia"]],
	3: [35.106, 33.93716667, ["ファマグスタ", "Famagusta", "Famagusta", "Famagouste", "Famagusta", "Famagosta", "Famagusta"]],
	4: [35.32566667, 33.32583333, ["キレニア", "Kyrenia", "Kyrenia", "Kyrenia", "Kyrenia", "Kyrenia", "Kyrenia"]],
	5: [34.91733333, 33.63483333, ["ラルナカ", "Larnaca", "Larnaka", "Larnaca", "Larnaca", "Larnaca", "Larnaca"]],
	6: [34.68366667, 33.05033333, ["リマソル", "Limassol", "Limassol", "Limassol", "Limassol", "Limassol", "Limasol"]],
	7: [34.77616667, 32.4265, ["パフォス", "Paphos", "Paphos", "Paphos", "Pafos", "Paphos", "Paphos"]]
}

regioninfo_073 = {
	1: [0, 0, ["チェコ", "Czech Republic", "Tschechische Republik", "République tchèque", "República Checa", "Repubblica Ceca", "Tsjechië"]],
	2: [50.07383333, 14.4335, ["プラハ", "Prague", "Prag", "Prague", "Praga", "Praga", "Praag"]],
	3: [50.07383333, 14.4335, ["中部ボヘミア地方", "Central Bohemian Region", "Mittelböhmische Region", "Bohême Centrale", "Bohemia Central", "Boemia Centrale", "Centraal-Boheemse Regio"]],
	4: [48.974, 14.473, ["南ボヘミア地方", "South Bohemian Region", "Südböhmische Region", "Bohême Sud", "Bohemia Meridional", "Boemia Meridionale", "Zuid-Boheemse Regio"]],
	5: [49.73916667, 13.37166667, ["プルゼニ地方", "Plzen Region", "Region Pilsen", "Région de Plzen", "Plzen", "Regione di Pilsen", "Pilsen Regio"]],
	6: [50.22583333, 12.8745, ["カールスバート地方", "Karlovy Vary Region", "Region Karlsbad", "Région de Karlovy Vary", "Karlovy Vary", "Regione di Carlsbad", "Karlsbad Regio"]],
	7: [50.66966667, 14.08566667, ["ウースチー・ナド・ラベム地方", "Ústi nad Labem Region", "Region Ústi", "Région d'Usti nad Labem", "Ústí nad Labem", "Regione di Ústi nad Labem", "Ústi nad Labem"]],
	8: [50.7595, 15.04166667, ["リベレツ地方", "Liberec Region", "Region Liberec", "Région de Liberec", "Liberec", "Regione di Liberec", "Liberec Regio"]],
	9: [50.20366667, 15.80733333, ["フラデツ・クラロベ地方", "Hradec Králové Region", "Region Hradec Králové", "Région de Hradec Králové", "Hradec Králové", "Regione di Hradec Králové", "Hradec Králové"]],
	10: [50.02383333, 15.769, ["パルドゥビツェ地方", "Pardubice Region", "Region Pardubice", "Région de Pardubice", "Pardubice", "Regione di Pardubice", "Pardubice Regio"]],
	11: [49.59133333, 17.25716667, ["オロモウツ地方", "Olomouc Region", "Region Olmütz", "Région d'Olomouc", "Olomouc", "Regione di Olomouc", "Olomouc Regio"]],
	12: [49.81783333, 18.25733333, ["モラビア・シレジア地方", "Moravian-Silesian Region", "Region Mährisch-Schlesien", "Région de Moravie-Silésie", "Moravia-Silesia", "Regione di Moravia-Slesia", "Moravisch-Silezische Regio"]],
	13: [49.20166667, 16.60966667, ["南モラビア地方", "South Moravian Region", "Südmährische Region", "Région de Moravie du Sud", "Moravia Meridional", "Moravia Meridionale", "Zuid-Moravische Regio"]],
	14: [49.22166667, 17.65366667, ["ズリン地方", "Zlín Region", "Region Zlin", "Région de Zlín", "Zlín", "Regione di Zlin", "Zlin Regio"]],
	15: [49.393, 15.58566667, ["ヴィソチナ地方", "Vysocina Region", "Region Vysocina", "Région de Vysocina", "Vysocina", "Regione di Vysocina", "Vysocina Regio"]]
}

regioninfo_074 = {
	1: [0, 0, ["デンマーク", "Denmark", "Dänemark", "Danemark", "Dinamarca", "Danimarca", "Denemarken"]],
	2: [55.692, 12.554, ["コペンハーゲン市", "Copenhagen", "Kopenhagen", "Copenhague", "Municipio de Copenhague", "Copenaghen", "Kopenhagen (stad)"]],
	3: [55.672, 12.5065, ["フレゼリクスベア市", "Frederiksberg", "Frederiksberg Amt", "Commune de Frederiksborg", "Municipio de Frederiksberg", "Frederiksberg", "Frederiksberg"]],
	4: [55.654, 12.386, ["コペンハーゲン県", "Copenhagen County", "Amt Kopenhagen", "Comté de Copenhague", "Distrito de Copenhague", "Contea di Copenaghen", "Kopenhagen (provincie)"]],
	5: [55.9245, 12.29316667, ["フレゼリクスボー県", "Frederiksborg", "Frederiksborgs Amt", "Frederiksborg", "Distrito de Frederiksborg", "Frederiksborg", "Frederiksborg"]],
	6: [55.6395, 12.0845, ["ロスキレ県", "Roskilde", "Roskilde Amt", "Roskilde", "Distrito de Roskilde", "Roskilde", "Roskilde"]],
	7: [55.43933333, 11.55833333, ["ヴェストシェラン県", "West Zealand", "West-Seeland", "Sjælland de l'ouest", "Distrito de Selandia Occidental", "Zelanda Occidentale", "West-Seeland"]],
	8: [55.221, 11.757, ["ストーストレム県", "Storstrøm", "Storstrøms Amt", "Storstrøm", "Distrito de Storstrøm", "Storstrøm", "Storstrøm"]],
	9: [55.3925, 10.38833333, ["フュン県", "Funen", "Fyns Amt", "Fionie", "Distrito de Fionia", "Fionia", "Funen"]],
	10: [55.048, 9.414, ["セナーユラン県", "South Jutland", "Süd-Jütland", "Jutland du sud", "Distrito de Jutlandia Meridional", "Jutland Meridionale", "Zuid-Jutland"]],
	11: [55.32566667, 8.773, ["リーベ県", "Ribe", "Ribe Amt", "Ribe", "Distrito de Ribe", "Ribe", "Ribe"]],
	12: [55.70516667, 9.534, ["ヴァイレ県", "Vejle", "Vejle Amt", "Vejle", "Distrito de Vejle", "Vejle", "Vejle"]],
	13: [56.084, 8.254, ["リングケービング県", "Ringkjøbing", "Ringkjøbing Amt", "Ringkjøbing", "Distrito de Ringkjøbing", "Ringkjøbing", "Ringkjøbing"]],
	14: [56.4515, 9.416666667, ["ヴィボー県", "Viborg", "Viborg Amt", "Viborg", "Distrito de Viborg", "Viborg", "Viborg"]],
	15: [57.03416667, 9.926, ["ノーズユラン県", "North Jutland", "Nord-Jütland", "Jutland du nord", "Distrito de Jutlandia Septentrional", "Jutland Settentrionale", "Noord-Jutland"]],
	16: [56.14316667, 10.221, ["オーフス県", "Århus", "Århus Amt", "Århus", "Distrito de Aarhus", "Århus", "Aarhus"]],
	17: [53.418, 10.33766667, ["ボーンホルム県", "Bornholm", "Bornholm Amt", "Commune régionale de Bornholm", "Distrito de Bornholm", "Bornholm", "Bornholm"]],
	18: [64.184, -51.721, ["グリーンランド", "Greenland", "Grönland", "Groenland", "Groenlandia", "Groenlandia", "Groenland"]]
}

regioninfo_075 = {
	1: [0, 0, ["エストニア", "Estonia", "Estland", "Estonie", "Estonia", "Estonia", "Estland"]],
	2: [59.431, 24.73416667, ["ハリュ", "Harju", "Harju", "Harjumaa", "Harju", "Harjumaa", "Harjumaa"]],
	3: [58.994, 22.75016667, ["ヒウマ", "Hiiu", "Hiiu", "Hiiumaa", "Hiiu", "Hiiumaa", "Hiiumaa"]],
	4: [59.36, 27.414, ["イダ・ビルマ", "Ida-Viru", "Ida-Viru", "Ida-Virumaa", "Ida-Viru", "Ida-Virumaa", "Ida-Virumaa"]],
	5: [58.7525, 26.38983333, ["ユゲヴァ", "Jõgeva", "Jõgeva", "Jõgevamaa", "Jõgeva", "Jõgevamaa", "Jõgevamaa"]],
	6: [58.8885, 25.55883333, ["ヤルバ", "Järva", "Järva", "Järvamaa", "Järva", "Järvamaa", "Järvamaa"]],
	7: [58.939, 23.569, ["ラーネ", "Lääne", "Lääne", "Läänemaa", "Lääne", "Läänemaa", "Läänemaa"]],
	8: [59.346, 26.365, ["ラーネ・ビルマ", "Lääne-Viru", " Lääne-Viru", "Lääne-Virumaa", "Lääne-Viru", "Lääne-Virumaa", "Lääne-Virumaa"]],
	9: [58.05133333, 27.057, ["プルヴァ", "Põlva", " Põlva", "Põlvamaa", "Põlva", "Põlvamaa", "Põlvamaa"]],
	10: [58.398, 24.501, ["ピャルヌ", "Pärnu", "Pärnu", "Pärnumaa", "Pärnu", "Pärnumaa", "Pärnumaa"]],
	11: [59.00183333, 24.7925, ["ラプラ", "Rapla", "Rapla", "Raplamaa", "Rapla", "Raplamaa", "Raplamaa"]],
	12: [58.25383333, 22.4875, ["サーレ", "Saare", "Saare", "Saaremaa", "Saare", "Saaremaa", "Saaremaa"]],
	13: [58.35666667, 26.7095, ["タルトゥ", "Tartu", "Tartu", "Tartumaa", "Tartu", "Tartumaa", "Tartumaa"]],
	14: [57.768, 26.016, ["ヴァルカ", "Valga", "Valga", "Valgamaa", "Valga", "Valgamaa", "Valgamaa"]],
	15: [58.37216667, 25.60416667, ["ヴィリヤンディ", "Viljandi", "Viljandi", "Viljandimaa", "Viljandi", "Viljandimaa", "Viljandimaa"]],
	16: [57.83983333, 27.00816667, ["ヴルチャ県", "Võru", "Võru", "Võrumaa", "Võru", "Võrumaa", "Võrumaa"]]
}

regioninfo_076 = {
	1: [0, 0, ["フィンランド", "Finland", "Finnland", "Finlande", "Finlandia", "Finlandia", "Finland"]],
	2: [60.171, 24.93733333, ["南フィンランド州", "Southern Finland", "Südfinnland", "Finlande méridionale", "Finlandia Meridional", "Finlandia Meridionale", "Zuid-Finland"]],
	3: [60.44283333, 22.25533333, ["西フィンランド州", "Western Finland", "Westfinnland", "Finlande occidentale", "Finlandia Occidental", "Finlandia Occidentale", "West-Finland"]],
	4: [61.7, 27.25583333, ["東フィンランド州", "Eastern Finland", "Ostfinnland", "Finlande orientale", "Finlandia Oriental", "Finlandia Orientale", "Oost-Finland"]],
	5: [65.03333333, 25.46666667, ["オウル州", "Province of Oulu", "Oulu (Provinz)", "Province d'Oulu", "Provincia de Oulu", "Provincia di Oulu", "Oulu"]],
	6: [66.48733333, 25.7, ["ラッピ州", "Lapland", "Lappland", "Laponie", "Laponia", "Lapponia", "Lapland"]],
	7: [60.09166667, 19.93616667, ["アハベナンマー州", "Åland", "Åland", "Åland", "Islas de Åland", "Isole Åland", "Åland"]]
}

regioninfo_077 = {
	1: [0, 0, ["フランス", "France", "Frankreich", "France", "Francia", "Francia", "Frankrijk"]],
	2: [48.85284, 2.349857, ["イール・ド・フランス", "Île-de-France", "Île-de-France", "Ile-de-France", "Isla de Francia", "Île-de-France", "Île-de-France"]],
	3: [48.585015, 7.740026, ["アルザス", "Alsace", "Elsass", "Alsace", "Alsacia", "Alsazia", "Elzas"]],
	4: [44.837976, -0.585171, ["アキテーヌ", "Aquitaine", "Aquitanien", "Aquitaine", "Aquitania", "Aquitania", "Aquitanië"]],
	5: [45.779223, 3.084225, ["オーベルニュ", "Auvergne", "Auvergne", "Auvergne", "Auvernia", "Alvernia", "Auvergne"]],
	6: [49.183196, -0.35806, ["バス・ノルマンディ", "Lower Normandy", "Basse-Normandie", "Basse-Normandie", "Baja Normandía", "Bassa Normandia", "Laag-Normandië"]],
	7: [47.321, 5.039, ["ブルゴーニュ", "Burgundy", "Burgund", "Bourgogne", "Borgoña", "Borgogna", "Bourgondië"]],
	8: [48.11042, -1.682645, ["ブルターニュ", "Brittany", "Bretagne", "Bretagne", "Bretaña", "Bretagna", "Bretagne"]],
	9: [47.90183333, 1.903, ["サントル", "Centre Loire Valley", "Centre", "Centre", "Centro", "Centro", "Centre"]],
	10: [48.963, 4.363, ["シャンパーニュ・アルデンヌ", "Champagne-Ardenne", "Champagne-Ardenne", "Champagne-Ardenne", "Champaña-Ardenas", "Champagne-Ardenne", "Champagne-Ardennen"]],
	11: [41.92266667, 8.735333333, ["コルシカ", "Corsica", "Korsika", "Corse", "Córcega", "Corsica", "Corsica"]],
	12: [47.23916667, 6.019833333, ["フランシュ・コンテ", "Franche-Comté", "Franche-Comté", "Franche-Comté", "Franco Condado", "Franca Contea", "Franche-Comté"]],
	13: [49.43966667, 1.102, ["オート・ノルマンディ", "Upper Normandy", "Haute-Normandie", "Haute-Normandie", "Alta Normandía", "Alta Normandia", "Hoog-Normandië"]],
	14: [43.60716667, 3.873, ["ラングドック・ルシヨン", "Languedoc-Roussillon", "Languedoc-Roussillon", "Languedoc-Roussillon", "Languedoc-Rosellón", "Linguadoca-Rossiglione", "Languedoc-Roussillon"]],
	15: [45.830091, 1.256957, ["リムーザン", "Limousin", "Limousin", "Limousin", "Lemosín", "Limosino", "Limousin"]],
	16: [49.11883333, 6.173333333, ["ロレーヌ", "Lorraine", "Lothringen", "Lorraine", "Lorena", "Lorena", "Lotharingen"]],
	17: [43.60316667, 1.439, ["ミディ・ピレネー", "Midi-Pyrénées", "Midi-Pyrénées", "Midi-Pyrénées", "Mediodía-Pirineos", "Midi-Pirenei", "Midi-Pyreneeën"]],
	18: [50.634635, 3.062891, ["ノール・パ・ド・カレー", "Nord-Pas-de-Calais", "Nord-Pas-de-Calais", "Nord-Pas-de-Calais", "Norte-Paso de Calais", "Nord-Passo di Calais", "Noord-Nauw van Calais"]],
	19: [47.2175, -1.551666667, ["ペイ・ド・ラ・ロワール", "Western Loire Valley", "Pays de la Loire", "Pays de la Loire", "Países del Loira", "Loira", "Pays de la Loire"]],
	20: [49.88866667, 2.2925, ["ピカルディー", "Picardy", "Picardie", "Picardie", "Picardía", "Picardia", "Picardië"]],
	21: [46.584641, 0.339781, ["ポワトゥー・シャラント", "Poitou-Charentes", "Poitou-Charentes", "Poitou-Charentes", "Poitou-Charentes", "Poitou-Charentes", "Poitou-Charentes"]],
	22: [43.29183333, 5.373, ["プロヴァンス・アルプ・コート・ダジュール", "Provence-Alpes-Côte d'Azur", "Provence-Alpes-Côte d'Azur", "Provence-Alpes-Côte d'Azur", "Provenza-Alpes-Costa Azul", "Provenza-Alpi-Costa Azzurra", "Provence-Alpes-Côte d'Azur"]],
	23: [45.75583333, 4.832, ["ローヌ・アルプ", "Rhône-Alpes", "Rhône-Alpes", "Rhône-Alpes", "Ródano-Alpes", "Rodano-Alpi", "Rhône-Alpes"]],
	24: [16, -61.72, ["グアドループ", "Guadeloupe", "Guadeloupe", "Guadeloupe", "Guadalupe", "Guadalupa", "Guadeloupe"]],
	25: [14.601, -61.076, ["マルチニーク", "Martinique", "Martinique", "Martinique", "Martinica", "Martinica", "Martinique"]],
	26: [4.934, -52.33, ["フランス領ギアナ", "French Guiana", "Französisch-Guayana", "Guyane Française", "Guayana Francesa", "Guayana Francese", "Frans-Guyana"]],
	27: [-20.879, 55.453, ["レユニオン", "Réunion", "Réunion", "Réunion", "La Reunión", "La Réunion", "Réunion"]]
}

regioninfo_078 = {
	1: [0, 0, ["ドイツ", "Germany", "Deutschland", "Allemagne", "Alemania", "Germania", "Duitsland"]],
	2: [52.52116667, 13.40366667, ["ベルリン", "Berlin", "Berlin", "Berlin", "Berlín", "Berlino", "Berlijn"]],
	3: [50.0755, 8.2385, ["ヘッセン州", "Hesse", "Hessen", "Hesse", "Hesse", "Assia", "Hessen"]],
	4: [48.77316667, 9.174833333, ["バーデン・ビュルテンベルク州", "Baden-Württemberg", "Baden-Württemberg", "Bade-Wurtemberg", "Baden-Wurtemberg", "Baden-Württemberg", "Baden-Württemberg"]],
	5: [48.13333333, 11.556, ["バイエルン州", "Bavaria", "Bayern", "Bavière", "Baviera", "Baviera", "Beieren"]],
	6: [52.39283333, 13.03966667, ["ブランデンブルク州", "Brandenburg", "Brandenburg", "Brandebourg", "Brandeburgo", "Brandeburgo", "Brandenburg"]],
	7: [53.06666667, 8.806666667, ["ブレーメン", "Bremen", "Bremen", "Brême", "Bremen", "Brema", "Bremen"]],
	8: [53.55, 9.99, ["ハンブルク", "Hamburg", "Hamburg", "Hambourg", "Hamburgo", "Amburgo", "Hamburg"]],
	9: [53.61666667, 11.41666667, ["メクレンブルク・フォアポンメルン州", "Mecklenburg-Western Pomerania", "Mecklenburg-Vorpommern", "Mecklembourg-Poméranie occidentale", "Mecklemburgo-Pomerania Occidental", "Meclemburgo-Pomerania Occidentale", "Mecklenburg-Voor-Pommeren"]],
	10: [52.36666667, 9.734833333, ["ニーダーザクセン州", "Lower Saxony", "Niedersachsen", "Basse-Saxe", "Baja Sajonia", "Bassa Sassonia", "Nedersaksen"]],
	11: [51.24033333, 6.774166667, ["ノルトライン・ウェストファーレン州", "North Rhine-Westphalia", "Nordrhein-Westfalen", "Rhénanie-du-Nord-Westphalie", "Renania del Norte-Westfalia", "Nord Reno-Westfalia", "Noord-Rijnland-Westfalen"]],
	12: [50, 8.259833333, ["ラインラント・ファルツ州", "Rhineland-Palatinate", "Rheinland-Pfalz", "Rhénanie-Palatinat", "Renania-Palatinado", "Renania-Palatinato", "Rijnland-Palts"]],
	13: [49.23333333, 7, ["ザールラント州", "Saarland", "Saarland", "Sarre", "Sarre", "Saarland", "Saarland"]],
	14: [51.03333333, 13.73333333, ["ザクセン州", "Saxony", "Sachsen", "Saxe", "Sajonia", "Sassonia", "Saksen"]],
	15: [52.125, 11.61666667, ["ザクセン・アンハルト州", "Saxony-Anhalt", "Sachsen-Anhalt", "Saxe-Anhalt", "Sajonia-Anhalt", "Sassonia-Anhalt", "Saksen-Anhalt"]],
	16: [54.32133333, 10.12283333, ["シュレスビヒ・ホルシュタイン州", "Schleswig-Holstein", "Schleswig-Holstein", "Schleswig-Holstein", "Schleswig-Holstein", "Schleswig-Holstein", "Sleeswijk-Holstein"]],
	17: [50.97283333, 11.02416667, ["テューリンゲン州", "Thuringia", "Thüringen", "Thuringe", "Turingia", "Turingia", "Thüringen"]]
}

regioninfo_079 = {
	1: [0, 0, ["ギリシャ", "Greece", "Griechenland", "Grèce", "Grecia", "Grecia", "Griekenland"]],
	2: [37.97466667, 23.7245, ["アッティカ", "Attica", "Attika", "Attique", "Ática", "Attica", "Attika"]],
	3: [38.8925, 22.43383333, ["中央ギリシャ", "Central Greece", "Mittelgriechenland", "Grèce centrale", "Grecia Central", "Grecia Centrale", "Centraal Griekenland"]],
	4: [40.62166667, 22.97016667, ["中央マケドニア", "Central Macedonia", "Zentralmakedonien", "Macédoine centrale", "Macedonia Central", "Macedonia Centrale", "Centraal Macedonië"]],
	5: [35.336, 25.13366667, ["クレタ", "Crete", "Kreta", "Crète", "Creta", "Creta", "Kreta"]],
	6: [41.12216667, 25.41766667, ["東マケドニア・トラキア", "East Macedonia and Thrace", "Ostmakedonien und Thrakien", "Macédoine de l'Est et Thrace", "Macedonia Oriental y Tracia", "Macedonia Orientale e Tracia", "Oost-Macedonië en Thracië"]],
	7: [39.65466667, 20.85166667, ["イピロス", "Epirus", "Epirus", "Epire", "Epiro", "Epiro", "Epirus"]],
	8: [39.61883333, 19.91683333, ["イオニア", "Ionian Islands", "Ionische Inseln", "Iles ioniennes", "Islas Jónicas", "Isole Ionie", "Ionische Eilanden"]],
	9: [39.10216667, 26.55116667, ["北エーゲ", "North Aegean", "Nördliche Ägäis", "Nord de l'Égée", "Egeo Septentrional", "Egeo Settentrionale", "Noord-Egeïsche Eilanden"]],
	10: [37.5045, 22.368, ["ペロポネソス", "Peloponnese", "Peloponnes", "Péloponnèse", "Peloponeso", "Peloponneso", "Peloponnesos"]],
	11: [36.43916667, 28.21983333, ["南エーゲ", "South Aegean", "Südliche Ägäis", "Sud de l'Égée", "Egeo Meridional", "Egeo Meridionale", "Zuid-Egeïsche Eilanden"]],
	12: [39.637, 22.418, ["テッサリーア", "Thessaly", "Thessalien", "Thessalie", "Tesalia", "Tessaglia", "Thessalië"]],
	13: [38.23616667, 21.73683333, ["西ギリシャ", "West Greece", "Westgriechenland", "Grèce de l'Ouest", "Grecia Occidental", "Grecia Occidentale", "West-Griekenland"]],
	14: [40.312, 21.802, ["西マケドニア", "West Macedonia", "Westmakedonien", "Macédoine de l'Ouest", "Macedonia Occidental", "Macedonia Occidentale", "West-Macedonië"]]
}

regioninfo_080 = {
	1: [0, 0, ["ハンガリー", "Hungary", "Ungarn", "Hongrie", "Hungría", "Ungheria", "Hongarije"]],
	2: [47.49, 19.08, ["ブダペスト", "Budapest", "Budapest", "Budapest", "Budapest", "Budapest", "Boedapest"]],
	3: [46.905, 19.68833333, ["バーチ・キシュクン州", "Bács-Kiskun", "Bács-Kiskun", "Bács-Kiskun", "Bács-Kiskun", "Bács-Kiskun", "Bács-Kiskun"]],
	4: [46.07166667, 18.21666667, ["バラニャ州", "Baranya", "Baranya", "Baranya", "Baranya", "Baranya", "Baranya"]],
	5: [46.671, 21.101, ["ベーケーシュ州", "Békés", "Békés", "Békés", "Békés", "Békés", "Békés"]],
	6: [48.1, 20.78833333, ["ボルショド・アバウーイ・ゼンプレーン州", "Borsod-Abaúj-Zemplén", "Borsod-Abaúj-Zemplén", "Borsod-Abaúj-Zemplén", "Borsod-Abaúj-Zemplén", "Borsod-Abaúj-Zemplén", "Borsod-Abaúj-Zemplén"]],
	7: [46.255, 20.15666667, ["チョングラード州", "Csongrád", "Csongrád", "Csongrád", "Csongrád", "Csongrád", "Csongrád"]],
	8: [47.2, 18.405, ["フェイェール州", "Fejér", "Fejér", "Fejér", "Fejér", "Fejér", "Fejér"]],
	9: [47.678, 17.638, ["ジェール・モション・ショプロン州", "Gyor-Moson-Sopron", "Gyor-Moson-Sopron", "Gyor-Moson-Sopron", "Gyor-Moson-Sopron", "Gyor-Moson-Sopron", "Gyor-Moson-Sopron"]],
	10: [47.53333333, 21.62333333, ["ハイドゥー・ヒバル州", "Hajdú-Bihar", "Hajdú-Bihar", "Hajdú-Bihar", "Hajdú-Bihar", "Hajdú-Bihar", "Hajdú-Bihar"]],
	11: [47.895, 20.382, ["ヘヴェシュ州", "Heves", "Heves", "Heves", "Heves", "Heves", "Heves"]],
	12: [47.17, 20.187, ["ヤース・ナチクン・ソルノク州", "Jász-Nagykun-Szolnok", "Jász-Nagykun-Szolnok", "Jász-Nagykun-Szolnok", "Jász-Nagykun-Szolnok", "Jász-Nagykun-Szolnok", "Jász-Nagykun-Szolnok"]],
	13: [47.55, 18.43666667, ["コマーロム・エステルゴム州", "Komárom-Esztergom", "Komárom-Esztergom", "Komárom-Esztergom", "Komárom-Esztergom", "Komárom-Esztergom", "Komárom-Esztergom"]],
	14: [48.10666667, 19.81666667, ["ノーグラード州", "Nógrád", "Nógrád", "Nógrád", "Nógrád", "Nógrád", "Nógrád"]],
	15: [47.49, 19.08, ["ペシュト州", "Pest", "Pest", "Pest", "Pest", "Pest", "Pest"]],
	16: [46.35666667, 17.79, ["ショモジ州", "Somogy", "Somogy", "Somogy", "Somogy", "Somogy", "Somogy"]],
	17: [47.957, 21.722, ["サボルチ・サトマール・ベレグ州", "Szabolcs-Szatmár-Bereg", "Szabolcs-Szatmár-Bereg", "Szabolcs-Szatmár-Bereg", "Szabolcs-Szatmár-Bereg", "Szabolcs-Szatmár-Bereg", "Szabolcs-Szatmár-Bereg"]],
	18: [46.35, 18.705, ["トルナ州", "Tolna", "Tolna", "Tolna", "Tolna", "Tolna", "Tolna"]],
	19: [47.23333333, 16.62333333, ["ヴァシュ州", "Vas", "Vas", "Vas", "Vas", "Vas", "Vas"]],
	20: [47.1, 17.91666667, ["ベスプレーム州", "Veszprém", "Veszprém", "Veszprém", "Veszprém", "Veszprém", "Veszprém"]],
	21: [46.843, 16.839, ["ザラ州", "Zala", "Zala", "Zala", "Zala", "Zala", "Zala"]]
}

regioninfo_081 = {
	1: [0, 0, ["アイスランド", "Iceland", "Island", "Islande", "Islandia", "Islanda", "IJsland"]],
	2: [64.13483333, -21.89066667, ["グレーター・レイキャヴィーク", "Capital Region", "Hauptstadtregion", "Région de la capitale", "Región de la Capital", "Regione della capitale", "Hoofdstedelijke regio"]],
	3: [65.2855, -14.43416667, ["東アイスランド", "Eastland", "Austurland", "Terre de l'Est", "Oriental", "Est", "Oostland"]],
	4: [65.68383333, -18.10616667, ["北アイスランド（東部）", "Northland East", "Östliches Nordland", "Terre du Nord-Est", "Nororiental", "Nordest", "Noordland oost"]],
	5: [65.7385, -19.65116667, ["北アイスランド（西部）", "Northland West", "Westliches Nordland", "Terre du Nord-Ouest", "Noroccidental", "Nordovest", "Noordland West"]],
	6: [63.935, -21.00166667, ["南アイスランド", "Southland", "Suðurland", "Terre du Sud", "Meridional", "Sud", "Zuidland"]],
	7: [64.00466667, -22.57, ["南西アイスランド", "Southern Peninsula", "Suðurnes", "Péninsule du Sud", "Suroccidental", "Penisola Meridionale", "Zuidelijk Schiereiland"]],
	8: [66.073, -23.141, ["西部フィヨルド", "Western Fjords", "Westfjorde", "Fjords de l'Ouest", "Fiordos Occidentales", "Fiordi Occidentali", "Westfjorden"]],
	9: [64.5355, -21.924, ["西アイスランド", "Westland", "Vesturland", "Terre de l'Ouest", "Occidental", "Ovest", "Westland"]]
}

regioninfo_082 = {
	1: [0, 0, ["アイルランド", "Ireland", "Irland", "Irlande", "Irlanda", "Irlanda", "Ierland"]],
	2: [53.341, -6.257, ["ダブリン首都圏", "Dublin", "Dublin", "Dublin", "Dublín", "Dublino", "Dublin"]],
	3: [54.005, -6.403333333, ["国境", "Border", "Border", "Border", "Frontera", "Border", "Border"]],
	4: [53.271, -9.065, ["西部地方", "West", "West", "West", "Oeste", "West", "West"]],
	5: [53.426, -7.94, ["中部地方", "Midland", "Midland", "Midland", "Centro", "Midland", "Midland"]],
	6: [53.21666667, -6.671666667, ["中東部地方", "Mid-East", "Mid-East", "Mid-East", "Medio Este", "Mid-East", "Mid-East"]],
	7: [52.666, -8.637, ["中西部地方", "Mid-West", "Mid-West", "Mid-West", "Medio Oeste", "Mid-West", "Mid-West"]],
	8: [52.25, -7.116666667, ["南東部地方", "South-East", "South-East", "South-East", "Sureste", "South-East", "South-East"]],
	9: [51.9, -8.471666667, ["南西部地方", "South-West", "South-West", "South-West", "Suroeste", "South-West", "South-West"]]
}

regioninfo_083 = {
	1: [0, 0, ["イタリア", "Italy", "Italien", "Italie", "Italia", "Italia", "Italië"]],
	2: [41.89283333, 12.48916667, ["ラツィオ州", "Lazio", "Latium", "Latium", "Lacio", "Lazio", "Latium"]],
	3: [45.736, 7.314, ["バッレ・ダオスタ州", "Aosta Valley", "Aostatal", "Val d'Aoste", "Valle de Aosta", "Valle d'Aosta", "Valle d'Aosta"]],
	4: [45.07283333, 7.6745, ["ピエモンテ州", "Piedmont", "Piemont", "Piémont", "Piamonte", "Piemonte", "Piëmont"]],
	5: [44.40616667, 8.9345, ["リグリア州", "Liguria", "Ligurien", "Ligurie", "Liguria", "Liguria", "Ligurië"]],
	6: [45.46933333, 9.184666667, ["ロンバルディア州", "Lombardy", "Lombardei", "Lombardie", "Lombardía", "Lombardia", "Lombardije"]],
	7: [46.069, 11.12033333, ["トレンティノ・アルト・アディジェ州", "Trentino-South Tyrol", "Trentino-Südtirol", "Trentin-Haut-Adige", "Trentino-Alto Adigio", "Trentino-Alto Adige", "Trentino-Zuid-Tirol"]],
	8: [45.43333333, 12.33333333, ["ベネト州", "Veneto", "Venetien", "Vénétie", "Véneto", "Veneto", "Veneto"]],
	9: [45.642, 13.76983333, ["フリウリ・ベネチア・ジュリア州", "Friuli Venezia Giulia", "Friaul-Julisch Venetien", "Frioul-Vénétie julienne", "Friul-Venecia Julia", "Friuli-Venezia Giulia", "Friuli-Venezia Giulia"]],
	10: [44.50233333, 11.337, ["エミリア・ロマーニャ州", "Emilia-Romagna", "Emilia-Romagna", "Emilie Romagne", "Emilia-Romaña", "Emilia-Romagna", "Emilia-Romagna"]],
	11: [43.77616667, 11.25, ["トスカナ州", "Tuscany", "Toskana", "Toscane", "Toscana", "Toscana", "Toscane"]],
	12: [43.112, 12.384, ["ウンブリア州", "Umbria", "Umbrien", "Ombrie", "Umbría", "Umbria", "Umbrië"]],
	13: [43.61866667, 13.512, ["マルケ州", "Marche", "Marken", "Marches", "Las Marcas", "Marche", "Marken"]],
	14: [42.3505, 13.391, ["アブルッツィ州", "Abruzzo", "Abruzzen", "Abruzzes", "Abruzos", "Abruzzo", "Abruzzen"]],
	15: [41.561, 14.661, ["モリーゼ州", "Molise", "Molise", "Molise", "Molise", "Molise", "Molise"]],
	16: [40.838, 14.25316667, ["カンパニア州", "Campania", "Kampanien", "Campanie", "Campania", "Campania", "Campanië"]],
	17: [41.12116667, 16.85983333, ["プーリア州", "Apulia", "Apulien", "Pouilles", "Apulia", "Puglia", "Apulië"]],
	18: [40.637, 15.79266667, ["バジリカータ州", "Basilicata", "Basilikata", "Basilicate", "Basilicata", "Basilicata", "Basilicata"]],
	19: [38.90216667, 16.591, ["カラブリア州", "Calabria", "Kalabrien", "Calabre", "Calabria", "Calabria", "Calabrië"]],
	20: [38.1175, 13.35583333, ["シチリア州", "Sicily", "Sizilien", "Sicile", "Sicilia", "Sicilia", "Sicilië"]],
	21: [39.21733333, 9.106333333, ["サルデーニャ州", "Sardinia", "Sardinien", "Sardaigne", "Cerdeña", "Sardegna", "Sardinië"]]
}

regioninfo_084 = {
	1: [0, 0, ["ラトビア", "Latvia", "Lettland", "Lettonie", "Letonia", "Lettonia", "Letland"]],
	2: [56.948, 24.085, ["リガ", "Riga", "Riga", "Riga", "Riga", "Riga", "Riga"]],
	3: [56.967, 21.966, ["クルディガ", "Kuldiga", "Kuldiga", "Kuldiga", "Kuldigas", "Kuldiga", "Kuldiga"]],
	4: [56.504, 21.009, ["リエパーヤ", "Liepaja", "Liepaja", "Liepaja", "Liepaja", "Liepaja", "Liepaja"]],
	5: [57.247, 22.6, ["タルス", "Talsi", "Talsi", "Talsi", "Talsu", "Talsi", "Talsi"]],
	6: [57.39083333, 21.558, ["ヴェンツピルス", "Ventspils", "Ventspils", "Ventspils", "Ventspils", "Ventspils", "Ventspils"]],
	7: [56.65766667, 22.48666667, ["Saldus", "Saldus", "Saldus", "Saldus", "Saldus", "Saldus", "Saldus"]],
	8: [56.95816667, 23.15116667, ["トゥクマ", "Tukums", "Tukuma", "Tukums", "Tukuma", "Tukums", "Tukums"]],
	9: [56.59, 25.2, ["Aizkraukle", "Aizkraukle", "Aizkraukle", "Aizkraukle", "Aizkraukles", "Aizkraukle", "Aizkraukle"]],
	10: [57.419, 27.057, ["アルークスネ", "Aluksne", "Aluksne", "Aluksne", "Aluksnes", "Aluksne", "Aluksne"]],
	11: [57.317, 25.2595, ["Cesis", "Cesis", "Cesis", "Cesis", "Cesu", "Cesis", "Cesis"]],
	12: [57.175, 26.753, ["グルベネ", "Gulbene", "Gulbene", "Gulbene", "Gulbenes", "Gulbene", "Gulbene"]],
	13: [56.8515, 26.21833333, ["マドナ", "Madona", "Madona", "Madona", "Madonas", "Madona", "Madona"]],
	14: [57.512, 24.713, ["リンバジ", "Limbazi", "Limbazi", "Limbazi", "Limbazu", "Limbazi", "Limbazi"]],
	15: [56.81, 24.609, ["オグレ", "Ogre", "Ogre", "Ogre", "Ogres", "Ogre", "Ogres"]],
	16: [57.768, 26.016, ["ヴァルカ", "Valka", "Valka", "Valka", "Valkas", "Valka", "Valka"]],
	17: [57.53616667, 25.41766667, ["ヴァルミエラ", "Valmiera", "Valmiera", "Valmiera", "Valmieras", "Valmiera", "Valmiera"]],
	18: [57.12616667, 27.2685, ["バルブ", "Balvi", "Balvu", "Balvi", "Balvu", "Balvi", "Balvi"]],
	19: [55.88, 26.519, ["ダウガフピルス", "Daugavpils", "Daugavpils", "Daugavpils", "Daugavpils", "Daugavpils", "Daugavpils"]],
	20: [56.50283333, 25.872, ["Jekabpils", "Jekabpils", "Jekabpils", "Jekabpils", "Jekabpils", "Jekabpils", "Jekabpils"]],
	21: [55.891, 27.173, ["Kraslava", "Kraslava", "Kraslava", "Kraslava", "Kraslavas", "Kraslava", "Kraslava"]],
	22: [56.546, 27.726, ["ルザ", "Ludza", "Ludza", "Ludza", "Ludzas", "Ludza", "Ludza"]],
	23: [56.291, 26.729, ["プレイリ", "Preili", "Preili", "Preili", "Preilu", "Preili", "Preili"]],
	24: [56.5015, 27.336, ["レーゼクネ", "Rezekne", "Rezekne", "Rezekne", "Rezeknes", "Rezekne", "Rezekne"]],
	25: [56.417, 24.197, ["バウスカ", "Bauska", "Bauska", "Bauska", "Bauskas", "Bauska", "Bauska"]],
	26: [56.61833333, 23.2835, ["ドベレ", "Dobele", "Dobele", "Dobele", "Dobeles", "Dobele", "Dobele"]],
	27: [56.635, 23.70916667, ["イェルガヴァ", "Jelgava", "Jelgava", "Jelgava", "Jelgava", "Jelgava", "Jelgava"]]
}

regioninfo_085 = {
	1: [0, 0, ["レソト", "Lesotho", "Lesotho", "Lesotho", "Lesotho", "Lesotho", "Lesotho"]],
	2: [-29.319, 27.471, ["マセル県", "Maseru", "Maseru", "Maseru", "Maseru", "Maseru", "Maseru"]],
	3: [-29.15, 27.742, ["べレア県", "Berea", "Berea", "Berea", "Berea", "Berea", "Berea"]],
	4: [-28.769, 28.26, ["ブータ・ブーテ県", "Butha-Buthe", "Butha-Buthe", "Butha-Buthe", "Butha-Buthe", "Butha-Buthe", "Butha-Buthe"]],
	5: [-28.878, 28.055, ["レリベ県", "Leribe", "Leribe", "Leribe", "Leribe", "Leribe", "Leribe"]],
	6: [-29.82033333, 27.474, ["マフェテング県", "Mafeteng", "Mafeteng", "Mafeteng", "Mafeteng", "Mafeteng", "Mafeteng"]],
	7: [-30.155, 27.24033333, ["モハーレスフーク県", "Mohale's Hoek", "Mohales Hoek", "Mohale's Hoek", "Mohale's Hoek", "Mohale's Hoek", "Mohale's Hoek"]],
	8: [-29.28733333, 29.06866667, ["モコトロング県", "Mokhotlong", "Mokhotlong", "Mokhotlong", "Mokhotlong", "Mokhotlong", "Mokhotlong"]],
	9: [-30.125, 28.702, ["クァクハスネック県", "Qacha's Nek", "Qacha's Nek", "Qacha's Nek", "Qacha's Nek", "Qacha's Nek", "Qacha's Nek"]],
	10: [-30.40683333, 27.70966667, ["クティング県", "Quthing", "Quthing", "Quthing", "Quthing", "Quthing", "Quthing"]],
	11: [-29.516, 28.605, ["ターバ・ツェーカ県", "Thaba-Tseka", "Thaba-Tseka", "Thaba-Tseka", "Thaba-Tseka", "Thaba-Tseka", "Thaba-Tseka"]]
}

regioninfo_086 = {
	1: [0, 0, ["リヒテンシュタイン", "Liechtenstein", "Liechtenstein", "Liechtenstein", "Liechtenstein", "Liechtenstein", "Liechtenstein"]],
	2: [47.1405, 9.524333333, ["オーバーラント", "Upper Country", "Oberland", "Oberland", "Oberland", "Oberland", "Oberland"]],
	3: [47.20666667, 9.522166667, ["ウンターラント", "Lower Country", "Unterland", "Unterland", "Unterland", "Unterland", "Unterland"]]
}

regioninfo_087 = {
	1: [0, 0, ["リトアニア", "Lithuania", "Litauen", "Lituanie", "Lituania", "Lituania", "Litouwen"]],
	2: [54.681, 25.282, ["ヴィリニュス州", "Vilnius", "Vilnius", "Vilnius", "Vilna", "Vilnius", "Vilnius"]],
	3: [54.38733333, 24.0525, ["アリートゥス州", "Alytus", "Alytus", "Alytus", "Alytus", "Alytus", "Alytus"]],
	4: [54.893, 23.922, ["カウナス州", "Kaunas", "Kaunas", "Kaunas", "Kaunas", "Kaunas", "Kaunas"]],
	5: [55.712, 21.134, ["クライペダ州", "Klaipeda", "Klaipeda", "Klaipeda", "Klaipeda", "Klaipeda", "Klaipeda"]],
	6: [54.55133333, 23.35216667, ["マリヤンポレ州", "Marijampole", "Marijampole", "Marijampole", "Marijampole", "Marijampole", "Marijampole"]],
	7: [55.732, 24.368, ["パネベジス州", "Panevezys", "Panevezys", "Panevezys", "Panevezys", "Panevezys", "Panevezys"]],
	8: [55.93333333, 23.3095, ["シャウレイ州", "Šiauliai", "Siauliai", "Siauliai", "Siauliai", "Siauliai", "Siauliai"]],
	9: [55.25016667, 22.2865, ["タウラゲ州", "Taurage", "Taurage", "Taurage", "Taurage", "Taurage", "Taurage"]],
	10: [55.982, 22.25016667, ["テルシェイ州", "Telšiai", "Telšiai", "Telšiai", "Telsiai", "Telsiai", "Telsiai"]],
	11: [55.492, 25.60683333, ["ウテナ州", "Utena", "Utena", "Utena", "Utena", "Utena", "Utena"]]
}

regioninfo_088 = {
	1: [0, 0, ["ルクセンブルク", "Luxembourg", "Luxemburg", "Luxembourg", "Luxemburgo", "Lussemburgo", "Luxemburg"]],
	2: [49.609, 6.125, ["ルクセンブルク", "Luxembourg", "Luxemburg", "Luxembourg", "Luxemburgo", "Lussemburgo", "Luxemburg"]],
	3: [49.86833333, 6.155666667, ["ディーキルヒ", "Diekirch", "Diekirch", "Diekirch", "Diekirch", "Diekirch", "Diekirch"]],
	4: [49.682, 6.44, ["グレーベンマハ", "Grevenmacher", "Grevenmacher", "Grevenmacher", "Grevenmacher", "Grevenmacher", "Grevenmacher"]]
}

regioninfo_089 = {
	1: [0, 0, ["北マケドニア", "North Macedonia", "Nordmazedonien", "Macédoine du Nord", "Macedonia del Norte", "Macedonia del Nord", "Noord-Macedonië"]],
	2: [42.00316667, 21.45016667, ["スコピエ", "Skopje", "Skopje", "Skopje", "Skopje", "Skopje", "Skopje"]],
	3: [41.745, 22.196, ["東部", "Eastern", "Ostmazedonien", "Macédoine de l'Est", "Macedonia del Este", "Orientale", "Oost-Macedonië"]],
	4: [42.1345, 21.72216667, ["北東部", "Northeastern", "Nordostmazedonien", "Macédoine du Nord-Est", "Macedonia del Noreste", "Nordorientale", "Noord-Oost-Macedonië"]],
	5: [41.35116667, 21.55716667, ["ペラゴニア", "Pelagonia", "Pelagonia", "Pelagonia", "Pelagonia", "Pelagonia", "Pelagonia"]],
	6: [42.00566667, 20.971, ["ポログ", "Polog", "Polog", "Polog", "Polog", "Polog", "Polog"]],
	7: [41.14116667, 22.51683333, ["南東部", "Southeastern", "Südostmazedonien", "Macédoine du Sud-Est", "Macedonia del Sureste", "Sudorientale", "Zuid-Oost-Macedonië"]],
	8: [41.12, 20.81816667, ["南西部", "Southwestern", "Südwestmazedonien", "Macédoine du Sud-Ouest", "Macedonia del Suroeste", "Sudoccidentale", "Zuid-West-Macedonië"]],
	9: [41.729, 21.78, ["ヴァルダル", "Vardar", "Vardar", "Vardar", "Vardar", "Vardar", "Vardar"]]
}

regioninfo_090 = {
	1: [0, 0, ["マルタ", "Malta", "Malta", "Malte", "Malta", "Malta", "Malta"]],
	2: [35.9025, 14.518, ["マルタ", "Malta", "Malta", "Malta", "Malta", "Malta", "Malta"]],
	3: [36.045, 14.243, ["ゴゾ・コミーノ", "Gozo and Comino", "Gozo und Comino", "Gozo et Comino", "Gozo y Comino", "Gozo e Comino", "Gozo en Comino"]]
}

regioninfo_091 = {
	1: [0, 0, ["モンテネグロ", "Montenegro", "Montenegro", "Monténégro", "Montenegro", "Montenegro", "Montenegro"]],
	2: [42.43883333, 19.26783333, ["ポドゴリツァ", "Podgorica", "Podgorica", "Podgorica", "Podgorica", "Podgorica", "Podgorica"]],
	3: [42.739, 19.786, ["アンドリエヴィツァ", "Andrijevica", "Andrijevica", "Andrijevica", "Andrijevica", "Andrijevica", "Andrijavica"]],
	4: [42.08, 19.10583333, ["バル", "Bar", "Bar", "Bar", "Bar", "Antivari", "Bar"]],
	5: [42.854, 19.87233333, ["ベラネ", "Berane", "Berane", "Berane", "Berane", "Berane", "Berane"]],
	6: [43.03583333, 19.742, ["ビイェロ・ポリェ", "Bijelo Polje", "Bijelo Polje", "Bijelo Polje", "Bijelo Polje", "Bijelo Polje", "Bijelo Polje"]],
	7: [42.28, 18.832, ["ブドヴァ", "Budva", "Budva", "Budva", "Budva", "Budua", "Budva"]],
	8: [42.39, 18.914, ["ツェティニェ", "Cetinje", "Cetinje", "Cetinje", "Cetinje", "Cettigne", "Cetinje"]],
	9: [42.55333333, 19.10333333, ["ダニロフグラド", "Danilovgrad", "Danilovgrad", "Danilovgrad", "Danilovgrad", "Danilovgrad", "Danilovgrad"]],
	10: [42.454, 18.531, ["ヘルツ ェ グ・ノヴィ", "Herceg Novi", "Herceg Novi", "Herceg Novi", "Herceg Novi", "Castelnuovo di Cattaro", "Herceg Novi"]],
	11: [42.82226, 19.5163, ["コラシン", "Kolasin", "Kolasin", "Kolasin", "Kolasin", "Kolasin", "Kolasin"]],
	12: [42.43966667, 18.7755, ["コトル", "Kotor", "Kotor", "Kotor", "Kotor", "Cattaro", "Kotor"]],
	13: [42.96683333, 19.58733333, ["モイコヴァツ", "Mojkovac", "Mojkovac", "Mojkovac", "Mojkovac", "Mojkovac", "Mojkovac"]],
	14: [42.773, 18.944, ["ニクシチェ", "Niksic", "Niksic", "Niksic", "Niksic", "Niksic", "Niksic"]],
	15: [42.60216667, 19.95116667, ["プラヴ", "Plav", "Plav", "Plav", "Plav", "Plav", "Plav"]],
	16: [43.15533333, 18.8265, ["プルジネ", "Plužine", "Plužine", "Plužine", "Pluzine", "Pluzine", "Pluzine"]],
	17: [43.35516667, 19.35783333, ["プリエヴィリア", "Pljevlja", "Pljevlja", "Pljevlja", "Pljevlja", "Pljevlja", "Pljevlja"]],
	18: [42.8405, 20.1625, ["ロジャイェ", "Rozaje", "Rozaje", "Rozaje", "Rozaje", "Rozaje", "Rozaj"]],
	19: [42.95516667, 19.1085, ["シャヴニク", "Šavnik", "Savnik", "Savnik", "Savnik", "Savnik", "Savnik"]],
	20: [42.43, 18.6999, ["ティヴァト", "Tivat", "Tivat", "Tivat", "Tivat", "Teodo", "Tivat"]],
	21: [41.9299, 19.2241, ["ウルツィニ", "Ulcinj", "Ulcinj", "Ulcinj", "Ulcinj", "Dulcigno", "Ulcinj"]],
	22: [43.154, 19.1231, ["ジャブリャック", "Zabljak", "Zabljak", "Zabljak", "Zabljak", "Zabljak", "Zabljak"]]
}

regioninfo_092 = {
	1: [0, 0, ["モザンビーク", "Mozambique", "Mosambik", "Mozambique", "Mozambique", "Mozambico", "Mozambique"]],
	2: [-25.968, 32.56833333, ["マプート市", "Maputo (City)", "Maputo (Stadt)", "Maputo (Ville)", "Ciudad de Maputo", "Maputo (provincia)", "Maputo, de stad"]],
	3: [-25.96666667, 32.46666667, ["マプート州", "Maputo (Province)", "Maputo (Provinz)", "Maputo (province)", "Provincia de Maputo", "Maputo (provincia)", "Maputo (Provincie)"]],
	4: [-12.96, 40.487, ["カボ・デルガード州", "Cabo Delgado", "Cabo Delgado", "Cabo Delgado", "Cabo Delgado", "Cabo Delgado", "Cabo Delgado"]],
	5: [-25.03766667, 33.63716667, ["ガザ州", "Gaza", "Gaza", "Gaza", "Gaza", "Gaza", "Gaza"]],
	6: [-23.87066667, 35.38616667, ["イニャンバネ州", "Inhambane", "Inhambane", "Inhamabane", "Inhambane", "Inhambane", "Inhambane"]],
	7: [-19.1185, 33.46766667, ["マニッカ州", "Manica", "Manica", "Manica", "Manica", "Manica", "Manica"]],
	8: [-15.10916667, 39.254, ["ナンプラ州", "Nampula", "Nampula", "Nampula", "Nampula", "Nampula", "Nampula"]],
	9: [-13.30016667, 35.237, ["ニアサ州", "Niassa", "Niassa", "Niassa", "Niassa", "Niassa", "Niassa"]],
	10: [-19.823, 34.83483333, ["ソファラ州", "Sofala", "Sofala", "Sofala", "Sofala", "Sofala", "Sofala"]],
	11: [-16.1585, 33.58516667, ["テテ州", "Tete", "Tete", "Tete", "Tete", "Tete", "Tete"]],
	12: [-17.87466667, 36.88733333, ["ザンベジア州", "Zambezia", "Zambezia", "Zambézia", "Zambezia", "Zambezia", "Zambezia"]]
}

regioninfo_093 = {
	1: [0, 0, ["ナミビア", "Namibia", "Namibia", "Namibie", "Namibia", "Namibia", "Namibië"]],
	2: [-22.55366667, 17.0835, ["ホマス州", "Khomas", "Khomas", "Khomas", "Khomas", "Khomas", "Khomas"]],
	3: [-17.50233333, 24.255, ["カプリビ州", "Caprivi", "Caprivi", "Caprivi", "Caprivi", "Caprivi", "Caprivi"]],
	4: [-22.674, 14.527, ["エロンゴ州", "Erongo", "Erongo", "Erongo", "Erongo", "Erongo", "Erongo"]],
	5: [-24.62166667, 17.95683333, ["ハルダプ州", "Hardap", "Hardap", "Hardap", "Hardap", "Hardap", "Hardap"]],
	6: [-26.57116667, 18.1335, ["カラス州", "Karas", "Karas", "Karas", "Karas", "Karas", "Karas"]],
	7: [-17.92383333, 19.75583333, ["カバンゴ州", "Okavango", "Kavango", "Kavango", "Kavango", "Kavango", "Kavango"]],
	8: [-18.05983333, 13.84316667, ["クネネ州", "Kunene", "Kunene", "Kunene", "Kunene", "Kunene", "Kunene"]],
	9: [-17.41866667, 16.31866667, ["オハングウェナ州", "Ohangwena", "Ohangwena", "Ohangwena", "Ohangwena", "Ohangwena", "Ohangwena"]],
	10: [-22.45066667, 18.97, ["オマヘケ州", "Omaheke", "Omaheke", "Omaheke", "Omaheke", "Omaheke", "Omaheke"]],
	11: [-17.5, 15, ["オムサティ州", "Omusati", "Omusati", "Omusati", "Omusati", "Omusati", "Omusati"]],
	12: [-17.782, 15.695, ["オシャナ州", "Oshana", "Oshana", "Oshana", "Oshana", "Oshana", "Oshana"]],
	13: [-19.25016667, 17.70733333, ["オシコト州", "Oshikoto", "Oshikoto", "Oshikoto", "Oshikoto", "Oshikoto", "Oshikoto"]],
	14: [-20.4585, 16.65166667, ["オチョソンデュパ州", "Otjozondjupa", "Otjozondjupa", "Otjozondjupa", "Otjozondjupa", "Otjozondjupa", "Otjozondjupa"]]
}

regioninfo_094 = {
	1: [0, 0, ["オランダ", "Netherlands", "Niederlande", "Pays-Bas", "Países Bajos", "Paesi Bassi", "Nederland"]],
	2: [52.369, 4.886, ["ノールト・ホラント州", "North Holland", "Nordholland", "Hollande septentrionale", "Holanda Septentrional", "Olanda Settentrionale", "Noord-Holland"]],
	3: [52.99183333, 6.555833333, ["ドレンテ州", "Drenthe", "Drenthe", "Drenthe", "Drente", "Drenthe", "Drenthe"]],
	4: [52.5075, 5.469833333, ["フレボラント州", "Flevoland", "Flevoland", "Flevoland", "Flevoland", "Flevoland", "Flevoland"]],
	5: [53.19266667, 5.785666667, ["フリースラント州", "Friesland", "Friesland", "Frise", "Frisia", "Frisia", "Friesland"]],
	6: [51.98466667, 5.905833333, ["ヘルデンラント州", "Gelderland", "Gelderland", "Gueldre", "Güeldres", "Gheldria", "Gelderland"]],
	7: [53.21816667, 6.571833333, ["フローニンゲン州", "Groningen", "Groningen", "Groningue", "Groninga", "Groninga", "Groningen"]],
	8: [50.85066667, 5.676333333, ["リンビュルフ州", "Limburg", "Limburg", "Limbourg", "Limburgo", "Limburgo", "Limburg"]],
	9: [51.692, 5.316833333, ["ノールト・ブラバント州", "North Brabant", "Nordbrabant", "Brabant septentrional", "Brabante Septentrional", "Brabante Settentrionale", "Noord-Brabant"]],
	10: [52.50916667, 6.087666667, ["オーベルアイセル州", "Overijssel", "Overijssel", "Overijssel", "Overijssel", "Overijssel", "Overijssel"]],
	11: [52.083, 4.313, ["ゾイト・ホラント州", "South Holland", "Südholland", "Hollande méridionale", "Holanda Meridional", "Olanda Meridionale", "Zuid-Holland"]],
	12: [52.08833333, 5.108666667, ["ユトレヒト州", "Utrecht", "Utrecht", "Utrecht", "Utrecht", "Utrecht", "Utrecht"]],
	13: [51.499, 3.61, ["ゼーラント州", "Zeeland", "Zeeland", "Zélande", "Zelanda", "Zelanda", "Zeeland"]]
}

regioninfo_095 = {
	1: [0, 0, ["ニュージーランド", "New Zealand", "Neuseeland", "Nouvelle-Zélande", "Nueva Zelanda", "Nuova Zelanda", "Nieuw-Zeeland"]],
	2: [-41.3162, 174.782, ["ウェリントン", "Wellington", "Wellington", "Wellington", "Región de Wellington", "Wellington", "Wellington"]],
	3: [-36.895, 174.76, ["オークランド", "Auckland", "Auckland", "Auckland", "Auckland", "Auckland", "Auckland"]],
	4: [-37.68, 176.17, ["ベイ・オブ・プレンティ", "Bay of Plenty", "Bay of Plenty", "Bay of Plenty", "Bahía de Plenty", "Bay of Plenty", "Bay of Plenty"]],
	5: [-43.53, 172.64, ["カンタベリー", "Canterbury", "Canterbury", "Canterbury", "Región de Canterbury", "Canterbury", "Canterbury"]],
	6: [-45.883, 170.474, ["ダニーデン", "Otago", "Otago", "Otago", "Otago", "Otago", "Otago"]],
	7: [-39.5, 176.89, ["ホークスベイ", "Hawke's Bay", "Hawke's Bay", "Hawke's Bay", "Bahía de Hawke", "Hawke's Bay", "Hawke's Bay"]],
	8: [-40.36, 175.62, ["マナワツ・ワンガヌイ", "Manawatu-Wanganui", "Manawatu-Wanganui", "Manawatu-Wanganui", "Manawatu-Wanganui", "Manawatu-Wanganui", "Manawatu-Wanganui"]],
	9: [-41.2965, 173.248, ["ネルソン", "Nelson", "Nelson", "Nelson Bay", "Nelson", "Nelson", "Nelson"]],
	10: [-35.7207, 174.316, ["ノースランド", "Northland", "Northland", "Northland", "Northland", "Northland", "Northland"]],
	11: [-38.1428, 176.238, ["ロトルア", "Rotorua", "Rotorua", "Rotorua", "Rotorua", "Rotorua", "Rotorua"]],
	12: [-46.4127, 168.373, ["サウスランド", "Southland", "Southland", "Southland", "Southland", "Southland", "Zuidereiland"]],
	13: [-39.0702, 174.0783, ["タラナキ", "Taranaki", "Taranaki", "Taranaki", "Taranaki", "Taranaki", "Taranaki"]],
	14: [-37.78, 175.27, ["ワイカト", "Waikato", "Waikato", "Waikato", "Waikato", "Waikato", "Waikato"]]
}

regioninfo_096 = {
	1: [0, 0, ["ノルウェー", "Norway", "Norwegen", "Norvège", "Noruega", "Norvegia", "Noorwegen"]],
	2: [59.936, 10.70733333, ["オストランデット", "Østlandet", "Østlandet", "Østlandet", "Østlandet", "Norvegia dell'Est", "Østlandet"]],
	3: [69.66683333, 18.95233333, ["ノルド・ノルゲ", "Nord-Norge", "Nord-Norge", "Nord-Norge", "Noruega Septentrional", "Norvegia del Nord", "Nord-Norge"]],
	4: [63.40983333, 10.40716667, ["トロンデラグ", "Trøndelag", "Trøndelag", "Trøndelag", "Trøndelag", "Trøndelag", "Trøndelag"]],
	5: [60.3395, 5.340833333, ["ヴェストランネ", "Vestlandet", "Vestlandet", "Vestlandet", "Vestlandet", "Norvegia dell'Ovest", "Vestlandet"]],
	6: [58.15, 7.9895, ["ソールランネ", "Sørlandet", "Sørlandet", "Sørlandet", "Sørlandet", "Norvegia del Sud", "Sørlandet"]]
}

regioninfo_097 = {
	1: [0, 0, ["ポーランド", "Poland", "Polen", "Pologne", "Polonia", "Polonia", "Polen"]],
	2: [52.24016667, 21.007, ["マゾフシェ", "Masovia", "Masowien", "Mazovie", "Mazovia", "Masovia", "Mazovië"]],
	3: [51.11666667, 17.03333333, ["ドルヌィ・シロンスク", "Lower Silesia", "Niederschlesien", "Basse-Silésie", "Baja Silesia", "Bassa Slesia", "Neder-Silezië"]],
	4: [53.11666667, 18.03333333, ["クヤヴィ・ポモージェ", "Kuyavia-Pomerania", "Kujawien-Pommern", "Cujavie-Poméranie", "Cuyavia y Pomerania", "Cuiavia-Pomerania", "Kujavië-Pommeren"]],
	5: [51.77333333, 19.4725, ["ウッジ", "Lodz", "Lodsch", "Lodz", "Lodz", "Lodz", "Lodz"]],
	6: [51.2385, 22.57316667, ["ルブリン", "Lublin", "Lublin", "Lublin", "Lublin", "Lublino", "Lublin"]],
	7: [52.73483333, 15.235, ["ルブシュ", "Lubusz", "Lebus", "Lubusz", "Lebus", "Lebus", "Lubusz"]],
	8: [50.05733333, 19.942, ["マウォポルスカ", "Lesser Poland", "Kleinpolen", "Petite-Pologne", "Pequeña Polonia", "Piccola Polonia", "Klein-Polen"]],
	9: [50.6685, 17.92366667, ["オポーレ", "Opole", "Oppeln", "Opole", "Opole", "Opole", "Opole"]],
	10: [50.03983333, 22.00966667, ["ポトカルパチェ", "Subcarpathia", "Karpatenvorland", "Basses-Carpates", "Subcarpacia", "Precarpazi", "Subkarpaten"]],
	11: [53.13733333, 23.156, ["ポドラシェ", "Podlasie", "Podlachien", "Podlachie", "Podlaquia", "Podlachia", "Podlachië"]],
	12: [54.35583333, 18.63733333, ["ポモージェ", "Pomerania", "Pommern", "Poméranie", "Pomerania", "Pomerania", "Pommeren"]],
	13: [50.26866667, 19.01716667, ["シュレジエン", "Silesia", "Schlesien", "Silésie", "Silesia", "Slesia", "Silezië"]],
	14: [50.87016667, 20.626, ["シフィェンティクシシュ", "Swietokrzyskie", "Heiligkreuz", "Sainte-Croix", "Santa Cruz", "Santacroce", "Swiety Krzyz"]],
	15: [53.77333333, 20.48816667, ["ヴァルミア・マスールィ", "Warmia-Masuria", "Ermland-Masuren", "Warmie-Mazurie", "Varmia y Masuria", "Varmia-Masuria", "Ermland-Mazurië"]],
	16: [52.391, 16.88566667, ["ヴィェルコポルスカ", "Greater Poland", "Großpolen", "Grande-Pologne", "Gran Polonia", "Grande Polonia", "Groot-Polen"]],
	17: [53.70166667, 16.70283333, ["西ポモージェ", "Western Pomerania", "Westpommern", "Poméranie Occidentale", "Pomerania Occidental", "Pomerania Occidentale", "West-Pommeren"]]
}

regioninfo_098 = {
	1: [0, 0, ["ポルトガル", "Portugal", "Portugal", "Portugal", "Portugal", "Portogallo", "Portugal"]],
	2: [38.7245, -9.1425, ["リスボン都市圏", "Lisbon", "Lissabon", "Lisbonne", "Lisboa", "Lisbona", "Lissabon"]],
	3: [38.55616667, -7.903333333, ["アレンテージョ", "Alentejo", "Alentejo", "Alentejo", "Alentejo", "Alentejo", "Alentejo"]],
	4: [37.01683333, -7.9255, ["アルガルベ", "Algarve", "Algarve", "Algarve", "Algarve", "Algarve", "Algarve"]],
	5: [40.20783333, -8.4095, ["セントロ", "Centro", "Zentralportugal", "Région Centre", "Centro", "Centro", "Centro"]],
	6: [41.15083333, -8.604166667, ["ノルテ", "Norte", "Nordportugal", "Région Nord", "Norte", "Nord", "Norte"]],
	7: [32.644, -16.909, ["マディラ自治州", "Madeira", "Madeira", "Madère", "Madeira", "Madera", "Madeira"]],
	8: [37.741, -25.66666667, ["アソレス自治州", "Azores", "Azoren", "Açores", "Azores", "Azzorre", "Azoren"]]
}

regioninfo_099 = {
	1: [0, 0, ["ルーマニア", "Romania", "Rumänien", "Roumanie", "Rumanía", "Romania", "Roemenië"]],
	2: [44.43333333, 26.08333333, ["ブカレスト州", "Bucharest", "Bukarest", "Bucarest", "Bucarest", "Bucarest", "Boekarest"]],
	3: [46.06833333, 23.56666667, ["アルバ州", "Alba", "Alba", "Alba", "Alba", "Alba", "Alba"]],
	4: [46.18333333, 21.31666667, ["アラド州", "Arad", "Arad", "Arad", "Arad", "Arad", "Arad"]],
	5: [44.85, 24.88333333, ["アルジェシュ州", "Arges", "Arges", "Arges", "Arges", "Arges", "Arges"]],
	6: [46.57, 26.91666667, ["バカウ州", "Bacau", "Bacau", "Bacau", "Bacau", "Bacau", "Bacau"]],
	7: [47.06666667, 21.91666667, ["ビホル州", "Bihor", "Bihor", "Bihor", "Bihor", "Bihor", "Bihor"]],
	8: [47.13333333, 24.5, ["ビストリツァ・ナサウド州", "Bistrita-Nasaud", "Bistrita-Nasaud", "Bistrita-Nasaud", "Bistrita-Nasaud", "Bistrita-Nasaud", "Bistrita-Nasaud"]],
	9: [47.75, 26.66666667, ["ボトシャニ州", "Botosani", "Botosani", "Botosani", "Botosani", "Botosani", "Botosani"]],
	10: [45.28333333, 27.96666667, ["ブライラ州", "Braila", "Braila", "Braila", "Braila", "Braila", "Braila"]],
	11: [45.65, 25.61666667, ["ブラショヴ州", "Brasov", "Brasov", "Brasov", "Brasov", "Brasov", "Brasov"]],
	12: [45.15, 26.81666667, ["ブザウ州", "Buzau", "Buzau", "Buzau", "Buzau", "Buzau", "Buzau"]],
	13: [44.2, 27.33333333, ["カララシ州", "Calarasi", "Calarasi", "Calarasi", "Calarasi", "Calarasi", "Calarasi"]],
	14: [45.3, 21.88333333, ["カラシュ・セヴェリン州", "Caras-Severin", "Caras-Severin", "Caras-Severin", "Caras-Severin", "Caras-Severin", "Caras-Severin"]],
	15: [46.78333333, 23.58333333, ["クルージュ州", "Cluj", "Cluj", "Cluj", "Cluj", "Cluj", "Cluj"]],
	16: [44.18333333, 28.63333333, ["コンスタンツァ州", "Constanta", "Constanta", "Constanta", "Constanta", "Constanza", "Constanta"]],
	17: [45.86666667, 25.8, ["コヴァスナ州", "Covasna", "Covasna", "Covasna", "Covasna", "Covasna", "Covasna"]],
	18: [44.938, 25.459, ["ドゥンボビツァ州", "Dâmbovita", "Dâmbovita", "Dâmbovita", "Dâmbovita", "Dâmbovita", "Dâmbovita"]],
	19: [44.31666667, 23.81666667, ["ドルジュ州", "Dolj", "Dolj", "Dolj", "Dolj", "Dolj", "Dolj"]],
	20: [45.43333333, 28.03333333, ["ガラツィ州", "Galati", "Galati", "Galati", "Galati", "Galati", "Galati"]],
	21: [43.9, 25.96666667, ["ジュルジュ州", "Giurgiu", "Giurgiu", "Giurgiu", "Giurgiu", "Giurgiu", "Giurgiu"]],
	22: [45.05, 23.26666667, ["ゴルジュ州", "Gorj", "Gorj", "Gorj", "Gorj", "Gorj", "Gorj"]],
	23: [46.36666667, 25.8, ["ハルギタ州", "Harghita", "Harghita", "Harghita", "Harghita", "Harghita", "Harghita"]],
	24: [45.88333333, 22.90333333, ["フネドアラ州", "Hunedoara", "Hunedoara", "Hunedoara", "Hunedoara", "Hunedoara", "Hunedoara"]],
	25: [44.56666667, 27.38333333, ["ヤロミツァ州", "Ialomita", "Ialomita", "Ialomita", "Ialomita", "Ialomita", "Ialomita"]],
	26: [47.16666667, 27.56666667, ["ヤシ州", "Iasi", "Iasi", "Iasi", "Iasi", "Iasi", "Iasi"]],
	27: [44.56666667, 25.95, ["イルホヴ州", "Ilfov", "Ilfov", "Ilfov", "Ilfov", "Ilfov", "Ilfov"]],
	28: [47.65, 23.58333333, ["マラムレシュ州", "Maramures", "Maramures", "Maramures", "Maramures", "Maramures", "Maramures"]],
	29: [44.63333333, 22.65, ["メヘディンツィ州", "Mehedinti", "Mehedinti", "Mehedinti", "Mehedinti", "Mehedinti", "Mehedinti"]],
	30: [46.53833333, 24.55, ["ムレシュ州", "Mures", "Mures", "Mures", "Mures", "Mures", "Mures"]],
	31: [46.93333333, 26.36666667, ["ネアムツ州", "Neamt", "Neamt", "Neamt", "Neamt", "Neamt", "Neamt"]],
	32: [44.43333333, 24.35, ["オルト州", "Olt", "Olt", "Olt", "Olt", "Olt", "Olt"]],
	33: [44.93333333, 26.01666667, ["プラホヴァ州", "Prahova", "Prahova", "Prahova", "Prahova", "Prahova", "Prahova"]],
	34: [47.18333333, 23.055, ["サラージュ州", "Salaj", "Salaj", "Salaj", "Salaj", "Salaj", "Salaj"]],
	35: [47.78833333, 22.88333333, ["サトゥ・マーレ州", "Satu Mare", "Satu Mare", "Satu Mare", "Satu Mare", "Satu Mare", "Satu Mare"]],
	36: [45.78333333, 24.15, ["シビウ州", "Sibiu", "Sibiu", "Sibiu", "Sibiu", "Sibiu", "Sibiu"]],
	37: [47.65, 26.25, ["スチャヴァ州", "Suceava", "Suceava", "Suceava", "Suceava", "Suceava", "Suceava"]],
	38: [43.96666667, 25.33333333, ["テレオルマン州", "Teleorman", "Teleorman", "Teleorman", "Teleorman", "Teleorman", "Teleorman"]],
	39: [45.755, 21.225, ["ティミシュ州", "Timis", "Timis", "Timis", "Timis", "Timis", "Timis"]],
	40: [45.16666667, 28.8, ["トゥルチャ州", "Tulcea", "Tulcea", "Tulcea", "Tulcea", "Tulcea", "Tulcea"]],
	41: [45.10666667, 24.37333333, ["ヴルチャ州", "Vâlcea", "Vâlcea", "Vâlcea", "Vâlcea", "Vâlcea", "Vâlcea"]],
	42: [46.64, 27.72333333, ["ヴァスルイ州", "Vaslui", "Vaslui", "Vaslui", "Vaslui", "Vaslui", "Vaslui"]],
	43: [45.7, 27.18333333, ["フランチェア州", "Vrancea", "Vrancea", "Vrancea", "Vrancea", "Vrancea", "Vrancea"]]
}

regioninfo_100 = {
	1: [0, 0, ["ロシア", "Russia", "Russland", "Russie", "Rusia", "Russia", "Rusland"]],
	2: [55.76666667, 37.61666667, ["中央連邦管区", "Central Federal District", "Zentralrussland", "District fédéral central", "Distrito Federal Central", "Distretto Federale Centrale", "Centraal Federaal District"]],
	3: [48.48433333, 135.0931667, ["極東連邦管区", "Far Eastern Federal District", "Ferner Osten", "District fédéral extrême-oriental", "Distrito Federal de Extremo Oriente", "Estremo Oriente Russo ", "Federaal District Verre Oosten"]],
	4: [59.93333333, 30.43333333, ["北西連邦管区", "Northwestern Federal District", "Nordwestrussland", "District fédéral du Nord-Ouest", "Distrito Federal del Noroeste", "Distretto Federale Nordoccidentale", "Noordwestelijk Federaal District"]],
	5: [55.03333333, 82.93583333, ["シベリア連邦管区", "Siberian Federal District", "Sibirien", "District fédéral sibérien", "Distrito Federal de Siberia", "Distretto Federale Siberiano", "Federaal District Siberië"]],
	6: [47.21666667, 39.71666667, ["南部連邦管区", "Southern Federal District", "Südrussland", "District fédéral du Sud", "Distrito Federal Meridional", "Distretto Federale Meridionale", "Zuidelijk Federaal District"]],
	7: [56.83333333, 60.6, ["ウラル連邦管区", "Urals Federal District", "Ural", "District fédéral de l'Oural", "Distrito Federal de los Urales", "Distretto Federale degli Urali", "Federaal District Oeral"]],
	8: [56.28716667, 43.93333333, ["沿ヴォルガ連邦管区", "Volga Federal District", "Wolga", "District fédéral de Privoljsk", "Distrito Federal del Volga", "Distretto Federale del Volga", "Federaal District Wolga"]]
}

regioninfo_101 = {
	1: [0, 0, ["セルビア", "Serbia", "Serbien", "Serbie", "Serbia", "Serbia", "Servië"]],
	2: [44.83433333, 20.4865, ["中央セルビア", "Central Serbia", "Engeres Serbien", "Serbie Intérieure", "Serbia Central", "Serbia Centrale", "Centraal Servië"]],
	3: [46.07116667, 19.67633333, ["ボイボディナ", "Vojvodina", "Vojvodina", "Voïvodine", "Vojvodina", "Vojvodina", "Vojvodina"]],
	4: [42.6525, 21.1595, ["コソボ・メトヒア", "Kosovo & Metohija", "Kosovo", "Kosovo", "Kosovo y Metohija", "Kosovo e Metohija", "Kosovo-Metohija"]]
}

regioninfo_102 = {
	1: [0, 0, ["スロバキア", "Slovakia", "Slowakei", "Slovaquie", "Eslovaquia", "Slovacchia", "Slowakije"]],
	2: [48.152, 17.124, ["ブラティスラバ", "Bratislava", "Bratislava", "Bratislava", "Bratislava", "Bratislava", "Bratislava"]],
	3: [48.726, 19.145, ["バンスカ・ビストリツァ", "Banská Bystrica", "Banská Bystrica", "Banská Bystrica", "Banska Bystrica", "Banská Bystrica", "Banská Bystrica"]],
	4: [48.72333333, 21.2565, ["コシツェ", "Košice", "Košice", "Košice", "Kosice", "Košice", "Košice"]],
	5: [48.30383333, 18.0755, ["二トラ", "Nitra", "Nitra", "Nitra", "Nitra", "Nitra", "Nitra"]],
	6: [48.97066667, 21.2575, ["プレショフ", "Prešov", "Prešov", "Prešov", "Presov", "Prešov", "Prešov"]],
	7: [48.893, 18.054, ["トレンチーン", "Trencín", "Trencín", "Trencin", "Trencin", "Trencín", "Trencin"]],
	8: [48.37633333, 17.576, ["トルナバ", "Trnava", "Trnava", "Trnava", "Trnava", "Trnava", "Trnava"]],
	9: [49.2195, 18.72633333, ["ジリナ", "Žilina", "Žilina", "Zilina", "Zilina", "Žilina", "Žilina"]]
}

regioninfo_103 = {
	1: [0, 0, ["スロベニア", "Slovenia", "Slowenien", "Slovénie", "Eslovenia", "Slovenia", "Slovenië"]],
	2: [46.053, 14.50216667, ["クラニェスカ地方", "Carniola", "Krain", "Carniole", "Carniola", "Carniola", "Krain"]],
	3: [46.5525, 15.63516667, ["シュタィエルスカ地方", "Lower Styria", "Untersteiermark", "Styrie", "Estiria", "Stiria Slovena", "Stiermarken"]],
	4: [46.656, 16.15666667, ["プレクムリエ地方", "Prekmurje", "Prekmurje", "Prekmurje", "Región del Mur", "Prekmurje", "Prekmurje"]],
	5: [45.53783333, 13.723, ["プリモルスカ地方", "Slovenian Littoral", "Primorska", "Littoral", "Región del Litoral", "Litorale", "Küstenland"]],
	6: [46.5065, 15.0685, ["カリンティア地方", "Carinthia", "Slovenska Koroska", "Carinthie", "Carintia", "Carinzia Slovena", "Karinthië"]]
}

regioninfo_104 = {
	1: [0, 0, ["南アフリカ", "South Africa", "Südafrika", "Afrique du Sud", "Sudáfrica", "Repubblica Sudafricana", "Zuid-Afrika"]],
	2: [-26.143, 28.05, ["ハウテン州", "Gauteng", "Gauteng", "Gauteng", "Gauteng", "Gauteng", "Gauteng"]],
	3: [-33.92133333, 18.4245, ["ウェスタン・ケープ州", "Western Cape", "Westkap", "Cap-Occidental", "Cabo Occidental", "Capo Occidentale", "West-Kaap"]],
	4: [-28.74333333, 24.77666667, ["ノーザン・ケープ州", "Northern Cape", "Nordkap", "Cap-du-Nord", "Cabo del Norte", "Capo Settentrionale", "Noord-Kaap"]],
	5: [-32.876, 27.38733333, ["イースタン・ケープ州", "Eastern Cape", "Ostkap", "Cap-Oriental", "Cabo Oriental", "Capo Orientale", "Oost-Kaap"]],
	6: [-29.6005, 30.38333333, ["クワズールー・ナタール州", "KwaZulu-Natal", "KwaZulu-Natal", "KwaZulu-Natal", "KwaZulu-Natal", "KwaZulu-Natal", "KwaZoeloe-Natal"]],
	7: [-29.1185, 26.2215, ["フリー・ステート州", "Free State", "Freistaat", "Etat-libre", "Estado Libre", "Stato Libero", "Vrijstaat"]],
	8: [-25.85566667, 25.65133333, ["ノース・ウェスト州", "North West", "Nordwest", "Province du Nord-Ouest", "Noroeste", "Nord Ovest", "Noordwest"]],
	9: [-25.466, 30.9845, ["ムプマランガ州", "Mpumalanga", "Mpumalanga", "Mpumalanga", "Mpumalanga", "Mpumalanga", "Mpumalanga"]],
	10: [-23.89316667, 29.44316667, ["リンポポ州", "Limpopo", "Limpopo", "Limpopo", "Limpopo", "Limpopo", "Limpopo"]]
}

regioninfo_105 = {
	1: [0, 0, ["スペイン", "Spain", "Spanien", "Espagne", "España", "Spagna", "Spanje"]],
	2: [40.41666667, -3.7025, ["マドリード州", "Madrid", "Madrid", "Madrid", "Comunidad de Madrid", "Comunità di Madrid", "Madrid"]],
	3: [37.38583333, -6, ["アンダルシーア州", "Andalusia", "Andalusien", "Andalousie", "Andalucía", "Andalusia", "Andalusië"]],
	4: [41.65, -0.873333333, ["アラゴン州", "Aragon", "Aragonien", "Aragon", "Aragón", "Aragona", "Aragón"]],
	5: [43.36666667, -5.838333333, ["アストゥーリアス州", "Principality of Asturias", "Asturien", "Asturies", "Principado de Asturias", "Asturie", "Asturië"]],
	6: [39.56916667, 2.641666667, ["バレアーレス諸島", "Balearic Islands", "Balearische Inseln", "Iles Baléares", "Illes Balears", "Baleari", "Balearen"]],
	7: [28.12166667, -15.431, ["カナリア諸島", "Canary Islands", "Kanarische Inseln", "Canaries", "Canarias", "Canarie", "Canarische Eilanden"]],
	8: [43.462, -3.805, ["カンタブリア州", "Cantabria", "Kantabrien", "Cantabrie", "Cantabria", "Cantabria", "Cantabrië"]],
	9: [39.855, -4.024, ["カスティーリャ・ラ・マンチャ", "Castile-La Mancha", "Kastilien-La Mancha", "Castille-La Manche", "Castilla-La Mancha", "Castiglia-La Mancia", "Kastilië-La Mancha"]],
	10: [41.64166667, -4.72, ["カスティーリャ・レオン", "Castilla y León", "Kastilien-León", "Castille-et-León", "Castilla y León", "Castiglia e Leon", "Kastilië en León"]],
	11: [41.38333333, 2.172, ["カタルーニャ", "Catalonia", "Katalonien", "Catalogne", "Cataluña", "Catalogna", "Catalonië"]],
	12: [39.471, -0.367, ["バレンシア州", "Valencia", "Valencia", "Valence", "Comunidad Valenciana", "Comunità Valenciana", "Valencia"]],
	13: [38.914, -6.342, ["エストレマドゥーラ", "Extremadura", "Extremadura", "Estrémadure", "Extremadura", "Estremadura", "Extremadura"]],
	14: [42.879, -8.543, ["ガリーシア", "Galicia", "Galicien", "Galice", "Galicia", "Galizia", "Galicië"]],
	15: [37.98333333, -1.126, ["ムルシア州", "Murcia", "Murcia", "Murcie", "Región de Murcia", "Murcia", "Murcia"]],
	16: [42.814, -1.648, ["ナバーラ州", "Navarre", "Navarra", "Navarre", "Comunidad Foral de Navarra", "Navarra", "Navarra"]],
	17: [42.849, -2.672, ["バスク", "Basque Country", "Baskenland", "Pays basque", "País Vasco", "Paesi Baschi", "Baskenland"]],
	18: [42.46666667, -2.45, ["ラ・リオハ州", "La Rioja", "La Rioja", "La Rioja", "La Rioja", "La Rioja", "La Rioja"]]
}

regioninfo_106 = {
	1: [0, 0, ["エスワティニ", "Eswatini", "Eswatini", "Eswatini", "Eswatini", "Eswatini", "Eswatini"]],
	2: [-26.31783333, 31.1395, ["ホホ", "Hhohho", "Hhohho", "Hhohho", "Hhohho", "Hhohho", "Hhohho"]],
	3: [-26.453, 31.95116667, ["ルボンボ", "Lubombo", "Lubombo", "Lubombo", "Lubombo", "Lubombo", "Lubombo"]],
	4: [-26.49033333, 31.38583333, ["マンジニ", "Manzini", "Manzini", "Manzini", "Manzini", "Manzini", "Manzini"]],
	5: [-27.107, 31.203, ["シセルウェニ", "Shiselweni", "Shiselweni", "Shiselweni", "Shiselweni", "Shiselweni", "Shiselweni"]]
}

regioninfo_107 = {
	1: [0, 0, ["スウェーデン", "Sweden", "Schweden", "Suède", "Suecia", "Svezia", "Zweden"]],
	2: [59.286, 18.073, ["ストックホルム州", "Stockholm County", "Stockholms län", "Comté de Stockholm", "Estocolmo", "Stoccolma", "Stockholms län"]],
	3: [55.6015, 13.0005, ["スコーネ州", "Skåne County", "Skåne län", "Comté de Skåne", "Escania", "Scania", "Skåne län"]],
	4: [57.709, 11.971, ["ヴェストラ・イェータランド州", "Västra Götaland County", "Västra Götalands län", "Comté de Västra Götaland", "Västra Götaland", "Västra Götaland", "Västergötlands län"]],
	5: [58.402, 15.638, ["エステルイェトランド州", "Östergötland County", "Östergötlands län", "Comté d'Ostergötland", "Östergötland", "Östergötland", "Östergötlands län"]],
	6: [58.756, 17.015, ["セーデルマンランド州", "Södermanland County", "Södermanlands län", "Comté de Södermanland", "Södermanland", "Södermanland", "Södermanlands län"]],
	7: [59.387, 13.50283333, ["ベルムランド州", "Värmland County", "Värmlands län", "Comté de Värmland", "Värmland", "Värmland", "Värmlands län"]],
	8: [59.855, 17.63333333, ["ウプサラ州", "Uppsala County", "Uppsala län", "Comté d’Uppsala", "Uppsala", "Uppsala", "Uppsala län"]],
	9: [60.672, 17.183, ["イェーブレボリ州", "Gävleborg County", "Gävleborgs län", "Comté de Gävleborg", "Gävleborg", "Gävleborg", "Gävleborgs län"]],
	10: [63.82283333, 20.252, ["ベステルボッテン州", "Västerbotten County", "Västerbottens län", "Comté de Västerbotten", "Västerbotten", "Västerbotten", "Västerbottens län"]],
	11: [65.58, 22.216, ["ノルボッテン州", "Norrbotten County", "Norrbottens län", "Comté de Norrbotten", "Norrbotten", "Norrbotten", "Norrbottens län"]],
	12: [57.63666667, 18.29, ["ゴトランド州", "Gotland Island", "Gotland", "Gotland", "Gotland", "Gotland", "Gotland län"]],
	13: [63.17083333, 14.651, ["イェムトランド州", "Jämtland County", "Jämtlands län", "Comté de Jämtland", "Jämtland", "Jämtland", "Jämtlands län"]],
	14: [60.613, 15.647, ["ダーラナ州", "Dalarna County", "Dalarnas län", "Comté de Dalarna", "Dalecarlia", "Dalarna", "Dalarnas län"]],
	15: [56.17083333, 15.588, ["ブレーキンゲ州", "Blekinge County", "Blekinge län", "Comté de Blekinge", "Blekinge", "Blekinge", "Blekinge län"]],
	16: [59.27483333, 15.224, ["エレブルー州", "Örebro County", "Örebro län", "Comté d'Orebro", "Örebro", "Örebro", "Örebro län"]],
	17: [62.633, 17.934, ["ベステルノルランド州", "Västernorrland County", "Västernorrlands län", "Comté de Västernorrland", "Västernorrland", "Västernorrland", "Västernorrlands län"]],
	18: [57.77583333, 14.169, ["イェンチェピング州", "Jönköping County", "Jönköpings län", "Comté de Jönköping", "Jönköping", "Jönköping", "Jönköpings län"]],
	19: [56.88366667, 14.81966667, ["クロノベリ州", "Kronoberg County", "Kronobergs län", "Comté de Kronoberg", "Kronoberg", "Kronoberg", "Kronobergs län"]],
	20: [56.66666667, 16.36833333, ["カルマル州", "Kalmar County", "Kalmar län", "Comté de Kalmar", "Kalmar", "Kalmar", "Kalmar län"]],
	21: [59.61683333, 16.55516667, ["ベストマンランド州", "Västmanland County", "Västmanlands län", "Comté de Västmanland", "Västmanland", "Västmanland", "Västmanlands län"]],
	22: [56.659, 12.861, ["ハランド州", "Halland County", "Hallands län", "Comté de Halland", "Halland", "Halland", "Hallands län"]]
}

regioninfo_108 = {
	1: [0, 0, ["スイス", "Switzerland", "Schweiz", "Suisse", "Suiza", "Svizzera", "Zwitserland"]],
	2: [46.95383333, 7.417666667, ["ベルン州", "Bern", "Bern", "Berne", "Berna", "Berna", "Bern"]],
	3: [47.34266667, 9.409333333, ["アッペンツェル", "Appenzell", "Appenzell", "Appenzell", "Appenzell", "Appenzello", "Appenzell"]],
	4: [47.394795, 8.04623, ["アールガウ州", "Aargau", "Aargau", "Argovie", "Argovia", "Argovia", "Aargau"]],
	5: [47.54266667, 7.587833333, ["バーゼル", "Basel-City", "Basel", "Bâle-Ville", "Basilea", "Basilea Città", "Bazel"]],
	6: [46.80516667, 7.1585, ["フリブール州", "Fribourg", "Freiburg", "Fribourg", "Friburgo", "Friburgo", "Fribourg"]],
	7: [46.20283333, 6.169, ["ジュネーヴ州", "Geneva", "Genf", "Genève", "Ginebra", "Ginevra", "Genève"]],
	8: [47.03766667, 9.072666667, ["グラールス州", "Glarus", "Glarus", "Glaris", "Glaris", "Glarona", "Glarus"]],
	9: [46.85983333, 9.5415, ["グラウビュンデン州", "Graubünden", "Graubünden", "Grisons", "Grisones", "Grigioni", "Graubünden"]],
	10: [47.36733333, 7.516833333, ["ジュラ州", "Jura", "Jura", "Jura", "Jura", "Giura", "Jura"]],
	11: [47.05233333, 8.307, ["ルツェルン州", "Luzern", "Luzern", "Lucerne", "Lucerna", "Lucerna", "Luzern"]],
	12: [46.95216667, 6.9345, ["ヌシャテル州", "Neuchâtel", "Neuenburg", "Neuchâtel", "Neuchatel", "Neuchâtel", "Neuchâtel"]],
	13: [46.88783333, 8.239166667, ["オプバルデン準州", "Obwalden", "Obwalden", "Obwald", "Obwalden", "Obvaldo", "Obwalden"]],
	14: [47.42483333, 9.374, ["ザンクト・ガレン州", "St. Gallen", "Sankt Gallen", "Saint-Gall", "Sankt Gallen", "San Gallo", "Sankt Gallen"]],
	15: [48.191, 9.043166667, ["シャフハウゼン州", "Schaffhausen", "Schaffhausen", "Schaffhouse", "Schaffhausen", "Sciaffusa", "Schaffhausen"]],
	16: [47.05066667, 8.618666667, ["シュビーツ州", "Schwyz", "Schwyz", "Schwytz", "Schwyz", "Svitto", "Schwyz"]],
	17: [47.20883333, 7.537166667, ["ゾーロトゥルン州", "Solothurn", "Solothurn", "Soleure", "Soleura", "Soletta", "Solothurn"]],
	18: [47.5565, 8.8915, ["トゥールガウ州", "Thurgau", "Thurgau", "Thurgovie", "Turgovia", "Turgovia", "Thurgau"]],
	19: [46.196941, 9.020233, ["ティチーノ州", "Ticino", "Tessin", "Tessin", "Tesino", "Ticino", "Ticino"]],
	20: [46.86766667, 8.637, ["ウーリ州", "Uri", "Uri", "Uri", "Uri", "Uri", "Uri"]],
	21: [46.236, 7.356, ["バレー州", "Valais", "Wallis", "Valais", "Valais", "Vallese", "Wallis"]],
	22: [46.522, 6.63, ["ボー州", "Vaud", "Waadt", "Vaud", "Vaud", "Vaud", "Vaud"]],
	23: [47.18, 8.504, ["ツーク州", "Zug", "Zug", "Zoug", "Zug", "Zugo", "Zug"]],
	24: [47.38983333, 8.541, ["チューリヒ州", "Zürich", "Zürich", "Zurich", "Zúrich", "Zurigo", "Zürich"]]
}

regioninfo_109 = {
	1: [0, 0, ["トルコ", "Turkey", "Türkei", "Turquie", "Turquía", "Turchia", "Turkije"]],
	2: [39.92433333, 32.852, ["アンカラ県", "Ankara", "Ankara", "Ankara", "Ankara", "Ankara", "Ankara"]],
	3: [41.0595, 29.0035, ["イスタンブル県", "Istanbul", "Istanbul", "Istanbul", "Estambul", "Istanbul", "Istanbul"]],
	4: [38.43333333, 27.1405, ["イズミル県", "Izmir", "Izmir", "Izmir", "Esmirna", "Smirne", "Izmir"]],
	5: [40.191, 29.0715, ["ブルサ県", "Bursa", "Bursa", "Bursa", "Bursa", "Bursa", "Bursa"]],
	6: [36.99316667, 35.32116667, ["アダナ県", "Adana", "Adana", "Adana", "Adana", "Adana", "Adana"]],
	7: [37.06783333, 37.387, ["ガジアンテプ県", "Gaziantep", "Gaziantep", "Gaziantep", "Gaziantep", "Gaziantep", "Gaziantep"]],
	8: [37.87316667, 32.47566667, ["コニヤ県", "Konya", "Konya", "Konya", "Konya", "Konya", "Konya"]],
	9: [36.88883333, 30.70566667, ["アンタリヤ県", "Antalya", "Antalya", "Antalya", "Antalya", "Antalya", "Antalya"]],
	10: [37.9085, 40.225, ["ディヤルバクル県", "Diyarbakir", "Diyarbakir", "Diyarbakir", "Diyarbakir", "Diyarbakir", "Diyarbakir"]],
	11: [36.8025, 34.63633333, ["メルシン県", "Mersin", "Mersin", "Mersin", "Mersin", "Mersin", "Mersin"]],
	12: [38.72533333, 35.47383333, ["カイセリ県", "Kayseri", "Kayseri", "Kayseri", "Kayseri", "Kayseri", "Kayseri"]],
	13: [39.78383333, 30.51816667, ["エスキシェヒル県", "Eskisehir", "Eskisehir", "Eskisehir", "Eskisehir", "Eskisehir", "Eskisehir"]],
	14: [37.15533333, 38.79133333, ["シャンルウルファ県", "Sanliurfa", "Sanliurfa", "Sanliurfa", "Sanliurfa", "Sanliurfa", "Sanliurfa"]],
	15: [38.353, 38.3055, ["マラティヤ県", "Malatya", "Malatya", "Malatya", "Malatya", "Malatya", "Malatya"]],
	16: [39.9025, 41.28833333, ["エルズルム県", "Erzurum", "Erzurum", "Erzurum", "Erzurum", "Erzurum", "Erzurum"]],
	17: [41.289, 36.32533333, ["サムスン県", "Samsun", "Samsun", "Samsun", "Samsun", "Samsun", "Samsun"]],
	18: [38.48666667, 43.40516667, ["ワン県", "Van", "Van", "Van", "Van", "Van", "Van"]],
	19: [37.58483333, 36.9355, ["カフラマンマラシュ県", "Kahramanmaras", "Kahramanmaras", "Kahramanmaras", "Kahramanmaras", "Kahramanmaras", "Kahramanmaras"]],
	20: [37.7725, 29.08516667, ["デニズリ県", "Denizli", "Denizli", "Denizli", "Denizli", "Denizli", "Denizli"]],
	21: [37.87533333, 41.13433333, ["バトマン県", "Batman", "Batman", "Batman", "Batman", "Batman", "Batman"]],
	22: [38.67516667, 39.2225, ["エラズー県", "Elazig", "Elazig", "Elazig", "Elazig", "Elazig", "Elazig"]],
	23: [40.788, 30.405, ["サカリヤ県", "Sakarya", "Sakarya", "Sakarya", "Sakarya", "Sakarya", "Sakarya"]],
	24: [40.774, 29.90583333, ["コジャエリ県", "Kocaeli", "Kocaeli", "Kocaeli", "Kocaeli", "Kocaeli", "Kocaeli"]],
	25: [39.74183333, 37.01733333, ["シワス県", "Sivas", "Sivas", "Sivas", "Sivas", "Sivas", "Sivas"]],
	26: [38.618, 27.424, ["マニサ県", "Manisa", "Manisa", "Manisa", "Manisa", "Manisa", "Manisa"]],
	27: [41.00083333, 39.71733333, ["トラブゾン県", "Trabzon", "Trabzon", "Trabzon", "Trebisonda", "Trabzon", "Trabzon"]],
	28: [39.64233333, 27.87616667, ["バルケシル県", "Balikesir", "Balikesir", "Balikesir", "Balikesir", "Balikesir", "Balikesir"]],
	29: [37.75883333, 38.27366667, ["アディヤマン県", "Adiyaman", "Adiyaman", "Adiyaman", "Adiyaman", "Adiyaman", "Adiyaman"]],
	30: [40.9845, 27.50983333, ["テキルダー県", "Tekirdag", "Tekirdag", "Tekirdag", "Tekirdag", "Tekirdag", "Tekirdag"]],
	31: [39.84133333, 33.509, ["クルッカレ県", "Kirikkale", "Kirikkale", "Kirikkale", "Kirikkale", "Kirikkale", "Kirikkale"]],
	32: [37.06733333, 36.25683333, ["オスマニエ県", "Osmaniye", "Osmaniye", "Osmaniye", "Osmaniye", "Osmaniye", "Osmaniye"]],
	33: [39.41816667, 29.9745, ["キュターヤ県", "Kütahya", "Kütahya", "Kütahya", "Kütahya", "Kütahya", "Kütahya"]],
	34: [40.5525, 34.95816667, ["チョルム県", "Corum", "Corum", "Çorum", "Corum", "Corum", "Corum"]],
	35: [37.75883333, 30.55383333, ["イスパルタ県", "Isparta", "Isparta", "Isparta", "Isparta", "Isparta", "Isparta"]],
	36: [37.8535, 27.83816667, ["アイドゥン県", "Aydin", "Aydin", "Aydin", "Aydin", "Aydin", "Aydin"]],
	37: [36.2, 36.17, ["ハタイ県", "Hatay", "Hatay", "Hatay", "Hatay", "Hatay", "Hatay"]],
	38: [37.30466667, 40.74316667, ["マルディン県", "Mardin", "Mardin", "Mardin", "Mardin", "Mardin", "Mardin"]],
	39: [38.36783333, 34.0355, ["アクサライ県", "Aksaray", "Aksaray", "Aksaray", "Aksaray", "Aksaray", "Aksaray"]],
	40: [38.76866667, 30.53733333, ["アフヨンカラヒサル", "Afyonkarahisar", "Afyonkarahisar", "Afyonkarahisar", "Afyon", "Afyonkarahisar", "Afyonkarahisar"]],
	41: [40.30366667, 36.55783333, ["トカト県", "Tokat", "Tokat", "Tokat", "Tokat", "Tokat", "Tokat"]],
	42: [41.67566667, 26.55733333, ["エディルネ県", "Edirne", "Edirne", "Edirne", "Edirne", "Edirne", "Edirne"]],
	43: [37.17216667, 33.22383333, ["カラマン県", "Karaman", "Karaman", "Karaman", "Karaman", "Karaman", "Karaman"]],
	44: [40.9835, 37.8725, ["オルドゥ県", "Ordu", "Ordu", "Ordu", "Ordu", "Ordu", "Ordu"]],
	45: [37.93983333, 41.92633333, ["シイルト県", "Siirt", "Siirt", "Siirt", "Siirt", "Siirt", "Siirt"]],
	46: [39.73716667, 39.50266667, ["エルジンジャン県", "Erzincan", "Erzincan", "Erzincan", "Erzincan", "Erzincam", "Erzincan"]],
	47: [40.60416667, 33.61933333, ["チャンクル県", "Cankiri", "Cankiri", "Çankiri", "Cankiri", "Cankiri", "Cankiri"]],
	48: [41.45383333, 31.7925, ["ゾングルダク県", "Zonguldak", "Zonguldak", "Zonguldak", "Zonguldak", "Zonguldak", "Zonguldak"]],
	49: [39.8175, 34.80866667, ["ヨズガト県", "Yozgat", "Yozgat", "Yozgat", "Yozgat", "Yozgat", "Yozgat"]],
	50: [38.676, 29.40483333, ["ウシャク県", "Usak", "Usak", "Usak", "Usak", "Usak", "Usak"]]
}

regioninfo_110 = {
	1: [0, 0, ["イギリス", "United Kingdom", "Großbritannien", "Royaume-Uni", "Reino Unido", "Regno Unito", "Verenigd Koninkrijk"]],
	2: [51.50533333, -0.120166667, ["イングランド", "England", "England", "Angleterre", "Inglaterra", "Inghilterra", "Engeland"]],
	3: [54.16733333, -4.483333333, ["マン島", "Isle of Man", "Isle of Man", "Ile de Man", "Isla de Man", "Isola di Man", "Man"]],
	4: [55.9545, -3.202666667, ["スコットランド", "Scotland", "Schottland", "Ecosse", "Escocia", "Scozia", "Schotland"]],
	5: [51.47798, -3.177053, ["ウェールズ", "Wales", "Wales", "Pays de Galles", "Gales", "Galles", "Wales"]],
	6: [54.58583333, -5.906, ["北アイルランド", "Northern Ireland", "Nordirland", "Irlande du Nord", "Irlanda del Norte", "Irlanda del Nord", "Noord-Ierland"]]
}

regioninfo_111 = {
	1: [0, 0, ["ザンビア", "Zambia", "Sambia", "Zambie", "Zambia", "Zambia", "Zambia"]],
	2: [-15.41666667, 28.28333333, ["ルサカ州", "Lusaka Province", "Provinz Lusaka", "Province de Lusaka", "Provincia de Lusaka", "Provincia di Lusaka", "Lusaka"]],
	3: [-14.437, 28.44316667, ["中央州", "Central Province", "Zentralprovinz", "Province Centrale", "Provincia Central", "Provincia Centrale", "Central"]],
	4: [-12.96866667, 28.63733333, ["コッパーベルト州", "Copperbelt Province", "Provinz Copperbelt", "Province du Copperbelt", "Provincia de Copperbelt", "Provincia di Copperbelt", "Copperbelt"]],
	5: [-13.632, 32.645, ["東部州", "Eastern Province", "Ostprovinz", "Province Orientale", "Provincia Oriental", "Provincia Orientale", "Eastern"]],
	6: [-11.2, 28.88733333, ["ルアプラ州", "Luapula Province", "Provinz Luapula", "Province de Luapula", "Provincia de Luapula", "Provincia di Luapula", "Luapula"]],
	7: [-10.199, 31.18, ["北部州", "Northern Province", "Nordprovinz", "Province Septentrionale", "Provincia del Norte", "Provincia Settentrionale", "Northern"]],
	8: [-12.17466667, 26.4, ["北西州", "North-Western Province", "Nordwestprovinz", "Province Nord-Occidentale", "Provincia del Noroeste", "Provincia Nordoccidentale", "North-Western"]],
	9: [-17.86666667, 25.85, ["南部州", "Southern Province", "Südprovinz", "Province Méridionale", "Provincia del Sur", "Provincia Meridionale", "Southern"]],
	10: [-15.277, 23.131, ["西部州", "Western Province", "Westprovinz", "Province Occidentale", "Provincia Occidental", "Provincia Occidentale", "Western"]]
}

regioninfo_112 = {
	1: [0, 0, ["ジンバブエ", "Zimbabwe", "Simbabwe", "Zimbabwe", "Zimbabue", "Zimbabwe", "Zimbabwe"]],
	2: [-17.82416667, 31.05233333, ["ハラーレ市", "Harare", "Harare", "Harare", "Harare", "Harare", "Harare"]],
	3: [-20.16983333, 28.57533333, ["ブラワヨ市", "Bulawayo", "Bulawayo", "Bulawayo", "Bulawayo", "Bulawayo", "Bulawayo"]],
	4: [-18.9715, 32.65333333, ["マニカランド州", "Manicaland", "Manicaland", "Manicaland", "Manicalandia", "Manicaland", "Manicaland"]],
	5: [-17.3055, 31.3235, ["マショナランド中央州", "Mashonaland Central", "Zentral-Mashonaland", "Mashonaland Centre", "Mashonalandia Central", "Mashonaland Centrale", "Mashonaland Central"]],
	6: [-18.18883333, 31.55233333, ["マショナランド東部州", "Mashonaland East", "Ost-Mashonaland", "Mashonaland Est", "Mashonalandia Oriental", "Mashonaland Orientale", "Mashonaland East"]],
	7: [-17.36, 30.181, ["マショナランド西部州", "Mashonaland West", "West-Mashonaland", "Mashonaland Ouest", "Mashonalandia Occidental", "Mashonaland Occidentale", "Mashonaland West"]],
	8: [-20.062, 30.823, ["マスビンゴ州", "Masvingo", "Masvingo", "Masvingo", "Masvingo", "Masvingo", "Masvingo"]],
	9: [-18.9265, 27.76666667, ["北マタベレランド州", "Matabeleland North", "Nord-Matabeleland", "Matabeleland Nord", "Matabelelandia Septentrional", "Matabeleland Settentrionale", "Matabeleland North"]],
	10: [-20.94, 29.015, ["南マタベレランド州", "Matabeleland South", "Süd-Matabeleland", "Matabeleland Sud", "Matabelelandia Meridional", "Matabeleland Meridionale", "Matabeleland South"]],
	11: [-19.45066667, 29.81716667, ["ミッドランズ州", "Midlands", "Midlands", "Midlands", "Midlands", "Midlands", "Midlands"]]
}

regioninfo_113 = {
	1: [40.379571, 49.891233, ["アゼルバイジャン", "Azerbaijan", "Aserbaidschan", "Azerbaïdjan", "Azerbaiyán", "Azerbaigian", "Azerbeidzjan", "阿塞拜疆", "阿塞拜疆", "아제르바이잔"]]
}

regioninfo_114 = {
	1: [18.1, -15.95, ["モーリタニア", "Mauritania", "Mauretanien", "Mauritanie", "Mauritania", "Mauritania", "Mauritanië", "毛里塔尼亚", "毛里塔尼亚", "모리타니"]]
}

regioninfo_115 = {
	1: [12.65, -8, ["マリ", "Mali", "Mali", "Mali", "Mali", "Mali", "Mali", "马里", "马里", "말리"]]
}

regioninfo_116 = {
	1: [13.521389, 2.105278, ["ニジェール", "Niger", "Niger", "Niger", "Níger", "Niger", "Niger", "尼日尔", "尼日尔", "니제르"]]
}

regioninfo_117 = {
	1: [12.112, 15.035, ["チャド", "Chad", "Tschad", "Tchad", "Chad", "Ciad", "Tsjaad", "乍得", "乍得", "차드"]]
}

regioninfo_118 = {
	1: [15.633056, 32.533056, ["スーダン", "Sudan", "Sudan", "Soudan", "Sudán", "Sudan", "Soedan", "苏丹", "苏丹", "수단"]]
}

regioninfo_119 = {
	1: [15.333333, 38.933333, ["エリトリア", "Eritrea", "Eritrea", "Erythrée", "Eritrea", "Eritrea", "Eritrea", "厄立特里亚", "厄立特里亚", "에리트레아"]]
}

regioninfo_120 = {
	1: [11.588, 43.145, ["ジブチ", "Djibouti", "Dschibuti", "Djibouti", "Yibuti", "Gibuti", "Djibouti", "吉布提", "吉布提", "지부티"]]
}

regioninfo_121 = {
	1: [2.033333, 45.35, ["ソマリア", "Somalia", "Somalia", "Somalie", "Somalia", "Somalia", "Somalië", "索马里", "索马里", "소말리아"]]
}

regioninfo_128 = {
	1: [0, 0, ["台湾", "Taiwan", "Taiwan", "Taiwan", "Taiwán", "Taiwan", "Taiwan"]],
	2: [25.035089, 121.506699, ["台北市", "Taipei City", "Taipeh", "Taïpei", "Taipéi", "Taipei", "Taipei"]],
	3: [22.6, 120.2833333, ["高雄市", "Kaohsiung City", "Kaohsiung", "Kaohsiung", "Condado de Kaohsiung", "Kaohsiung", "Kaohsiung"]],
	4: [25.123417, 121.735174, ["基隆市", "Keelung City", "Keelung", "Keelung", "Keelung", "Keelung", "Chilung"]],
	5: [24.730181, 120.956328, ["新竹市", "Hsinchu City", "Hsinchu", "Hsinchu", "Hsinchu", "Hsinchu", "Hsinchu"]],
	6: [24.13333333, 120.65, ["台中市", "Taichung City", "Taichung", "Taichung", "Taichung", "Taichung", "Taichung"]],
	7: [23.46666667, 120.45, ["嘉義市", "Chiayi City", "Chiayi", "Chiayi", "Chiayi", "Chiayi", "Chiayi"]],
	8: [22.99374, 120.194901, ["台南市", "Tainan City", "Tainan", "Tainan", "Tainan", "Tainan", "Tainan"]],
	9: [24.980915, 121.450832, ["台北県", "Taipei County", "Kreis Taipeh", "Taïpei (district de)", "Condado de Taipéi", "Provincia di Taipei", "Taipei"]],
	10: [24.974429, 121.292642, ["桃園県", "Taoyuan County", "Kreis Taoyuan", "Taoyuan (district de)", "Condado de Taoyuan", "Provincia di Taoyuan", "Taoyuan"]],
	11: [24.83333333, 121, ["新竹県", "HsinChu County", "Kreis Hsinchu", "HsinChu (district de)", "Condado de Hsinchu", "Provincia di HsinChu", "HsinChu"]],
	12: [24.53333333, 120.8, ["苗栗県", "Miaoli County", "Kreis Miaoli", "Miaoli (district de)", "Distrito de Miaoli", "Provincia di Miaoli", "Miaoli"]],
	13: [24.221445, 120.704985, ["台中県", "Taichung County", "Kreis Taichung", "Taichung (district de)", "Condado de Taichung", "Provincia di Taichung", "Taichung"]],
	14: [24.06666667, 120.5333333, ["彰化県", "Changhua County", "Kreis Changhua", "Changhua (district de)", "Condado de Changhua", "Provincia di Changhua", "Changhua"]],
	15: [23.9, 120.7, ["南投県", "Nantou County", "Kreis Nantou", "Nantou (district de)", "Condado de Nantou", "Provincia di Nantou", "Nantou"]],
	16: [23.688809, 120.525676, ["雲林県", "Yunlin County", "Kreis Yunlin", "Yunlin (district de)", "Condado de Yunlin", "Provincia di Yunlin", "Yunlin"]],
	17: [23.46666667, 120.45, ["嘉義県", "Chiayi County", "Kreis Chiayi", "Chiayi (district de)", "Condado de Chiayi", "Provincia di Chiayi", "Chiayi"]],
	18: [23.05, 120.3333333, ["台南県", "Tainan County", "Kreis Tainan", "Tainan (district de)", "Condado de Tainan", "Provincia di Tainan", "Tainan"]],
	19: [22.625681, 120.354103, ["高雄県", "Kaohsiung County", "Kreis Kaohsiung", "Kaohsiung (district de)", "Distrito de Kaohsiung", "Provincia di Kaohsiung", "Kaohsiung"]],
	20: [22.66666667, 120.5, ["屏東県", "Pingtung County", "Kreis Pingtung", "Pingtung (district de)", "Condado de Pingtung", "Provincia di Pingtung", "Pingtung"]],
	21: [24.766239, 121.745102, ["宜蘭県", "Yilan County", "Kreis Yilan", "Ilan (district de)", "Condado de Yilan", "Provincia di Yilan", "Yilan"]],
	22: [23.98333333, 121.6333333, ["花蓮県", "Hualien County", "Kreis Hualien", "Hualien (district de)", "Condado de Haulien", "Provincia di Hualien", "Hualien"]],
	23: [22.757549, 121.141899, ["台東県", "Taitung County", "Kreis Taitung", "Taitung (district de)", "Condado de Taitung", "Provincia di Taitung", "Taitung"]],
	24: [23.56666667, 119.5833333, ["澎湖県", "Penghu County", "Kreis Penghu", "Penghu (district de)", "Islas Pescadores", "Provincia di Penghu", "Penghu"]],
	25: [24.43333333, 118.3333333, ["金門県", "Kinmen County", "Kreis Chinmen", "Kinmen (district de)", "Condado de Kinmen", "Provincia di Kinmen", "Kinmen"]],
	26: [26.1509283, 119.9290529, ["連江県", "Lienchiang County", "Kreis Lienchiang", "Lienchiang (district de)", "Condado de Lienchiang", "Provincia di Lienchiang", "Lienchiang"]]
}

regioninfo_136 = {
	1: [0, 0, ["韓国", "South Korea", "Südkorea", "Corée du Sud", "Corea del Sur", "Corea del Sud", "Zuid-Korea", "韩国", "韩国", "대한민국"]],
	2: [37.5, 127, ["ソウル特別市", "Seoul-teukbyeolsi", "Seoul", "Séoul", "Seúl", "Seoul", "Seoul", "首尔特別市", "首尔特別市", "서울 특별시"]],
	3: [35.08333333, 129.0333333, ["プサン広域市", "Busan-gwangyeoksi", "Busan", "Pusan", "Busán", "Busan", "Busan", "釜山广域市", "釜山广域市", "부산 광역시"]],
	4: [35.85, 128.5833333, ["テグ広域市", "Daegu-gwangyeoksi", "Daegu", "Daegu", "Daegu", "Daegu", "Daegu", "大邱广域市", "大邱广域市", "대구 광역시"]],
	5: [37.5, 126.6333333, ["インチョン広域市", "Incheon-gwangyeoksi", "Incheon", "Incheon", "Inchon", "Incheon", "Incheon", "仁川广域市", "仁川广域市", "인천 광역시"]],
	6: [35.11666667, 126.8666667, ["クァンジュ広域市", "Gwangju-gwangyeoksi", "Gwangju", "Gwangju", "Gwangju", "Gwangju", "Gwangju", "光州广域市", "光州广域市", "광주 광역시"]],
	7: [36.35, 127.4333333, ["テジョン広域市", "Daejeon-gwangyeoksi", "Daejeon", "Daejeon", "Daejeon", "Daejeon", "Daejeon", "大田广域市", "大田广域市", "대전 광역시"]],
	8: [35.51666667, 129.3666667, ["ウルサン広域市", "Ulsan-gwangyeoksi", "Ulsan", "Ulsan", "Ulsan", "Ulsan", "Ulsan", "蔚山广域市", "蔚山广域市", "울산 광역시"]],
	9: [37.5, 127, ["キョンギ道", "Gyeonggi-do", "Gyeonggi-do", "Gyeonggi", "Gyeonggi", "Gyeonggi-do", "Gyeonggi-do", "京畿道", "京畿道", "경기도"]],
	10: [37.93333333, 127.7666667, ["カンウォン道", "Gangwon-do", "Gangwon-do", "Gangwon", "Gangwon", "Gangwon-do", "Gangwon-do", "江原道", "江原道", "강원도"]],
	11: [36.96666667, 127.8833333, ["チュンチョンブク道", "Chungcheongbuk-do", "Chungcheongbuk-do", "Chungcheong du Nord", "Chungcheong del Sur", "Chungcheongbuk-do", "Noord-Chungcheong", "忠清北道", "忠清北道", "충청북도"]],
	12: [36.35, 127.4333333, ["チュンチョンナム道", "Chungcheongnam-do", "Chungcheongnam-do", "Chungcheong du Sud", "Chungcheong del Norte", "Chungcheongnam-do", "Zuid-Chungcheong", "忠清南道", "忠清南道", "충청남도"]],
	13: [35.85, 127.0833333, ["チョルラブク道", "Jeollabuk-do", "Jeollabuk-do", "Jeolla du Nord", "Jeolla del Norte", "Jeollabuk-do", "Noord-Jeolla", "全罗北道", "全罗北道", "전라북도"]],
	14: [35.11666667, 126.8666667, ["チョルラナム道", "Jeollanam-do", "Jeollanam-do", "Jeolla du Sud", "Jeolla del Sur", "Jeollanam-do", "Zuid-Jeolla", "全罗南道", "全罗南道", "전라남도"]],
	15: [35.85, 128.5833333, ["キョンサンブク道", "Gyeongsangbuk-do", "Gyeongsangbuk-do", "Gyeongsang du Nord", "Gyeongsang del Norte", "Gyeongsangbuk-do", "Noord-Gyeongsang", "庆尚北道", "庆尚北道", "경상북도"]],
	16: [35.3, 128.65, ["キョンサンナム道", "Gyeongsangnam-do", "Gyeongsangnam-do", "Gyeongsang du Sud", "Gyeongsang del Sur", "Gyeongsangnam-do", "Zuid-Gyeongsang", "庆尚南道", "庆尚南道", "경상남도"]],
	17: [33.51666667, 126.5333333, ["チェジュ特別自治道", "Jeju-teukbyeoljachido", "Jeju-do", "Jeju", "Jeju", "Provincia Speciale autogovernata di Jeju", "Jeju-do", "济州道", "济州道", "제주 특별자치도"]]
}

regioninfo_144 = {
	1: [22.46666667, 114.3, ["ホンコン", "Hong Kong", "Hongkong", "Hong Kong", "Hong Kong", "Hong Kong", "Hongkong"]]
}

regioninfo_145 = {
	1: [22.21666667, 113.6, ["マカオ", "Macao", "Macau", "Macao", "Macao", "Macao", "Macau"]]
}

regioninfo_152 = {
	1: [0, 0, ["インドネシア", "Indonesia", "Indonesien", "Indonésie", "Indonesia", "Indonesia", "Indonesië"]],
	2: [-6.1744444, 106.8294444, ["ジャカルタ・ラヤ", "Jakarta Raya", "Jakarta", "Jakarta", "Jakarta Raya", "Giakarta", "Jakarta"]],
	3: [5.5616667, 95.3258333, ["アチェ特別自治区", "Aceh", "Aceh", "Aceh", "Aceh", "Aceh", "Aceh"]],
	4: [-8.65, 115.2166667, ["バリ州", "Bali", "Bali", "Bali", "Bali", "Bali", "Bali"]],
	5: [-3.8, 102.2666667, ["ベンクル州", "Bengkulu", "Bengkulu", "Bengkulu", "Bengkulu", "Bengkulu", "Bengkulu"]],
	6: [-1.6, 103.6166667, ["ジャンビ州", "Jambi", "Jambi", "Jambi", "Jambi", "Jambi", "Jambi"]],
	7: [-6.9666667, 110.4166667, ["中ジャワ州", "Central Java", "Zentraljava", "Java Centre", "Java Central", "Giava Centrale", "Centraal-Java"]],
	8: [-7.2491667, 112.7508333, ["ジャワティモール州", "East Java", "Ostjava", "Java Est", "Java Oriental", "Giava Orientale", "Oost-Java"]],
	9: [-2.5333333, 140.7, ["パプア州", "Papua", "Papua", "Papua", "Papua", "Papua", "Papoea"]],
	10: [-7.7827778, 110.3608333, ["ジョクジャカルタ特別自治区", "Yogyakarta", "Yogyakarta", "Yogyakarta", "Yogyakarta", "Yogyakarta", "Jogjakarta"]],
	11: [-0.0333333, 109.3333333, ["西カリマンタン州", "West Kalimantan", "Westkalimantan", "Kalimantan Ouest", "Kalimantan Occidental", "Kalimantan Occidentale", "West-Kalimantan"]],
	12: [-3.3333333, 114.5833333, ["南カリマンタン州", "South Kalimantan", "Südkalimantan", "Kalimantan Sud", "Kalimantan Meridional", "Kalimantan Meridionale", "Zuid-Kalimantan"]],
	13: [-2.29, 113.9224, ["中部カリマンタン州", "Kalimantan Tengah", "Zentralkalimantan", "Kalimantan Centre", "Kalimantan Central", "Kalimantan Centrale", "Centraal-Kalimantan"]],
	14: [-0.5, 117.15, ["東カリマンタン州", "Kalimantan Timur", "Ostkalimantan", "Kalimantan Est", "Kalimantan Oriental", "Kalimantan Orientale", "Oost-Kalimantan"]],
	15: [-5.45, 105.2666667, ["ランプン州", "Lampung", "Lampung", "Lampung", "Lampung", "Lampung", "Lampung"]],
	16: [-8.5833333, 116.1166667, ["西ヌサトゥンガラ州", "Nusa Tenggara Barat", "West-Nusa Tenggara", "Nusa Tenggara Ouest", "Nusa Tenggara Occidental", "Nusa Tenggara Barat", "West-Nusa Tenggara"]],
	17: [-10.1666667, 123.5833333, ["東ヌサトゥンガラ州", "East Nusa Tenggara", "Ost-Nusa Tenggara", "Nusa Tenggara Est", "Nusa Tenggara Oriental", "Nusa Tenggara Timur", "Oost-Nusa Tenggara"]],
	18: [0.5333333, 101.45, ["リアウ州", "Riau", "Riau", "Riau", "Riau", "Riau", "Riau"]],
	19: [-5.1463889, 119.4386111, ["南スラウェシ州", "Sulawesi Selatan", "Südzulawesi", "Sulawesi Sud", "Sulawesi Meridional", "Sulawesi Selatan", "Zuid-Celebes"]],
	20: [-0.9016667, 119.8597222, ["中部スラウェシ州", "Sulawesi Tengah", "Zentralcelebes", "Sulawesi Centre", "Sulawesi Central", "Sulawesi Tengah", "Centraal-Celebes"]],
	21: [-3.866666667, 121.8166667, ["東南スラウェシ州", "Sulawesi Tenggara", "Südostcelebes", "Sulawesi Sud-Est", "Sulawesi Suroriental", "Sulawesi Tenggara", "Zuidoost-Celebes"]],
	22: [-0.95, 100.35, ["西スマトラ州", "West Sumatra", "Westsumatra", "Sumatera Ouest", "Sumatra Occidental", "Sumatera Barat", "West-Celebes"]],
	23: [3.5833333, 98.6666667, ["北スマトラ州", "North Sumatra", "Nordsumatra", "Sumatera Nord", "Sumatra Norte", "Sumatera Utara", "Noord-Celebes"]],
	24: [-3.2, 129.4333333, ["マルク州", "Maluku", "Maluku", "Moluques", "Molucas", "Maluku", "Molukken"]],
	25: [-3.7166667, 128.2, ["北マルク州", "Maluku Utara", "Maluku Utara", "Moluques du Nord", "Molucas del Norte", "Maluku Utara", "Noord-Molukken"]],
	26: [-6.9127778, 107.6205556, ["西ジャワ州", "Jawa Barat", "Westjava", "Java Ouest", "Java Occidental", "Jawa Barat", "West-Java"]],
	27: [1.5016667, 124.8441667, ["北スラウェシ州", "Sulawesi Utara", "Nordcelebes", "Sulawesi Nord", "Sulawesi del Norte", "Sulawesi Utara", "Noord-Celebes"]],
	28: [-3.3, 102.8666667, ["南スマトラ州", "Sumatera Selatan", "Südsumatra", "Sumatera Sud", "Sumatra del Sur", "Sumatera Selatan", "Zuid-Sumatra"]],
	29: [-6.0166667, 105.95, ["バンテン州", "Banten", "Banten", "Banten", "Banten", "Banten", "Bantam"]],
	30: [0.55, 123.05, ["ゴロンタロ", "Gorontalo", "Gorontalo", "Gorontalo", "Gorontalo", "Gorontalo", "Gorontalo"]],
	31: [-2.25, 105.9833333, ["バンカ・ブリトゥン州", "Kepulauan Bangka Belitung", "Bangka-Belitung", "Bangka Belitung", "Bangka-Belitung", "Kepulauan Bangka Belitung", "Bangka Belitung"]],
	32: [-2.091421148, 133.1413494, ["西イリアン・ジャヤ州", "Irian Jaya Barat", "West-Irian Jaya", "Irian Jaya Occidental", "Irian Jaya Occidental", "Irian Jaya Barat", "Irian Jaya Barat"]],
	33: [0.533333333, 103.75, ["リアウ諸島州", "Kepulauan Riau", "Riau-Inseln", "Archipel de Riau", "Archipiélago de Riau", "Kepulauan Riau", "Riouwarchipel"]],
	34: [-2.516666667, 119.4, ["西スラウェシ州", "Sulawesi Barat", "Westcelebes", "Sulawesi Ouest", "Sulawesi Occidental", "Sulawesi Barat", "West-Celebes"]]
}

regioninfo_153 = {
	1: [1.2930556, 103.8558333, ["シンガポール", "Singapore", "Singapur", "Singapour", "Singapur", "Singapore", "Singapore"]]
}

regioninfo_154 = {
	1: [0, 0, ["タイ", "Thailand", "Thailand", "Thaïlande", "Tailandia", "Thailandia", "Thailand"]],
	2: [13.75, 100.5166667, ["バンコク", "Krung Thep Mahanakhon", "Bangkok", "Bangkok", "Bangkok", "Bangkok", "Bangkok"]],
	3: [18.73333333, 98.01666667, ["メーホンソン県", "Mae Hong Son", "Mae Hong Son", "Mae Hong Son", "Mae Hong Son", "Mae Hong Son", "Mae Hong Son"]],
	4: [18.7902778, 98.9816667, ["チェンマイ県", "Chiang Mai", "Chiang Mai", "Chiang Mai", "Chiang Mai", "Chiang Mai", "Chiang Mai"]],
	5: [19.81666667, 99.86666667, ["チェンライ県", "Chiang Rai", "Chiang Rai", "Chiang Rai", "Chiang Rai", "Chiang Rai", "Chiang Rai"]],
	6: [18.83333333, 100.85, ["ナン県", "Nan", "Nan", "Nan", "Nan", "Nan", "Nan"]],
	7: [18.1, 98.95, ["ランプーン県", "Lamphun", "Lamphun", "Lamphun", "Lamphun", "Lamphun", "Lamphun"]],
	8: [18.2983333, 99.5072222, ["ランパン県", "Lampang", "Lampang", "Lampang", "Lampang", "Lampang", "Lampang"]],
	9: [18.18813997, 100.1050735, ["プラエ県", "Phrae", "Phrae", "Phrae", "Phrae", "Phrae", "Phrae"]],
	10: [16.73462761, 98.80241166, ["ターク県", "Tak", "Tak", "Tak", "Tak", "Tak", "Tak"]],
	11: [17.23442591, 99.71826912, ["スコータイ県", "Sukhothai", "Sukhothai", "Sukhothai", "Sukhothai", "Sukhothai", "Sukhothai"]],
	12: [17.73333333, 100.5166667, ["ウタラディット県", "Uttaradit", "Uttaradit", "Uttaradit", "Uttaradit", "Uttaradit", "Uttaradit"]],
	13: [16.31666667, 99.5, ["カムペーンペット県", "Kamphaeng Phet", "Kamphaeng Phet", "Kamphaeng Phet", "Kamphaeng Phet", "Kamphaeng Phet", "Kamphaeng Phet"]],
	14: [16.8333333, 100.25, ["ピッサヌローク県", "Phitsanulok", "Phitsanulok", "Phitsanulok", "Phitsanulok", "Phitsanulok", "Phitsanulok"]],
	15: [16.21666667, 100.35, ["ピチト県", "Phichit", "Phichit", "Phichit", "Phichit", "Phichit", "Phichit"]],
	16: [16.75, 101.1333333, ["ペチャブーン県", "Phetchabun", "Phetchabun", "Phetchabun", "Phetchabun", "Phetchabun", "Phetchabun"]],
	17: [15.31666667, 99.45, ["ウタイ・タニー県", "Uthai Thani", "Uthai Thani", "Uthai Thani", "Uthai Thani", "Uthai Thani", "Uthai Thani"]],
	18: [15.66666667, 100.1166667, ["ナコーン・サワン県", "Nakhon Sawan", "Nakhon Sawan", "Nakhon Sawan", "Nakhon Sawan", "Nakhon Sawan", "Nakhon Sawan"]],
	19: [17.16666667, 102.3166667, ["ノン・カイ県", "Nong Khai", "Nong Khai", "Nong Khai", "Nong Khai", "Nong Khai", "Nong Khai"]],
	20: [17.38333333, 101.6166667, ["ルーイ県", "Loei", "Loei", "Loei", "Loei", "Loei", "Loei"]],
	21: [17.36666667, 103.8, ["サコン・ナコーン県", "Sakon Nakhon", "Sakon Nakhon", "Sakon Nakhon", "Sakon Nakhon", "Sakon Nakhon", "Sakhon Nakhon"]],
	22: [16.4333333, 102.8333333, ["コン・ケン県", "Khon Kaen", "Khon Kaen", "Khon Kaen", "Khon Kaen", "Khon Kaen", "Khon Kaen"]],
	23: [16.6, 103.6166667, ["カーラシン県", "Kalasin", "Kalasin", "Kalasin", "Kalasin", "Kalasin", "Kalasin"]],
	24: [15.96666667, 103.1666667, ["マハー・サラカム県", "Maha Sarakham", "Maha Sarakham", "Maha Sarakham", "Maha Sarakham", "Maha Sarakham", "Maha Sarakham"]],
	25: [15.9, 103.8166667, ["ロイ・エト県", "Roi Et", "Roi Et", "Roi Et", "Roi Et", "Roi Et", "Roi Et"]],
	26: [16, 101.7666667, ["チャイヤプーン県", "Chaiyaphum", "Chaiyaphum", "Chaiyaphum", "Chaiyaphum", "Chaiyaphum", "Chaiyaphum"]],
	27: [14.9666667, 102.1166667, ["ナコーン・ラッチャシマ県", "Nakhon Ratchasima", "Nakhon Ratchasima", "Nakhon Ratchasima", "Nakhon Ratchasima", "Nakhon Ratchasima", "Nakhon Ratchasima"]],
	28: [14.8, 102.95, ["ブーリラム県", "Buriram", "Buri Ram", "Buri Ram", "Buriram", "Buriram", "Buriram"]],
	29: [14.86666667, 103.6666667, ["スリン県", "Surin", "Surin", "Surin", "Surin", "Surin", "Surin"]],
	30: [14.83333333, 104.3833333, ["シーサケート県", "Sisaket", "Si Sa Ket", "Si Sa Ket", "Sisaket", "Sisaket", "Sisaket"]],
	31: [6.15, 101.7, ["ナラーティワート県", "Narathiwat", "Narathiwat", "Narathiwat", "Narathiwat", "Narathiwat", "Narathiwat"]],
	32: [15.11666667, 100.0166667, ["チャイナート県", "Chai Nat", "Chainat", "Chai Nat", "Chai Nat", "Chai Nat", "Chainat"]],
	33: [14.9, 100.35, ["シンブリー県", "Sing Buri", "Singburi", "Sing Buri", "Sing Buri", "Sing Buri", "Singburi"]],
	34: [15.05, 100.9, ["ロプブリー県", "Lop Buri", "Lopburi", "Lop Buri", "Lop Buri", "Lop Buri", "Lopburi"]],
	35: [14.6, 100.3333333, ["アーン・トーン県", "Ang Thong", "Ang Thong", "Ang Thong", "Ang Thong", "Ang Thong", "Ang Thong"]],
	36: [14.33333333, 100.5166667, ["アユタヤ県", "Phra Nakhon Si Ayutthaya", "Ayutthaya", "Ayutthaya", "Ayutthaya", "Phra Nakhon Si Ayutthaya", "Ayutthaya"]],
	37: [14.55, 100.9333333, ["サラ・ブリ県", "Sara Buri", "Saraburi", "Saraburi", "Sara Buri", "Sara Buri", "Saraburi"]],
	38: [13.9166667, 100.5, ["ノンタブリー県", "Nonthaburi", "Nonthaburi", "Nonthaburi", "Nonthaburi", "Nonthaburi", "Nonthaburi"]],
	39: [14.05, 100.6666667, ["パトゥムターニー県", "Pathum Thani", "Pathum Thani", "Pathum Thani", "Pathum Thani", "Pathum Thani", "Pathum Thani"]],
	40: [19.2, 100.2, ["パヤオ県", "Phayao", "Phayao", "Phayao", "Phayao", "Phayao", "Phayao"]],
	41: [13.6666667, 100.5333333, ["サムット・プラカン県", "Samut Prakan", "Samut Prakan", "Samut Prakan", "Samut Prakan", "Samut Prakan", "Samut Prakan"]],
	42: [14.18333333, 101.1666667, ["ナコーン・ナヨク県", "Nakhon Nayok", "Nakhon Nayok", "Nakhon Nayok", "Nakhon Nayok", "Nakhon Nayok", "Nakhon Nayok"]],
	43: [13.58333333, 101.4166667, ["チャチューンソー県", "Chachoengsao", "Chachoengsao", "Chachoengsao", "Chachoengsao", "Chachoengsao", "Chachoengsao"]],
	44: [13.1666667, 100.9333333, ["チョン・ブリー県", "Chon Buri", "Chonburi", "Chon Buri", "Chon Buri", "Chon Buri", "Chonburi"]],
	45: [12.83333333, 101.4166667, ["ラヨン県", "Rayong", "Rayong", "Rayong", "Rayong", "Rayong", "Rayong"]],
	46: [12.83333333, 102.1166667, ["チャンタブリー県", "Chanthaburi", "Chanthaburi", "Chanthaburi", "Chanthaburi", "Chanthaburi", "Chantaburi"]],
	47: [12.35, 102.5333333, ["トラート県", "Trat", "Trat", "Trat", "Trat", "Trat", "Trat"]],
	48: [14.56666667, 99.03333333, ["カンチャナブリ県", "Kanchanaburi", "Kanchanaburi", "Kanchanaburi", "Kanchanaburi", "Kanchanaburi", "Kanchanaburi"]],
	49: [14.58333333, 99.9, ["スパン・ブリー県", "Suphan Buri", "Suphanburi", "Suphan Buri", "Suphan Buri", "Suphan Buri", "Suphanburi"]],
	50: [13.539, 99.82, ["ラトブリー県", "Ratchaburi", "Ratchaburi", "Ratchaburi", "Ratchaburi", "Ratchaburi", "Ratchaburi"]],
	51: [13.8166667, 100.05, ["ナコーン・パトム県", "Nakhon Pathom", "Nakhon Pathom", "Nakhon Pathom", "Nakhon Pathom", "Nakhon Pathom", "Nakhon Pathom"]],
	52: [13.413, 100, ["サムット・ソンクラム県", "Samut Songkhram", "Samut Songkhram", "Samut Songkhram", "Samut Songkhram", "Samut Songkhram", "Samut Songkhram"]],
	53: [13.55, 100.1833333, ["サムット・サコン県", "Samut Sakhon", "Samut Sakhon", "Samut Sakhon", "Samut Sakhon", "Samut Sakhon", "Samut Sakhon"]],
	54: [13.101, 99.947, ["ペトーブリ県", "Phetchaburi", "Phetchaburi", "Phetchaburi", "Phetchaburi", "Phetchaburi", "Phetchaburi"]],
	55: [11.8166667, 99.8, ["プラチュー・アプ・キリ・カン県", "Prachuap Khiri Khan", "Prachuap Khiri Khan", "Prachuap Khiri Khan", "Prachuap Khiri Khan", "Prachuap Khiri Khan", "Prachuap Khiri Khan"]],
	56: [10.492, 99.176, ["チュンポン県", "Chumphon", "Chumphon", "Chumphon", "Chumphon", "Chumphon", "Chumphon"]],
	57: [9.961, 98.638, ["ラノン県", "Ranong", "Ranong", "Ranong", "Ranong", "Ranong", "Ranong"]],
	58: [9.1333333, 99.3166667, ["スラト・タニー県", "Surat Thani", "Surat Thani", "Surat Thani", "Surat Thani", "Surat Thani", "Surat Thani"]],
	59: [8.451, 98.533, ["パンガ県", "Phangnga", "Phangnga", "Phangnga", "Phangnga", "Phangnga", "Phang Nga"]],
	60: [7.8833333, 98.4, ["プーケット県", "Phuket", "Phuket", "Phuket", "Phuket", "Phuket", "Phuket"]],
	61: [8.133333333, 99, ["クラビ県", "Krabi", "Krabi", "Krabi", "Krabi", "Krabi", "Krabi"]],
	62: [8.4333333, 99.9666667, ["ナコーン・シ・タマラート県", "Nakhon Si Thammarat", "Nakhon Si Thammarat", "Nakhon Si Thammarat", "Nakhon Si Thammarat", "Nakhon Si Thammarat", "Nakhon Si Thammarat"]],
	63: [7.5, 99.6, ["トラン県", "Trang", "Trang", "Trang", "Trang", "Trang", "Trang"]],
	64: [7.614, 100.08, ["パッタルン県", "Phatthalung", "Phattalung", "Phatthalung", "Phatthalung", "Phatthalung", "Phattalung"]],
	65: [6.604, 100.064, ["サトゥン県", "Satun", "Satun", "Satun", "Satun", "Satun", "Satun"]],
	66: [7.0166667, 100.4666667, ["ソンクラ県", "Songkhla", "Songkhla", "Songkhla", "Songkhla", "Songkhla", "Songkhla"]],
	67: [6.864, 101.249, ["パタニ県", "Pattani", "Pattani", "Pattani", "Pattani", "Pattani", "Pattani"]],
	68: [6.55, 101.288, ["ヤラ県", "Yala", "Yala", "Yala", "Yala", "Yala", "Yala"]],
	69: [15.86666667, 104.3, ["ヤソートーン県", "Yasothon", "Yasothon", "Yasothon", "Yasothon", "Yasothon", "Yasothon"]],
	70: [17.36666667, 104.4166667, ["ナコーン・パノム県", "Nakhon Phanom", "Nakhon Phanom", "Nakhon Phanom", "Nakhon Phanom", "Nakhon Phanom", "Nakhon Phanom"]],
	71: [14.0502778, 101.3702778, ["プラチン・ブリー県", "Prachin Buri", "Prachinburi", "Prachin Buri", "Prachin Buri", "Prachin Buri", "Prachinburi"]],
	72: [15.2330556, 104.8630556, ["ウボン・ラーチャターニー県", "Ubon Ratchathani", "Ubon Ratchathani", "Ubon Ratchathani", "Ubon Ratchathani", "Ubon Ratchathani", "Ubon Ratchathani"]],
	73: [17.4075, 102.7930556, ["ウドン・タニー県", "Udon Thani", "Udon Thani", "Udon Thani", "Udon Thani", "Udon Thani", "Udon Thani"]],
	74: [15.85, 104.7666667, ["アムナート・チャルーン県", "Amnat Charoen", "Amnat Charoen", "Amnat Charoen", "Amnat Charoen", "Amnat Charoen", "Amnat Charoen"]],
	75: [16.51666667, 104.6666667, ["ムクダハン県", "Mukdahan", "Mukdahan", "Mukdahan", "Mukdahan", "Mukdahan", "Mukdahan"]],
	76: [18.22522028, 103.4681794, ["ノーンブワラムプー県", "Nong Bua Lamphu", "Nong Bua Lamphu", "Nong Bua Lamphu", "Nong Bua Lamphu", "Nong Bua Lamphu", "Nongbua Lamphu"]],
	77: [13.812, 102.07, ["サケーオ県", "Sa Kaeo", "Sa Kaeo", "Sa Kaeo", "Sa Kaeo", "Sa Kaeo", "Sa Kaew"]]
}

regioninfo_155 = {
	1: [0, 0, ["フィリピン", "Philippines", "Philippinen", "Philippines", "Filipinas", "Filippine", "Filipijnen"]],
	2: [14.6041667, 120.9822222, ["マニラ", "Manila", "Metro Manila", "Manille", "Manila", "Manila", "Metro Manilla"]],
	3: [7.233333333, 124.25, ["イスラム教徒ミンダナオ自治地域", "Autonomous Region in Muslim Mindanao", "Autonome Bezirk Muslim Mindanao", "Région autonome musulmane de Mindanao", "La Región Autónoma para el Mindanao Musulmán", "Regione Autonoma del Mindanao Mussulmano", "Autonomous Region in Muslim Mindanao"]],
	4: [13.13333333, 123.7333333, ["ビコル", "Bicol", "Bicol Region", "Bicol", "Región de Bícol", "Bicol", "Bicol Region"]],
	5: [17.61666667, 121.7333333, ["カガヤン", "Cagayan", "Cagayan Valley", "Vallée de Cagayan", "Valle del Cagayán", "Valle del Cagayan", "Cagayan Valley"]],
	6: [14.21666667, 121.1666667, ["Calabarzon", "Calabarzon", "Calabarzon", "Calabarzón", "Calabarzón", "Calabarzon", "Calarbarzon"]],
	7: [8.95, 125.55, ["カラガ", "Caraga", "Caraga", "Caraga", "Caraga", "Caraga", "Caraga"]],
	8: [16.61666667, 120.3, ["中部ルソン", "Central Luzon", "Central Luzon", "Luçon central", "Luzón Central", "Luzon Centrale", "Central Luzon"]],
	9: [10.311111, 123.891667, ["中部ヴィサヤ", "Central Visayas", "Central Visayas", "Visayas centrales", "Visayas Central", "Visayas Centrale", "Central Visayas"]],
	10: [16.4166667, 120.6, ["コルディエラ", "Cordillera", "Regierungsbezirk Cordillera", "Région Administrative de la Cordillera", "Región Administrativa de Cordillera", "Cordillera", "Cordillera Administrative Region"]],
	11: [7.073056, 125.612778, ["ダバオ", "Davao", "Autonomer Bezirk Muslim Mindanao", "Région de Davao", "Región de Davao", "Davao", "Davao Region"]],
	12: [11.25, 125, ["東ヴィサヤ", "Eastern Visayas", "Eastern Visayas", "Visayas orientales", "Visayas Orientales", "Eastern Visayas", "Eastern Visayas"]],
	13: [15.03333333, 120.6833333, ["イロコス", "Ilocos", "Ilocos", "Région d'Ilocos", "Región de Ilocos", "Ilocos", "Ilocos Region"]],
	14: [13.41666667, 121.1833333, ["Mimaro", "Mimaro", "Mimaro", "Mimaropa", "Mimaropa", "Mimaro", "Mimaro"]],
	15: [7.633333333, 125.2333333, ["ミンダナオ", "Mindanao", "Mindanao", "Mindanao", "Mindanao", "Mindanao", "Mindanao"]],
	16: [8.483333333, 124.65, ["北ミンダナオ", "Northern Mindanao", "Northern Mindanao", "Mindanao du Nord", "Mindanao del Norte", "Mindanao Settentrionale", "Northern Mindanao"]],
	17: [6.233333333, 125.1, ["ソクサージェン", "Soccsksargen", "Soccsksargen", "Soccsksargen", "Soccsksargen", "Soccsksargen", "Soccsksargen"]],
	18: [10.71666667, 122.55, ["西ヴィサヤ", "Western Visayas", "Western Visayas", "Visayas occidentales", "Visayas Occidental", "Visayas Occidentale", "Western Visayas"]],
	19: [7.833333333, 123.45, ["サンボアンガ半島", "Zamboanga Peninsula", "Zamboanga Peninsula", "Péninsule de Zamboanga", "Península de Zamboanga", "Penisola di Zamboanga", "Zamboanga Peninsula"]]
}

regioninfo_156 = {
	1: [0, 0, ["マレーシア", "Malaysia", "Malaysia", "Malaisie", "Malasia", "Malaysia", "Maleisië"]],
	2: [3.1666667, 101.7, ["クアラ・ルンプール", "Kuala Lumpur", "Kuala Lumpur", "Kuala Lumpur", "Kuala Lumpur", "Kuala Lumpur", "Kuala Lumpur"]],
	3: [1.4666667, 103.75, ["ジョホール州", "Johor", "Johor", "Johor", "Johor", "Johor", "Johor"]],
	4: [6.1166667, 100.3666667, ["ケダ州", "Kedah", "Kedah", "Kedah", "Kedah", "Kedah", "Kedah"]],
	5: [6.1333333, 102.25, ["ケランタン州", "Kelantan", "Kelantan", "Kelantan", "Kelantan", "Kelantan", "Kelantan"]],
	6: [2.1969444, 102.2480556, ["マラッカ州", "Melaka", "Malakka", "Malacca", "Melaka", "Malacca", "Malakka"]],
	7: [2.7166667, 101.9333333, ["ヌグリ・センビラン州", "Negeri Sembilan", "Negeri Sembilan", "Negeri Sembilan", "Negeri Sembilan", "Negeri Sembilan", "Negeri Sembilan"]],
	8: [3.8, 103.3333333, ["パハン州", "Pahang", "Pahang", "Pahang", "Pahang", "Pahang", "Pahang"]],
	9: [4.5833333, 101.0833333, ["ペラ州", "Perak", "Perak", "Perak", "Perak", "Perak", "Perak"]],
	10: [6.4333333, 100.2, ["ペルリス州", "Perlis", "Perlis", "Perlis", "Perlis", "Perlis", "Perlis"]],
	11: [5.4166667, 100.3333333, ["ピナン州", "Penang", "Penang", "Penang", "Penang", "Penang", "Penang"]],
	12: [1.55, 110.3333333, ["サラワク州", "Sarawak", "Sarawak", "Sarawak", "Sarawak", "Sarawak", "Sarawak"]],
	13: [3.0833333, 101.5333333, ["セランゴール州", "Selangor", "Selangor", "Selangor", "Selangor", "Selangor", "Selangor"]],
	14: [5.3333333, 103.1333333, ["トレンガヌ州", "Terengganu", "Terengganu", "Terengganu", "Terengganu", "Terengganu", "Terengganu"]],
	15: [5.2766667, 115.2416667, ["ラブアン", "Labuan", "Labuan", "Labuan", "Labuan", "Labuan", "Labuan"]],
	16: [5.9833333, 116.0666667, ["サバ州", "Sabah", "Sabah", "Sabah", "Sabah", "Sabah", "Sabah"]],
	17: [2.91667, 101.667, ["プトラジャヤ", "Putrajaya", "Putrajaya", "Putrajaya", "Putrajaya", "Putrajaya", "Putrajaya"]]
}

regioninfo_160 = {
	1: [0, 0, ["中国", "China", "China", "Chine", "China", "Cina", "China", "中国", "中国", "중국"]],
	2: [39.91666667, 116.4333333, ["北京市", "Beijing", "Peking", "Pékin", "Pekín", "Pechino", "Beijing", "北京市", "北京市", "베이징"]],
	3: [29.6, 106.3666667, ["重慶市", "Chongqing", "Chongqing", "Chongqing", "Chongqing", "Chongqing", "Tsjoengking", "重庆市", "重庆市", "충칭"]],
	4: [31.247869, 121.472702, ["上海市", "Shanghai", "Shanghai", "Shanghai", "Shanghái", "Shanghai", "Sjanghai", "上海市", "上海市", "상하이"]],
	5: [39.15, 117.1833333, ["天津市", "Tianjin", "Tianjin", "Tianjin", "Tianjin", "Tianjin", "Tianjin", "天津市", "天津市", "톈진"]],
	6: [31.93333333, 117.3166667, ["安徽省", "Anhui", "Anhui", "Anhui", "Anhui", "Anhui", "Anhui", "安徽省", "安徽省", "안후이 성"]],
	7: [26.08333333, 119.3, ["福建省", "Fujian", "Fujian", "Fujian", "Fujian", "Fujian", "Fujian", "福建省", "福建省", "푸젠 성"]],
	8: [36.03333333, 103.75, ["甘粛省", "Gansu", "Gansu", "Gansu", "Gansu", "Gansu", "Gansu", "甘肃省", "甘肃省", "간쑤 성"]],
	9: [23.1, 113.1, ["広東省", "Guangdong", "Guangdong", "Guangdong", "Cantón", "Guangdong", "Kanton", "广东省", "广东省", "광둥 성"]],
	10: [26.56666667, 106.6833333, ["貴州省", "Guizhou", "Guizhou", "Guizhou", "Guizhou", "Guizhou", "Guizhou", "贵州省", "贵州省", "구이저우 성"]],
	11: [20.08333333, 110.3333333, ["海南省", "Hainan", "Hainan", "Hainan", "Hainan", "Hainan", "Hainan", "海南省", "海南省", "하이난 성"]],
	12: [38.05, 114.4666667, ["河北省", "Hebei", "Hebei", "Hebei", "Hebei", "Hebei", "Hebei", "河北省", "河北省", "허베이 성"]],
	13: [45.76666667, 126.7, ["黒龍江", "Heilongjiang", "Heilongjiang", "Heilongjiang", "Heilongjiang", "Heilongjang", "Heilongjiang", "黑龙江省", "黑龙江省", "헤이룽장 성"]],
	14: [34.6, 113.6333333, ["河南省", "Henan", "Henan", "Henan", "Henan", "Henan", "Henan", "河南省", "河南省", "허난 성"]],
	15: [30.58333333, 114.3166667, ["湖北省", "Hubei", "Hubei", "Hubei", "Hubei", "Hubei", "Hubei", "湖北省", "湖北省", "후베이 성"]],
	16: [28.18333333, 112.9833333, ["湖南省", "Húnán", "Hunan", "Hunan", "Hunan", "Hunan", "Hunan", "湖南省", "湖南省", "후난 성"]],
	17: [32.03333333, 118.8333333, ["江蘇省", "Jiangsu", "Jiangsu", "Jiangsu", "Jiangsu", "Jiangsu", "Jiangsu", "江苏省", "江苏省", "장쑤 성"]],
	18: [28.63333333, 115.9333333, ["江西省", "Jiangxi", "Jiangxi", "Jiangxi", "Jiangxi", "Jiangxi", "Jiangxi", "江西省", "江西省", "장시 성"]],
	19: [43.9, 125.2833333, ["吉林省", "Jilin", "Jilin", "Jilin", "Jilin", "Jilin", "Jilin", "吉林省", "吉林省", "지린 성"]],
	20: [41.802158, 123.383102, ["遼寧省", "Liaoning", "Liaoning", "Liaoning", "Liaoning", "Liaoning", "Liaoning", "辽宁省", "辽宁省", "랴오닝 성"]],
	21: [36.6, 101.9166667, ["青海省", "Qinghai", "Qinghai", "Qinghai", "Qinghai", "Qinghai", "Qinghai", "青海省", "青海省", "칭하이 성"]],
	22: [34.26666667, 108.9, ["陝西省", "Shanxi", "Shaanxi", "Shaanxi", "Shaanxi", "Shaanxi", "Shanxi", "陕西省", "陕西省", "산시 성"]],
	23: [36.71666667, 117.0166667, ["山東省", "Shandong", "Shandong", "Shandong", "Shandong", "Shandong", "Shandong", "山东省", "山东省", "상둥 성"]],
	24: [37.83333333, 112.5, ["山西省", "Shanxi", "Shanxi", "Shanxi", "Shanxi", "shanxi", "Shanxi", "山西省", "山西省", "산시 성"]],
	25: [30.63333333, 104.1166667, ["四川省", "Sichuan", "Sichuan", "Sichuan", "Sichuan", "Sichuan", "Sichuan", "四川省", "四川省", "쓰촨 성"]],
	26: [25.06666667, 102.6833333, ["雲南省", "Yunnan", "Yunnan", "Yunnan", "Yunnan", "Yunnan", "Yunnan", "云南省", "云南省", "윈난 성"]],
	27: [30.3, 120.1166667, ["浙江省", "Zhejiang", "Zhejiang", "Zhejiang", "Zhejiang", "Zhejiang", "Zhejiang", "浙江省", "浙江省", "저장 성"]],
	29: [22.83333333, 108.3166667, ["広西チワン族自治区", "Guangxi-Zhuangzu", "Guangxi", "Guangxi", "Guangxi", "Guangxi", "Guangxi", "广西壮族自治区", "广西壮族自治区", "광시 광족 자치구"]],
	30: [40.81666667, 111.6166667, ["内モンゴル自治区", "Nei-Menggu", "Innere Mongolei", "Mongolie Intérieure", "Mongolia Interior", "Mongolia interna", "Binnen-Mongolië", "内蒙古自治区", "内蒙古自治区", "네이멍구 자치구"]],
	31: [38.5, 106.3166667, ["寧夏回族自治区", "Ningxia-huizu", "Ningxia", "Ningxia", "Ningxia", "Ningxia", "Ningxia", "宁夏回族自治区", "宁夏回族自治区", "닝샤 후이족 자치구"]],
	32: [43.782669, 87.586517, ["新疆ウイグル自治区", "Xinjiang-Weiwu'er-zu", "Xinjiang", "Xinjiang", "Xinjiang", "Xinjiang", "Xinjiang", "新疆维吾尔自治区", "新疆维吾尔自治区", "신장 웨이우얼 자치구"]],
	33: [29.66666667, 91.16666667, ["チベット自治区", "Xizang", "Tibet", "Tibet", "Tíbet", "Tibet", "Tibet", "西藏自治区", "西藏自治区", "티베트 자치구"]]
}

regioninfo_168 = {
	1: [0, 0, ["アラブ首長国連邦", "U.A.E", "Vereinigte Arabische Emirate", "Emirats arabes unis", "Emiratos Árabes Unidos", "Emirati Arabi Uniti", "Verenigde Arabische Emiraten"]],
	2: [24.4666667, 54.3666667, ["アブダビ", "Abu Dhabi", "Abu Dhabi", "Abu Dhabi", "Abu Dabi", "Abu Dhabi", "Abu Dhabi"]],
	3: [25.406111, 55.442778, ["アジュマン", "‘Ajman", "Adschman", "‘Ajman", "Ajman", "Ajman", "Ajman"]],
	4: [25, 55.75, ["シャルジャ", "Ash Shariqah", "Schardscha", "Ash Shariqah", "Sharjah", "Sharjah", "Sharjah"]],
	5: [25.6666667, 56, ["ラアス・アル・カイマー", "Ras al-Khaimah", "Ras al-Khaimah", "Ras al-Khaïmah", "Ras Al-Khaimah", "Ras al-Khaymah", "R'as al Khaymah"]],
	6: [25.252222, 55.28, ["ドゥバイ", "Dubai", "Dubai", "Dubaï", "Dubái", "Dubai", "Dubai"]],
	7: [25.123056, 56.3375, ["フジャイラー", "Al Fujayrah", "Fudschaira", "Fujaïrah", "Fujairah", "Fujairah", "Al Fujayrah"]],
	8: [25.5, 55.75, ["ウム・アル・カイワイン", "Umm al Qaywayn", "Umm Al-Qaiwain", "Umm al-Qaiwain", "Umm al-Qaiwain", "Umm al-Quwain", "Umm al Qaywayn"]]
}

regioninfo_169 = {
	1: [0, 0, ["インド", "India", "Indien", "Inde", "India", "India", "India", "印度", "印度", "인도 "]],
	2: [28.6, 77.2, ["デリー", "Delhi", "Delhi", "Delhi", "Delhi", "Delhi", "Delhi", "德里中央直辖区", "德里中央直辖区", "델리 수도권"]],
	3: [11.6666667, 92.75, ["アンダマン・ニコバル諸島", "Andaman and Nicobar Islands", "Andamanen und Nikobaren", "Andaman et Nicobar", "Islas Andamán y Nicobar", "Andamane e Nicobare", "Andamanen en Nicobaren", "安达曼和尼科巴群岛中央直辖区", "安达曼和尼科巴群岛中央直辖区", "안다만 니코바르 제도"]],
	4: [17.375278, 78.474444, ["アーンドラ・プラデーシュ州", "Andhra Pradesh", "Andhra Pradesh", "Andhra Pradesh", "Andhra Pradesh", "Andhra Pradesh", "Andhra Pradesh", "安得拉邦", "安得拉邦", "안드라프라데시 주"]],
	5: [26.11, 91.83, ["アッサム州", "Assam", "Assam", "Assam", "Assam", "Assam", "Assam", "阿萨姆邦", "阿萨姆邦", "아삼 주"]],
	6: [30.7372222, 76.7872222, ["チャンディーガル州", "Chandigarh", "Chandigarh", "Chandigarh", "Chandigarh", "Chandigarh", "Chandigarh", "昌迪加尔中央直辖区", "昌迪加尔中央直辖区", "찬디가르"]],
	7: [20.2666667, 73.0166667, ["ダドラ及びナガル・アベリ連邦直轄地", "Dadra and Nagar Haveli", "Dadra und Nagar Haveli", "Dadra et Nagar Haveli", "Dadra y Nagar Haveli", "Dadra e Nagar Haveli", "Dadra en Nagar Haveli", "达德拉和纳加尔哈维利中央直辖区", "达德拉和纳加尔哈维利中央直辖区", "다드라 나게르 하벨리"]],
	8: [23.0333333, 72.6166667, ["グジャラート州", "Gujarat", "Gujarat", "Gujarat", "Gujarat", "Gujarat", "Gujarat ", "古吉拉特邦", "古吉拉特邦", "구자라트 주"]],
	9: [30.73333333, 76.78333333, ["ハリヤーナー州", "Haryana", "Haryana", "Haryana", "Haryana", "Haryana", "Haryana", "哈里亚纳邦", "哈里亚纳邦", "하리아나 주"]],
	10: [31.1, 77.1666667, ["ヒマーチャル・プラデーシュ州", "Himachal Pradesh", "Himachal Pradesh", "Himachal Pradesh", "Himachal Pradesh", "Himachal Pradesh", "Himachal Pradesh", "喜马偕尔邦", "喜马偕尔邦", "히마찰프라데시 주"]],
	12: [8.4833333, 76.9166667, ["ケーララ州", "Kerala", "Kerala", "Kerala", "Kerala", "Kerala", "Kerala", "喀拉拉邦", "喀拉拉邦", "케랄라 주"]],
	13: [10.5666667, 72.6166667, ["ラクシャドウィープ", "Lakshadweep", "Lakshadweep", "Lakshadweep", "Laquedivas", "Laccadive", "Laccadiven", "拉克沙群岛中央直辖区", "拉克沙群岛中央直辖区", "라크샤드위프"]],
	14: [18.975, 72.8258333, ["マハーラーシュトラ州", "Maharashtra", "Maharashtra", "Maharashtra", "Maharastra", "Maharashtra", "Maharashtra", "马哈拉施特拉邦", "马哈拉施特拉邦", "마하라슈트라 주"]],
	15: [24.8166667, 93.95, ["マニプル州", "Manipur", "Manipur", "Manipur", "Manipur", "Manipur", "Manipur", "曼尼普尔邦", "曼尼普尔邦", "마니푸르 주"]],
	16: [25.5666667, 91.8833333, ["メガラヤ州", "Meghalaya", "Meghalaya", "Meghalaya", "Megalaya", "Meghalaya", "Meghalaya", "梅加拉亚邦", "梅加拉亚邦", "메갈라야 주"]],
	17: [12.9833333, 77.5833333, ["カルナータカ州", "Karnataka", "Karnataka", "Karnataka", "Karnataka", "Karnataka", "Karnataka", "卡纳塔克邦", "卡纳塔克邦", "카르나타카 주"]],
	18: [25.6666667, 94.1166667, ["ナーガーランド州", "Nagaland", "Nagaland", "Nagaland", "Nagaland", "Nagaland", "Nagaland", "那加兰邦", "那加兰邦", "나갈랜드 주"]],
	19: [20.2333333, 85.8333333, ["オリッサ州", "Odisha", "Odisha", "Odisha", "Odisha", "Odisha", "Odisha", "奥里萨邦", "奥里萨邦", "오리사 주"]],
	20: [11.93, 79.83, ["ポンディシェリー", "Puducherry", "Puducherry", "Pondichéry", "Pondicherry", "Pondicherry", "Pondicherry", "本地治里中央直辖区", "本地治里中央直辖区", "퐁디셰리 "]],
	21: [30.7372222, 76.7872222, ["パンジャーブ州", "Punjab", "Punjab", "Penjab", "Panyab", "Punjab", "Punjab", "旁遮普邦", "旁遮普邦", "펀자브 주"]],
	22: [26.9166667, 75.8166667, ["ラージャスターン州", "Rajasthan", "Rajasthan", "Rajasthan", "Rajastán", "Rajasthan", "Rajasthan", "拉贾斯坦邦", "拉贾斯坦邦", "라자스탄 주"]],
	23: [13.0833333, 80.2833333, ["タミル・ナードゥ州", "Tamil Nadu", "Tamil Nadu", "Tamil Nadu", "Tamil Nadu", "Tamil Nadu", "Tamil Nadu", "泰米尔纳德邦", "泰米尔纳德邦", "타밀나두 주"]],
	24: [23.8363889, 91.275, ["トリプラ州", "Tripura", "Tripura", "Tripura", "Tripura", "Tripura", "Tripura", "特里普拉邦", "特里普拉邦", "트리푸라 주"]],
	25: [22.5697222, 88.3697222, ["西ベンガル州", "West Bengal", "Westbengalen", "Bengale-Occidental", "Bengala Occidental", "Bengala Occidentale", "West-Bengalen", "西孟加拉邦", "西孟加拉邦", "서벵골 주"]],
	26: [27.3333333, 88.6166667, ["シッキム州", "Sikkim", "Sikkim", "Sikkim", "Sikkim", "Sikkim", "Sikkim", "锡金邦", "锡金邦", "시킴 주"]],
	28: [23.7333333, 92.7166667, ["ミゾラム州", "Mizoram", "Mizoram", "Mizoram", "Mizorán", "Mizoram", "Mizoram", "米佐拉姆邦", "米佐拉姆邦", "미조람 주"]],
	29: [20.4166667, 72.85, ["ダマン・ディウ直轄地", "Daman and Diu", "Daman und Diu", "Daman et Diu", "Damán y Diu", "Daman e Diu", "Daman en Diu", "达曼和第乌中央直辖区", "达曼和第乌中央直辖区", "다만 디우"]],
	30: [15.4833333, 73.8333333, ["ゴア州", "Goa", "Goa", "Goa", "Goa", "Goa", "Goa", "果阿邦", "果阿邦", "고아 주"]],
	31: [25.6, 85.1166667, ["ビハール州", "Bihar", "Bihar", "Bihar", "Bihar", "Bihar", "Bihar", "比哈尔邦", "比哈尔邦", "비하르 주"]],
	32: [23.2666667, 77.4, ["マディヤ・プラデーシュ州", "Madhya Pradesh", "Madhya Pradesh", "Madhya Pradesh", "Madhya Pradesh", "Madhya Pradesh", "Madhya Pradesh", "中央邦", "中央邦", "마디아프라데시 주"]],
	33: [26.85, 80.9166667, ["ウッタル・プラデーシュ州", "Uttar Pradesh", "Uttar Pradesh", "Uttar Pradesh", "Uttar Pradesh", "Uttar Pradesh", "Uttar Pradesh", "北方邦", "北方邦", "우타르프라데시 주"]],
	34: [21.2333333, 81.6333333, ["チャッティースガル州", "Chhattisgarh", "Chhattisgarh", "Chhattisgarh", "Chhattisgarh", "Chhattisgarh", "Chhattisgarh", "查蒂斯加尔邦", "查蒂斯加尔邦", "차티스가르 주"]],
	35: [23.36, 85.329, ["ジャールカンド州", "Jharkhand", "Jharkhand", "Jharkhand", "Jharkhand", "Jharkhand", "Jharkhand", "贾坎德邦", "贾坎德邦", "자르칸드 주"]],
	36: [30.3166667, 78.0333333, ["ウッタラーカンド州", "Uttarakhand", "Uttarakhand", "Uttarakhand", "Uttarakhand", "Uttarakhand", "Uttarakhand", "北安查尔邦", "北安查尔邦", "우타라칸드 주"]],
	37: [28.6, 77.2, ["その他", "Other", "Sonstige", "Autre", "(Otra)", "Altre", "Overig", "其他", "其他", "기타"]]
}

regioninfo_170 = {
	1: [0, 0, ["エジプト", "Egypt", "Ägypten", "Egypte", "Egipto", "Egitto", "Egypte"]],
	2: [30.05, 31.25, ["カイロ", "Al Qahirah", "Kairo", "Le Caire", "El Cairo", "Il Cairo", "Caïro"]],
	3: [31.08333333, 32.06666667, ["ダカリーヤ", "Ad Daqahliyah", "Ad Daqahliyah", "Dakahleya", "Ad Daqahliyah", "Ad Daqahliyah", "Dakahleya"]],
	4: [27.2388889, 33.8361111, ["バフルアルアフマル", "Al Bahr al Ahmar", "Al-Bahr al-Ahmar", "Mer Rouge", "Al Bahr al Ahmar", "Al Bahr al Ahmar", "Rode Zee"]],
	5: [30.35, 30.21666667, ["ブハイラ", "Al Buhayrah", "Al Buhaira", "Beheira", "Al Buhayrah", "Al Buhayrah", "Beheira"]],
	6: [29.3077778, 30.84, ["ファイユーム", "Al Fayyum", "Al-Fayyum", "Fayoum", "Al Fayyum", "Al Fayyum", "Faium"]],
	7: [30.7911111, 30.9980556, ["カルビーヤ", "Al Gharbiyah", "Al-Gharbiyya", "Gharbeya", "Al Gharbiyah", "Al Gharbiyah", "Gharbeya"]],
	8: [31.1980556, 29.9191667, ["アレクサンドリア", "Al Iskandariyah", "Alexandria", "Alexandrie", "Alejandría", "Alessandria", "Alexandrië"]],
	9: [30.5833333, 32.2666667, ["イスマーイリーヤ", "Al Isma‘iliyah", "Al Isma'iliyah", "Ismaïlia", "Al Isma'iliyah", "Al Isma‘iliyah", "Ismailia"]],
	10: [30.0086111, 31.2122222, ["ジーザ", "Al Jizah", "Al-Dschiza", "Gizeh", "Al Gizah", "Giza", "Gizeh"]],
	11: [30.2, 31.55, ["ミヌーフィーヤ", "Al Minufiyah", "Al Minufiyya", "Menufeya", "Al Minufiyah", "Al Minufiyah", "Menufeya"]],
	12: [28.1194444, 30.7444444, ["ミニヤ", "Al Minya", "Al Minya", "Minya", "Al Minya", "Al Minya", "Minya"]],
	13: [30.4608333, 31.1875, ["カリュビーヤ", "Al Qalyubiyah", "Al Qalyubiyya", "Kalyubeya", "Al Qalyubiyah", "Al Qalyubiyah", "Kalyubeya"]],
	14: [25.4333333, 30.55, ["ニューバレル", "Al Wadi al Jadid", "al-Wadi al-Dschadid", "New Valley", "Al Wadi al Jadid", "Al Wadi al Jadid", "Nieuwe Vallei"]],
	15: [30.5913889, 31.5102778, ["シャルキーヤ", "Ash Sharqiyah", "Asch Scharqiyya", "Zagazig", "Ash Sharqiyah", "Ash Sharqiyah", "Sharkeya"]],
	16: [29.9666667, 32.55, ["スエズ", "As Suways", "As-Suwais", "Suez", "As Suways", "As Suways", "Suez"]],
	17: [24.0875, 32.8988889, ["アスワン", "Aswan", "Assuan", "Assouan", "Aswan", "Aswan", "Aswan"]],
	18: [27.1827778, 31.1827778, ["アシュート", "Asyut", "Asyut", "Assiout", "Asyut", "Asyut", "Assioet"]],
	19: [29.0638889, 31.0888889, ["ベニ・スエフ", "Bani Suwayf", "Bani Suwaif", "Beni Souef", "Bani Suwayf", "Bani Suwayf", "Beni Suef"]],
	20: [31.2666667, 32.3, ["ブールサイド", "Bur Sa‘id", "Port Said", "Port-Saïd", "Port Said", "Bur Sa‘id", "Port Saïd"]],
	21: [31.4194444, 31.815, ["ドゥミヤート", "Dumyat", "Damiette", "Damiette", "Dumyat", "Dumyat", "Damietta"]],
	22: [31.1113889, 30.9363889, ["カフルアッシャイアフ", "Kafr ash Shaykh", "Kafr asch-Schaich", "Kafr el-Cheik", "Kafr Al Shaykh", "Kafr ash Shaykh", "Kafr el Sheikh"]],
	23: [31.35, 27.2333333, ["マトルーフ", "Matruh", "Matruh", "Marsa-Matruh", "Matruh", "Matruh", "Matruh"]],
	24: [26.17, 32.7272222, ["キーナ", "Qina", "Qina", "Qena", "Qina", "Qina", "Qina"]],
	25: [26.55, 31.7, ["ソハーグ", "Suhaj", "Suhaj", "Sohag", "Suhag", "Suhaj", "Suhaj"]],
	26: [28.2372222, 33.6138889, ["ジャヌーブシーナー", "Janub Sina'", "Dschanub Sina", "Sud de Sinai", "Janub Sina'", "Janub Sinai", "Zuidelijke Sinaï"]],
	27: [31.1244444, 33.8005556, ["シャーマルシーナ", "Shamal Sina'", "Schimal Sina", "Nord de Sinai", "Shamal Sina'", "Shamal Sinai", "Noordelijke Sinaï"]],
	28: [25.6833333, 32.65, ["ルクソール", "Luxor", "Al Uqsur", "Al Uqsur", "Luxor", "Al Uqsur", "Al Uqsur"]]
}

regioninfo_171 = {
	1: [0, 0, ["オマーン", "Oman", "Oman", "Oman", "Omán", "Oman", "Oman"]],
	2: [23.6133333, 58.5933333, ["マスカット州", "Masqat", "Maskat", "Mascate", "Mascate", "Mascate", "Masqat"]],
	3: [22.9333333, 57.5333333, ["Ad Dakhiliyah", "Ad Dakhiliyah", "ad-Dachliyya (Region)", "Intérieure", "Ad Dakhiliyah", "Ad Dakhiliyah", "Ad Dakhiliyah"]],
	4: [24.3688889, 56.7438889, ["Al Batinah", "Al Batinah", "Batina (Region)", "Al Batinah", "Al Batinah", "Al Batinah", "Al Batinah"]],
	5: [19.65, 57.7, ["Al Wusta", "Al Wusta", "Wusta (Region)", "Al Wusta", "Al Wusta", "Al Wusta", "Al Wusta"]],
	6: [22.5666667, 59.5288889, ["Ash Sharqiyah", "Ash Sharqiyah", "Scharqiyya (Region)", "Est", "Ash Sharqiyah", "Ash Sharqiyah", "Ash Sharqiyah"]],
	7: [23.2363889, 56.5044444, ["Az Zahirah", "Az Zahirah", "adh-Dhahira (Region)", "Az-Zahirah", "Ad Dhahirah", "Az Zahirah", "Az Zahirah"]],
	8: [26.1916667, 56.2436111, ["マサンダム", "Musandam", "Musandam", "Moussandam", "Musandam", "Musandam", "Musandam"]],
	9: [17.0175, 54.0827778, ["Zufar", "Zufar", "Dhofar", "Sud", "Zufar", "Zufar", "Zufar"]]
}

regioninfo_172 = {
	1: [25.2866667, 51.5333333, ["カタール", "Qatar", "Katar", "Qatar", "Qatar", "Qatar", "Qatar"]]
}

regioninfo_173 = {
	1: [29.3697222, 47.9783333, ["クウェート", "Kuwait", "Kuwait", "Koweït", "Kuwait", "Kuwait", "Koeweit"]]
}

regioninfo_174 = {
	1: [0, 0, ["サウジアラビア", "Saudi Arabia", "Saudi-Arabien", "Arabie saoudite", "Arabia Saudí", "Arabia Saudita", "Saoedi-Arabië"]],
	2: [24.6408333, 46.7727778, ["リヤド州", "Ar Riyad", "Riad", "Ar Riyâd", "Ar Riyad", "Al Riyad", "Ar Riyad"]],
	3: [20.0166667, 41.4666667, ["バーハ州", "Al Bahah", "Baha", "Al Bâhah", "Al Bahah", "Al Bahah", "Al Bahah"]],
	4: [24.0852778, 38.0486111, ["メディナ州", "Al Madinah", "Medina", "Médine", "Al Madinah", "Medina", "Medina"]],
	5: [26.4258333, 50.1141667, ["東部州", "Ash Sharqiyah", "Asch Scharqiyya", "Province Est", "Ash Sharqiyah", "Ash Sharqiyah", "Ash Sharqiyah"]],
	6: [26.3316667, 43.9716667, ["カスィーム州", "Al Qasim", "Qasim", "Al Qasim", "Al Qasim", "Al Qasim", "Al Qasim"]],
	7: [18.2163889, 42.5052778, ["アシール州", "'Asir", "Asir", "Assir", "'Asir", "‘Asir", "Asir"]],
	8: [27.33333333, 41.6, ["ハーイル州", "Ha'il", "Hail", "Haîl", "Ha'il", "Ha'il", "Ha´il"]],
	9: [21.4266667, 39.8261111, ["メッカ州", "Makkah", "Mekka", "La Mecque", "Hiyaz", "Hijàz", "Mekka"]],
	10: [30.985, 41.0205556, ["北部国境州", "Al Hudud ash Shamaliyah", "Northern Frontier", "Frontière Nord", "Al Hudud ash Shamaliyah", "Al Hudud ash Shamaliyah", "Al Hudud ash-Shamaliyah"]],
	11: [17.5055556, 44.1841667, ["ナジュラーン州", "Najran", "Nadschran", "Nadjrân", "Najran", "Najran", "Najran"]],
	12: [16.8891667, 42.5511111, ["ジーザーン州", "Jizan", "Dschaizan", "Djîzân", "Jizan", "Jizan", "Jizan"]],
	13: [28.3833333, 36.5833333, ["タブーク州", "Tabuk", "Tabuk", "Taboûk", "Tabuk", "Tabuk", "Tabuk"]],
	14: [29.81, 39.869, ["ジャウフ州", "Al Jawf", "Dschauf", "Al Djôf", "Al Jawf", "Al Jawf", "Al Jawf"]]
}

regioninfo_175 = {
	1: [0, 0, ["シリア", "Syria", "Syrien", "Syrie", "Siria", "Siria", "Syrië"]],
	2: [33.5, 36.3, ["ダマスカス", "Rif Dimashq", "Damaskus", "Rif Dimashq", "Damasco", "Damasco", "Damascus"]],
	3: [36.4833333, 40.75, ["ハサカ", "Al Hasakah", "Al Hasaka", "Al Hasakah", "Al Hasakah", "Al Hasakah", "Al Hasakah"]],
	4: [35.5166667, 35.7833333, ["ラタキア", "Al Ladhiqiyah", "Latakia", "Latakia", "Al Ladhiqiyah", "Al Ladhiqiyah", "Latakia"]],
	5: [33.1252778, 35.8236111, ["クナイトゥラ", "Al Qunaytirah", "Al Qunaitira", "Quneitra", "Altos de Golán", "Quneitra", "Al Qunaytirah"]],
	6: [35.95, 39.0166667, ["ラッカ", "Ar Raqqah", "Ar Raqqah", "Rakka", "Ar Raqqah", "Ar Raqqah", "Ar Raqqah"]],
	7: [32.7, 36.5666667, ["スウェイダー", "As Suwayda'", "As Suwaida", "Es Suweidiya", "As Suwayda'", "As Suwaida", "As Suwayda"]],
	8: [32.61666667, 36.1, ["ダルアー", "Dar‘a", "Dara", "Dera", "Dar'a", "Dara", "Dara"]],
	9: [35.3333333, 40.15, ["デーレッゾール", "Dayr az Zawr", "Dair az-Zaur", "Deïr ez-Zôr", "Dayr az Zawr", "Dayr ar Zawr", "Dayr az-Zawr"]],
	10: [33.5, 36.3, ["ディマシュク", "Rif Dimashq", "Rif Dimaschq", "Rif Dimashq", "Rif Dimashq", "Rif Dimashq", "Rif Damascus"]],
	11: [36.2027778, 37.1586111, ["ハラブ", "Halab", "Aleppo", "Alep", "Halab", "Aleppo", "Aleppo"]],
	12: [35.1333333, 36.75, ["ハマー", "Hamah", "Hama", "Hamâh", "Hamah", "Hamah", "Hama"]],
	13: [34.7333333, 36.7166667, ["ホムス", "Hims", "Homs", "Homs", "Hims", "Hims", "Homs"]],
	14: [35.9297222, 36.6316667, ["イドリブ", "Idlib", "Idlib", "Idlib", "Idlib", "Idlib", "Idlib"]],
	15: [34.8833333, 35.8833333, ["タルトゥース", "Tartus", "Tartus", "Tartous", "Tartus", "Tartus", "Tartus"]]
}

regioninfo_176 = {
	1: [26.2361111, 50.5830556, ["バーレーン", "Bahrain", "Bahrain", "Bahreïn", "Bahréin", "Bahrain", "Bahrein"]]
}

regioninfo_177 = {
	1: [31.95, 35.9333333, ["ヨルダン", "Jordan", "Jordanien", "Jordanie", "Jordania", "Giordania", "Jordanië"]]
}

regioninfo = {
	1: regioninfo_001,
	8: regioninfo_008,
	9: regioninfo_009,
	10: regioninfo_010,
	11: regioninfo_011,
	12: regioninfo_012,
	13: regioninfo_013,
	14: regioninfo_014,
	15: regioninfo_015,
	16: regioninfo_016,
	17: regioninfo_017,
	18: regioninfo_018,
	19: regioninfo_019,
	20: regioninfo_020,
	21: regioninfo_021,
	22: regioninfo_022,
	23: regioninfo_023,
	24: regioninfo_024,
	25: regioninfo_025,
	26: regioninfo_026,
	27: regioninfo_027,
	28: regioninfo_028,
	29: regioninfo_029,
	30: regioninfo_030,
	31: regioninfo_031,
	32: regioninfo_032,
	33: regioninfo_033,
	34: regioninfo_034,
	35: regioninfo_035,
	36: regioninfo_036,
	37: regioninfo_037,
	38: regioninfo_038,
	39: regioninfo_039,
	40: regioninfo_040,
	41: regioninfo_041,
	42: regioninfo_042,
	43: regioninfo_043,
	44: regioninfo_044,
	45: regioninfo_045,
	46: regioninfo_046,
	47: regioninfo_047,
	48: regioninfo_048,
	49: regioninfo_049,
	50: regioninfo_050,
	51: regioninfo_051,
	52: regioninfo_052,
	64: regioninfo_064,
	65: regioninfo_065,
	66: regioninfo_066,
	67: regioninfo_067,
	68: regioninfo_068,
	69: regioninfo_069,
	70: regioninfo_070,
	71: regioninfo_071,
	72: regioninfo_072,
	73: regioninfo_073,
	74: regioninfo_074,
	75: regioninfo_075,
	76: regioninfo_076,
	77: regioninfo_077,
	78: regioninfo_078,
	79: regioninfo_079,
	80: regioninfo_080,
	81: regioninfo_081,
	82: regioninfo_082,
	83: regioninfo_083,
	84: regioninfo_084,
	85: regioninfo_085,
	86: regioninfo_086,
	87: regioninfo_087,
	88: regioninfo_088,
	89: regioninfo_089,
	90: regioninfo_090,
	91: regioninfo_091,
	92: regioninfo_092,
	93: regioninfo_093,
	94: regioninfo_094,
	95: regioninfo_095,
	96: regioninfo_096,
	97: regioninfo_097,
	98: regioninfo_098,
	99: regioninfo_099,
	100: regioninfo_100,
	101: regioninfo_101,
	102: regioninfo_102,
	103: regioninfo_103,
	104: regioninfo_104,
	105: regioninfo_105,
	106: regioninfo_106,
	107: regioninfo_107,
	108: regioninfo_108,
	109: regioninfo_109,
	110: regioninfo_110,
	111: regioninfo_111,
	112: regioninfo_112,
	113: regioninfo_113,
	114: regioninfo_114,
	115: regioninfo_115,
	116: regioninfo_116,
	117: regioninfo_117,
	118: regioninfo_118,
	119: regioninfo_119,
	120: regioninfo_120,
	121: regioninfo_121,
	128: regioninfo_128,
	136: regioninfo_136,
	144: regioninfo_144,
	145: regioninfo_145,
	152: regioninfo_152,
	153: regioninfo_153,
	154: regioninfo_154,
	155: regioninfo_155,
	156: regioninfo_156,
	160: regioninfo_160,
	168: regioninfo_168,
	169: regioninfo_169,
	170: regioninfo_170,
	171: regioninfo_171,
	172: regioninfo_172,
	173: regioninfo_173,
	174: regioninfo_174,
	175: regioninfo_175,
	176: regioninfo_176,
	177: regioninfo_177,
}
