from flask import jsonify, request
from app import db
from app.models import Comment
from app.api import bp

@bp.route('/comments', methods=['GET'])
def get_comments():
    """Get Comments.
    ---
    responses:
        '200':
          description: return all comments
        """
    return jsonify(Comment.get_all_comments())

@bp.route('/setComments', methods=['POST'])
def set_comments():
    """Set comments to db.
    ---
    responses:
        '200':
          description: comments added
        """
    data = request.get_json()
    Comment.set_comments(data)
    return Response("", 201, mimetype='application/json')
