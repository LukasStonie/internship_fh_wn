import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'app.db'
APPDATA = 'appdata'

class Config:
    SECRET_KEY = "df0531cefc6c2b9a5d0208b726a5d1c0fd37324feba25506"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DATABASE)
    APPDATA_PATH = os.path.join(basedir, APPDATA)
