import os
from grobid import parse_pdf
from zotero import Zotero
from flask import Flask, request, Response, render_template
from werkzeug.utils import secure_filename
import config
import xml_parser
import summary
import json
from paper import Paper
import nltk
import asyncio

UPLOAD_FOLDER = config.get_upload_path()
SEGMENT_FOLDER = config.get_segment_path()
ALLOWED_EXTENSIONS = ['pdf', 'Pdf', 'PDF']
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret_key'
nltk.download('punkt')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
def flask_log(content):
    app.logger.info(content) 

@app.route("/", methods=['GET', 'POST'])
async def hello_world():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "PDF file has not been chosen", 400

        file = request.files['file']
        if file.filename == '':
            return "PDF file has not been chosen", 400

        if 'preprocessing' not in request.form:
            return "Preprocessing has not been chosen", 400
        preprocessing = request.form['preprocessing']

        if 'processing' not in request.form:
            return "Processing has not been chosen", 400
        processing = request.form['processing']

        # Save file to folder
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Create PDF Segment
        result = await parse_pdf()
        if not result:
            return "Failed to contact GROBID server", 500

        # Parse PDF segment
        papers = xml_parser.parse_xml_folder(filename)

        # Summarize paper
        s_papers = await summary.summarize_folder(papers, preprocessing, processing)
        
        app.logger.info("[s_paper] " + str(s_papers[0].to_json_format()))

        # Generate the result HTML
        result_html = await div_result_html(s_papers)
        return result_html, 200

    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload():
    if (request.method != 'POST'):
        return "No GET method"

    # If header 'files' is not in the payload 
    if 'files' not in request.files:
        print('No pdf file')
        return "No 'files' header in payload.", 404
        
    pdf_file = request.files['files']

    # If the file has no name
    if pdf_file.filename == '':
        print('No pdf file selected')
        return "File has no name.", 404
        
    # If the file does not exist 
    if not pdf_file: 
        return "File does not exist.", 404
        
    # If the extension does not end with .pdf
    if not allowed_file(pdf_file.filename):
        return "File does not end with .pdf", 404

    filename = secure_filename(pdf_file.filename)
    pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    print("END POST")
    return 'Successfully send files', 200

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
        return "Required keys are missing form headers.", 400
        # return Response(
        #     status = 400, 
        #     response = "Required keys are missing from headers"
        # )    
    api_key = request.headers.get("Api-Key")
    library_type = request.headers.get("Library-Type")
    library_id = request.headers.get("Library-Id")
    item_key = request.headers.get("Item-Key")

    if(item_key == None):
        return "Required values are missing form headers", 400
        # return Response(
        #     status = 400,
        #     response = "Required values are missing from heaaders"
        # )

    zot = Zotero(library_id, library_type, api_key)
    result = await zot.get_pdf_file(item_key, UPLOAD_FOLDER)

    if(result):
        return "Successfully retrieved corresponding PDF file", 200
        # return Response(
        #     status = 200,
        #     response = "Succesfully retrieved corresponding PDF file."
        # )
    else:
        return "Failed to retrieved corresponding PDF file", 400
        # return Response (
        #     status = 400, 
        #     response = "Failed to retrieved corresponding PDF file."
        # )

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
        return "Required keys are missing from headers", 400
        # return Response(
        #     status = 400, 
        #     response = "Required keys are missing from headers"
        # )    
    api_key = request.headers.get("Api-Key")
    library_type = request.headers.get("Library-Type")
    library_id = request.headers.get("Library-Id")
    item_key = request.headers.get("Item-Key")

    if(item_key == None):
        return "Required values are missing from headers", 400
        # return Response(
        #     status = 400,
        #     response = "Required values are missing from heaaders"
        # )

    zot = Zotero(library_id, library_type, api_key)
    result = await zot.get_pdf_file(item_key, None, UPLOAD_FOLDER)
    if result:
        return "Successfully retrieved corresponding PDF file."
        return Response(
            status = 200,
            response = "Succesfully retrieved corresponding PDF file."
        )
    else:
        return "Failed to retrieved corresponding PDF file.", 400
        # return Response (
        #     status = 400, 
        #     response = "Failed to retrieved corresponding PDF file."
        # )

@app.route("/summarize", methods=['POST'])
async def summarize():
    keys = set(request.headers.keys())
    if ('Sum-Algo' not in keys 
        or 'Preprocess-Algo' not in keys):
        app.logger.error("Required keys are missing from headers")
        return "Required keys are missing from headers", 400
        
    sum_algo = request.headers.get("Sum-Algo")
    preprocess_algo = request.headers.get("Preprocess-Algo")
    result = await parse_pdf()
    if not result:
        return "Failed to contact GROBID server", 500
        
    # Parse PDF segment
    # papers = xml_parser.parse_xml_folder()
    # Parse PDF segment
    papers = xml_parser.parse_xml_folder()

    # Summarize paper
    # s_papers = summary.summarize_folder(papers, preprocess_algo, sum_algo)
    s_papers = await summary.summarize_folder(papers, preprocess_algo, sum_algo)
    
    summary.save_to_folder(s_papers)
    
    # Delete all files after parsing
    paper_json_list = []
    for s_paper in s_papers:
        paper_json_list.append(s_paper.to_json_format())
        
    return json.dumps(paper_json_list), 200
    

def div_error_html(error_list:list[str]) -> str:
    result = '<div id="notification" class="error-notification container">\n'
    for e in error_list:
        result += '<p class="error-text atkinson-hyperlegible-bold">' + e + '</p>'
    result += '</div>'
    return result

async def div_result_html(s_papers:list[Paper]) -> str:
    result = ""
    for s_paper in s_papers:
        result = '<div id="result" class="container result">\n' 
        for segment in s_paper.get_segment_list():
            result += '<h2 class="atkinson-hyperlegible-bold">' + segment.get_header() + '</h2>'
            result += '<p class="atkinson-hyperlegible-regular">' + segment.get_content() + '</p>'
        result += '</div>'
    return result

if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = "secret_key"
    app.run(debug=False, threaded = True)

    # summarize()
