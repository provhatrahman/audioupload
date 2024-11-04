from flask import Flask, render_template, send_file
import os
import soundfile as sf
import pyloudnorm as pyln
import numpy as np
from pydub import AudioSegment
import tempfile

app = Flask(__name__)

MP3_DIRECTORY = 'music'
TARGET_LUFS = -10  # Target LUFS level
os.makedirs(MP3_DIRECTORY, exist_ok=True)

def normalize_audio(file_path):
    # Convert MP3 to WAV for processing
    audio = AudioSegment.from_mp3(file_path)
    temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    audio.export(temp_wav.name, format='wav')
    
    # Load audio with soundfile
    data, rate = sf.read(temp_wav.name)
    
    # Create meter
    meter = pyln.Meter(rate)
    
    # Measure loudness
    loudness = meter.integrated_loudness(data)
    
    # Calculate gain needed
    gain_db = TARGET_LUFS - loudness
    
    # Normalize audio
    normalized_audio = pyln.normalize.loudness(data, loudness, TARGET_LUFS)
    
    # Save normalized audio to temporary file
    temp_output = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    sf.write(temp_output.name, normalized_audio, rate)
    
    # Clean up temporary WAV file
    os.unlink(temp_wav.name)
    
    return temp_output.name

@app.route('/')
def index():
    mp3_files = sorted([f for f in os.listdir(MP3_DIRECTORY) if f.endswith('.mp3')])
    return render_template('index.html', mp3_files=mp3_files)

@app.route('/play/<filename>')
def play_file(filename):
    file_path = os.path.join(MP3_DIRECTORY, filename)
    
    # Normalize the audio
    normalized_path = normalize_audio(file_path)
    
    response = send_file(
        normalized_path,
        mimetype='audio/mpeg',
        as_attachment=False,
        download_name=filename
    )
    
    # Clean up temporary file after sending
    @response.call_on_close
    def cleanup():
        if os.path.exists(normalized_path):
            os.unlink(normalized_path)
    
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)