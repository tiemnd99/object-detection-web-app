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