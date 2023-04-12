from ast import While
from re import sub
import sounddevice as sd
import vosk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from func_v import *
import word

import json
import queue
import os
import webbrowser
from threading import *

q = queue.Queue()

model = vosk.Model('vosk_model_small')
device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])

vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform(list(word.data_set.keys()))
clf = LogisticRegression()
clf.fit(vectors, list(word.data_set.values()))

voenmeh_vectorizer = CountVectorizer()
vectors = voenmeh_vectorizer.fit_transform(list(word.voenmeh_sections.keys()))
voenmeh_clf = LogisticRegression()
voenmeh_clf.fit(vectors, list(word.voenmeh_sections.values()))

guessing_vectorizer = CountVectorizer()
vectors = guessing_vectorizer.fit_transform(list(word.guessing_game.keys()))
guessing_clf = LogisticRegression()
guessing_clf.fit(vectors, list(word.guessing_game.values()))


browser_path = None

def register_browser_path():
    if not os.path.isfile('Browser_path.txt'):
        print('Файл \"Browser_path.txt\" отсутствует')
        return
    global browser_path
    with open('Browser_path.txt', 'r', encoding='utf-8') as f:
        path = f.readline().rstrip("\n")
        if os.path.isfile(path):
            browser_path = path
            webbrowser.register('browser', None, webbrowser.BackgroundBrowser(browser_path))


def check_key(data, keys_tuple):
    if data in keys_tuple:
        return True
    else:
        return False


def sub_recognize(rec, vec, clf, keys_tuple):
    b = None 
    while Visual.isRunned:
        data = q.get()
        if rec.AcceptWaveform(data) and not SubThread.isSayProcessing:
            data = json.loads(rec.Result())['text']
            if check_key(data, keys_tuple):
                data = recognize(data, vec, clf, True)
                return data
            elif data != '':
                speaker('Ничё не понятно')
      
            

def voice_request(rec) :
    data = ''
    #if not cont:
    while Visual.isRunned and (data == '' or SubThread.isSayProcessing):
        buf = q.get()
        if rec.AcceptWaveform(buf):
            data = json.loads(rec.Result())['text']
    #else :
    #    if isinstance(cont, dict):
    #        while Visual.isRunned and (not data in cont or SubThread.isSayProcessing):
    #            buf = q.get()
    #            if rec.AcceptWaveform(buf):
    #                data = json.loads(rec.Result())['text']
    #                print(data)
    #        if not Visual.isRunned:
    #            return ''
    #        data = cont[data]

        #elif isinstance(cont, list):
        #    while Visual.isRunned and (not data in cont or SubThread.isSayProcessing):
        #        buf = q.get()
        #        if rec.AcceptWaveform(buf):
        #            data = json.loads(rec.Result())['text']
        #    if not Visual.isRunned:
        #        return ''
        #    data = cont[data]
    return data



def callback(indata, frames, time, status):
    q.put(bytes(indata))


def recognize(data, vectorizer, clf, flag=False):

    if flag:
        text_vector = vectorizer.transform([data]).toarray()[0]
        answer = clf.predict([text_vector])[0]
        return answer

    trg = word.TRIGGERS.intersection(data.split())
    if not trg:
        return 0

    data.replace(list(trg)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    #print(answer) // при распозновании консоль иногда виснет, и надо на неё тыкать, чтоб Капи продолжил разговаривать

    buf = answer.split(' ', 1)
    func_name = buf[0]
    phrase = buf[1]

    if phrase == 'военмех':
        return 1
    elif phrase == 'яндекс':
        return 2
    elif phrase == 'ютуб':
        return 3
    elif phrase == 'игра':
        return 4
    elif phrase == 'XD':
        SubThread.speaker_start(readJoke())
    elif phrase == 'время':
        SubThread.speaker_start(getTime())
    elif phrase == 'дата':
        SubThread.speaker_start(getDate())
    else:
        SubThread.speaker_start(phrase) # answer.replace(func_name, '')
        if func_name == 'offBot':
            Visual.Closing = True
        while SubThread.isSayProcessing: Visual.window.update()  
        if func_name == 'offBot':
            Visual.window.destroy()
        #while SubThread.isSayProcessing : continue
        #if func_name[-1] != ')':
        #    exec(func_name + '()')
        #else:
        exec(func_name + '()')
    return 0


def start():
    #del word.data_set
    #SubThread.speaker_start('Я слушаю')
    SubThread.speaker_start(for_welcome())

    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                            channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)

        while True:
            if not Visual.isRunned:
                SubThread.speaker_start("урА канИкулы")
                break

            data = q.get()
            if rec.AcceptWaveform(data):
                data =  json.loads(rec.Result())['text']
                #print(data) #для проверки распознавания
                #if not check_key(data, tuple(word.data_set)) and data != '':
                #    SubThread.speaker_start('Ничё не понятно')
                #    while SubThread.isSayProcessing:
                #        if not Visual.isRunned:
                #            SubThread.speaker_start("урА канИкулы")
                #            return
                #        continue
                #    continue

                result = recognize(data, vectorizer, clf)

                if result != 0:
                    if result == 1:
                        SubThread.speaker_start('какой раздел?')
                        data = sub_recognize(rec, voenmeh_vectorizer, voenmeh_clf, tuple(word.voenmeh_sections))
                        if not Visual.isRunned:
                            SubThread.speaker_start("урА канИкулы")
                            return
                        if data != '!':  
                            domen = 'www.'
                            message = 'Военмех лучше всех!!!'
                            if data == '/login/index.php':
                                domen = 'moodle.'
                                message = 'иди решай тесты'
                            elif data == '/mail/':
                                domen = 'mail.'
                                message = 'сейчас посмотрим что новенького'

                            SubThread.speaker_start(message)
                            webbrowser.get('browser').open_new_tab('https://' + domen + 'voenmeh.ru' + data)
                        else:
                            SubThread.speaker_start('Ладно')

                    elif result == 4:
                        num = randint(1, 5)
                        SubThread.speaker_start('вероятность успеха 20 процентов')
                        data = sub_recognize(rec, guessing_vectorizer, guessing_clf, tuple(word.guessing_game))
                        #print('Загаданное: ' + str(num))
                        #print('Распознанное: ' + str(data))
                        if not Visual.isRunned:
                            SubThread.speaker_start("урА канИкулы")
                            return
                        if data == -1:
                            SubThread.speaker_start('Ладно')
                        elif num == data:
                            SubThread.speaker_start('Да ты чемпион!')
                        else:
                            SubThread.speaker_start('Было загадано ' + str(num) + '. В следующий раз повезёт')
                    else:
                        SubThread.speaker_start('говорите')
                        data = voice_request(rec)
                        if not Visual.isRunned:
                            SubThread.speaker_start("урА канИкулы")
                            return
                        if result == 2:
                            webbrowser.get('browser').open_new_tab('https://yandex.ru/search/?text=' + data) 
                        elif result == 3:
                            webbrowser.get('browser').open_new_tab('https://www.youtube.com/results?search_query=' + data)
                           
            #Visual.window.update()


def read_file(path):
    if not (Visual.isRunned or SubThread.isRecognizeProcessing or SubThread.isSayProcessing) :
        if not os.path.isfile(path):
            print(f'Файл \"{path}\" отсутствует')
            return
        with open(path, 'r', encoding='utf-8') as f:
            a = f.readlines()
            l = len(a)
            i = 0
            SubThread.isSayProcessing = True
            while i < l:
                speaker(a[i])
                i+=1
            SubThread.isSayProcessing = False
                

class SubThread :

    isSayProcessing = False
    isRecognizeProcessing = False
    isReadingFile = False

    @staticmethod 
    def schedule_check(t, flag):
        Visual.window.after(1000, SubThread.check_if_done, t, flag)


    @staticmethod 
    def check_if_done(t, flag):
        if not t.is_alive():
            if flag == 0:
                SubThread.isSayProcessing = False
            elif flag == 1 :
                SubThread.isRecognizeProcessing = False
            elif flag == 2 :
                SubThread.isReadingFile = False
        else:
            SubThread.schedule_check(t, flag)

    @staticmethod 
    def speaker_start(text):
        if not SubThread.isSayProcessing:
            SubThread.isSayProcessing = True
            t = Thread(target=speaker, args=(text,), daemon=True)
            t.start()
            SubThread.schedule_check(t, 0)


    @staticmethod 
    def recognize_start():
        if not SubThread.isReadingFile:
            SubThread.isRecognizeProcessing = True
            t = Thread(target=start, daemon=True)
            t.start()
            SubThread.schedule_check(t, 1)


    @staticmethod 
    def read_file_start(path):
        if not SubThread.isReadingFile:
            SubThread.isReadingFile = True
            t = Thread(target=read_file, args=(path,), daemon=True)
            t.start()
            SubThread.schedule_check(t, 2)

    


from settings import *
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
#from pil import Image, ImageTk


class Visual:
    window = None
    main_frame = None
    centre_frame = None
    
    centre_button = None
    centre_button_border = None

    side_frame = None
    commands_text_frame = None
    commands_buttons_frame = None
    button_back = None
    button_commands_speech = None

    name_label = None
    commands_text = None

    buttons_frame = None
    button_commands = None
    button_help = None
    button_exit = None
    
    isCommandsActive = False
    isRunned = False
    Closing = False

    @staticmethod
    def Init() :
        Visual.window = Tk()
        w = SCREEN_WIDTH
        h = SCREEN_HEIGHT
        x = (Visual.window.winfo_screenwidth() - SCREEN_WIDTH) // 2
        y = (Visual.window.winfo_screenheight() - SCREEN_HEIGHT) // 2
        Visual.window.geometry(f"{w}x{h}+{x}+{y}")
        Visual.window.resizable(width=False, height=False)

        #Visual.window.call('wm', 'iconphoto', Visual.window._w, PhotoImage(file='/path/to/ico/icon.png')
        Visual.window.iconphoto(False, PhotoImage(file='Kapi.png'))
        Visual.window.title('Капи')

        Visual.main_frame = Frame(Visual.window, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg = FRAMES_BG)

        Visual.centre_frame = LabelFrame(Visual.main_frame, width=CENTRE_FRAME_WIDTH, height=CENTRE_FRAME_HEIGHT, bg = FRAMES_BG)
 
        Visual.side_frame = Frame(Visual.main_frame, 
                                      width=SCREEN_WIDTH-CENTRE_FRAME_WIDTH, 
                                      height=SCREEN_HEIGHT, bg = FRAMES_BG)

        Visual.buttons_frame = Frame(Visual.side_frame, 
                                      width=SCREEN_WIDTH-CENTRE_FRAME_WIDTH, 
                                      height=BUTTON_Y*3 + BUTTON_PADY*6, bg = FRAMES_BG) #height=BUTTON_Y*2 + BUTTON_PADY*4

        Visual.commands_buttons_frame = Frame(Visual.side_frame, 
                                      width=SCREEN_WIDTH-CENTRE_FRAME_WIDTH, 
                                      height=BUTTON_Y, bg = FRAMES_BG)

        Visual.commands_text_frame = Frame(Visual.side_frame, 
                                      width=SCREEN_WIDTH-CENTRE_FRAME_WIDTH, 
                                      height=SCREEN_WIDTH-BUTTON_Y, bg = FRAMES_BG)

        Visual.main_frame.pack()
       
        Visual.centre_frame.pack(side=LEFT)
        Visual.side_frame.pack(side=LEFT)

        Visual.centre_frame.pack_propagate(False)
        Visual.side_frame.pack_propagate(False)

        Visual.buttons_frame.pack(expand=1)
        Visual.buttons_frame.pack_propagate(False)

        #img = Image.open("sound.png")
        #photo = ImageTk.PhotoImage(img)
        photo = PhotoImage(file="sound.png")
        Visual.button_back = Button(Visual.commands_buttons_frame, font=('Courier', 12, 'bold'), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text= "НАЗАД", bg=BUTTONS_BG,  fg=BUTTONS_FG, activebackground=BUTTONS_BG, activeforeground=BUTTONS_FG, command=Visual.click_comands_button)
        Visual.button_commands_speech = Button(Visual.commands_buttons_frame, width=50, height=44, bg=BUTTONS_BG, image=photo, compound=CENTER, activebackground=BUTTONS_BG, command=Visual.click_button_commands_speech)
        Visual.button_commands_speech.image = photo


        Visual.button_commands = Button(Visual.buttons_frame, font=('Courier', 12, 'bold'), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text= "СПИСОК КОМАНД", bg=BUTTONS_BG,  fg=BUTTONS_FG, activebackground=BUTTONS_BG, activeforeground=BUTTONS_FG, command=Visual.click_comands_button) #'steel blue' 'light gray'
        Visual.button_help = Button(Visual.buttons_frame, font=('Courier', 12, 'bold'), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text= "ПОМОЩЬ", bg=BUTTONS_BG,  fg=BUTTONS_FG, activebackground=BUTTONS_BG, activeforeground=BUTTONS_FG, command=Visual.click_help_button)
        Visual.button_exit = Button(Visual.buttons_frame, font=('Courier', 12, 'bold'), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text= "ОТКЛЮЧЕНИЕ", bg=BUTTONS_BG,  fg=BUTTONS_FG, activebackground=BUTTONS_BG, activeforeground=BUTTONS_FG, command=Visual.on_close)

        Visual.button_commands.pack(pady=BUTTON_PADY) #pady=20
        Visual.button_help.pack(pady=BUTTON_PADY)
        Visual.button_exit.pack(pady=BUTTON_PADY)
        
        Visual.commands_text = ScrolledText(Visual.commands_text_frame, font=('Courier', 10, 'bold'), height = SCREEN_HEIGHT-BUTTON_Y,
                                        width=(SCREEN_WIDTH-CENTRE_FRAME_WIDTH) // 2, fg=SCROLLED_TEXT_FG, bg=SCROLLED_TEXT_BG)
        

        long_text = "Обращение:\nКапи\n\n" + "Фразы для разговора:\n- хочу спать\n" + "- не могу заснуть\n- как дела?\n- что делать?\n\n"
        long_text += "Команды:\n- отключись\n- скажи привет на\nанглийском\n- развесели\n- включи музыку\n- скажи время\n- скажи дату\n- запрос яндекс\n- запрос ютуб\n- загадай число\n- Военмех\n\n"
        long_text += "Разделы команды\n\"Военмех\":\n- главная\n- карта\n- факультеты и кафедры\n- расписание\n- контакты\n- moodle\n- почта\n\n"
        long_text += "Пояснение команды\n\"загадай число\":\nЭто мини игра.\nКапи загадывает число от 1 до 5.\nВаша задача угадать:)\n\n"
        long_text += "Примечание для команд\n\"Военмех\" и\n\"загадай число\":\nЕсли вы хотите перейти\nобратно к главному меню\nкоманд, ничего не\nвыбирая в этих разделах,\nвоспользуйтесь командой\n\"назад\"."

        Visual.commands_text.insert(END, long_text)
        Visual.commands_text.configure(state='disabled')


        Visual.name_label = Label(Visual.centre_frame, font=('Courier', 16, 'bold'), text = "ГОЛОСОВОЙ ПОМОЩНИК \"КАПИ\"", fg=BUTTONS_FG, bg=FRAMES_BG) #"Голосовой помощник Капи"
        Visual.name_label.pack()

        Visual.centre_button_border = LabelFrame(Visual.centre_frame, 
                                      width=IMAGE_WIDTH + IMAGE_BORDER, 
                                      height=IMAGE_HEIGHT + IMAGE_BORDER, bg = CENTRE_BUTTON_BORDER_DISABLE)
        Visual.centre_button_border.pack()
        Visual.centre_button_border.pack_propagate(False)
       
        #img = Image.open("Kapi.png")
        #photo = ImageTk.PhotoImage(img)
        photo = PhotoImage(file="Kapi.png")
        Visual.centre_button = Button(Visual.centre_button_border, width=IMAGE_WIDTH, height=IMAGE_HEIGHT, bg=BUTTONS_BG,
                                   image=photo, compound=CENTER, activebackground=BUTTONS_BG,
                                   highlightthickness=1, highlightbackground=BUTTONS_BG, command=Visual.click_centre_button)
        Visual.centre_button.image = photo
        Visual.centre_button.pack(expand=1)
       
        Visual.window.protocol('WM_DELETE_WINDOW', Visual.on_close)
        
       

    
    @staticmethod 
    def on_close():
        if not Visual.Closing:
            if messagebox.askokcancel('Выход', 'Действительно хотите закрыть окно?'):
                Visual.isRunned = False
                Visual.window.destroy()
                offBot()


    @staticmethod 
    def click_centre_button():
        if not SubThread.isSayProcessing:
            if not Visual.isRunned:
                Visual.centre_button_border.config(bg = CENTRE_BUTTON_BORDER_ENABLE)
                Visual.isRunned = True
                #Visual.window.update()
                #start()
                SubThread.recognize_start()
            else :
                Visual.centre_button_border.config(bg = CENTRE_BUTTON_BORDER_DISABLE)
                Visual.isRunned = False
        

    @staticmethod
    def click_comands_button():
        if not Visual.isCommandsActive:
            Visual.button_commands.pack_forget()
            Visual.button_help.pack_forget()
            Visual.button_exit.pack_forget()
            Visual.buttons_frame.pack_forget()

            Visual.commands_buttons_frame.pack()
            Visual.commands_text_frame.pack()
            Visual.commands_buttons_frame.pack_propagate(False)
            Visual.commands_text_frame.pack_propagate(False)

            Visual.button_back.pack(side=LEFT) #, padx=53
            Visual.button_commands_speech.pack(side=LEFT)
            Visual.commands_text.pack(side=LEFT)
        else:
            Visual.button_back.pack_forget()
            Visual.button_commands_speech.pack_forget()
            Visual.commands_text.pack_forget()

            Visual.commands_buttons_frame.pack_forget()
            Visual.commands_text_frame.pack_forget()

            Visual.buttons_frame.pack(expand=1)
            Visual.buttons_frame.pack_propagate(False)
            Visual.button_commands.pack(pady=BUTTON_PADY) #pady=20
            Visual.button_help.pack(pady=BUTTON_PADY)
            Visual.button_exit.pack(pady=BUTTON_PADY)

        Visual.isCommandsActive = not Visual.isCommandsActive

    @staticmethod
    def click_help_button():
        SubThread.read_file_start('Help.txt')

    @staticmethod
    def click_button_commands_speech():
        SubThread.read_file_start('Comands.txt')


def main():
    global browser_path
    register_browser_path()
    if browser_path == None:
        print('Путь к браузеру указан неверно')
        return
    Visual.Init()
    SubThread.speaker_start('Голосовой помощник Капи запущен')
    Visual.window.mainloop()


if __name__ == '__main__':
    main()