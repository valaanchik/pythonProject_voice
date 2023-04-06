Библиотеки
pip install pyttsx3
pip install requests
pip install scikit-learn
pip install sounddevice
pip install vosk
pip install numpy
pip install pyaudio    ---- -_-


ДЛЯ РАСПОЗНАВАНИЯ РУССКОГО 
    Библиотека VOSK маленькая русская(vosk-model-small-ru-0.22): https://alphacephei.com/vosk/models
	
    model = vosk.Model() <- в конструктор передать полный путь к скачанной модели, если она находится не в рабочем каталоге


Для функций
    def offBot(): <--------------Даёшь имя
    '''Отключает бота''' <----------Что делает
    sys.exit() <-------------- Тело функции

    ДЛЯ ПРОВЕРКИ РАБОТЫ. В word.ru пишешь сценарий(имя функции в начале)


В ФАЙЛЕ "Browser_path.txt" ЗАМЕНИТЬ СОДЕРЖИМОЕ ПЕРВОЙ СТРОКИ НА ПОЛНЫЙ ПУТЬ ДО СВОЕГО БРАУЗЕРА

