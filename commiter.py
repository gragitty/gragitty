import os
import sys
from datetime import datetime

AUTHOR = "Krushi Raj Tula <krushiraj123@gmail.com>"

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
		write_to_file(current_date_time)
		command = 'git add -A'
		os.system(command)
		CURR_TIME = current_date_time.split()[-1].split('.')[0]
		command = 'git commit --date "' + DATE + ' ' + CURR_TIME + '" -m "commiting to past at ' + current_date_time + '" --author "' + AUTHOR + '"'
		os.system(command)
		command = 'git push'
		os.system(command)
		count += 1


configs = [
	{'DATE': '2018-10-29', 'COUNT': 15},

	{'DATE': '2018-11-04', 'COUNT': 15},
	{'DATE': '2018-11-05', 'COUNT': 10},
	{'DATE': '2018-11-06', 'COUNT': 5},
	{'DATE': '2018-11-07', 'COUNT': 15},

	{'DATE': '2018-11-11', 'COUNT': 15},
	{'DATE': '2018-11-12', 'COUNT': 10},
	{'DATE': '2018-11-13', 'COUNT': 5},
	{'DATE': '2018-11-14', 'COUNT': 1},
	{'DATE': '2018-11-15', 'COUNT': 15},

	{'DATE': '2018-11-19', 'COUNT': 15},
	{'DATE': '2018-11-20', 'COUNT': 5},
	{'DATE': '2018-11-21', 'COUNT': 1},
	{'DATE': '2018-11-22', 'COUNT': 5},
	{'DATE': '2018-11-23', 'COUNT': 15},

	{'DATE': '2018-11-27', 'COUNT': 15},
	{'DATE': '2018-11-28', 'COUNT': 1},
	{'DATE': '2018-11-29', 'COUNT': 5},
	{'DATE': '2018-11-30', 'COUNT': 10},
	{'DATE': '2018-12-01', 'COUNT': 15},

	{'DATE': '2018-12-03', 'COUNT': 15},
	{'DATE': '2018-12-04', 'COUNT': 5},
	{'DATE': '2018-12-05', 'COUNT': 1},
	{'DATE': '2018-12-06', 'COUNT': 5},
	{'DATE': '2018-12-07', 'COUNT': 15},

	{'DATE': '2018-12-09', 'COUNT': 15},
	{'DATE': '2018-12-10', 'COUNT': 10},
	{'DATE': '2018-12-11', 'COUNT': 5},
	{'DATE': '2018-12-12', 'COUNT': 1},
	{'DATE': '2018-12-13', 'COUNT': 15},

	{'DATE': '2018-12-16', 'COUNT': 15},
	{'DATE': '2018-12-17', 'COUNT': 10},
	{'DATE': '2018-12-18', 'COUNT': 5},
	{'DATE': '2018-12-19', 'COUNT': 15},

	{'DATE': '2018-12-24', 'COUNT': 15},
	{'DATE': '2018-12-25', 'COUNT': 15}
]

for config in configs:
	commit_stub(**config)
