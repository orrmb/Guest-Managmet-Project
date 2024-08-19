import random
import requests

for i in range(10):

        relationship = random.choice(["משפחה רחוקה", "משפחה קרובה", "חברים"])
        side = random.choice(["חתן", "כלה"])
        number = random.randint(1, 5)
        names = random.choice(['Or Bohadana', 'Jason Sweet', 'Raz Bohadana', 'Jhon Lenon', 'Test Work'])

        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {
                "name": names,
                "phone": '0522449797',
                "number": number,
                "side": side,
                "relationship": relationship}

        response = requests.post('http://127.0.0.1:5000/submit', headers=headers, data=data)
        print(response)




