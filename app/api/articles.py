from flask import jsonify, request, Response
from app import db
from app.models import Article
from app.api import bp


@bp.route('/articles', methods=['GET'])
def get_articles():
    """Get all articles
     ---
    responses:
         200:
           description: return all article
        """
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
    """Download a file.
    ---
    parameters:
         - in: path
           name: id
           type: int
           required: true
    responses:
        '200':
          description: return article
        """
    return jsonify(Article.get_by_id(id))

@bp.route('/articles', methods=['POST'])
def add_article():
    """Add article.
    ---
    responses:
        '200':
          description: article added
        """
    data = request.get_json()
    Article.add_json(data)
    return Response("", 201, mimetype='application/json')


@bp.route('/articles', methods=['PUT'])
def update_article():
    """Update article.
    ---
    responses:
        '200':
          description: article updated
        """
    data = request.get_json()
    Article.update_json(data)
    return Response("", 201, mimetype='application/json')
