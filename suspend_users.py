import config
import csv
import logging
import os
import requests
import sys
from datetime import datetime

TASK_ID = f"user_suspension_{datetime.now().strftime('%d-%m-%y_%H%M%S')}"


def get_token():
    return {'Authorization': f'Bearer {config.TOKEN}'}


def create_log():
    filename = f'{TASK_ID}.log'
    if os.path.isdir('logs') is False:
        os.mkdir('logs')
    logfile = os.path.join('logs', filename)
    logging.basicConfig(
        filename=logfile,
        filemode='w',
        encoding='utf-8',
        level=logging.DEBUG,
        format='%(asctime)s - %(message)s',
    )
    logging.info(f'TASK_ID: {TASK_ID}\n')
    logging.info(f'{"="*9} START LOGGER {"="*9}')
    logging.info(f'Create log file: {logfile}\n')


def validate_token():
    logging.info(f'{"="*9} VALIDATE CANVAS TOKEN {"="*9}')
    print(f'Authenticating API Token:')
    try:
        url = f'{config.BASE_URL}/api/v1/accounts/'
        res = requests.get(url, headers=get_token())
        status = res.status_code
        if status != 200:
            print(f'\tNot authorized. Enter API token in config.py')
            logging.info('Not authorized. Enter API token in config.py')
            sys.exit(1)
        else:
            print(f'\tSuccessfully authenticated to {config.BASE_URL}')
            logging.info(f'Successfully authenticated to {config.BASE_URL}\n')
    except Exception as e:
        print(f'\tError, try again: {e}')
        logging.exception(f'Error validating canvas token: {e}')
        sys.exit(1)


def read_input():
    data = []
    logging.info(f'{"="*9} READ SUSPENSION INPUT FILE {"="*9}')
    print(f'\nReading {config.INPUT_FILE_PATH}:')
    try:
        with open(config.INPUT_FILE_PATH, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)
            for row in csvreader:
                if len(row) != 0:
                    data.append(row[0])
        logging.info(f'File {config.INPUT_FILE_PATH} read successfully')
        logging.info(f'Users to suspend: {len(data)}')
        logging.info(f'Data: {data}\n')
        print(f'\tSuccess, users to suspend: {len(data)}')
        return data
    except Exception as e:
        print(f'\tError, try again: {e}')
        logging.exception(f'Error reading input file: {e}')
        sys.exit(1)


def create_output_file():
    output_filename = f'{TASK_ID}.csv'
    row = ['id', 'created_at', 'login_id', 'status']
    logging.info(f'{"="*9} CREATE OUTPUT STATUS FILE {"="*9}')
    print(f'\nCreating output file {output_filename} with headers:')
    try:
        with open(output_filename, 'w', newline ='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        logging.info(f'File {output_filename} created with headers\n')
        print('\tSuccess')
        return output_filename
    except Exception as e:
        print(f'\tError, try again: {e}')
        logging.exception(f'Error creating output file: {e}')
        sys.exit(1)


def update_output_file(output_filename, data):
    try:
        with open(output_filename, 'a', newline ='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
    except Exception as e:
        logging.info(f'Unexpected error updating status file. Data: {data}')
        logging.exception(f'{e}')
        sys.exit(1)


def suspend_users(users, output_filename):
    logging.info(f'{"="*9} SUSPEND USERS {"="*9}')
    print(f'\nSuspend Users:')
    try:
        for i, user in enumerate(users):
            user = user.strip()
            logging.info(f'{i+1}. User ID: {user}')
            print(f'\t{i+1}. {user}: ', end='')
            url = config.BASE_URL+f'/api/v1/users/{user}'
            body = {'user': {'event': 'suspend'}}
            r = requests.put(url, headers=get_token(), json=body)
            if r.status_code == 200:
                print('Suspension successful')
                logging.info('Suspension successful')
                status = 'Suspension Successful'
            else:
                print('Suspension failed')
                logging.info('Suspension failed')
                status = 'Suspension Failed'
            res = r.json()
            created_at = res.get('created_at', '')
            login_id = res.get('login_id', '')
            output_data = [user, created_at, login_id, status]
            update_output_file(output_filename, output_data)
        print('')
    except Exception as e:
        print(f'\tError, try again: {e}')
        logging.exception(f'Error creating output file: {e}')
        sys.exit(1)


def main():
    #
    # 1. Create log file
    #
    create_log()

    #
    # 2. Validate Canvas API Token
    #
    validate_token()

    #
    # 3. Read user suspension input file
    #
    users = read_input()

    #
    # 4. Create output file
    #
    output_filename = create_output_file()

    #
    # 4. Suspend user accounts
    #
    suspend_users(users, output_filename)


if __name__ == '__main__':
    main()