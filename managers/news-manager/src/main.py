from flask import Flask, jsonify,Blueprint 
import requests
import logging
from services.routes import news_api

app = Flask(__name__)
app.register_blueprint(news_api)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=5001)