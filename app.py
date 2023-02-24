import os
import subprocess
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'cc'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/compile')

    flash('Invalid file type')
    return redirect(request.url)


@app.route('/compile')
def compile():
    try:
        output = subprocess.check_output(['python3', 'compile.py'], timeout=10)
    except subprocess.TimeoutExpired:
        return render_template('error.html', message='Compilation took too long.')

    output = output.decode('utf-8')
    return render_template('result.html', output=output)


if __name__ == '__main__':
    app.run(debug=True)