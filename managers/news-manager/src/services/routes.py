import json
from flask import Flask, jsonify,Blueprint
import requests
import logging
import os
news_api = Blueprint('news_api', __name__)

@news_api.route('/get-news')
def get_news():
    """
    Retrieves news data from the news-service API.

    This request is simulated when the app is running and sends the latest news to each user
    who has registered to the app based on their preferences.

    Returns:
        A JSON response containing the news data.
        If successful, the response will have a status code of 200 and the news data.
        If there is a bad request, the response will have a status code of 400 and an error message.
        If there is an internal server error, the response will have a status code of 500 and an error message.
        If there is an unexpected status code, the response will have the corresponding status code and an error message.
        If an exception occurs, the response will have a status code of 500 and an error message.
    """
    dapr_port = os.getenv('DAPR_HTTP_PORT', 3500)
    url=f'http://news-service:{dapr_port}/v1.0/invoke/news-service/method/get-news'
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
    
