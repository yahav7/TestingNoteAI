import os
import pygame
import time
from gtts import gTTS
import openai
import speech_recognition as sr
import pyautogui
import pytesseract
from PIL import Image

api_key = ""

lang = 'en'
openai.api_key = api_key

guy = ""
microphone = sr.Microphone(device_index=1)


def play_audio(text):
    speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
    speech.save("output.mp3")

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the audio file
    pygame.mixer.music.load("output.mp3")

    # Play the audio
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)


def get_audio():
    r = sr.Recognizer()
    while True:
        with microphone as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                global guy
                guy = said

                if "suck" in said:
                    play_audio("I am sorry you are frustrated")
                elif "Friday" in said:
                    new_string = said.replace("Friday", "")
                    print(new_string)

                    # Complete the sentence using OpenAI
                    completion = openai.Completion.create(model="gpt-3.5-turbo", prompts=new_string)
                    text = completion.choices[0].text
                    play_audio(text)
                    continue
            except Exception as e:
                print("Exception:", str(e))
                continue

get_audio()
