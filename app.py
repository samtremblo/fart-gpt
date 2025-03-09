from flask import Flask, render_template, request, jsonify
import openai
import random
import os

app = Flask(__name__)

# Initialize OpenAI client with API key from file
try:
    with open('key', 'r') as f:
        api_key = f.read().strip()
    if not api_key:
        raise ValueError("API key file is empty")
    openai.api_key = api_key
except (FileNotFoundError, ValueError) as e:
    print(f"Error loading API key: {e}")
    print("Please make sure the 'key' file exists and contains your OpenAI API key")
    exit(1)

FART_NOISES = [
    "pffffft",
    "BRAAAP",
    "pfft pfft",
    "PRRRRP",
    "*squeaky fart*",
    "THBBBBBT",
    "*wet fart*",
    "poot",
    "BRRRRRRRT",
    "*tiny fart*"
]

def fartify_response(text):
    """Convert normal text into fart-speak by adding fart noises."""
    words = text.split()
    fartified = []
    
    for i, word in enumerate(words):
        fartified.append(word)
        # Add a fart noise roughly every 3-5 words
        if i > 0 and random.randint(1, 5) <= 2:
            fartified.append(f"*{random.choice(FART_NOISES)}*")
    
    return ' '.join(fartified)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')

    try:
        # Get response from GPT
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a silly chatbot that likes to make fart sounds. Keep responses short and playful."}, 
                {"role": "user", "content": user_message}
            ],
            max_tokens=100
        )
        
        # Get the response text
        response_text = completion.choices[0].message['content']
        
        # Convert the response to fart-speak
        fartified_response = fartify_response(response_text)
        
        return jsonify({'response': fartified_response})
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'response': f"*{random.choice(FART_NOISES)}* (Excuse me, I had a technical difficulty: {str(e)})"})        

if __name__ == '__main__':
    app.run(debug=True, port=5001)
