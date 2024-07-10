from models.models import NotificationByPreferences
from flask import jsonify
import logging
def insert_new_user_to_notification_list(collection, request):
    """
    Inserts or updates user preferences in the notification list based on their preferences.
    Each preference is a unique document identified by its name (_id).
    The email and preferences are stored within each preference document.

    Parameters:
    - collection: The MongoDB collection where the preference document is stored.
    - request: The Flask request object containing the JSON payload.

    Returns:
    - A result object indicating the success of the operations.
    """
    data = request.json
    
    preferences = data['preferences']
    user_email = data['_id']
    results = []

    if not preferences:
        logging.error('No preferences provided.')
        return {"acknowledged": False, "error": "No preferences provided"}

    for preference in preferences:
        result = collection.update_one(
            {"_id": preference},
            {
                "$setOnInsert": {"_id": preference},
                "$addToSet": {"notificationGroup": user_email}  # Insert the email into the notificationGroup array
            },
            upsert=True
        )
        results.append(result.acknowledged)

    # Check if all operations were successful
    if all(results):
        return {"acknowledged": True}
    else:
        return {"acknowledged": False, "error": "One or more preferences failed to update"}
    
def remove_user_from_preference_notification_group(collection, request):
    """
    Removes a user from the notificationGroup of a preference when the user deletes that preference.
    If the notificationGroup becomes empty after removal, it removes the entire preference from the schema.

    Parameters:
    - collection: The MongoDB collection where the preference document is stored.
    - user_id: The identifier of the user to be removed.
    - preferences: A list of preferences from which the user should be removed.

    Returns:
    - A result object indicating the success of the operations.
    """
    data=request.json
    logging.info(data)
    preferences = data['preferences']
    
    user_email = data['_id']
    results = []
    if not preferences:
        logging.error('No preferences provided.')
        return {"acknowledged": False, "error": "No preferences provided"}

    for preference in preferences:
        # Step 1: Remove the user from the notificationGroup
        result = collection.update_one(
            {"_id": preference},
            {
                "$pull": {"notificationGroup": user_email}  # Remove the user_id from the notificationGroup array
            }
        )

        # Step 2 & 3: Check if the notificationGroup is empty and remove the preference if it is
        if result.modified_count > 0:  # Ensure the update was successful and made changes
            # Check if the notificationGroup is now empty
            updated_document = collection.find_one({"_id": preference})
            if not updated_document['notificationGroup']:  # If notificationGroup is empty
                # Remove the entire preference from the schema
                delete_result = collection.delete_one({"_id": preference})
                results.append(delete_result.acknowledged)
            else:
                results.append(True)
        else:
            results.append(False)

    # Check if all operations were successful
    if all(results):
        return {"acknowledged": True}
    else:
        return {"acknowledged": False, "error": "One or more preferences failed to update or remove"}