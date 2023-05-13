from flask import jsonify, request, Response
from app import db
from app.models import Article
from app.api import bp


@bp.route('/articles', methods=['GET'])
def get_articles():
    try:
        if request.args and request.args['limit']:
           limit = int(request.args['limit'])
           offset = int(request.args['offset'])        
           return jsonify(Article.filter(limit, offset))
        return jsonify(Article.get_all())
    except Exception as e:
        return Response(e, 400, mimetype='application/json')

@bp.route('/article/<int:id>', methods=['GET'])
def get_article(id):
    return jsonify(Article.get_by_id(id))

@bp.route('/articles', methods=['POST'])
def add_article():
    data = request.get_json()
    id = Article.add_json(data)
    return Response(f'{id}', 201, mimetype='application/json')

@bp.route('/articles', methods=['PUT'])
def update_article():
    data = request.get_json()
    Article.update_json(data)
    return Response("", 201, mimetype='application/json')
