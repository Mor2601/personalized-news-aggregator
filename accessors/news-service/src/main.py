from flask import Flask
from db import init_db 
import logging
import threading
from services.routes import news_api

app = Flask(__name__)
app.register_blueprint(news_api)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    collection = init_db()
    app.collection = collection
    app.run(port=5002)