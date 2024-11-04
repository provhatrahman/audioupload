from flask import Flask, render_template, redirect, url_for, abort
import os
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# AWS Configuration
S3_BUCKET = os.environ.get('AWS_BUCKET_NAME')
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
)

AUDIO_EXTENSIONS = {'.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac'}

def get_audio_files():
    """Get all audio files from S3 bucket"""
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        audio_files = []
        for obj in response.get('Contents', []):
            if any(obj['Key'].lower().endswith(ext) for ext in AUDIO_EXTENSIONS):
                audio_files.append(obj['Key'])
        return audio_files
    except ClientError:
        return []

@app.route('/')
def index():
    audio_files = get_audio_files()
    return render_template('index.html', audio_files=audio_files)

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Generate presigned URL for audio files"""
    try:
        url = s3_client.generate_presigned_url('get_object',
                                            Params={'Bucket': S3_BUCKET,
                                                    'Key': filename},
                                            ExpiresIn=3600)
        return redirect(url)
    except ClientError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=False)
