from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

# Change to look for MP3s in the music directory
MP3_DIRECTORY = 'music'
os.makedirs(MP3_DIRECTORY, exist_ok=True)

@app.route('/')
def index():
    # Get list of MP3 files from the music directory
    mp3_files = [f for f in os.listdir(MP3_DIRECTORY) if f.endswith('.mp3')]
    return render_template('index.html', mp3_files=mp3_files)

@app.route('/play/<filename>')
def play_file(filename):
    # Serve the MP3 file from the music directory
    return send_file(os.path.join(MP3_DIRECTORY, filename), mimetype='audio/mpeg')

if __name__ == '__main__':
    # Make the app accessible from outside the container
    app.run(debug=True, host='0.0.0.0') 