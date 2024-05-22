import os
from grobid import parse_pdf
from zotero import Zotero
from flask import Flask, request, Response, jsonify, session
from werkzeug.utils import secure_filename
import config
import xml_parser
import summary
import json

UPLOAD_FOLDER = config.get_upload_path()
SEGMENT_FOLDER = config.get_segment_path()
ALLOWED_EXTENSIONS = ['pdf', 'Pdf', 'PDF']
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret_key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
def flask_log(content):
    app.logger.info(content) 

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

@app.route("/getPdfFileZotero", methods=['GET', 'POST'])
async def getPdfFileZotero():
    app.logger.info(dict(request.headers))
    keys = set(request.headers.keys())
    if(
        'Item-Key' not in keys
        or 'Api-Key' not in keys
        or 'Library-Type' not in keys
        or 'Library-Id' not in keys     
    ): 
        app.logger.error("Required keys are missing from headers")
        return Response(
            status = 400, 
            response = "Required keys are missing from headers"
        )    
    api_key = request.headers.get("Api-Key")
    library_type = request.headers.get("Library-Type")
    library_id = request.headers.get("Library-Id")
    item_key = request.headers.get("Item-Key")

    if(item_key == None):
        return Response(
            status = 400,
            response = "Required values are missing from heaaders"
        )

    zot = Zotero(library_id, library_type, api_key)
    result = await zot.get_pdf_file(item_key, UPLOAD_FOLDER)

    if(result):
        return Response(
            status = 200,
            response = "Succesfully retrieved corresponding PDF file."
        )
    else:
        return Response (
            status = 400, 
            response = "Failed to retrieved corresponding PDF file."
        )

@app.route("/getAllPdfFileZotero", methods=['GET'])
async def getAllPdfFilesZotero():
    app.logger.info(dict(request.headers))
    keys = set(request.headers.keys())
    if(
        'Item-Key' not in keys
        or 'Api-Key' not in keys
        or 'Library-Type' not in keys
        or 'Library-Id' not in keys     
    ):
        app.logger.error("Required keys are missing from headers")
        
        return Response(
            status = 400, 
            response = "Required keys are missing from headers"
        )    
    api_key = request.headers.get("Api-Key")
    library_type = request.headers.get("Library-Type")
    library_id = request.headers.get("Library-Id")
    item_key = request.headers.get("Item-Key")

    if(item_key == None):
        return Response(
            status = 400,
            response = "Required values are missing from heaaders"
        )

    zot = Zotero(library_id, library_type, api_key)
    result = await zot.get_pdf_file(item_key, None, UPLOAD_FOLDER)
    if(result):
        return Response(
            status = 200,
            response = "Succesfully retrieved corresponding PDF file."
        )
    else:
        return Response (
            status = 400, 
            response = "Failed to retrieved corresponding PDF file."
        )

@app.route("/summarize", methods=['POST'])
async def summarize():
    keys = set(request.headers.keys())
    if('Sum-Algo' not in keys):
        app.logger.error("Required keys are missing from headers")
        return Response(
            status = 400, 
            response = "Required keys are missing from headers"
        )
    sum_algo = request.headers.get("Sum-Algo")
    preprocess_algo = request.headers.get("Preprocess-Algo")
    result = await parse_pdf()
    if(not result):
        return Response(
            status=500,
            response = "Failed to contact GROBID server"
        ) 
    papers = xml_parser.parse_xml_folder()
    s_papers = summary.summarize_folder(papers, preprocess_algo, sum_algo)
    summary.save_to_folder(s_papers)
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
    app.run(debug=False, threaded = True)

    # summarize()
