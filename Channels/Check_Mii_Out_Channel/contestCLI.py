from time import mktime
from datetime import date, datetime
import MySQLdb
from json import load

with open("/var/rc24/File-Maker/Channels/Check_Mii_Out_Channel/config.json", "r") as f:
        config = load(f)
        
db = MySQLdb.connect('localhost', config['dbuser'], config['dbpass'], 'cmoc', charset='utf8mb4')
cursor = db.cursor()

class colors:
	HEADER = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	END = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def searchContest():
	search = str(input('-> Please enter a keyword or phrase in the contest\'s topic or description: '))
	formattedSearch = '%' + search.replace(' ', '%') + '%'
	cursor.execute('SELECT id, description FROM contests WHERE topic LIKE %s OR description LIKE %s', (formattedSearch, formattedSearch))
	result = cursor.fetchall()

	print(len(result), 'results for "' + str(search) + '"')
	print('ID   | Description\n-------------------')
	for i in result:
		print(str(i[0]) + ' ' * (4 - len(str(i[0]))), '|', i[1])

	print()

def showInfo(id):
	cursor.execute('SELECT start, end, status, entrycount, topic, description FROM contests WHERE id = %s', [id])
	result = cursor.fetchone()
	if result == None:
		print(f'{colors.FAIL}ID:', id, f'does not exist!{colors.END}')

	else:
		print('ID:', id)
		print('Start:', datetime.fromtimestamp(result[0] + 946684800).date())
		print('End:', datetime.fromtimestamp(result[1] + 946684800).date())
		print('Status:', result[2].capitalize())
		print('Submissions:', result[3])
		print('Topic:', result[4])
		print('Description:', result[5])
	print()

print(f'{colors.BOLD}CMOC Contest Editor\nRiiConnect24 - Created by Josh{colors.END}\n1 - Add\n2 - Edit\n3 - Remove\n4 - View')
entry = int(input('-> Selection: '))

if entry == 1:
	print('\nCreating new contest ->')
	while True:
		month = input('-> Enter starting month (leave blank to start when next contest changes status): ')

		if len(month) == 0:
			currentTime = int(mktime(datetime.utcnow().timetuple())) - 946684800
			cursor.execute('SELECT end, status, description FROM contests WHERE end > %s AND status != \'closed\' ORDER BY end ASC LIMIT 1', [currentTime])
			nextContest = cursor.fetchone()

			if len(nextContest) == 0:
				print('There are no future contests scheduled. Please try again and enter the date manually.')
				exit()

			start = int(nextContest[0]) #set start time to next contest's end time
			startDate = datetime.fromtimestamp(start + 946684800).date()

			end = int(start + (7 * 24 * 60 * 60)) #change status every 7 days until closure
			endDate = datetime.fromtimestamp(end + 946684800).date()

			if nextContest[1] == 'waiting':		nextStatus = 'open'
			elif nextContest[1] == 'open':    nextStatus = 'judging'
			elif nextContest[1] == 'judging':   nextStatus = 'results'
			elif nextContest[1] == 'results':   nextStatus = 'closed'

			print('\nThe contest \'{}\' will become status \'{}\' on {}.'.format(nextContest[2], nextStatus, startDate))
			choice = str(input('-> This new contest will begin at this date. Is this correct? [Y/N]: '))
			if choice.upper() != 'Y':
				print(f'{colors.FAIL}Contest adding aborted.{colors.END}')
				exit()
			
			break

		else:
			try:
				month = int(month)
			except:
				print(f'{colors.FAIL}Invalid month!{colors.END} Make sure you are entering the month by its number.')
				continue

			if month < datetime.now().month and datetime.now().month != 12:
				print('That month has already passed.')
				exit()

			day = int(input('-> Enter starting day: '))
			if day < datetime.now().day:
				print('That date has already passed.')
				exit()

			try:
				d = date(datetime.now().year, month, day)
				
			except ValueError as e:
				print(e)
				exit()

			start = int(mktime(d.timetuple()) - 946684800)
			startDate = datetime.fromtimestamp(start + 946684800).date()

			end = int(start + (7 * 24 * 60 * 60))
			endDate = datetime.fromtimestamp(end + 946684800).date()
			break

	while True:
		topic = str(input('-> Enter topic: '))
		if len(topic) > 10:
			print('The contest topic cannot be longer than 10 characters. That topic is', len(topic), 'characters.')

		else:
			break

	while True:
		description = str(input('-> Enter description: '))
		if len(description) > 64:
			print('The contest description cannot be longer than 64 characters. That topic is', len(description), 'characters.')

		else:
			break

	print()
	print('Description:', description)
	print('Topic:', topic)
	print('Start date:', startDate)
	print('End date:', endDate)
	choice = str(input('-> Is this information correct? [Y/N]: '))
	if choice.upper() == 'Y':
		cursor.execute('INSERT INTO contests(start, end, status, entrycount, topic, description) VALUES (%s, %s, %s, %s, %s, %s)', (start, end, 'waiting', 0, topic, description))
		db.commit()
		print(f'{colors.GREEN}Contest added successfully.{colors.END}')

	else:
		print(f'{colors.FAIL}Contest adding aborted.{colors.END}')
		exit()

elif entry == 2:
	stop = False
	print('\nEditing contest ->')

	cursor.execute('SELECT id, description FROM contests ORDER BY id DESC limit 5')
	print('---5 most recently created contests---')
	print('ID   | Description\n-------------------')
	for i in cursor.fetchall():
		print(str(i[0]) + ' ' * (4 - len(str(i[0]))), '|', i[1])
	print()

	while not stop:      
		print('1 - Enter a contest ID\n2 - Search for a contest by keyword')
		selection = int(input('-> Selection: '))
		if selection == 1:
			id = int(input('-> Enter contest ID: '))
			cursor.execute('SELECT COUNT(*) FROM contests WHERE id = %s', [id])
			if cursor.fetchone()[0] == 0:
				print(f'{colors.FAIL}ID:', id, f'does not exist!{colors.END}\n')
				continue

			showInfo(id)

			print('1 - Change topic\n2 - Change description')
			editSelection = int(input('-> Selection: '))

			if editSelection == 1:
				while True:
					topic = str(input('-> Enter a new topic for the contest: '))
					if len(topic) > 10:
						print('The contest topic cannot be longer than 10 characters. That topic is', len(topic), 'characters.')
					else:
						break

				cursor.execute('UPDATE contests SET topic = %s WHERE id = %s', (topic, id))
				db.commit()
				print(f'{colors.GREEN}Contest topic updated successfully.{colors.END}')
				stop = True

			elif editSelection == 2:
				while True:
					description = str(input('-> Enter a new description for the contest: '))
					if len(description) > 64:
						print('The contest topic cannot be longer than 64 characters. That topic is', len(description), 'characters.')
					else:
						break

				cursor.execute('UPDATE contests SET description = %s WHERE id = %s', (description, id))
				db.commit()
				print(f'{colors.GREEN}Contest description updated successfully.{colors.END}')
				stop = True

			else:
				print(f'{colors.FAIL}Invalid entry!{colors.END}')
				stop = True

		elif selection == 2:
			searchContest()

		else:
			print(f'{colors.FAIL}Invalid entry!{colors.END}\n')

elif entry == 3:
	stop = False
	print('\nRemoving contest ->')

	cursor.execute('SELECT id, description FROM contests ORDER BY id DESC limit 5')
	print('---5 most recently created contests---')
	print('ID   | Description\n-------------------')
	for i in cursor.fetchall():
		print(str(i[0]) + ' ' * (4 - len(str(i[0]))), '|', i[1])

	while not stop:
		print('\n1 - Enter a contest ID\n2 - Search for a contest by keyword')
		selection = int(input('-> Selection: '))

		if selection == 1:
			id = int(input('-> Enter contest ID: '))
			cursor.execute('SELECT status, entrycount FROM contests WHERE id = %s', [id])
			result = cursor.fetchone()
			if result == None:
				print(f'ID:{colors.FAIL}', id, f'does not exist!{colors.END}')
				continue

			showInfo(id)

			if result[0] != 'closed':   print('WARNING: This contest is still active with status \'{}\'.'.format(result[0]))

			if int(result[1]) != 0:
				print('This contest and its', result[1], 'miis will be permanently deleted.')

			else:
				print('This contest will be permanently deleted.')

			choice = str(input(f'-> Are you sure you want to {colors.UNDERLINE}delete{colors.END} contest #{id}? [Y/N]: '))

			if choice.upper() == 'Y': #REMEMBER TO DELETE THE MIIS TOO IDIOT
				cursor.execute('DELETE FROM contests WHERE id = %s', [id])
				db.commit()
				print(f'{colors.GREEN}Contest', id, f'deleted.{colors.END}')
				stop = True

			else:
				print(f'{colors.FAIL}Contest deletion aborted.{colors.END}')
				stop = True

		elif selection == 2:
			searchContest()

		else:
			print(f'{colors.FAIL}Invalid entry!{colors.END}\n')

elif entry == 4:
	print('\nViewing contest information ->')
	cursor.execute('SELECT id, description FROM contests ORDER BY id DESC limit 5')
	print('---5 most recently created contests---')
	print('ID   | Description\n-------------------')
	for i in cursor.fetchall():
		print(str(i[0]) + ' ' * (4 - len(str(i[0]))), '|', i[1])
	print()

	while True:
		print('1 - Enter a contest ID\n2 - Search for a contest by keyword\n3 - Exit')
		selection = int(input('-> Selection: '))

		if selection == 1:
			id = int(input('-> Enter contest ID: '))
			showInfo(id)

		elif selection == 2:
			searchContest()

		elif selection == 3:
			break

		else:
			print(f'{colors.FAIL}Invalid entry!{colors.END}\n')

db.close()
