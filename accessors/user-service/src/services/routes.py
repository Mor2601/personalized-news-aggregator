from flask import Blueprint,request,jsonify,current_app
import logging
import requests
import os
from models.repositories.data_queries  import add_new_data,update_user_preferences,delete_user_preferences
user_service_api = Blueprint('user_service_api', __name__)
@user_service_api.route('/set-customer-preferences', methods=['POST'])
def set_customer_preferences():
    """
    Sets customer preferences for the news service and forwards them to the next service.

    Returns:
        A JSON response containing the status code and a success message if successful.
        A JSON response containing an error message and status code if unsuccessful.
    """
    try:
        
        
         # Validate the received data
        result= add_new_data(current_app.collection, request)
        logging.info(f'result is:{result}')
        # Check if the request was successful
        if result.acknowledged:
            logging.info('customer preferences forwarded successfully.')
            return jsonify({"status":200,"data":"customer preferences forwarded successfully."})
        else:
            logging.error('Failed to forward customer preferences.')
            return jsonify({"error": "Failed to forward customer preferences"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@user_service_api.route('/update-customer-preferences', methods=['PUT'])
def update_customer_preferences():
    """
    Updates customer preferences for the news service and forwards them to the next service.

    Returns:
        A JSON response containing the status code and a success message if successful.
        A JSON response containing an error message and status code if unsuccessful.
    """
    try:
      # Validate the received data
        result= update_user_preferences(current_app.collection, request)

        # Check if the request was successful
        if result.acknowledged:
            logging.info('customer preferences forwarded successfully.')
            return jsonify({"status":200,"data":"customer preferences forwarded successfully."})
        else:
            logging.error('Failed to forward customer preferences.')
            return jsonify({"error": "Failed to forward customer preferences"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@user_service_api.route('/remove-customer-preferences', methods=['DELETE'])
def remove_customer_preferences():
    """
    Removes customer preferences for the news service and forwards them to the next service.

    Returns:
        A JSON response containing the status code and a success message if successful.
        A JSON response containing an error message and status code if unsuccessful.
    """
    try:
      # Validate the received data
        result= delete_user_preferences(current_app.collection, request)

        # Check if the request was successful
        if result.acknowledged:
            logging.info('customer preferences removed successfully.')
            return jsonify({"status":200,"data":"customer preferences removed successfully."})
        else:
            logging.error('Failed to remove customer preferences.')
            return jsonify({"error": "Failed to remove customer preferences"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500