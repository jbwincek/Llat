import urwid
import random
import speech_recognition as sr

ACCESS_TOKEN = '6W3RVPVZMJIK3JQ3VPC27D7ALF6HVNBI'

"""
Speech recognition proof of concept, utilizing the speech_recognition package
and wit.ai
"""

r = sr.Recognizer()
with sr.Microphone() as source:
    print('say something')
    audio = r.listen(source)

response = r.recognize_wit(audio, ACCESS_TOKEN,show_all=True)

print(response)





