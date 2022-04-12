# from crypt import methods
from flask import Flask, render_template, request, redirect
# from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
#import video_classifier as v
from video_classifier import *

app = Flask(__name__)

app.config['VIDEO_UPLOADS'] = "C:\\Users\\Blakes\\Documents\\ML Assignment\\static\\uploads"
app.config['ALLOWED_VIDEO_EXTENSIONS'] = ["AVI", "MP4"]
app.config['MAX_VIDEO_FILESIZE'] = 2 * 1024 * 1024

def allowed_video_filesize(filesize):
    if int(filesize) <= app.config['MAX_VIDEO_FILESIZE']:
        return True
    else:
        return False
        
def allowed_video(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config['ALLOWED_VIDEO_EXTENSIONS']:
        return True
    else:
        return False

# @app.route("/upload")
# def upload_file():
#    return render_template('upload.html')
    
@app.route("/uploader", methods=['GET', 'POST'])
def upload_video():
    if request.method == "POST":
        if "filesize" in request.cookies:
            # if not allowed_video_filesize(request.cookies["filesize"]):
                #print("Filesize exceeded maximum limit")
                #return redirect(request.url)
            f = request.files['file']
            if f.filename == "":
                print("No filename")
                return redirect(request.url)
            if allowed_video(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config["VIDEO_UPLOADS"], filename))
                video_pred = sequence_prediction(app.config["VIDEO_UPLOADS"])
                vid = video_pred
                return redirect(request.url)
            else:
                print("That file extension is not allowed")
                return redirect(request.url)
    return render_template("upload.html", my_vid=vid)

            # f.save(secure_filename(f.filename))
            # return "Video uploaded successfully"
   
if __name__ == "__main__":
    app.run(debug=True)