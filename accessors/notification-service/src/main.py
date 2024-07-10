from flask import Flask
import logging
from services.routes import notification_service_api
from db import init_db 
app = Flask(__name__)
app.register_blueprint(notification_service_api)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    collection = init_db()
    app.collection = collection
    app.run(debug=True, port=5008)