from flask import Flask
import logging
from services.routes import user_manager_api
app = Flask(__name__)
app.register_blueprint(user_manager_api)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=5005)