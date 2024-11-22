import openai
from gtts import gTTS
import os
import subprocess
import pygame
import speech_recognition as sr
import time
from pydub import AudioSegment
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import mysql.connector

# Configure your OpenAI API key
openai.api_key = ''

# Configure Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='',
                                               client_secret='',
                                               redirect_uri='',
                                               scope='user-library-read user-modify-playback-state'))

# Configure MySQL
def retrieve_info_from_db():
    try:
        connection = mysql.connector.connect(
            host="",  # Replace with the IP address or hostname of the database
            user="",  # Replace with the user of the database
            password="", # Replace with the password of the database
            database=""  # Replace with the name of the database
        )
        cursor = connection.cursor()

        query = "SELECT * FROM user;"
        cursor.execute(query)

        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return data

    except mysql.connector.Error as error:
        print("Error connecting to the database:", error)
        return None

# Function to find the email of a user by their username
def find_email_by_username(Prenom):
    try:
        connection = mysql.connector.connect(
            host="",  # Replace with the IP address or hostname of the database
            user="",  # Replace with the user of the database
            password="", # Replace with the password of the database
            database=""  # Replace with the name of the database
        )
        cursor = connection.cursor()

        query = "SELECT Email FROM user WHERE Prenom = %s"
        cursor.execute(query, (Prenom,))

        email = cursor.fetchone()

        cursor.close()
        connection.close()

        if email:
            return email[0]
        else:
            return "No user found with this username."

    except mysql.connector.Error as error:
        print("Error searching for email in the database:", error)
        return "Error searching for email."

# List of messages for the conversation
messages = [{"role": "system", "content": "Vous êtes Mia, l'une des créations du professeur Dante. Il travaille actuellement à la création d’un corps permettant d’interagir avec les humains."}]

# Initialize pygame for audio playback
pygame.init()

# Initialize SpeechRecognition
recognizer = sr.Recognizer()

# Token limit for MIA's responses
max_tokens = 500

while True:
    time.sleep(3)

    with sr.Microphone() as source:
        print("Je t'écoute")
        audio = recognizer.listen(source)

    try:
        message = recognizer.recognize_google(audio, language="fr-FR")
        print("Vous (Speech-to-Text):", message)
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio.")
        continue
    except sr.RequestError:
        print("Unable to connect to Google Web Speech API. Check your internet connection.")
        continue

    messages.append({"role": "user", "content": message})

    if "recherche la musique " in message:
        search_query = message.replace("recherche la musique ", "").strip()
        results = sp.search(q=search_query, type='track')

        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            response = f"I added the song to the queue: {results['tracks']['items'][0]['name']} by {results['tracks']['items'][0]['artists'][0]['name']}"
            sp.start_playback(uris=[track_uri])
        else:
            response = "No song found for the search."
    elif "yeux" in message:
        chemin_script = "/home/USER/Desktop/Preview.py" #Replace USER with your name
        subprocess.run(["python", chemin_script])
        response = "c'est bon je te voit"
    elif "information" in message:
        data_from_db = retrieve_info_from_db()
        if data_from_db:
            response = "I retrieved information from the database: " + str(data_from_db)
        else:
            response = "Failed to retrieve information from the database."

    elif "recherche l'email de " in message:
        username_to_find = message.replace("recherche l'email de ", "").strip()
        email_result = find_email_by_username(username_to_find)
        response = "The email of the user {} is: {}".format(username_to_find, email_result)

    else:
        # Nouvelle façon d'interagir avec GPT-3.5-turbo
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = chat['choices'][0]['message']['content']
        reply_tokens = len(reply.split())
        if reply_tokens > max_tokens:
            reply = "La réponse de MIA est trop longue pour être prononcée."

        response = reply

    print("MIA:", response)

    tts = gTTS(text=response, lang='fr')
    tts.save('message.mp3')

    sound = AudioSegment.from_file("message.mp3")
    sound = sound.speedup(playback_speed=1.5)
    sound.export("message_accelerated.mp3", format="mp3")

    pygame.mixer.music.load('message_accelerated.mp3')
    pygame.mixer.music.play()
