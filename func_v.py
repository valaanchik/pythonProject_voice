import os
import sys
import pyttsx3
import time
import datetime
from random import randint


engine = pyttsx3.init()
engine.setProperty('rate', 180)


def speaker(text):
	'''Озвучка текста'''
	engine.say(text)
	engine.runAndWait()


def offBot():
    '''Отключает бота'''
    sys.exit()


def empty():
    '''Функция заглушка отсутствии команды'''
    pass


def passive():
    '''Функция заглушка при простом диалоге с ботом'''
    pass


def for_welcome():
    now = datetime.datetime.now()
    res = ''
    if now.hour >= 6 and now.hour < 12 : res = 'Доброе утро!'
    elif now.hour >= 12 and now.hour < 18: res = 'Добрый день!'
    elif now.hour >= 18 and now.hour < 23: res = 'Добрый вечер!'
    else: res = 'Доброй ночи!'
    return res


prev_song = None
def play_music():
    '''🎧 включение музыки 🎧'''
    global prev_song
    music_dir = 'music\\'
    if not os.path.isdir(music_dir):
        print('Указанный каталог отсутствует')
        return
    songs = os.listdir(music_dir)
    d = len(songs)
    num = randint(0, d-1)
    if prev_song == num:
        if num == d-1:
            num = 0
        else:
            num += 1
    prev_song = num
    os.startfile(os.path.join(music_dir, songs[num]))


prev_joke = None
def readJoke():
    '''🤡 Капи смешно веселит 🤡'''
    global prev_joke
    if not os.path.isfile('Superfunny_Jokes.txt'):
            print(f'Файл \"Superfunny_Jokes.txt\" отсутствует')
            return
    with open('Superfunny_Jokes.txt', 'r', encoding='utf-8') as f:
        count = f.readline().rstrip("\n")
        if str.isdigit(count) == False:
            return "АШИБКА В ФОРМИРОВАНИИ ФАЙЛА ШУТОК"
        d = int(count)
        num = randint(1, d)
        if prev_joke == num:
            if num == d:
                num = 1
            else:
                num += 1
        prev_joke = num
        line = None;
        for i in range(num):
            line = f.readline()
        return line


def getTime():
    '''⌚ Получение текущего системного времени ⌚'''

    decades = {

        2:'двадцать',
        3:'тридцать',
        4:'сорок',
        5:'пятьдесят',

    }

    s = time.strftime('%H %M').split(' ')

    #s = '01 51' # ТЕСТ, УБРАТЬ!!!
    #s = s.split(' ') # ТЕСТ, УБРАТЬ!!!

    h = int(s[0])
    m = int(s[1])

    res = s[0]

    if h < 10 or h > 19:
        if h % 10 == 1:
            res += ' час '
        elif h % 10 > 1 and h % 10 < 5:
            res += ' часа '
        else:
            res += ' часов '
    else:
        res += ' часов '
    

    whole = m // 10
    rem = m % 10

    if m > 9 and m < 20:
        res += s[1]
    elif m < 10 :
        if rem == 1:
            res += '0 одна'
        elif rem == 2:
            res += '0 две'
        else:
            res += s[1]
    else:
        if rem == 1:
            res += decades[whole]
            res += ' одна'
        elif rem == 2:
            res += decades[whole]
            res += ' две'
        else:
            res += s[1]

    if m < 10 or m > 19:
        if rem == 1:
            res += ' минута'
        elif rem > 1 and rem < 5:
            res += ' минуты'
        else:
            res += ' минут'
    else:
        res += ' минут'
            
    return res
   

def getDate():
    '''📆 Получение текущей системной даты 📆'''
    days = {

        '01':'первое',
        '02':'второе',
        '03':'третье',
        '04':'четвёртое',
        '05':'пятое',
        '06':'шестое',
        '07':'седьмое',
        '08':'восьмое',
        '09':'девятое',
        '10':'десятое',
        '11':'одиннадцатое',
        '12':'двенадцатое',
        '13':'тринадцатое',
        '14':'четырнадцатое',
        '15':'пятнадцатое',
        '16':'шестнадцатое',
        '17':'семнадцатое',
        '18':'восемнадцатое',
        '19':'девятнадцатое',
        '20':'двадцатое',
        '30':'тридцатое',

    }

    months = {

        '01':'января',
        '02':'февраля',
        '03':'марта',
        '04':'апреля',
        '05':'мая',
        '06':'июня',
        '07':'июля',
        '08':'августа',
        '09':'сентября',
        '10':'октября',
        '11':'ноября',
        '12':'декабря',

    }

    centuries = {

        '1':'сто',
        '2':'двести',
        '3':'триста',
        '4':'четыреста',
        '5':'пятьсот',
        '6':'шестьсот',
        '7':'семьсот',
        '8':'восемьсот',
        '9':'девятьсот',

    }

    decades = {

        '2':'двадцать',
        '3':'тридцать',
        '4':'сорок',
        '5':'пятьдесят',
        '6':'шестьдесят',
        '7':'семьдесят',
        '8':'восемьдесят',
        '9':'девяносто',

    }

    years = {

        '01':'первого',
        '02':'второго',
        '03':'третьего',
        '04':'четвёртого',
        '05':'пятого',
        '06':'шестого',
        '07':'седьмого',
        '08':'восьмого',
        '09':'девятого',
        '10':'десятого',
        '11':'одиннадцатого',
        '12':'двенадцатого',
        '13':'тринадцатого',
        '14':'четырнадцатого',
        '15':'пятнадцатого',
        '16':'шестнадцатого',
        '17':'семнадцатого',
        '18':'восемнадцатого',
        '19':'девятнадцатого',
        '20':'двадцатого',
        '30':'тридцатого',
        '40':'сорокового',
        '50':'пятидесятого',
        '60':'шестидесятого',
        '70':'семидесятого',
        '80':'восьмидесятого',
        '90':'девяностого',
        '100':'сотого',
        '200':'двухсотого',
        '300':'трехсотого',
        '400':'четырёхсотого',
        '500':'пятисотого',
        '600':'шестисотого',
        '700':'семисотого',
        '800':'восьмисотого',
        '900':'девятисотого',
        '2000':'двухтысячного',
    }

    d = ''
    m = ''
    y = ''

    s = time.strftime('%d %m %Y')
    s = s.split(' ')

    #s = '01 01 2019' # ТЕСТ, УБРАТЬ!!!
    #s = s.split(' ') # ТЕСТ, УБРАТЬ!!!

    if int(s[0]) < 20 or int(s[0][1]) == 0:
        d = days[s[0]]
    elif int(s[0][0]) == 2:
        d = 'двадцать ' + days['0'+s[0][1]]
    else: # elif int(s[0][0]) == 3:
        d = 'тридцать ' + days['0'+s[0][1]]
    
    d += ' '

    m = months[s[1]]
    m += ' '


    if s[2][3] == '0':
        if s[2][2] == '0':
            if s[2][1] == '0':
                y = years[s[2]]
            else:
                if s[2][0] == '1':
                    y = 'одна тысяча '
                else:
                    y = 'две тысячи '
                y += years[s[2][1:]]
        else:
            if s[2][0] == '1':
                y = 'одна тысяча '
            else:
                y = 'две тысячи '
            y += centuries[s[2][1]]
            y += ' '
            y += years[s[2][2:]]
    else:
        if s[2][0] == '1':
            y = 'одна тысяча '
        else:
            y = 'две тысячи '

        if s[2][1] != '0':
            y += centuries[s[2][1]]
            y += ' '

        if s[2][2] != '0' and s[2][2] != '1':
            y += decades[s[2][2]]
            y += ' '

        if s[2][2] == '1':
            y += years[s[2][2:]]
        else:
            y += years['0'+s[2][3]]
    
    y += ' года'

    return d + m + y
