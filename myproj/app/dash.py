import ffmpeg_streaming
from ffmpeg_streaming import Formats,FFProbe, Bitrate, Representation, Size

video=ffmpeg_streaming.input('L:/CreDStack/myproj/test.mp4')


# _360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
# _480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
# _720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
dash = video.dash(Formats.h264())
dash.auto_generate_representations()
# dash.representations(_360p,_480p,_720p)
dash.output('L:/CreDStack/myproj/dash.mpd')
# dash.output()

# hls = video.hls(Formats.h264())
# hls.representations(_360p,_480p,_720p)
# hls.output()
# hls.auto_generate_representations()
# hls.output('static/videos/dash.mpd')
