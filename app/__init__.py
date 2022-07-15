from flask_admin import Admin
from flask import Flask, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_pyfile('../app_config.py')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from app.route import *
from app.api import *
from app.models import *
from app.views import *

admin = Admin(app, name='逾期應收帳款')
admin.add_view(view_opr.View_OPR(model_opr.Model_OPR, db.session, name='逾期應收帳款'))
app.run(host='192.168.88.80', port=7711, debug=True)
