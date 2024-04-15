import os
from grobid import parse_pdf
from flask import Flask, request, Response, jsonify
from werkzeug.utils import secure_filename
import config
import xml_parser
import textrank
import json

UPLOAD_FOLDER = '/code/resources/pdf_in'
SEGMENT_FOLDER = '/code/resources/pdf_segment'
ALLOWED_EXTENSIONS = set(['pdf'])

# UPLOAD_FOLDER = 'resources\\pdf_in'
# SEGMENT_FOLDER = 'resources\\pdf_segment'

UPLOAD_FOLDER = config.get_upload_path()
SEGMENT_FOLDER = config.get_segment_path()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret_key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
@app.route("/")
def hello_world():
    return '<p>Hello World!</p>'

@app.route("/upload", methods=['POST'])
def upload():
    if (request.method != 'POST'):
        return "No GET method"

    # If header 'files' is not in the payload 
    if 'files' not in request.files:
        print('No pdf file')
        return Response(
            response="No 'files' header in payload.",
            status=404
        )
        
    pdf_file = request.files['files']

    # If the file has no name
    if pdf_file.filename == '':
        print('No pdf file selected')
        return Response(
            response="File has no name.",
            status=404
        )
        
    # If the file does not exist 
    if not pdf_file: 
        return Response(
            response="File does not exist.",
            status=404
        )
        
    # If the extension does not end with .pdf
    if not allowed_file(pdf_file.filename):
        return Response(
            response="File does not end with .pdf",
            status=404
        )    

    filename = secure_filename(pdf_file.filename)
    pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    print("END POST")
    return 'Successfully send files'

@app.route("/summarize", methods=['POST'])
def summarize():
    # parse_pdf()
    papers = xml_parser.parse_xml_folder()
    s_papers = textrank.summarize_folder(papers)
    textrank.save_to_folder(s_papers)
    # Delete all files after parsing
    paper_json_list = []
    for s_paper in s_papers:
        paper_json_list.append(s_paper.to_json_format())
    return Response(
        status=200,
        response=json.dumps(paper_json_list)
    )
if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = "secret_key"
    app.run(debug=True)

    # summarize()