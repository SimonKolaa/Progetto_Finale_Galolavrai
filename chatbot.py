from flask import Flask, request, jsonify, render_template
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

def generate_response(prompt):
    """Generates a response from the text generator."""
    output = text_generator(prompt, max_length=50, do_sample=True, top_k=90, top_p=0.55, num_return_sequences=1)
    return output[0]['generated_text']

def check_winner():
    """Checks if the game is over and a winner can be determined."""
    if users['user1']['round'] == rounds and users['user2']['round'] == rounds:
        if users['user1']['score'] > users['user2']['score']:
            return "user1"
        elif users['user1']['score'] < users['user2']['score']:
            return "user2"
        else:
            return "draw"
    return None

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    """Handles user input and generates a response."""
    if request.method == 'POST':
        data = request.get_json()
        user_input = data['user_input']
        user_id = data['user_id']

        if "meme3M" in user_input:
            return jsonify({"response": "Vuoi giocare al meme3M? Inserisci una foto per iniziare"})
        elif "Inserisci una foto per iniziare!" in user_input:
            try:
                image_file = request.files['image']
                image = Image.open(io.BytesIO(image_file.read()))
                meme_image = create_meme(image)
                meme_image.save('meme.jpg')
                users[user_id]['round'] += 1
                return jsonify({"response": "Ecco il tuo meme"})
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        elif "Vota il meme" in user_input:
            vote = data['vote']
            users[user_id]['score'] += vote
            users[user_id]['round'] += 1
            return jsonify({"response": "Voto registrato"})
        else:
            try:
                output = generate_response(user_input)
                return jsonify({"response": output})
            except Exception as e:
                return jsonify({"error": str(e)}), 400
    else:
        return generate_response("How much is 2 + 3?")

def create_meme(image):
    """Funzione per manipolare l'immagine e creare il meme"""
    return image

@app.route('/images')
def show_images():
    """Funzione per mostrare le immagini dei meme"""
    return render_template('immmagini.html')

@app.route('/test')
def dfsdfsdfs():
    """Funzione per mostrare le immagini dei meme"""
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True, port=4674)
