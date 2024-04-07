from grobid import parse_pdf
from flask import Flask, redirect, flash, render_template, url_for, request, Response
import os
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = 'src/resources/pdf_in'
UPLOAD_FOLDER = 'resources\\pdf_in'
ALLOWED_EXTENSIONS = set(['pdf'])


app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
@app.route("/")
def hello_world():
    flash("hi")
    return '<p>Hello World!</p>'

@app.route("/summarize", methods=['GET', 'POST'])
def summarize():
    if(request.method == 'POST'):
        # check if the post request has the file part
        print("request files:", request.files)
        if 'files' not in request.files:
            print('No pdf file')
            return Response(
                response="<p>No pdf file</p>",
                status=404
            )
        for file in request.files:
            print(file)
        pdf_file = request.files['files']

        if pdf_file.filename == '':
            print('No pdf file selected')
            flash('No pdf file selected')
            return redirect(request.url)
        if pdf_file and allowed_file(pdf_file.filename):
            filename = secure_filename(pdf_file.filename)
            pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("END POST")
        return 'Successfully send files'
    else:
        print("END GET")
        return 'Get sth i dunno'


def main():
    parse_pdf()
    return 

if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = "secret_key"
    app.run(debug=True)
    # main()