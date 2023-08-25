import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from fastertranscription import transcribefaster
from emailing import email
from datetime import datetime

application = Flask(__name__)
CORS(application)

AUDIO_UPLOAD_FOLDER = os.path.join(os.getcwd(),'audios')
TRANSCRIPTS_UPLOAD_FOLDER = os.path.join(os.getcwd(),'transcripts')

@application.route('/', methods=["GET","POST"])
def index():
    return render_template("index.html")

@application.route('/upload_static_file', methods=["GET","POST"])
def upload_static_file():
    audio_file = request.files["static_file"]
    if audio_file:
        audio_location = os.path.join(
            AUDIO_UPLOAD_FOLDER,
            audio_file.filename
        )
        audio_file.save(audio_location)
        response = transcribefaster(audio_location)
        filename = f'Transcription_{datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")}.txt'
        currfile = os.path.join(TRANSCRIPTS_UPLOAD_FOLDER,filename)
        with open(currfile,'w+') as f:
            f.write(f'{response["text"]}\n\nDURATION TAKEN: {response["duration"]}\n')
        if email(["devesh.paragiri@gmail.com","bhuvana.kundumani@gmail.com"], currfile, filename):
            os.remove(audio_location)
            os.remove(currfile)
        resp = {"success": True, 
                "response": "File processed!",
                "text": response["text"],
                "path":currfile}
        return jsonify(resp), 200
        
# if __name__=="__main__":
#     application.run(debug=True, port=3000)