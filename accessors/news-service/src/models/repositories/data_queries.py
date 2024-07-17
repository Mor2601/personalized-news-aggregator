from flask import jsonify
import logging

def get_all_notifications(collection):
    """
    Retrieves all notification preferences from the collection.

    Parameters:
    - collection: The MongoDB collection where the notification preferences are stored.

    Returns:
    - A list of all notification preferences.
    """
    try:
        notifications = collection.find({})
        notifications_list = list(notifications)
        
        # Convert MongoDB ObjectId to string if necessary
        for notification in notifications_list:
            notification['_id'] = str(notification['_id'])
        
        return jsonify({"acknowledged": True, "notifications": notifications_list})
    except Exception as e:
        logging.error(f"An error occurred while fetching notifications: {str(e)}")
        return jsonify({"acknowledged": False, "error": str(e)})