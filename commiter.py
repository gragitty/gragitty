import os
import requests
import re
import psycopg2
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

COLOR_TO_COUNT_MAP = {
	'EMPTY': 0,
	'GREEN1': 1,
	'GREEN2': 5,
	'GREEN3': 10,
	'GREEN4': 15
}

def write_to_file(date_time, AUTHOR):
	with open('contribution.txt', 'r') as file:
		lines = file.readlines()

	with open('contribution.txt', 'w') as file:
		lines.append(AUTHOR + ' wrote a line on ' + date_time)
		file.writelines(lines[-100:])


def commit_stub(COUNT=0, DATE='', AUTHOR='', MESSAGE='', TYPE=''):
	count = 0
	while(count < COUNT):
		current_date_time = datetime.now().__str__()
		write_to_file(current_date_time, AUTHOR)
		command = 'git add -A'
		os.system(command)
		CURR_TIME = current_date_time.split()[-1].split('.')[0]
		command = 'git commit --date "' + DATE + ' ' + CURR_TIME + '" -m "commiting to past at ' + current_date_time + '" --author "' + AUTHOR + '"'
		os.system(command)
		command = 'git push'
		os.system(command)
		count += 1

def get_request_body():
	body = {
		'clientID': os.environ['GITHUB_CLIENT_ID'],
		'clientSecret': os.environ['GITHUB_CLIENT_SECRET'],
		'username': os.environ['AUTH_USERNAME']
	}
	return body

def get_db_url():
	req_url = os.environ['REQUEST_URL']
	body = get_request_body()
	db_url = requests.get(
		req_url,
		json=body
	).content.decode('ascii')
	return db_url

def parse_url_to_credentials():
	credentials = re.compile(
		r'postgres://(\w+):(\w+)@([0-9\.\-a-z/]+):(\d+)/(\w+)'
	).search(get_db_url()).groups()
	return credentials

def get_db_credentials():
	db_credentials = dict(
		zip(
			('user', 'password', 'host', 'port', 'database'),
			parse_url_to_credentials()
		)
	)
	return db_credentials

def connect_to_db():
	connection = None
	try:
		connection = psycopg2.connect(**get_db_credentials())
	except Exception as e:
		print(e)
	return connection

def get_author_from_id(userId, connection):
	cursor = connection.cursor()
	query = '''
	select name, email from users
	where id='{0}';
	'''.format(userId)
	cursor.execute(query)
	user = cursor.fetchone()
	cursor.close()
	return '{0} <{1}>'.format(*user)

def arrange_tasks(db_tasks, connection):
	tasks = []
	for db_task in db_tasks:
		tasks.append((dict(zip(
			('MESSAGE', 'TYPE', 'DATE', 'COUNT', 'AUTHOR'),
			(
				db_task[0], db_task[1], db_task[2],
				COLOR_TO_COUNT_MAP[db_task[3]],
				get_author_from_id(db_task[4], connection)
			)
		)), db_task[5]))
	return tasks

def run_tasks_query(connection):
	cursor = connection.cursor()
	query = '''
	select
		message, type, date, color, "userId", id
	from tasks where completed = FALSE and date <= '{0}';
	'''.format(str(datetime.today().date()))
	cursor.execute(query)
	db_tasks = cursor.fetchall()
	cursor.close()
	return arrange_tasks(db_tasks, connection)


def get_todays_tasks(connection):
	return run_tasks_query(connection)

def mark_task_completed(connection, ID):
	cursor = connection.cursor()
	query = '''
	update tasks
	set completed=TRUE
	where id = '{0}';
	'''.format(ID)
	cursor.execute(query)
	cursor.close()

if __name__ == '__main__':
	try:
		load_dotenv(find_dotenv())
		connection = connect_to_db()
		tasks = get_todays_tasks(connection)
		for task, ID in tasks:
			commit_stub(**task)
			mark_task_completed(connection, ID)
	except Exception as e:
		print(e)
	finally:
		connection.close()