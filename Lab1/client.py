import requests
while(True):
    print('_' * 35)
    print("[1] POST-request \n[2] GET-request \n[3] Exit")
    c = int(input("Your choice: "))
    if c==3:
        exit()
    elif c==1:
        data = input("==> Message: ")
        response_post = requests.post('http://127.0.0.1:5000/data', data=data)
        print('* ' * 7)
        print('POST response: ', response_post.text, '\n')
    elif c==2:
        # Відправка GET запиту
        response_get = requests.get('http://127.0.0.1:5000/data')
        print('* ' * 7)
        print('GET response: ', response_get.json(), '\n')
    else:
        print("Retry", '\n')