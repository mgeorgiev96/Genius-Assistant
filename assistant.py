import wikipedia
import wolframalpha
from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import gtts
from playsound import playsound
import os
import webbrowser
import json

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
            app_id = '63H6YQ-LHJQUUR7TL'
            client = wolframalpha.Client(app_id)
            res = client.query(voice)
            answer = next(res.results).text
            info = answer
            try:
                topic_page = wikipedia.page(question)
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
    return render_template('index.html',answered=info,asked_question=question_by_voice)

#Converts text to speech
@app.route('/listen')
def speak_answer():
    global info
    os.remove('voice.mp3')
    tts = gtts.gTTS(info)
    tts.save('voice.mp3')
    playsound('voice.mp3')
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
        app_id = '63H6YQ-LHJQUUR7TL'
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        answer = next(res.results).text
        info = answer
    except:
        wiki = wikipedia.summary(question)
        info = wiki
    topic_link=wikipedia.page(question).url
    return render_template('index.html',answered=info,asked_question=question)

#Opens web page with additional info
@app.route('/info')
def show_web_page():
    if topic_link:
        webbrowser.open(topic_link)
    else:
        pass
    return render_template('index.html',answered=info)


if __name__ == '__main__':
    app.run(debug=True)