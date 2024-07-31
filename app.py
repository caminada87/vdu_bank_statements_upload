import os
from flask import Flask
from flask_cors import CORS
from src.blueprints import upload
from src.logging.logger import get_module_logger

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile(os.path.join(app.instance_path, "config.py"))

app.register_blueprint(upload.bp)

CORS(app,resources={r"/*":{"origins":"*"}})

logger = get_module_logger(__name__)
logger.debug("Driver, Server, DB, User, Allowed Extensions:")
logger.debug(app.config['DRIVER'])
logger.debug(app.config['SERVER'])
logger.debug(app.config['DB'])
logger.debug(app.config['USER'])
logger.debug(app.config['ALLOWED_EXTENSIONS'])

if __name__ == "__main__":
    #app.secret_key = os.urandom(24)
    #app.run(debug=True,host="0.0.0.0",use_reloader=False)
    app.run(host='0.0.0.0', port=5050)