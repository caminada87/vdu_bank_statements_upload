import os
from flask import Flask
from flask_cors import CORS
from src.blueprints import upload

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile(os.path.join(app.instance_path, "config.py"))

app.register_blueprint(upload.bp)

CORS(app,resources={r"/*":{"origins":"*"}})

if __name__ == "__main__":
    #app.secret_key = os.urandom(24)
    #app.run(debug=True,host="0.0.0.0",use_reloader=False)
    app.run(host='0.0.0.0', port=5050)