import os
import sys
from datetime import datetime

COUNT = 11
DATE = "2018-10-30"
AUTHOR = "Krushi Raj Tula <krushiraj123@gmail.com>"


def write_to_file(date_time):
	with open('contribution.txt', 'r') as file:
		lines = file.readlines()

	with open('contribution.text', 'w') as file:
		lines.append(AUTHOR + ' wrote a line on ' + date_time)
		file.writelines(lines[-100:])


count = 0
while(count < COUNT):
	current_date_time = datetime.now().__str__()
	write_to_file(current_date_time)
	command = 'git add -A'
	os.system(command)
	CURR_TIME = current_date_time.split()[-1].split('.')[0]
	command = 'git commit --date "' + DATE + ' ' + CURR_TIME + '" -m "commiting to past at ' + current_date_time + '" --author "' + AUTHOR + '"'
	os.system(command)
	command = 'git push'
	os.system(command)
	count += 1
