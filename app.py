import os
import subprocess
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'cc'}


app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
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
            return redirect(url_for('compile'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Hemant Gautam's Autograder</h1>
    <form method=post enctype=multipart/form-data>
    <h2><b>Please Select "walk.cc"</h2>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/compile')
def compile():
    file_path = os.path.join(os.getcwd(), 'compile.py')
    output = subprocess.check_output(['python3', file_path])
    output = output.decode('utf-8')

    output= f'<pre>{output}</pre>'
    return render_template('result.html', output=output)

if __name__ == "__main__":
    app.secret_key = 'secret key'
    app.debug = True
    app.run(host='0.0.0.0', debug=True)
