from flask import Flask,jsonify,Blueprint,request,current_app 
import requests
import logging
import os
from dotenv import load_dotenv
import json
from models.repositories.data_queries import get_all_notifications
from models.ai.news_ai import get_new_ai_for_preference
import pika
from pika.exchange_type import ExchangeType
import functools
load_dotenv()
news_api = Blueprint('news_api', __name__)

@news_api.route('/get-news',methods=['GET'])
def get_new():
    api_key = os.getenv('NEWS_API_KEY')
    
    url = f"https://newsdata.io/api/1/latest?apikey={api_key}"
    responses = []
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve news data, status code: {response.status_code}")
        return jsonify({"error": f"Failed to retrieve news data, status code: {response.status_code}"}), response.status_code
    responses.append(response.json())
    page_url = response.json().get('nextPage')
    for _ in range(1, 2):
        page_url = f"https://newsdata.io/api/1/latest?apikey={api_key}&page={page_url}"
        response = requests.get(page_url)
        if response.status_code != 200:
            logging.error(f"Failed to retrieve news data, status code: {response.status_code}")
            return jsonify({"error": f"Failed to retrieve news data, status code: {response.status_code}"}), response.status_code
        page_url = response.json().get('nextPage')
        responses.append(response)
    logging.info(f"News data retrieved successfully. Total pages: {len(responses)}")
    try:
        notification_preferences = get_all_notifications(current_app.collection)
        notification_preferences_dict = json.loads(notification_preferences.data.decode('utf-8'))
        notifications_array = notification_preferences_dict.get('notifications', [])
        ai_response = get_new_ai_for_preference(notifications_array, response.json())
        if ai_response.status_code == 200:
            logging.info("AI responses generated successfully.")
            queue_proccess_status=send_message_to_users(ai_response.data)
        else:
            logging.error(f"Failed to generate AI responses, status code: {ai_response.status_code}")
            return jsonify({"error": f"Failed to generate AI responses, status code: {ai_response.status_code}"})
        if queue_proccess_status.status_code==200:
            return jsonify({"status": 200, "data": "Message sent successfully"})
        else:
            return jsonify({"error": f"Failed to send message, status code: {queue_proccess_status}"}), queue_proccess_status
    except Exception as e:
        logging.error(f"An error occurred while generating AI responses: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    




def send_message_to_users(ai_response):
    try:
        connection_parameters = pika.ConnectionParameters('rabbitmq')
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()

        channel.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

        # Enable publisher confirmations
        channel.confirm_delivery()
        channel.basic_publish(exchange='topic', routing_key='gmail.users', body=ai_response, mandatory=True)
        
       
        response = jsonify({"status": 200, "data": "Message sent successfully"})
        logging.info(f'Message sent successfully')
        
        connection.close()
        return response
    except pika.exceptions.AMQPError as err:
        return jsonify({'error': f'Error sending message: {err}'}), 500

