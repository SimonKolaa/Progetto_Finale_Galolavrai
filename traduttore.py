from flask import Flask, render_template, request
from googletrans import Translator  
import random
app = Flask(__name__)

traduzioni_personalizzate = {
    "qiva nanen": "cives",
    "galo king": "non bisogna tradurre",  
    "galo": "king di mondaino",
    "mondaino": "capitale",
    "alberti": "non sarà mai come il galo", 
    "mafia,": "sei a mondaino",
    "civet": "qiva robt", "al"
    "qiva robt": "cives",
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

if __name__ == "__main__":
    random_port = random.randint(2000, 9000)
    app.run(debug=True, port=random_port) 
    
