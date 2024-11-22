from flask import Flask, render_template, send_file
import os
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

app = Flask(__name__)

MP3_DIRECTORY = 'music'
os.makedirs(MP3_DIRECTORY, exist_ok=True)

@app.route('/')
def index():
    mp3_files = sorted([f for f in os.listdir(MP3_DIRECTORY) if f.endswith('.mp3')],
                      key=natural_sort_key)
    return render_template('index.html', mp3_files=mp3_files)

@app.route('/play/<filename>')
def play_file(filename):
    file_path = os.path.join(MP3_DIRECTORY, filename)
    return send_file(
        file_path,
        mimetype='audio/mpeg',
        as_attachment=False,
        download_name=filename
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)