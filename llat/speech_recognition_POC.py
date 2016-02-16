import urwid
import random
import speech_recognition as sr
from wit import Wit

ACCESS_TOKEN = '6W3RVPVZMJIK3JQ3VPC27D7ALF6HVNBI'

"""
Speech recognition proof of concept, utilizing the speech_recognition package
and wit.ai  
"""

w = Wit(ACCESS_TOKEN)
r = sr.Recognizer()
with sr.Microphone() as source:
    print('say something')
    audio = r.listen(source)

response = w.post_speech(audio.get_wav_data())

print(response)





