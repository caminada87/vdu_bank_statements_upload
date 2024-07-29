import pyodbc, datetime, binascii
from io import BytesIO
from ..logging.logger import get_module_logger
from flask import Blueprint, current_app, request, flash, make_response, jsonify
from werkzeug.utils import secure_filename
#from bson.binary import Binary
bp = Blueprint("upload", __name__)
logger = get_module_logger(__name__)

logger.info("Driver, Server, DB, User, Allowed Extensions:")
#logger.info(current_app.config['DRIVER'])
#logger.info(current_app.config['SERVER'])
#logger.info(current_app.config['DB'])
#logger.info(current_app.config['USER'])
#logger.info(current_app.config['ALLOWED_EXTENSIONS'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route("/upload", methods=(['POST']))
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        logger.info('Request with no file part has been denied.')
        response = {'filename': 'None', 'error': 'No file part'}
        return make_response(jsonify(response), 420)
    file: werkzeug.datastructures.file_storage.FileStorage = request.files['file']
    logger.info('New file about to be uploaded.')
    logger.info(file)
    logger.info(file.content_length)
    logger.info(file.content_type)
    logger.info(file.mimetype)
    logger.info(file.mimetype_params)
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        logger.info('Request with an empty file has been denied.')
        response = {'filename': 'None', 'error': 'No selected file'}
        return make_response(jsonify(response), 420)

    # Always sanitize your user inputs :)
    filename = secure_filename(file.filename)

    # check if the filetype is allowed
    if not allowed_file(filename):
        logger.info('Request with a wrong file format has been denied.')
        response = {'filename': filename, 'error': 'File format not allowed'}
        return make_response(jsonify(response), 415)
    
    filesize = request.form['file_size']

    if int(filesize) > 10000000:
        logger.info('Request with a file exeeding 10MB has been denied.')
        response = {'filename': filename, 'error': 'File exeeds 10MB'}
        return make_response(jsonify(response), 413)
    
     # upload the file
    logger.info('1')
    if file:
        logger.info('2')
        try: 
            logger.info('3')
            logger.info(current_app.config['DRIVER'])
            connKstaDiversesTest = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s;Encrypt=yes;TrustServerCertificate=YES' % ( current_app.config['DRIVER'], current_app.config['SERVER'], current_app.config['DB'], current_app.config['USER'], current_app.config['PASSWORD'] ))
            logger.info('connection string:')
            logger.info(connKstaDiversesTest)
            buffer = BytesIO()
            file.save(buffer)
            bindata  = buffer.getvalue()
            base_query = "INSERT INTO [KSTADiverses_Test].[dbo].[vdu_bank_statements] (CreationDateTime, FileBinary, ProcessingStatus) VALUES (?,?,?)"
            params = (str(datetime.datetime.now()), pyodbc.Binary(bindata), 1)
            #query = base_query.format(str(datetime.datetime.now()), mssql_varbinary, 1)
            cursor = connKstaDiversesTest.cursor()
            queryResult = cursor.execute(base_query, params)
            cursor.commit()
            cursor.close()

            logger.info('Upload finished.')
            response = {"message":"successfully uploaded"}
            return make_response(jsonify(response), 200)
        except Exception as e:
            logger.error('Database query failed with the following error:')
            logger.error(e)
            response = {"message":"upload failed"}
            return make_response(jsonify(response), 500)