class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://shop:shop@localhost/shop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "static"
