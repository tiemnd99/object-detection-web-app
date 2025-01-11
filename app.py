# app.py
from flask import Flask, request, render_template, redirect, url_for, flash
from detect import detect_objects
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # cần thiết cho flash messages
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

"""
Xử lý yêu cầu tải lên tệp từ người dùng.

- Kiểm tra xem yêu cầu có chứa tệp hay không.
- Nếu không có tệp, hiển thị thông báo lỗi và chuyển hướng về trang chủ.
- Nếu có tệp nhưng không có tên tệp, hiển thị thông báo lỗi và chuyển hướng về trang chủ.
- Nếu có tệp hợp lệ, lưu tệp vào thư mục đã cấu hình.
- Gọi hàm `detect_objects` để phát hiện đối tượng trong tệp hình ảnh.
- Hiển thị kết quả phát hiện đối tượng trên trang kết quả.

Trả về:
    Trang HTML hiển thị kết quả phát hiện đối tượng và đường dẫn đến hình ảnh đã xử lý.
"""
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        results, output_path = detect_objects(file_path)
        # Save or process results as needed
        return render_template('results.html', results=results, image_path=output_path.replace('static/', ''))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)
    app.run(debug=True)