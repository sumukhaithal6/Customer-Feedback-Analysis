from urllib.request import urlopen

def print_text_in_read(text):
    CRED = '\033[91m'
    CEND = '\033[0m'
    print(CRED + text + CEND)

def check_link_health(link):
    if not link:
        return True
    try:
        response = urlopen(link)
        return True
    except :
        return False
