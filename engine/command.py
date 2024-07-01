# This file performs operetions affter taking command

import imp
import os
import pyttsx3
import speech_recognition as sr
import eel


#This function convert voice command in string as well as shows massages in forntend
def speak(text):
    # Initialize the engine
    text=str(text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

#This function only converst voice command in string
def speakText(text):
    # Initialize the engine
    text=str(text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


#This function actives microphone and takes voice command
def takecommand():
    try:
        r=sr.Recognizer() 
        with sr.Microphone() as source:
            print("listening...")
            eel.DisplayMessage("listening...")
            r.adjust_for_ambient_noise(source,1)
            r.pause_threshold=1
            r.energy_threshold=1000
            audio=r.listen(source)
            try:
                print("Recognizing...")
                eel.DisplayMessage("Recognizing...")
                speech=r.recognize_google(audio,language="en-in")
                print("you said")
                eel.DisplayMessage(speech)
                
            except Exception as e:
                print("Google recognizer can't recognize")
                speak("Google recognizer can't recognize")
                eel.DisplayMessage("Google recognizer can't recognize")
                eel.ShowHood()
                return ""
            return speech
    except:
        speak("Try Again")
        eel.ShowHood()

#@eel.expose Helps to active this function in 
@eel.expose
def allCommand(message=1):


    if message == 1:
        query = takecommand()
        eel.senderText(query)
        print(query)
      
    else:
        query = message
        eel.senderText(message)
      
    try:
       
        query.lower()
        print(query)
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "exit" in query:
            exit()

        elif "on YouTube" in query or "on youtube" in query:
            from engine.features import PlayYoutube
            print("working on it")
            PlayYoutube(query)
            print("working on it")

        elif 'wikipedia' in query or "who is" in query:
            from engine.features import onwikipedia
            onwikipedia(query)
            
        elif "send message" in query or "phone call" in query or "video call" in query:
          
            from engine.features import findContact, whatsApp
            flag = ''
            contact_no, name = findContact(query)
            print(contact_no,name)
            if(contact_no != 0):
                
                if "send message" in query:
                
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                    
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)

        elif "translate into Hindi" in query:
            query=query.replace("translate into Hindi","")
            from engine.features import translaor
            res=translaor(query)
            eel.receiverText(res)          
            
            speakText("result is added in Chat Box, pleacse chack it out")

        elif "hello" in query or "solve" in query or "solution of " in query or "what will be the output of" in query or "formula of " in query or "what is the time now" in query or "what's the time" in query:
            
            from engine.features import search
            search(query)

        elif "on Google" in query:
            from engine.features import searchGoogle
            searchGoogle(query)

        else:
            try:
                from engine.features import chatBot
                chatBot(query)
                
            except Exception as e:
                print(e)
            
    except:
        speakText("pleacse try again")


    eel.ShowHood()

