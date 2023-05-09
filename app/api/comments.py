from flask import jsonify, request, Response
from app import db
from app.models import Comment
from app.api import bp

@bp.route('item/<int:id>/comments', methods=['GET'])
def item_comments(id):
    return jsonify(Comment.get_by_id_item(id))

@bp.route('article/<int:id>/comments', methods=['GET'])
def article_comments(id):
    return jsonify(Comment.get_by_id_article(id))

@bp.route('/comments', methods=['POST'])
def add_comment():
    data = request.get_json()
    Comment.add_json(data)
    return Response("", 201, mimetype='application/json')
