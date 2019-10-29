import os
import sys
from datetime import datetime

AUTHOR = "Mahendra Pamidi <mahendrapamidi96@gmail.com>"


def write_to_file(date_time):
    with open('contribution.txt', 'r') as file:
        lines = file.readlines()

    with open('contribution.text', 'w') as file:
        lines.append(AUTHOR + ' wrote a line on ' + date_time)
        file.writelines(lines[-100:])


def commit_stub(COUNT=0, DATE=''):
    count = 0
    while(count < COUNT):
        current_date_time = datetime.now().__str__()
        # write_to_file(current_date_time)
        command = 'git add -A'
        os.system(command)
        CURR_TIME = current_date_time.split()[-1].split('.')[0]
        command = 'git commit --date "' + DATE + ' ' + CURR_TIME + \
            '" -m "commiting to past at ' + current_date_time + '" --author "' + AUTHOR + '"'
        os.system(command)
        command = 'git push'
        os.system(command)
        count += 1


configs = [
    {'DATE': '2019-10-29', 'COUNT': 15}


]

for config in configs:
    commit_stub(**config)
