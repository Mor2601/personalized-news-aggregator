from flask import Flask,jsonify,Blueprint
import requests
import logging
import os
from dotenv import load_dotenv
load_dotenv()
news_api = Blueprint('news_api', __name__)

"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""



import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)





@news_api.route('/get-news',methods=['GET'])
def get_new():
    dapr_port = os.getenv('DAPR_HTTP_PORT', 3500)
    api_key = os.getenv('NEWS_API_KEY')
    logging.info(f"api_key: {api_key}")
    url=f"https://newsdata.io/api/1/news?apikey={api_key}"
    response = requests.get(url)
    
    try:
        if response.status_code == 200:
            news_data = response.json()
            logging.info("News data retrieved successfully.")
            return jsonify({"status": response.status_code, "data": news_data})
        elif response.status_code == 400:
            logging.error("Bad Request: Invalid parameters.")
            return jsonify({"error": "Bad Request: Invalid parameters."}), 400
        elif response.status_code == 500:
            logging.error("Internal Server Error: Something went wrong on the server.")
            return jsonify({"error": "Internal Server Error: Something went wrong on the server."}), 500
        else:
            logging.error(f"Error: Unexpected status code {response.status_code}.")
            return jsonify({"error": f"Error: Unexpected status code {response.status_code}"}), response.status_code
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    
@news_api.route('/get-new-ai',methods=['GET'])
def get_new_ai():
    dapr_port = os.getenv('DAPR_HTTP_PORT', 3500)
    api_key = os.getenv('NEWS_API_KEY')
    
    logging.info(f"api_key: {api_key}")
    url=f"https://newsdata.io/api/1/news?apikey={api_key}"
    response = requests.get(url)
    news_data_str = response.json()
    SPORT = "Football, New Technology, and AI"
    prompt = f"Please provide the most interesting news articles about {SPORT} from this data:\n{news_data_str}\nProvide a concise summary based on the available information, including the articles titles and description dont omit nothig from the reposne."
    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(prompt)
    return jsonify({"status":200, "data": response.text})
    try:
        if response.status_code == 200:
            news_data = response.json()
            logging.info("News data retrieved successfully.")
            return jsonify({"status": response.status_code, "data": news_data})
        elif response.status_code == 400:
            logging.error("Bad Request: Invalid parameters.")
            return jsonify({"error": "Bad Request: Invalid parameters."}), 400
        elif response.status_code == 500:
            logging.error("Internal Server Error: Something went wrong on the server.")
            return jsonify({"error": "Internal Server Error: Something went wrong on the server."}), 500
        else:
            logging.error(f"Error: Unexpected status code {response.status_code}.")
            return jsonify({"error": f"Error: Unexpected status code {response.status_code}"}), response.status_code
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
