from models.models import Users_Detail
from flask import jsonify
import logging
def add_new_data(collection, request):
    """
    Inserts a new document into the MongoDB collection based on the JSON payload from the request.

    Parameters:
    - collection: The MongoDB collection where the document will be inserted.
    - request: The Flask request object containing the JSON payload.

    Returns:
    - Flask response object: A JSON response indicating the result of the insert operation.
    """
    data = request.json
    
    # Validation
    required_fields = ['_id', 'preferences']  # Assuming these are the correct field names
    logging.info(f"Validating request data: {data}")
    logging.info(f"Required fields: {required_fields}")
    logging.info(f"check {not all(field in data for field in required_fields)}")
    if not all(field in data for field in required_fields):
        logging.error("Validation failed: Missing required fields in the request data.")
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = collection.insert_one({
            Users_Detail._ID: data.get('_id'),
            Users_Detail.PREFERENCES: data.get('preferences')
        })
        logging.info(f"Data inserted successfully with ID: {result.acknowledged}")
        return result
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An error occurred during the insert operation"}), 500
    
def update_user_preferences(collection, request):
    """
    Updates the preferences of a user in the MongoDB collection based on the JSON payload from the request.

    Parameters:
    - collection: The MongoDB collection where the document will be updated.
    - request: The Flask request object containing the JSON payload.

    Returns:
    - Flask response object: A JSON response indicating the result of the update operation.
    """
    data = request.json
    
    # Validation
    required_fields = ['_id', 'preferences']  # Assuming these are the correct field names
    logging.info(f"Validating request data: {data}")
    logging.info(f"Required fields: {required_fields}")
    if not all(field in data for field in required_fields):
        logging.error("Validation failed: Missing required fields in the request data.")
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = collection.update_one(
            {Users_Detail._ID: data.get('_id')},
            {"$set": {Users_Detail.PREFERENCES: data.get('preferences')}}
        )
        logging.info(f"Data updated successfully with ID: {result.acknowledged}")
        return result
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An error occurred during the update operation"}), 500