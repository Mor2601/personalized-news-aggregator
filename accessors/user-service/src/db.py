from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

def init_db():
    """
    Initializes the database connection using the application's configuration.

    This function establishes a connection to a MongoDB database using the MongoClient from PyMongo. It then selects a specific database and collection based on the application's configuration and attaches the selected collection directly to the Flask app object for easy access throughout the application.

    Parameters:
    - app: The Flask application object. This object must have a configuration (`config`) attribute that includes 'MONGO_URL', 'DB_NAME', and 'COLLECTION_NAME' keys.

    Raises:
    - Exception: If there is an issue initializing the database connection or accessing the specified collection, an exception is printed to the console. The exception can optionally be raised to propagate the error to the caller.

    Note:
    - It's important to ensure that the Flask app object is properly configured with 'MONGO_URL', 'DB_NAME', and 'COLLECTION_NAME' before calling this function.
    """
    try:
        mongo_client = MongoClient(os.getenv('MONGO_DB_URL'))  # Establish connection to MongoDB
        db = mongo_client[os.getenv('DB_NAME')]  # Select the specified database
        return db[os.getenv('COLLECTION_NAME')]  # Attach the collection to the app object
    except Exception as e:
        # Handle the exception here
        print(f"Error initializing database: {e}")
        # Optionally, you can raise the exception again to propagate it to the caller
        # raise