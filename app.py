from flask import Flask, request, jsonify, render_template, redirect
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
    data = request.get_data()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, 'wb') as f:
        f.write(data)

    detected = detect_person(filepath)

    if detected:
        send_telegram(filepath, f"🚨 Phát hiện người lúc {timestamp}")
        return jsonify({'result': 'person_detected', 'filename': filename}), 200
    else:
        return jsonify({'result': 'no_person', 'filename': filename}), 200

# === Thêm 3 route mới ở đây ===
@app.route('/toggle-flash', methods=['POST'])
def toggle_flash():
    print("⚡ Yêu cầu bật/tắt flash")
    return redirect('/')

@app.route('/manual-capture', methods=['POST'])
def manual_capture():
    print("📸 Yêu cầu chụp ảnh thủ công")
    return redirect('/')

@app.route('/delete-images', methods=['POST'])
def delete_images():
    folder = 'static/images'
    for filename in os.listdir(folder):
        if filename.endswith('.jpg'):
            os.remove(os.path.join(folder, filename))
    print("🗑️ Đã xóa toàn bộ ảnh")
    return redirect('/')

# === Kết thúc ===

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
