from flask import Flask, request, jsonify
import logging
import requests
import os

app = Flask(__name__)

@app.route('/set-customer-preferences', methods=['POST'])
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
        url=f'http://customer-service:{dapr_port}/v1.0/invoke/customer-service/method/set-customer-preferences'
          
        # Forward the customer preferences to the next service
        response = requests.post(url, json=customer_preferences)
        
        # Check if the request was successful
        if response.status_code == 200:
            logging.info('customer preferences forwarded successfully.')
            return jsonify({"status": response.status_code, "data": response.json()}), response.status_code
        else:
            logging.error('Failed to forward customer preferences.')
            return jsonify({"error": "Failed to forward customer preferences"}), response.status_code
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@app.route('/update-customer-preferences', methods=['PUT'])
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
        url=f'http://customer-service:{dapr_port}/v1.0/invoke/customer-service/method/update-customer-preferences'
          
        # Forward the customer preferences to the next service
        response = requests.put(url, json=customer_preferences)
        
        # Check if the request was successful
        if response.status_code == 200:
            logging.info('customer preferences updated successfully.')
            return jsonify({"status": response.status_code, "data": response.json()}), response.status_code
        else:
            logging.error('Failed to update customer preferences.')
            return jsonify({"error": "Failed to update customer preferences"}), response.status_code
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/remove-customer-preferences', methods=['DELETE'])
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
        url=f'http://customer-service:{dapr_port}/v1.0/invoke/customer-service/method/remove-customer-preferences'
          
        # Forward the customer preferences to the next service
        response = requests.delete(url, json=customer_preferences)
        
        # Check if the request was successful
        if response.status_code == 200:
            logging.info('customer preferences removed successfully.')
            return jsonify({"status": response.status_code, "data": response.json()}), response.status_code
        else:
            logging.error('Failed to remove customer preferences.')
            return jsonify({"error": "Failed to remove customer preferences"}), response.status_code
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=5003)