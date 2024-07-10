from flask import Blueprint,request,jsonify
import logging
import requests
import os
customer_api = Blueprint('customer_api', __name__)
@customer_api.route('/set-customer-preferences', methods=['POST'])
def set_customer_preferences():
    """
    Sets customer preferences for the news service and forwards them to the next service.

    Returns:
        A JSON response containing the status code and a success message if successful.
        A JSON response containing an error message and status code if unsuccessful.
    """
    try:
        # Extract customer preferences from the incoming request
        customer_preferences = request.get_json()
         # Validate the received data
        if not customer_preferences or not isinstance(customer_preferences, dict):
            logging.error("Invalid request data.")
            return jsonify({"error": "Invalid request data"}), 400
        
        # Define the URL of the next service
        dapr_port = os.getenv('DAPR_HTTP_PORT', 3500)
        dapr_port2=os.getenv('DAPR_HTTP_PORT2', 3500)
        url=f'http://user-manager:{dapr_port}/v1.0/invoke/user-manager/method/set-customer-preferences'
        url2=f'http://notification-manager:{dapr_port2}/v1.0/invoke/notification-manager/method/add-new-user-to-notifcation-list'
          
        # Forward the customer preferences to the next service
        response = requests.post(url, json=customer_preferences)
        response2 = requests.post(url2, json=customer_preferences)
        # Check if the request was successful
        
        # Assuming response2 is defined somewhere above this block
        if response.status_code == 200 and response2.status_code == 200:
            logging.info('Customer preferences forwarded successfully.')
            # Combine data from both responses if necessary, or handle them separately
            return jsonify({"status": "success", "data": {"response": response.json(), "response2": response2.json()}})
        else:
            failed_responses = []
            if response.status_code != 200:
                logging.error('Failed to forward customer preferences from response.')
                failed_responses.append({"error": "Failed to forward customer preferences from response", "status": response.status_code})
            if response2.status_code != 200:
                logging.error('Failed to forward customer preferences from response2.')
                failed_responses.append({"error": "Failed to forward customer preferences from response2", "status": response2.status_code})
            
            return jsonify({"errors": failed_responses}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@customer_api.route('/update-customer-preferences', methods=['PUT'])
def update_customer_preferences():
    """
    Updates customer preferences for the news service and forwards them to the next service.

    Returns:
        A JSON response containing the status code and a success message if successful.
        A JSON response containing an error message and status code if unsuccessful.
    """
    try:
        # Extract customer preferences from the incoming request
        customer_preferences = request.get_json()
        
        # Validate the received data
        if not customer_preferences or not isinstance(customer_preferences, dict):
            logging.error("Invalid request data.")
            return jsonify({"error": "Invalid request data"}), 400
        
        # Define the URL of the next service
        dapr_port = os.getenv('DAPR_HTTP_PORT', 3500)
        dapr_port2=os.getenv('DAPR_HTTP_PORT2', 3500)
        url=f'http://user-manager:{dapr_port}/v1.0/invoke/user-manager/method/update-customer-preferences'
        url2=f'http://notification-manager:{dapr_port2}/v1.0/invoke/notification-manager/method/add-new-user-to-notifcation-list'
          
        # Forward the customer preferences to the next service
        response = requests.put(url, json=customer_preferences)
        response2 = requests.post(url2, json=customer_preferences)
        
        
        # Check if both requests were successful
        if response.status_code == 200 and response2.status_code == 200:
            logging.info('Customer preferences updated successfully.')
            return jsonify({"status": "success", "data1": response.json(), "data2": response2.json()})
        else:
            error_messages = []
            if response.status_code != 200:
                logging.error('Failed to update customer preferences in the first service.')
                error_messages.append("Failed to update customer preferences in the first service.")
            if response2.status_code != 200:
                logging.error('Failed to update customer preferences in the second service.')
                error_messages.append("Failed to update customer preferences in the second service.")
            return jsonify({"error": " ".join(error_messages)}), max(response.status_code, response2.status_code)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@customer_api.route('/remove-customer-preferences', methods=['DELETE'])
def remove_customer_preferences():
    """
    Removes customer preferences for the news service and forwards them to the next service.

    Returns:
        A JSON response containing the status code and a success message if successful.
        A JSON response containing an error message and status code if unsuccessful.
    """
    try:
        # Extract customer preferences from the incoming request
        customer_preferences = request.get_json()
        
        # Validate the received data
        if not customer_preferences or not isinstance(customer_preferences, dict):
            logging.error("Invalid request data.")
            return jsonify({"error": "Invalid request data"}), 400
        
        # Define the URL of the next service
        dapr_port = os.getenv('DAPR_HTTP_PORT', 3500)
        dapr_port2=os.getenv('DAPR_HTTP_PORT2', 3500)
        url=f'http://user-manager:{dapr_port}/v1.0/invoke/user-manager/method/remove-customer-preferences'
        url2=f'http://notification-manager:{dapr_port2}/v1.0/invoke/notification-manager/method/remove-user-from-notification-list'
          
        # Forward the customer preferences to the next service
        response = requests.delete(url, json=customer_preferences)
        response2 = requests.delete(url2, json=customer_preferences)
        
    
        # Check if both requests were successful
        if response.status_code == 200 and response2.status_code == 200:
            logging.info('Customer preferences removed successfully.')
            return jsonify({"status": "success", "data1": response.json(), "data2": response2.json()})
        else:
            error_messages = []
            if response.status_code != 200:
                logging.error('Failed to remove customer preferences from the first service.')
                error_messages.append("Failed to remove customer preferences from the first service.")
            if response2.status_code != 200:
                logging.error('Failed to remove customer preferences from the second service.')
                error_messages.append("Failed to remove customer preferences from the second service.")
            return jsonify({"error": " ".join(error_messages)}), max(response.status_code, response2.status_code)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500