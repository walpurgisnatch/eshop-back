from flask import jsonify, request, send_from_directory, Response
from app import app
from app import db
from app import allowed_extensions
from app.models import Item
from app.api import bp
from werkzeug.utils import secure_filename
import os
import json

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@bp.route('/items', methods=['GET'])
def get_items():
    try:
        if request.args and request.args['limit']:
           limit = int(request.args['limit'])
           offset = int(request.args['offset'])
           filters = json.loads(request.args['filters'])
           print(filters)
           return jsonify(Item.filter(limit, offset, filters))
        return jsonify(Item.get_all())
    except Exception as e:
        return Response(e, 400, mimetype='application/json')

@bp.route('/item/<int:id>', methods=['GET'])
def get_item(id):
    return jsonify(Item.get_by_id(id))

@bp.route('/items/photos', methods=['POST'])
def add_item_photo():
    if 'file' not in request.files:
        print('No file')
        return Response('', 500, mimetype='application/json')
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return Response('', 500, mimetype='application/json')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return Response('', 201, mimetype='application/json')

@bp.route('/photos/<path:name>', methods=['GET'])
def get_picture(name):
    folder = os.path.join('../', app.config['UPLOAD_FOLDER'])
    try:
        return send_from_directory(folder, name)
    except Exception as e:
        return Response(e, 400, mimetype='application/json')

@bp.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    id = Item.add_json(data)
    return Response(f'{id}', 201, mimetype='application/json')

@bp.route('/items', methods=['PUT'])
def update_item():
    data = request.get_json()
    id = Item.update_json(data)
    return Response(f'{id}', 201, mimetype='application/json')

@bp.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    Item.delete(id)
    return Response('', 201, mimetype='application/json')
