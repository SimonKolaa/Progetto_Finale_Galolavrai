from flask import Flask, request, jsonify
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import io

app = Flask(__name__)

model = AutoModelForCausalLM.from_pretrained("distilgpt2")
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

users = {
    'user1': {'score': 0, 'round': 0},
    'user2': {'score': 0, 'round': 0}
}

rounds = 3

@app.route('/', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_input = data['user_input']
    user_id = data['user_id']

    if "meme3M" in user_input:
        return jsonify({"response": "Vuoi giocare al meme3M? Inserisci una foto per iniziare!"})
    elif "Inserisci una foto per iniziare!" in user_input:
        image_file = request.files['image']
        image = Image.open(io.BytesIO(image_file.read()))
        meme_image = create_meme(image)
        meme_image.save('meme.jpg')
        return jsonify({"response": "Ecco il tuo meme!"})
    elif "Vota il meme" in user_input:
        vote = data['vote']
        if user_id == 'user1':
            users['user1']['score'] += vote
        elif user_id == 'user2':
            users['user2']['score'] += vote
        return jsonify({"response": "Voto registrato!"})
    else:
        prompt = user_input
        output = text_generator(prompt, max_length=50, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=1)
        return jsonify({"response": output[0]['generated_text']})

def create_meme(image):
    #Funzione per manipolare l'immagine e creare il meme
    return image

def check_winner():
    if users['user1']['round'] == rounds and users['user2']['round'] == rounds:
        if users['user1']['score'] > users['user2']['score']:
            return "user1"
        elif users['user1']['score'] < users['user2']['score']:
            return "user2"
        else:
            return "draw"
    return None

if __name__ == '__main__':
    app.run(debug=True)
