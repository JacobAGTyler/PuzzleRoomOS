import requests

run_listener = True

webserver = 'http://192.168.1.11:5001'

while run_listener:
    try:
        response = requests.get(f'{webserver}/ping')
        print(response.text)
    except requests.exceptions.ConnectionError:
        run_listener = False
        print('Webserver is down')
        break
