# *************************** Programing: Ali Ayed ***************************
from requests import get

def online():
    try:
        get('https://www.google.com')
    except:
        return False
    else:
        return True
