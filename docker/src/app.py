import os
from tasks.grobid import parse_pdf
from tasks.zotero import Zotero
from flask import Flask, request, Response, render_template
from werkzeug.utils import secure_filename
import tasks.xml_parser as xml_parser
import tasks.summary as summary
import json
from tasks.paper import Paper
import tasks

UPLOAD_FOLDER = tasks.get_upload_path()
SEGMENT_FOLDER = tasks.get_segment_path()
SUMMARY_FOLDER = tasks.get_summary_path()
ALLOWED_EXTENSIONS = ['pdf', 'Pdf', 'PDF']
app = Flask(__name__)

app.tasks['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'secret_key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
def flask_log(content):
    app.logger.info(content) 

@app.route("/", methods=['GET', 'POST'])
async def hello_world():
    if(request.method == 'POST'):
        if 'file' not in request.files:
            error_html = div_error_html(["PDF file has not been chosen"])
            return render_template('index.html', error=error_html), 400

        file = request.files['file']
        if file.filename == '':
            error_html = div_error_html(["PDF file has not been chosen"])
            return render_template('index.html', error=error_html), 400
        
        if 'preprocessing' not in request.form:
            error_html = div_error_html(["Preprocessing has not been chosen"])
            return render_template('index.html', error=error_html), 400
        preprocessing = request.form['preprocessing']

        if 'processing' not in request.form:
            error_html = div_error_html(["Processing has not been chosen"])
            return render_template('index.html', error=error_html), 400
        processing = request.form['processing']

        # Save file to folder
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.tasks['UPLOAD_FOLDER'], filename))
        
        # Create PDF Segment
        result = await parse_pdf()
        if(not result):
            error_html = div_error_html(["Failed to contact GROBID server"])
            return render_template('index.html', error=error_html), 500

        # Parse PDF segment
        app.logger.info("Before parse_xml_folder")
        xml_parser.parse_xml_folder.delay()
        
        app.logger.info("Before summarize_folder")
        summary.summarize_folder.delay(preprocessing, processing)
        # s_papers = jsonpickle.decode(s_papers)

        # Delete all files after parsing
        result_html = div_result_html(filename) 
        return render_template('index.html', result=result_html), 200

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
    pdf_file.save(os.path.join(app.tasks['UPLOAD_FOLDER'], filename))
        
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
  
    api_key = request.headers.get("Api-Key")
    library_type = request.headers.get("Library-Type")
    library_id = request.headers.get("Library-Id")
    item_key = request.headers.get("Item-Key")

    if(item_key == None):
        return "Required values are missing form headers", 400

    zot = Zotero(library_id, library_type, api_key)
    result = await zot.get_pdf_file(item_key, UPLOAD_FOLDER)

    if(result):
        return "Successfully retrieved corresponding PDF file", 200
    else:
        return "Failed to retrieved corresponding PDF file", 400


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
   
    api_key = request.headers.get("Api-Key")
    library_type = request.headers.get("Library-Type")
    library_id = request.headers.get("Library-Id")
    item_key = request.headers.get("Item-Key")

    if(item_key == None):
        return "No item key", 400

    zot = Zotero(library_id, library_type, api_key)
    result = await zot.get_pdf_file(item_key, None, UPLOAD_FOLDER)
    if result:
        return "Successfully retrieved corresponding PDF file.", 200
    else:
        return "Failed to retrieved corresponding PDF file.", 400


@app.route("/summarize", methods=['POST'])
async def summarize():
    keys = set(request.headers.keys())
    if 'Sum-Algo' not in keys:
        app.logger.error("Required keys are missing from headers")
        return "Required keys are missing from headers", 400
    sum_algo = request.headers.get("Sum-Algo")
    preprocess_algo = request.headers.get("Preprocess-Algo")
    result = await parse_pdf()
    if not result:
        return "Failed to contact GROBID server", 500
 
    papers = xml_parser.parse_xml_folder()
    s_papers = summary.summarize_folder(papers, preprocess_algo, sum_algo)
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

def div_result_html(filename:str) -> str: 
    paper = tasks.get_paper_from_folder(SUMMARY_FOLDER, filename, "json")
    app.logger.info(paper)
    s_papers = [paper]
    for s_paper in s_papers:
        result = '<div id="result" class="container result">\n' 
        for segment in s_paper.get_segment_list():
            result += '<h2 class="atkinson-hyperlegible-bold">' + segment.get_header() + '</h2>'
            result += '<p class="atkinson-hyperlegible-regular">' + segment.get_content() + '</p>'
        result += '</div>'
    return result

if __name__ == "__main__":
    app.tasks['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = "secret_key"
    app.run(debug=False, threaded = True)

    # summarize()
