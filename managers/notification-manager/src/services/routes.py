from flask import Flask,Blueprint,request,jsonify
import logging
import requests
import os
notification_api = Blueprint('notification_api', __name__)
@notification_api.route('/add-new-user-to-notifcation-list', methods=['POST'])
def add_new_user_to_notifcation_list():
    """
    Adds a new user to the notification list by invoking the 'add-new-user-to-notifcation-list' method
    of the user-manager service.

    Returns:
        A JSON response containing the status and data of the operation.
        If successful, the response will have a status of 'success' and the data will contain the response from the user-manager service.
        If unsuccessful, the response will have an error message and an appropriate status code.

    Raises:
        Exception: If an unexpected error occurs during the operation.
    """
    dapr_port = os.getenv('DAPR_HTTP_PORT', 3500)
    url=f'http://notification-service:{dapr_port}/v1.0/invoke/notification-service/method/add-new-user-to-notifcation-list'
    try:
        user_data = request.get_json()
        
        if not user_data or not isinstance(user_data, dict):
            logging.error("Invalid request data.")
            return jsonify({"error": "Invalid request data"}), 400
        response = requests.post(url, json=user_data)
        if response.status_code == 200:
            logging.info('User added to notification list successfully.')
            return jsonify({"status": "success", "data": response.json()})
        else:
            logging.error('Failed to add user to notification list.')
            return jsonify({"error": "Failed to add user to notification list"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@notification_api.route('/remove-user-from-notification-list', methods=['DELETE'])
def remove_user_from_notification_list():
    """
    Removes a user from the notification list by invoking the 'remove-user-from-notification-list' method
    of the user-manager service.

    Returns:
        A JSON response containing the status and data of the operation.
        If successful, the response will have a status of 'success' and the data will contain the response from the user-manager service.
        If unsuccessful, the response will have an error message and an appropriate status code.

    Raises:
        Exception: If an unexpected error occurs during the operation.
    """
    dapr_port = os.getenv('DAPR_HTTP_PORT', 3500)
    url=f'http://notification-service:{dapr_port}/v1.0/invoke/notification-service/method/remove-user-from-notification-list'
    try:
        user_data = request.get_json()
        
        if not user_data or not isinstance(user_data, dict):
            logging.error("Invalid request data.")
            return jsonify({"error": "Invalid request data"}), 400
        response = requests.delete(url, json=user_data)
        if response.status_code == 200:
            logging.info('User removed from notification list successfully.')
            return jsonify({"status": "success", "data": response.json()})
        else:
            logging.error('Failed to remove user from notification list.')
            return jsonify({"error": "Failed to remove user from notification list"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500