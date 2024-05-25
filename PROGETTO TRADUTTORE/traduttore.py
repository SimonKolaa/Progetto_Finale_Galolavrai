from flask import Flask, render_template, request
from googletrans import Translator  
import random
from gtts import gTTS
import speech_recognition as sr
import os


app = Flask(__name__)

traduzioni_personalizzate = {
    "qiva nanen": "ti scopo la mamma",
    "galo king": "non bisogna tradurre",  
    "galo": "king di mondaino",
    "mondaino": "capitale",
    "alberti": "non sarà mai come il galo", 
    "mafia,": "sei a mondaino",
    "civet": "qiva robt", "al"
    "qiva robt": "Ti scopo la famiglia",
    "c'amma fa?": "facciamo a mani",
    "ammò": "fratello" ,
    "t dev veng a piglià?": "devo venire a schiattarti?",
    "pari la uallera": "sembri un coglione",
    "pari o cazz": "sembri un coglione"
   
}

def traduci_testo(testo, lingua_destinazione):
    if testo.lower() in traduzioni_personalizzate:  #Case-insensitive
        return traduzioni_personalizzate[testo.lower()]
    else:
        try:
            translator = Translator()
            traduzione = translator.translate(testo, dest=lingua_destinazione)
            return traduzione.text
        except Exception:
            return "Traduzione non disponibile o lingua non supportata."

@app.route("/", methods=["GET", "POST"])
def index():
    original_text = ""
    translated_text = ""
    target_lang = "en"

    if request.method == "POST":
        original_text = request.form["text"]
        target_lang = request.form["lang"]
        translated_text = traduci_testo(original_text, target_lang)

    return render_template("index_traduttore.html", original_text=original_text, translated_text=translated_text, target_lang=target_lang)

def ascolta_comando_vocale():
    r = sr.Recognizer()
    with sr.AudioFile(os.path.join(app.root_path, 'static', '50_mila.wav')) as source:
 # Sostituisci con il percorso del tuo file audio
        audio = r.record(source)


    def traduci_e_pronuncia(testo):
        traduzione = traduci_testo(testo, "it")
        print(f"Traduzione: {traduzione}")
        tts = gTTS(traduzione, lang="it")
        tts.save("output.mp3")
        os.system("start output.mp3")

    try:
        testo = r.recognize_google(audio, language="it-IT")
        if testo.startswith("traduci"):
            testo_da_tradurre = testo[8:]
            traduci_e_pronuncia(testo_da_tradurre)
        elif testo == "esci":
            print("Arrivederci!")
            return True  # Segnala che il ciclo deve terminare
        else:
            print("Comando non riconosciuto")
    except sr.UnknownValueError:
        print("Audio non compreso")
    except sr.RequestError as e:
        print(f"Errore nel servizio di riconoscimento vocale; {e}")
    return False  # Il ciclo continua

while True:
    if ascolta_comando_vocale():
        break  # Esce dal ciclo se ascolta_comando_vocale() restituisce True
if __name__ == "__main__":
    random_port = random.randint(2000, 9000)
    app.run(debug=True, port=random_port) 
    