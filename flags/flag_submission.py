#!/usr/bin/env python3
import sys
from typing import List
import requests
import urllib3
import logging
import os
import time
import stat
import threading
from collections import Counter
from pathlib import Path
from http import HTTPStatus
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)
login_lock = threading.Lock()
urllib3.disable_warnings()

SERVER = '10.10.40.200'
PORT = 443
URL = f'https://{SERVER}:{PORT}'
MAX_RETRY = 5
BEARER_TOKEN_PATH = 'bearer_token' # usage of file as token buffer due to the initial design as pipe end
CREDENTIAL_PATH = 'credentials'

def login() -> str:
    """Uses the credentials saved in CREDENTIAL_PATH to request a valid token.
    Token is saved in BEARER_TOKEN_PATH.
    
    """ 
    logger.debug('Trying to login...')
    credentials_path = Path(CREDENTIAL_PATH)
    if not credentials_path.is_file():
        logger.error(f'Credential file missing! Should be present at {credentials_path.absolute}')
        exit(1)
    if oct(credentials_path.stat().st_mode)[-3:] != '600':
        logger.error(f'File {credentials_path.absolute()} does not have 600 permissions. Please fix for security purposes.')
        exit(1)

    with credentials_path.open() as f:
        credentials = f.read().strip().splitlines()
    if len(credentials) != 2:
        logger.error('Credential file should have exactly 2 lines. First line username, second line password.')
        exit(1)
    username, password = credentials
    credential_body = { 'username': username, 'password': password }
    try:
        r = requests.post(f'{URL}/api/auth/login', json=credential_body, verify=False) # TLS certification verification off due to invalid certificate of the game server
    except RequestException as e:
        logger.exception('Error while requesting Bearer token')
    token = r.json()['token']
    logger.info(f'New bearer token: {token}')

    bearer_file_path = Path(BEARER_TOKEN_PATH)
    if bearer_file_path.is_file():
        bearer_file_path.unlink()
    with bearer_file_path.open('w') as file:
        file.write(token)
    os.chmod(bearer_file_path.absolute(), stat.S_IRUSR | stat.S_IWUSR)
    
    return token

def retrieve_token() -> str:
    """Retrieves token from BEARER_TOKEN_PATH"""
    bearer_file_path = Path(BEARER_TOKEN_PATH)
    if not bearer_file_path.is_file():
        with login_lock:
            if not bearer_file_path.is_file():
                return login()
    with bearer_file_path.open('r') as f:
        token = f.read().strip()
    return token

def submit_flags(flags: List[str], bearer_token: str = None) -> None:
    """Submit the flags to {URL}/api/flags.

    Parameters:
        - flags: List of flags to submit
        - bearer_token <Optional>: Token for authentication, if missing it will be requested
    """
    if bearer_token == None:
        bearer_token = retrieve_token()

    flag_submission = {'data': flags}
    headers = {'Authorization': f'Bearer {bearer_token}'}

    for i in range(0, MAX_RETRY):
        try:
            request = requests.post(f'{URL}/api/flags', headers=headers, json=flag_submission, verify=False)
            break
        except RequestException as e:
            logger.exception('Error submitting flag! Try %d of %d', i+1, MAX_RETRY)
            time.sleep(i)    
    if request.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]:
        logger.warn('Invalid bearer token! Trying to login again...')
        with login_lock:
            current_token = retrieve_token()
            new_token = login() if bearer_token == current_token else current_token
        submit_flags(flags, new_token)
        return
    if not request.ok:
        logger.error('Request not ok, aborting...')
        return

    flag_information = request.json()
    flag_counts = Counter(map(lambda x: x['result'], flag_information['data']))
    logger.info(f'Flag\'s status: {flag_counts.most_common()}')

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    flags = [line.strip() for line in sys.stdin.readlines()]
    submit_flags(flags)
