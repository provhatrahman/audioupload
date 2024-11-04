from flask import Flask, render_template, send_file, abort
import os

app = Flask(__name__)

# Supported audio file extensions
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac'}

# Create a dedicated audio folder
AUDIO_FOLDER = os.path.join(os.path.dirname(__file__), 'audio_files')
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

def get_audio_files():
    """Get all audio files from the audio directory"""
    audio_files = []
    for file in os.listdir(AUDIO_FOLDER):
        if any(file.lower().endswith(ext) for ext in AUDIO_EXTENSIONS):
            audio_files.append(file)
    return audio_files

@app.route('/')
def index():
    audio_files = get_audio_files()
    return render_template('index.html', audio_files=audio_files)

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve audio files"""
    # Security check
    if not any(filename.lower().endswith(ext) for ext in AUDIO_EXTENSIONS):
        abort(404)
    
    file_path = os.path.join(AUDIO_FOLDER, filename)
    
    # Prevent directory traversal
    if not os.path.abspath(file_path).startswith(os.path.abspath(AUDIO_FOLDER)):
        abort(404)
        
    if not os.path.exists(file_path):
        abort(404)
        
    return send_file(file_path)

if __name__ == '__main__':
    app.run(debug=False)
