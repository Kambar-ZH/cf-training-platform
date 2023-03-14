import requests
import json

def validate_user_not_exist(user_handle: str):
    resp = requests.get('https://codeforces.com/api/user.info?handles=' + user_handle)

    json_data = json.loads(resp.text)
    if json_data['status'] == 'FAILED' or len(json_data['result']) == 0:
        return False
    
    return True

def get_user(user_handle: str):
    resp = requests.get(f'https://codeforces.com/api/user.info?handles={user_handle}')

    json_data = json.loads(resp.text)
    return json_data