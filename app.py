from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
from detect import detect_person
from telegram_bot import send_telegram

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    images = sorted(os.listdir(UPLOAD_FOLDER), reverse=True)
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image uploaded'}), 400

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Nhận diện người trong ảnh
    detected = detect_person(filepath)

    if detected:
        send_telegram(filepath, f"🚨 Phát hiện người lúc {timestamp}")
        return jsonify({'result': 'person_detected', 'filename': filename}), 200
    else:
        return jsonify({'result': 'no_person', 'filename': filename}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
