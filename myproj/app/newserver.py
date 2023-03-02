import os
from flask import Flask, redirect, render_template, request, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import cv2
from sqlalchemy.sql import func

app = Flask(__name__,static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)



CORS(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(200), nullable=False),
    bio = db.Column(db.Text)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/videos', methods=['GET', 'POST'])
def videos():
    if request.method == 'POST':
        video = Video(title=request.form['title'], description=request.form['description'], url=request.form['url'])
        db.session.add(video)
        db.session.commit()
        return redirect('/videos')
    else:
        videos = Video.query.all()
        return render_template('videos.html', videos=videos)

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        user = User(username=request.form['username'], email=request.form['email'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    else:
        users = User.query.all()
        return render_template('users.html', users=users)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/watermark', methods=['POST'])
def watermark():
    # Get user_info and video_info from the request
    # data=request.get_json()
    # user_info=data['user_info']
    # video_info=data['video_info']
    user_info = request.form.get('user_info')
    video_info = request.form.get('video_info')

    # Retrieve the corresponding video from local storage
    video_path = 'L:/CreDStack/myproj/' + video_info

    # Read the video using OpenCV
    video = cv2.VideoCapture(video_path)

    # Check if the video was successfully opened
    if not video.isOpened():
        return 'Error: Could not open video file'

    # Get the video dimensions
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a VideoWriter object to save the watermarked video
    watermark_path = 'L:/CreDStack/myproj/' + video_info
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(watermark_path, fourcc, 30, (width, height))

    # Loop through the video frames and apply the watermark
    while True:
        ret, frame = video.read()
        if not ret:
            break
        # Apply the watermark using user_info and OpenCV drawing functions
        # ...
        # Write the watermarked frame to the VideoWriter object
        writer.write(frame)

    # Release the VideoCapture and VideoWriter objects
    video.release()
    writer.release()

    # Send the watermarked video path and MIME type in a JSON response
    # return {'watermark_path': watermark_path, 'mime_type': 'video/mp4'}
    # Send the watermarked video to the requester using Flask's send_file function
    return render_template('result.html',file=video_info)
    # return render_template("index.html")
    # return send_file(watermark_path, mimetype='video/mp4', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,threaded=True)
