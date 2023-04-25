import json
import enum

from flask import Flask, jsonify
from dataclasses import dataclass
from app import db

# class ItemPhoto(db.Model):
#     __tablename__ = 'item_photo'
#     id = db.Column(db.Integer, primary_key=True)
#     link_to_photo = db.Column(db.String(80), nullable=False)

#     def get_photo(_id):
#         return ItemPhoto.query.filter_by(id=_id).first()

#     def add_photo(_link):
#         new_photo = ItemPhoto(link_to_photo=_link)
#         db.session.add(new_photo)
#         try:
#             db.session.commit()
#         except DatabaseError:
#             db.session.rollback()

#     def delete_photo(_id):
#         result = ItemPhoto.query.filter_by(id=_id).delete()
#         try:
#             db.session.commit()
#         except:
#             db.session.rollback()
#         return bool(result)

#     def update_photo(_id, _link):
#         ItemPhoto.query.filter_by(id=_id).first().link_to_photo = _link
#         try:
#             db.session.commit()
#         except:
#             db.session.rollback()

#     def __repr__(self):
#         return "item with id{0} ".format(self.id)

@dataclass
class Comment(db.Model):
    id: int
    item: int
    username: str
    body: str
    response: id
    
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, index=True)
    username = db.Column(db.String(127), index=True)
    body = db.Column(db.String(1023), index=True)
    response = db.Column(db.Integer, index=True)

    def get_all_comments():
        return Comment.query.all()

    def get_by_id(_id):
        return Comment.query.filter_by(id=_id).first()

    def add_comment(_item, _username, _body, _response):
        new_comment = Comment(item=_item, username=_username, body=_body, response=_response)
        db.session.add(new_comment)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

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
    
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), index=True, nullable=False)
    description = db.Column(db.String(127), index=True, nullable=False)
    cost = db.Column(db.Integer, index=True, nullable=False)

    def get_all():
        return Item.query.all()

    def filter(limit, offset, filters = {}):
        query = db.session.query(Item)
        for attr, value in filters.items():
            try:
                query = query.filter(getattr(Item, attr) == value)
            except:
                pass
        count = len(query.all())
        query = query.limit(limit)
        query = query.offset(offset)
        return query.all(), count

    def get_by_id(_id):
        return Item.query.filter_by(id=_id).first()

    def add_item(_name, _description, _cost):
        new_item = Item(name=_name, description=_description, cost=_cost)
        db.session.add(new_item)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def delete(_id):
        result = Item.query.filter_by(id=_id).delete()
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return bool(result)

    def update(_id, _name, _description, _cost):
        new_item = Item.query.filter_by(id=_id).first()
        new_item.name=_name
        new_item.description=_description
        new_item.cost=_cost
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
