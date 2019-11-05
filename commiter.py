import os
import requests
import re
import psycopg2
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

# A dictionary map for color to contribution count
COLOR_TO_COUNT_MAP = {
    'EMPTY': 0,
    'GREEN1': 1,
    'GREEN2': 5,
    'GREEN3': 10,
    'GREEN4': 15
}


def write_to_file(date_time, AUTHOR):
    '''
    Appends a new line with the author name and date time.
    This can be used as log for last 100 entries.
    If there are more than hundred lines then the latest 100 lines are retained.
    '''

    # Read the lines
    with open('contribution.txt', 'r') as file:
        lines = file.readlines()

    # Append and remove extra lines if there are any
    with open('contribution.txt', 'w') as file:
        lines.append(AUTHOR + ' wrote a line on ' + date_time + '\n')
        file.writelines(lines[-100:])


def commit_stub(COUNT=0, DATE='', AUTHOR='', MESSAGE='', TYPE=''):
    '''
    This will be used to commit by an author at a specified date with given message.
    '''
    count = 0
    while(count < COUNT):
        os.system('git pull')
        current_date_time = datetime.now().__str__()
        write_to_file(current_date_time, AUTHOR)
        command = 'git add -A'
        os.system(command)
        CURR_TIME = current_date_time.split()[-1].split('.')[0]
        command = 'git commit --date "' + DATE + ' ' + CURR_TIME + \
            '" -m "commiting to past at ' + current_date_time + '" --author "' + AUTHOR + '"'
        os.system(command)
        command = 'git push'
        os.system(command)
        count += 1


def get_request_body():
    '''
    Gets the body for request that has to be sent to backend to fetch URL for DB.
    '''
    body = {
        'clientID': os.environ['GITHUB_CLIENT_ID'],
        'clientSecret': os.environ['GITHUB_CLIENT_SECRET'],
        'username': os.environ['AUTH_USERNAME']
    }
    return body


def get_db_url():
    '''
    Gets the DB url by making a request to gragitty-backend server.
    '''
    req_url = os.environ['REQUEST_URL']
    body = get_request_body()
    db_url = requests.get(
        req_url,
        json=body
    ).content.decode('ascii')
    return db_url


def parse_url_to_credentials():
    '''
    Parse the recieved URL into credentials to pass to DB API, so that connection can be established.
    '''
    credentials = re.compile(
        r'postgres://(\w+):(\w+)@([0-9\.\-a-z/]+):(\d+)/(\w+)'
    ).search(get_db_url()).groups()
    return credentials


def get_db_credentials():
    '''
    Get DB credentials as a dictionary.
    '''
    db_credentials = dict(
        zip(
            ('user', 'password', 'host', 'port', 'database'),
            parse_url_to_credentials()
        )
    )
    return db_credentials


def connect_to_db():
    '''
    Connect to the gragitty-database.
    '''
    connection = None
    try:
        connection = psycopg2.connect(**get_db_credentials())
    except Exception as e:
        print(e)
    return connection


def get_author_from_id(userId, connection):
    '''
    Get Author details form user id.
    '''
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
    '''
    Arrange the pending tasks so that they can be picked up by the worker and executed.
    '''
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
    '''
    Fetch all tasks that are to be run at the time when this method is called.
    '''
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
    '''
    Fetches all the tasks that are scheduled or pending for today.
    '''
    return run_tasks_query(connection)


def mark_task_completed(connection, ID):
    '''
    Marks tasks as completed in the gragitty-database once they are committed
    '''
    cursor = connection.cursor()
    query = '''
	update tasks
	set completed=TRUE
	where id = '{0}';
	'''.format(ID)
    cursor.execute(query)
    connection.commit()
    cursor.close()


if __name__ == '__main__':
    try:
        load_dotenv(find_dotenv())
        connection = connect_to_db()
        tasks = get_todays_tasks(connection)
        for task, ID in tasks:
            commit_stub(**task)
            mark_task_completed(connection, ID)
        else:
            print('No tasks scheduled for the day')
    except Exception as e:
        print(e)
    finally:
        connection.close()
