from flask import Blueprint, send_file

app = Blueprint('gcsfs', __name__, url_prefix='/gcsfs')
class Gcsfs():
    @app.route('/videos/<filename>')
    def get_video(filename):
        video_path = 'L:\CreDStack\myproj' + filename
        return send_file(video_path, mimetype='video/mp4')


