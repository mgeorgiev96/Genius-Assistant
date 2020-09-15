import wikipedia
import wolframalpha
import requests
from flask import Flask, render_template, request, redirect
import gtts
import pyttsx3
from playsound import playsound
import os
import json
import ctypes

#Answer about the user question
info = ''

#Link for th topic
topic_link = ''

#Last voice question
question_by_voice = ''

app = Flask(__name__)

#User can verbally ask question
@app.route('/speak', methods=['POST','GET'])
def listen_voice():
    try:
        voice = json.loads(request.data)
        global question_by_voice
        global info
        global topic_link
        question_by_voice = voice
        try:
            app_id = os.environ.get('APP_ID')
            client = wolframalpha.Client(app_id)
            res = client.query(voice)
            answer = next(res.results).text
            info = answer
            try:
                topic_page = wikipedia.page(voice)
            except:
                pass
        except:
            wiki = wikipedia.summary(voice)
            info = wiki
        topic_link=wikipedia.page(voice).url
    except:
        print('Please repeat, could not recognize what you said.')

    return redirect('/voice_question')

@app.route('/voice_question')
def voice_question_answered():
    return render_template('index.html',answered=info,asked_question=question_by_voice,public_link=topic_link)

#Converts text to speech
@app.route('/listen')
def speak_answer():
    global info
    tts = gtts.gTTS(text=info,lang='en')
    file = 'voice.mp3'
    tts.save(file)
    playsound(file)
    return render_template('index.html', answered=info)

#Renders home page
@app.route('/')
def home_page():
    return render_template('index.html')

#Searches for information about the user question
@app.route('/question',methods=['POST','GET'])
def ask_question():
    if request.form:
        question = request.form['question']
    global info
    global topic_link
    try:
        app_id = os.environ.get('APP_ID')
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        answer = next(res.results).text
        info = answer
    except:
        try:
            wiki = wikipedia.summary(question)
            info = wiki
            topic_link=wikipedia.page(question).url
        except wikipedia.DisambiguationError as e:
            wiki = e.options[0]
            info = wiki
            topic_link=wikipedia.page(e.options[0]).url
        except wikipedia.PageError as e:
            info = f'No matches found for \"{question}\".'

    return render_template('index.html',answered=info,asked_question=question,public_link=topic_link)

#Opens web page with additional info
@app.route('/info', methods=['GET','POST'])
def show_web_page():
    return render_template('index.html',public_link=topic_link)


if __name__ == '__main__':
    app.run(debug=True)