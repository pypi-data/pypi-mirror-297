import os
import re
import requests
from . import utils
from datetime import datetime
def convert_data(file) -> list:

    """
    Tele : t.me/im_dlam
    Converts data from a file into a structured format.

    Returns:
        list: A list of dictionaries containing user data.
    """
    try:
        with open(file, "r", encoding="UTF-8") as f:
            data_lines = f.readlines()
    except Exception as e:
        return str(e)
    
    data = []
    for line in data_lines:
        line = line.strip()
        if not line:
            continue
        
        user_data = parse_user_data(line)
        data.append(user_data)
    
    return data

def parse_user_data(line: str) -> dict:
    """
    Parses a single line of user data into a dictionary.

    Args:
        line (str): A single line of user data.

    Returns:
        dict: Parsed user data.
    """
    rp = utils.dict_typ()
    user = extract_user(line)
    rp["c_user"] = user

    password = utils.type_pw(value=line, valueid=user)
    if password:
        rp["password"] = password

    tokens = line.split("|")
    for token in tokens:
        token = token.strip()
        update_user_data(rp, token, line)
    
    rp['headers'].update({'cookie':rp['cookie']})

    if rp['user-agent'] != "":
        rp['headers'].update({'user-agent':rp['user-agent']})
    else:
        rp['headers'].update({'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'})
    return rp

def extract_user(line: str) -> str:
    """
    Extracts the user ID from a line.

    Args:
        line (str): A single line of user data.

    Returns:
        str: Extracted user ID.
    """
    if "c_user" in line and "i_user" not in line:
        return line.split("c_user=")[1].split(";")[0]
    elif "i_user" in line:
        return line.split("i_user=")[1].split(";")[0]
    else:
        _token =  line.split("|")
        for tn in _token:
            if tn.isdigit() and len(tn) > 5:
                return tn
    return ""

def update_user_data(rp: dict, token: str, line: str):
    """
    Updates the user data dictionary with information from the token.
    Args:
        rp (dict): The user data dictionary.
        token (str): The token to parse.
        line (str): The original line of user data.
    """
    if "NA" in token and ":" in token:
        rp["fb_dtsg"] = token
    if "c_user" in token or "i_user" in token:
        rp["cookie"] = token
    if any(agent in token for agent in ["Mozilla", "Chrome", "Safari", "AppleWebKit"]):
        rp["user-agent"] = token
    if len(token) > 150 and '=' not in token:
        rp['access_token'] = token
    if len(token.split(':')) in [2, 4] or 'http://' in token:
        rp['proxy'] = token
    if "c_user" not in token and 32 <= len(token) <= 40 and "@" not in token:
        rp['code'] = token
    if "@" in token:
        email = re.search(r'@(.*)\.', token)
        if email and utils.type_emailr(email.group(1)):
            rp['email'] = token
            password_email = utils.type_pw(value=line, valueid=token)
            if password_email:
                rp['passemail'] = password_email


def lauch_page(requests : requests.Session , fb_dtsg : str) -> str:
    url = 'https://www.facebook.com/api/graphql/?doc_id=&7693664663985026method=post&variables={"count":10,"cursor":"","scale":1}'
    while True:
        requests.post(url)
def tf_date():
    return datetime.now()
def get_auth_ads(requests: requests.Session):
    response = requests.get('https://adsmanager.facebook.com/adsmanager/?business_id=242940417587041&nav_source=flyout_menu&nav_id=2011891163')
    if response.status_code == 200:
        return response.text.split('accessToken="')[1].split('"')[0]
def auth_account(requests: requests.Session , auth : int):
    """
      requests : sessions requests (cookie , headers ...)
      Returns auth : 
        auth[1] : EAABs
        auth[2] : EAAAAU
        auth[3] : EAAAG
    """
    if auth == 1 :
        return get_auth_ads(requests)
def convert_headers(header_str: str) -> dict:
    """
    Converts a string of headers into a dictionary.

    Returns:
        dict: A dictionary of headers.
    """
    headers = {}
    headers , check , name = {} , 0 , ""
    if "\n" not in header_str:
        print("""
        Headers are not in the correct format.
              Example 1: 

                   Accept:
*/*
              Content-Type:
application/x-www-form-urlencoded
              

              Example 2 :

                   Accept:*/*,
                   Content-Type:application/x-www-form-urlencoded
              
""")
    header_str =  header_str.replace('\n','|').replace('"','`').replace('://','(^)').split('|')
    try:
        for temp in header_str:
            if temp[-1:] == ':':
                name = temp[:-1].replace('\n','').replace('`','"').replace('(^)','://')
                headers.update({name:""})
                check = 1
            if temp[-1:] != ':' and check:
                headers.update({name:temp.replace('\n','').replace('`','"').replace('(^)','://')})
                check = 0
    except Exception as error:
        print(error)
        return headers
    return headers

def convert_proxy(proxy_str: str) -> dict:
    """
    Converts a proxy string into a dictionary format.

    Returns:
        dict: A dictionary containing proxy information.
    """
    proxy_dict = {}
    try:
        if "@" in proxy_str:
            proxy_dict = {
                "https": f"http://{proxy_str}",
                "http": f"http://{proxy_str}"
            }
        else:
            ip, port, user, pass_proxy = proxy_str.split(":")
            proxy_dict = {
                "https": f"http://{user}:{pass_proxy}@{ip}:{port}",
                "http": f"http://{user}:{pass_proxy}@{ip}:{port}"
            }
    except ValueError:
        pass
    return proxy_dict

def cookie_confirm_auth_2fa(session: requests.Session, code: str, fb_dtsg: str) -> bool:
    """
    Requests confirmation for 2FA.

    Args:
        session (requests.Session): The Facebook session.
        code (str): The 8-digit code.
        fb_dtsg (str): The FB token.

    Returns:
        bool: True if confirmation is successful, otherwise False.
    """
    try:
        response = session.post(
            "https://business.facebook.com/security/twofactor/reauth/enter/",
            data={
                "approvals_code": code,
                "save_device": "true",
                "__a": "1",
                "fb_dtsg": fb_dtsg
            },
            timeout=60
        )
        return '"codeConfirmed":true' in response.text
    except requests.RequestException as e:
        print(f"Error confirming 2FA: {e}")
        return False

def check_facebook_account(fbid: str) -> bool:
    """
    Checks if a Facebook account is live or not.

    Args:
        fbid (str): The Facebook ID.

    Returns:
        bool: True if the account is live, otherwise False.
    """
    try:
        response = requests.get(f'https://graph.facebook.com/{fbid}/picture?redirect=0')
        data = response.json()
        url = data.get('data', {}).get('url', '')
        return len(url) >= 150
    except (requests.RequestException, KeyError) as e:
        print(f"Error checking Facebook account: {e}")
        return False
