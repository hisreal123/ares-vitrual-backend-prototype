from flask import Flask, send_from_directory
from models import db, Video

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
db.init_app(app)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/api/videos/random', methods=['GET'])
def random_video():
    videos = Video.query.order_by(db.func.random()).limit(3).all()
    return {'videos': [video.to_dict() for video in videos]}

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory('videos', filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)