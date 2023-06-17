import json
import enum
import math

from flask import Flask, jsonify
from dataclasses import dataclass
from app import app
from app import db
from app import server_path


@dataclass
class Comment(db.Model):
    id: int
    item: int
    article: int
    username: str
    body: str
    response: id
    
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, index=True)
    article = db.Column(db.Integer, index=True)
    username = db.Column(db.String(127), index=True)
    body = db.Column(db.String(2047), index=True, nullable=False)
    response = db.Column(db.Integer, index=True)

    def get_all_comments():
        return Comment.query.all()

    def get_by_id_item(_id):
        return Comment.query.filter_by(item=_id).all()

    def get_by_id_article(_id):
        return Comment.query.filter_by(article=_id).all()

    def add_comment(_item, _article, _username, _body, _response):
        new_comment = Comment(item=_item, article=_article, username=_username, body=_body, response=_response)
        db.session.add(new_comment)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def add_json(comment):
        Comment.add_comment(comment['item'], comment['article'], comment['username'], comment['body'], comment['response'])

    def delete_comment(_id):
        result = Comment.query.filter_by(id=_id).delete()
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return bool(result)

@dataclass
class Item(db.Model):
    id: int
    name: str
    description: str
    cost: int
    pictures: str
    thumbnail: str
    
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), index=True, nullable=False)
    description = db.Column(db.Text, index=True, nullable=False)
    cost = db.Column(db.Integer, index=True, nullable=False)
    pictures = db.Column(db.Text)
    thumbnail = db.Column(db.String(127))

    def get_all():
        return Item.query.all()

    def filter(limit, offset, filters = {}):
        query = db.session.query(Item)
        for attr, value in filters.items():
            try:
                query = query.filter(getattr(Item, attr).like(f'%{value}%'))
            except:
                pass
        count = math.ceil(query.count() / limit)
        query = query.limit(limit)
        query = query.offset(offset*limit)
        return query.all(), count

    def prepare_picture_paths(item):
        if not item.pictures: return item
        pictures = item.pictures.split('; ')
        item.pictures = []
        for picture in pictures:
            item.pictures.append(f'{server_path}/api/photos/{picture}')
        return item

    def get_by_id(_id):
        return Item.prepare_picture_paths(Item.query.filter_by(id=_id).first())

    def add_item(_name, _description, _cost, _pictures):
        _thumbnail = f"{server_path}/api/photos/{_pictures.split('; ')[0]}"
        new_item = Item(name=_name, description=_description, cost=_cost, pictures=_pictures, thumbnail=_thumbnail)
        db.session.add(new_item)
        try:
            db.session.commit()
            return new_item.id
        except Exception as e:
            print(e)
            db.session.rollback()

    def add_json(item):
        return Item.add_item(item['name'], item['description'], item['cost'], item['pictures'])

    def delete(_id):
        result = Item.query.filter_by(id=_id).delete()
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return bool(result)

    def update(_id, _name, _description, _cost, _pictures):
        _thumbnail = f"{server_path}/api/photos/{_pictures.split('; ')[0]}"
        new_item = Item.query.filter_by(id=_id).first()
        new_item.name=_name
        new_item.description=_description
        new_item.cost=_cost
        new_item.pictures=_pictures
        new_item.thumbnail=_thumbnail
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def update_json(item):
        Item.update(item['id'], item['name'], item['description'], item['cost'], item['pictures'])

@dataclass
class Article(db.Model):
    id: int
    title: str
    body: str
    attachments: int
    rating: int
    
    __tabletitle__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(63), index=True, nullable=False)
    body = db.Column(db.Text, index=True, nullable=False)
    attachments = db.Column(db.String(10000), index=True)
    rating = db.Column(db.Integer, index=True, nullable=False)

    def get_all():
        return Article.query.all()

    def filter(limit, offset, filters = {}):
        query = db.session.query(Article)
        count = math.ceil(len(query.all()) / limit)
        query = query.limit(limit)
        query = query.offset(offset*limit)
        return query.all(), count

    def get_by_id(_id):
        return Article.query.filter_by(id=_id).first()

    def add_article(_title, _body, _attachments):
        new_article = Article(title=_title, body=_body, attachments=_attachments, rating=0)
        db.session.add(new_article)
        try:
            db.session.commit()
            return new_article.id
        except Exception as e:
            print(e)
            db.session.rollback()

    def add_json(article):
        return Article.add_article(article['title'], article['body'], article['attachments'])

    def delete(_id):
        result = Article.query.filter_by(id=_id).delete()
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return bool(result)

    def update(_id, _title, _body, _attachments, _rating):
        new_article = Article.query.filter_by(id=_id).first()
        new_article.title=_title
        new_article.body=_body
        new_article.attachments=_attachments,
        new_article.rating=_rating
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def update_json(article):
        Article.update(article['id'], article['title'], article['body'], article['attachments'], article['rating'])
