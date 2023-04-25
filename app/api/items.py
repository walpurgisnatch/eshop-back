from flask import jsonify, request, Response
from app import db
from app.models import Item
from app.api import bp


@bp.route('/items', methods=['GET'])
def get_items():
    """Get all items
     ---
    responses:
         200:
           description: return all item
        """
    try:
        limit = int(request.args['limit'])
        offset = int(request.args['offset'])
        #return jsonify(Item.filter(limit, offset, request.args))
        return jsonify(Item.get_all())
    except Exception as e:
        return Response(e, 400, mimetype='application/json')

@bp.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    """Download a file.
    ---
    parameters:
         - in: path
           name: id
           type: int
           required: true
    responses:
        '200':
          description: return item
        """
    return jsonify(Item.get_by_id(id))

@bp.route('/items', methods=['POST'])
def add_item():
    """Add item.
    ---
    responses:
        '200':
          description: item added
        """
    data = request.get_json()
    Item.add_json(data)
    return Response("", 201, mimetype='application/json')


@bp.route('/items', methods=['PUT'])
def update_item():
    """Update item.
    ---
    responses:
        '200':
          description: item updated
        """
    data = request.get_json()
    Item.update_json(data)
    return Response("", 201, mimetype='application/json')
