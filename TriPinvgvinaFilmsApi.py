import requests
import re
import json
from pprint import pprint

def get_tPin_films_api():
    #Скачиваем html с сайта кинотеатра "Три Пингвина"
    url = 'https://madagascarkino.ru/ticket/cheb/schedule/get?'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    html = requests.get(url, headers=headers)

    #Режем отдельные строчки с информацией по каждому сеансу
    info_list = html.text.split('show-wrapper')
    #Первый элемент сразу отбрасываем
    del info_list[0]

    #Создаем словарь, где будет храниться вся информация о каждом сеансе
    json_data = {'ANS' : []}
    f = 0  #Для итераций tickets
    z = 0  #для нахождения информации в каждом кусе кода сеанса
    for list in info_list:
        f1 = 0
        #Вырезаем название фильмов
        i = list.find('фильма">')
        j = list.find('</a>')
        name = list[i+8:j]
        list = list[j:-1]

        #Добавление жанр к названию
        i = list.find('</span>')
        j = list.find('<span')
        name = name + ' (' + list[i+8:j-2] + ')'
        list = list[j:-1]
        json_data['ANS'].append({'name': name, 'tickets': []})

        #Перечесляем все сеансы к определенному фильму
        j = list.find('3D</div>')   #Находим, где начинаются сеансы в 3D
        if j == -1:
            j = len(list)
        for m in re.finditer('booking-wrapper', list):
            i = m.start()
            if j > i:    #Добавляем title
                title = '2D'
            else:
                title = '3D'

            time = list[i+150:i+200]
            z = time.find('time">')
            time = time[z+6:z+11]

            price = list[i+340:i+370]
            z = price.find('&#8381')
            price = price[z-4:z-1]

            hall = list[i+520:i+600]
            z = list.find('>Зал')
            hall = list[z+5]

            id = list[i+980:i+1030]
            z = id.find('?performance=')
            id = id[z+13:z+18]

            json_data['ANS'][f]['tickets'].append({'title': title, 'time': time, 'price': price, 'hall': hall, 'id': id })
            f1 = f1 + 1


        f = f + 1
    return json_data
    #with open("TriPingvina.json", "w") as f:
     #   f.write(json.dumps(json_data, ensure_ascii=False ))
