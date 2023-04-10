import sys
import pyttsx3
import webbrowser
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


def passive():
    '''Функция заглушка при простом диалоге с ботом'''
    pass

listweb = ['https://mail.voenmeh.ru/mail/','https://moodle.voenmeh.ru/login/index.php','https://ya.ru/']
def browser(a):
	'''Открывает браузер'''
	webbrowser.open(listweb[a] , new=2)


prev = None

def readJoke():
    '''🤡 Капи смешно веселит 🤡'''
    global prev
    with open('Superfunny_Jokes.txt', 'r', encoding='utf-8') as f:
        count = f.readline().rstrip("\n")
        if str.isdigit(count) == False:
            return "АШИБКА В ФОРМИРОВАНИИ ФАЙЛА ШУТОК"
        num = randint(1, int(count))
        if prev == num:
            if num == int(count):
                num = 1
            else:
                num += 1
        prev = num
        line = None;
        for i in range(num):
            line = f.readline()
        return line


#def readFile(path):
#    with open(path, 'r') as f:
#        for line in f:
#            speaker(line.strip())