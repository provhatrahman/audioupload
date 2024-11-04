from flask import Flask, render_template, send_file
import os
from pydub import AudioSegment
from io import BytesIO
import tempfile

app = Flask(__name__)

MP3_DIRECTORY = 'music'
os.makedirs(MP3_DIRECTORY, exist_ok=True)

# Target level for normalization (in dB)
TARGET_LEVEL = -1.0

def process_audio(file_path):
    # Load the audio file
    audio = AudioSegment.from_mp3(file_path)
    
    # Calculate the change needed to reach target level
    change_in_dBFS = TARGET_LEVEL - audio.dBFS
    
    # Normalize the audio
    normalized_audio = audio.apply_gain(change_in_dBFS)
    
    # Apply a limiter to prevent clipping
    limited_audio = normalized_audio.apply_gain_stereo(
        min(0, -normalized_audio.max_dBFS - 0.1),
        min(0, -normalized_audio.max_dBFS - 0.1)
    )
    
    # Create a temporary file to store the processed audio
    temp_file = BytesIO()
    limited_audio.export(temp_file, format='mp3')
    temp_file.seek(0)
    
    return temp_file

@app.route('/')
def index():
    mp3_files = sorted([f for f in os.listdir(MP3_DIRECTORY) if f.endswith('.mp3')])
    return render_template('index.html', mp3_files=mp3_files)

@app.route('/play/<filename>')
def play_file(filename):
    file_path = os.path.join(MP3_DIRECTORY, filename)
    processed_audio = process_audio(file_path)
    return send_file(
        processed_audio,
        mimetype='audio/mpeg',
        as_attachment=False,
        download_name=filename
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)