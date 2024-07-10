from flask import Blueprint,request,jsonify,current_app
import logging
import requests
import os
from models.repositories.data_queries  import insert_new_user_to_notification_list,remove_user_from_preference_notification_group
notification_service_api = Blueprint('notification_service_api', __name__)
@notification_service_api.route('/add-new-user-to-notifcation-list', methods=['POST'])
def add_new_user_to_notification_list():
    """
    Sets customer preferences for the news service and forwards them to the next service.

    Returns:
        A JSON response containing the status code and a success message if successful.
        A JSON response containing an error message and status code if unsuccessful.
    """
    try:
        
        logging.info('Forwarding customer preferences to the notification service...')
         # Validate the received data
        result= insert_new_user_to_notification_list(current_app.collection, request)

        # Check if the request was successful
        if result:
            logging.info('customer preferences forwarded successfully.')
            return jsonify({"status":200,"data":"customer preferences forwarded successfully."})
        else:
            logging.error('Failed to forward customer preferences.')
            return jsonify({"error": "Failed to forward customer preferences"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@notification_service_api.route('/remove-user-from-notification-list', methods=['DELETE'])
def delete_user_from_preference_notification_group():
    """
    Removes a user from the notificationGroup of a preference when the user deletes that preference.
    If the notificationGroup becomes empty after removal, it removes the entire preference from the schema.

    Returns:
        A JSON response containing the status code and a success message if successful.
        A JSON response containing an error message and status code if unsuccessful.
    """
    try:
        logging.info('Removing user from preference notification group...')
        # Validate the received data
        result= remove_user_from_preference_notification_group(current_app.collection, request)
        # Check if the request was successful
        if result:
            logging.info('User removed from preference notification group.')
            return jsonify({"status":200,"data":"User removed from preference notification group."})
        else:
            logging.error('Failed to remove user from preference notification group.')
            return jsonify({"error": "Failed to remove user from preference notification group"}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500