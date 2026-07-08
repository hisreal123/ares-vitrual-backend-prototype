import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from models import db
from routes.assets import assets_bp
from routes.meetings import meetings_bp

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///videos.db')
db.init_app(app)

CORS(app)  # Enable CORS for all routes

with app.app_context():
    db.create_all()

app.register_blueprint(assets_bp)
app.register_blueprint(meetings_bp)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)