from flask import Flask, request, jsonify, render_template
import time  # Import the time module if not imported already
import traceback
from gradio_client import Client
import time

app = Flask(__name__, template_folder="templates")

gradio_cl = Client("https://osanseviero-mistral-super-fast.hf.space/")

# Define your mistralAI function here (assuming it's already defined)

def mistralAI(query):

    start_time = time.time()
    chat_response = gradio_cl.predict(
        query + "***act as Ada. Your made by Shibam. Give reply in less word if response might be rquire big then try fixed it between 100.",
        0.8,
        1024,
        0.9,
        1.1,
        api_name="/chat"
    )
    
    end_time = time.time()

    print(f"Bot: {chat_response[:-4]}\n Time Taken to respond: {round(end_time - start_time, 2)} seconds")
    return chat_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bot_reply', methods=['POST'])
def get_bot_reply():
    try:
        data = request.get_json()
        user_message = data['message']
        
        # Call mistralAI function with user's message to get the bot's response
        bot_reply = mistralAI(user_message)
        
        return jsonify({'bot_reply': bot_reply})
    
    except KeyError as ke:
        return jsonify({'error': f'Missing key in JSON data: {ke}'})
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Error in processing: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)



