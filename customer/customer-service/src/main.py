from flask import Flask
from services.routes import customer_api
import logging
app = Flask(__name__)
app.register_blueprint(customer_api)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=5004)