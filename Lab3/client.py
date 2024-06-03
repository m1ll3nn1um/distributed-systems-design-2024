import requests

while(True):
    print("[1] POST-request \n[2] GET-request \n[3] Exit")
    choose=int(input("Your choice: "))
    if choose==3:
        exit()
    elif choose==1:
        data = input("==> Message: ")
        response_post = requests.post('http://127.0.0.1:5000/data', data=data)
        print('*** POST response: ', response_post.text)
    elif choose==2:
        # Відправка GET запиту
        response_get = requests.get('http://127.0.0.1:5000/data')
        print('*** GET response: ', response_get.json())
    else:
        print("Retry")
    print('-' * 30)