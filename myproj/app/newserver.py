from flask import Flask, render_template, request, send_file
import cv2

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/watermark', methods=['POST'])
def watermark():
    # Get user_info and video_info from the request
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

    # Send the watermarked video to the requester using Flask's send_file function
    return send_file(watermark_path, mimetype='video/mp4', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
