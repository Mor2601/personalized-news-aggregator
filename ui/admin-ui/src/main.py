
from flask import Flask, jsonify
import requests
import os
import logging


app = Flask(__name__)
@app.route('/get-news', methods=['GET'])
def get_news():
        """
        Retrieves news data from the news manager service.

        Returns:
            A JSON response containing the status code and news data if successful.
            A JSON response containing an error message and status code if unsuccessful.
        """
        dapr_port = os.getenv('DAPR_HTTP_PORT', 3500)
        
       
        try:
            response = requests.get(f'http://news-manager:{dapr_port}/v1.0/invoke/news-manager/method/get-news')
            
            if response.status_code == 200:
                # Success
                news_data = response.json()
                # Process the news data
                logging.info("News data retrieved successfully.")
                return jsonify({"status": response.status_code, "data": news_data})
                
            elif response.status_code == 400:
                # Bad Request
                # Handle the error
                logging.error("Bad Request: Invalid parameters.")
                return jsonify({"error": "Bad Request: Invalid parameters."}), 400
                
            elif response.status_code == 500:
                # Internal Server Error
                # Handle the error
                logging.error("Internal Server Error: Something went wrong on the server.")
                return jsonify({"error": "Internal Server Error: Something went wrong on the server."}), 500
                
            else:
                # Other status codes
                # Handle the error
                logging.error(f"Error: Unexpected status code {response.status_code}.")
                return jsonify({"error": f"Error: Unexpected status code {response.status_code}"})

        except Exception as e:
            # Handle any exceptions that occur during the request
            logging.error(f"An error occurred: {str(e)}")
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
@app.route('/send-request-to-process')
def send_request_to_process():
    """
    Sends a request to the news manager service to process the latest news.

    Returns:
        A JSON response containing the status code and a success message if successful.
        A JSON response containing an error message and status code if unsuccessful.
    """
    try:
        # Define the URL of the news manager service
        dapr_port = os.getenv('DAPR_HTTP_PORT', 3500)
        url=f'http://news-manager:{dapr_port}/v1.0/invoke/news-manager/method/send-request-to-process'
        
        # Send a request to the news manager service
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Success
            logging.info('Request sent successfully.')
            return jsonify({"status": 200, "data": "Request sent successfully."})
            
        else:
            # Handle the error
            logging.error('Failed to send request.')
            return jsonify({"error": "Failed to send request."}), response.status_code
        
    except Exception as e:
        # Handle any exceptions that occur during the request
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=5000)
    