import google.generativeai as genai
import logging
import os
from flask import jsonify
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""


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

def get_new_ai_for_preference(preferences, news):
    # Validate inputs
    if not preferences or not news:
        logging.error("Invalid or empty preferences or news data.")
        return jsonify({"status": 400, "error": "Invalid or empty preferences or news data."})
    
    if not isinstance(preferences, list) or not isinstance(news, dict):
        logging.error("Invalid data types for preferences or news.")
        return jsonify({"status": 400, "error": "Invalid data types for preferences or news."})
    
    responses = []
    for preference in preferences:
        # Assuming preference is a string and news is a dictionary that can be converted to a string representation.
        prompt = f"Please provide the most interesting news articles about {preference['_id']} from this data:\n{news}\nProvide a list of the title of the article and there url link and concise summary based on the available information, including the articles titles and description. Do not omit anything from the response.  if there isnt latest news for a subject just write there isnt new articles"
        
        # Assuming model.start_chat and chat_session.send_message are defined elsewhere and handle the chat correctly.
        chat_session = model.start_chat(history=[]) 
        response = chat_session.send_message(prompt)
        
        # Collect each response
        responses.append({"preference": preference, "response": response.text})
    logging.info(f"Responses generated: {responses}")
    # Return all responses
    return jsonify({"status": 200, "data": responses})