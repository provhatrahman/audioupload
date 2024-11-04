from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

MP3_DIRECTORY = 'music'
os.makedirs(MP3_DIRECTORY, exist_ok=True)

@app.route('/')
def index():
    mp3_files = [f for f in os.listdir(MP3_DIRECTORY) if f.endswith('.mp3')]
    return render_template('index.html', mp3_files=mp3_files)

@app.route('/play/<filename>')
def play_file(filename):
    return send_file(os.path.join(MP3_DIRECTORY, filename), mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True) 