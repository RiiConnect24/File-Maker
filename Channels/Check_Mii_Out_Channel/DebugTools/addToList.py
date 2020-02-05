from cmoc import ResetList, QuickList, Prepare

#example script gets every single mii in the DB, then adds it to spot_list

ql = QuickList()
pr = Prepare()

miilist = []
artisanlist = []
miidata = 'gAoAPwAAAAAAAAAAAAAAAAAAAAAAAF4AhonbB8JJnRIgBDxAuX0ookiKBEAAMZkEAIoAiiUEAAAAAAAAAAAAAAAAAAAAAAAAAAAaLw=='
likes = 0
skill = 0
country = 49
initial = 'AA'

artisandata = 'gAsAUABlAGUAdwBlAGUAAAAAAAAAAAAAhorkD1RU1sYgADxAub0IPAiQCEAUabiQAIoAiiUEAAAAAAAAAAAAAAAAAAAAAAAAAAC68Q=='
master = 0

ResetList(b'NL')
for i in range(499):
	miilist.append((i, initial, likes, skill, country, miidata) + (artisandata, i, master))

list_type = 'NL'

data = ql.build(list_type, miilist)

with open('150/new_list01.ces', 'wb') as file:
	file.write(pr.prepare(data))

with open('150/new_list01.dec', 'wb') as file:
	file.write(data)
