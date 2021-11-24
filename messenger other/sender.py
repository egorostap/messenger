import requests
#r = requests.get('https://www.google.com/')
#r = requests.get('http://127.0.0.1:5000/status')

name = input('Введите имя: ')

while True:
    text = input()
    r = requests.post(
        'http://127.0.0.1:5000/send',
        json={'text': text, 'name': name}
                      )
