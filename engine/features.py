import datetime
from pipes import quote
import struct
import subprocess
import time
from unittest import result
from numpy import mat
from playsound import playsound
import os
import eel
import pyaudio
import pyautogui
from engine.config import ASSISTANT_NAME
from engine.command import speak, speakText, takecommand
import pywhatkit as kit
import re
import sqlite3
import webbrowser
import pvporcupine
import wikipedia
import wolframalpha
from googletrans import Translator
from hugchat import hugchat



conn=sqlite3.connect("TalkWeve.db")
cursor=conn.cursor()


@eel.expose
def playAssistantSound():
    mus_dir = 'C:\\Users\\user\\OneDrive\\Desktop\\Project2\\www\\assets\\audio\\start_sound.mp3'

    playsound(mus_dir)

# playAssistantSound()

def openCommand(query):
    
    ASSISTANT_NAME="talk weve"
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.replace(" ","")
    query.lower()
    print(query)

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    print("started 1")
    
    query=extract_yt_term(query)

    speak(f"Playing {query} on YouTube")
    kit.playonyt(query)

def searchGoogle(query):
    try:
        query = query.replace("search","")
        query = query.replace("on","")
        query = query.replace("Google","")
        query = query.replace("google","")

        # it will perform the Google search
        
        kit.search(query)
        print(query)
        print("Searching...",query)
    
    except:
    
        # Printing Error Message
        print("An unknown error occurred")


def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None


def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string


def search(query):
    try:

        # try is searching with wolframAlpha
        #it can tell wa
        try:

            app_id = "8KQA5J-6YVAQXTXKR"
            client = wolframalpha.Client(app_id)
            query = query.split(' ')
            query = " ".join(query[0:])

            res = client.query(query)
            answer = next(res.results).text
            print("Your answer is " + answer)
            eel.receiverText(answer)

            speak(answer)

            print("\nFound from wolframalpha")

        # if cant fi"nd in wolframAlpha then find in wikipedia
        except:
              speak("No matching found")

            
    except:
        speak("Something Went wrong")

def onwikipedia(query):
    try:

        query = query.split(' ')
        query = " ".join(query[0:])

        print(wikipedia.summary(query, sentences=3))
        speak(f"according to wikipedia, {wikipedia.summary(query, sentences=3)}")
        eel.receiverText(wikipedia.summary(query, sentences=3))


    except:
        speak("No matching found")

eel.expose
def greed():

    time=int(datetime.datetime.now().hour)

    if time>=0 and time<12:
        speakText("Good Morning!")

    elif time>=12 and time<18:
        speakText("Good Afternoon!")

    else:
        speakText("Good Evening!")

    speakText("loading your virtual assistant")
    speakText("I am here to help you")

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = message
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

def translaor(query):
    
    translator = Translator()
    translation = translator.translate(query, dest='hi')
    return translation.text

def chatBot(query):
    try:
        try:

            cursor.execute("SELECT ans FROM chatboot WHERE LOWER(question) LIKE ?",(query))
            results = cursor.fetchall()
            speak(results)
            print("working")

        except:
            user_input = query.lower()
            chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
            id = chatbot.new_conversation()
            chatbot.change_conversation(id)
            response =  chatbot.chat(user_input)
            # cursor.execute('INSERT INTO chatboot(question,ans) VALUES (?,?)',(user_input,response))
            # conn.commit()
            print(response)
            speak(response)
        

        return response
    except:
        search(query)
@eel.expose
def exitCode():
    exit()
