import urwid
import random
import speech_recognition as sr
import time

ACCESS_TOKEN = '6W3RVPVZMJIK3JQ3VPC27D7ALF6HVNBI'

"""
Speech recognition proof of concept, utilizing the speech_recognition package
and wit.ai
"""


def callback(recognizer,audio):
    try:
        print("heard: {}".format(recognizer.recognize_wit(audio, ACCESS_TOKEN)))
    except sr.UnknownValueError:
        print('unknown value')
    except sr.RequestError as e:
        print("Could not request results from wit Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone( sample_rate=44100, chunk_size=8192)
with m as source:
    r.adjust_for_ambient_noise(source)


stop_listening = r.listen_in_background(m,callback)
print('say something')

for step in range(500):
    time.sleep(0.1)
stop_listening()






#response = r.recognize_wit(audio, ACCESS_TOKEN,show_all=True)

#print(response)





