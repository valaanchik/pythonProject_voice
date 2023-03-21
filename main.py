import sounddevice as sd
import vosk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from func_v import *
import json
import queue
import word

q = queue.Queue()

model = vosk.Model('vosk_model_small')
device = sd.default.device

samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])


def callback(indata, frames, time, status):

    q.put(bytes(indata))

def recognize(data, vectorizer, clf):
    trg = word.TRIGGERS.intersection(data.split())
    if not trg:
        return

    data.replace(list(trg)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    print(answer)


    func_name = answer.split()[0]


    speaker(answer.replace(func_name, ''))

    
    exec(func_name + '()')





def main():


    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(word.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(word.data_set.values()))

    del word.data_set

    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                           channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data =  json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)



if __name__ == '__main__':
    main()