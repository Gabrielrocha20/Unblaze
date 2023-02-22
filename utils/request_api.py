import json
from threading import Lock, Thread
from time import sleep

import requests

lock = Lock()

def daterework(date):
    hour = date.split('T')[1][:5]
    if (int(hour[:2]) == 0):
        minute = hour[3:5]
        hour = 21
    elif int(hour[:2]) == 1:
        minute = hour[3:5]
        hour = 22
    elif int(hour[:2]) == 2:
        minute = hour[3:5]
        hour = 23
    else:
        minute = hour[3:5]
        hour = int(hour[:2]) - 3

    ano, mes, dia = date.split('T')[0][2:4], date.split('T')[0][5:7], date.split('T')[0][8:10]
    create_at = f'{dia}/{mes}/{ano}'

    return [hour, minute, create_at]



def start_last_colors():
    from bot.models import Historico, Sequencia
    listaNumeros = [0, 11, 5, 10, 6, 9, 7, 8, 1, 14, 2, 13, 3, 12, 4]
    try:
        URL_LINK_BLAZE = 'https://blaze.com/api/roulette_games/recent'
        last_result = None
        last_sequence = None

        while True:
            information = requests.get(URL_LINK_BLAZE)

            if information.status_code == 200:
                results_colors = json.loads(information.text)

                if last_result == None:
                    last_result = results_colors[0]
                
                if last_sequence == None:
                    last_sequence = results_colors[:6]
     
                if results_colors[0]['id'] == last_result['id']:
                    pass
                else:
                    last_result = results_colors[0]
                    last_sequence = results_colors[:6]
                    hour, minute, create_at = daterework(last_result['created_at'])

                    historico = Historico.objects.filter(identificador=last_result['id'])
                    if not historico:
                        if last_result['color'] == 1:
                            last_result['color'] = 'red'
                        elif last_result['color'] == 2:
                            last_result['color'] = 'black'
                        else:
                            last_result['color'] = 'white'
                        Historico.objects.create(
                            create_at=create_at, 
                            hour=hour,
                            minute=minute,
                            color=last_result['color'],
                            numero=last_result['roll'],
                            identificador=last_result['id']
                        )
                    for i, check  in enumerate(last_sequence):
                        if last_sequence[i]['color'] == 1:
                            last_sequence[i]['color'] = 'red'
                        elif last_sequence[i]['color'] == 2:
                            last_sequence[i]['color'] = 'black'
                        elif last_sequence[i]['color'] == 0:
                            last_sequence[i]['color'] = 'white' 
                        
                    sequencia = Sequencia.objects.filter(
                        p1=last_sequence[5]['color'],
                        p2=last_sequence[4]['color'],
                        p3=last_sequence[3]['color'], 
                        p4=last_sequence[2]['color'], 
                        p5=last_sequence[1]['color'], 
                        result=last_sequence[0]['color']
                    )
                    
                    if not sequencia:
                        Sequencia.objects.create(
                        p1=last_sequence[5]['color'],
                        p2=last_sequence[4]['color'],
                        p3=last_sequence[3]['color'], 
                        p4=last_sequence[2]['color'], 
                        p5=last_sequence[1]['color'], 
                        result=last_sequence[0]['color']
                    )

            sleep(5)
    except requests.exceptions.ConnectionError:
        pass

def return_sequence():
    URL_LINK_BLAZE = 'https://blaze.com/api/roulette_games/recent'

    information = requests.get(URL_LINK_BLAZE)

    if information.status_code == 200:
        results_colors = json.loads(information.text)
        last_sequence = results_colors[:6]
        
        for i, check  in enumerate(last_sequence):
            if last_sequence[i]['color'] == 1:
                last_sequence[i]['color'] = 'red'
            elif last_sequence[i]['color'] == 2:
                last_sequence[i]['color'] = 'black'
            elif last_sequence[i]['color'] == 0:
                last_sequence[i]['color'] = 'white'
        
        last_20_results = []
        for index in range(20):
            last_20_results.append(int(results_colors[index]['roll']))

        return [last_sequence, last_20_results]


def start_thread():
    thread = Thread(target=start_last_colors)
    thread.daemon = True
    thread.start()


            

