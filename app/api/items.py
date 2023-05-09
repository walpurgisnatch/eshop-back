from flask import jsonify, request, Response
from app import db
from app.models import Item
from app.api import bp


@bp.route('/items', methods=['GET'])
def get_items():
    try:
        if request.args and request.args['limit']:
           limit = int(request.args['limit'])
           offset = int(request.args['offset'])        
           return jsonify(Item.filter(limit, offset))
        return jsonify(Item.get_all())
    except Exception as e:
        return Response(e, 400, mimetype='application/json')

@bp.route('/item/<int:id>', methods=['GET'])
def get_item(id):
    return jsonify(Item.get_by_id(id))

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
