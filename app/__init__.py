from flask_admin import Admin
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../app_config.py')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from app.models import *
from app.views import *

admin = Admin(app, name='逾期應收帳款')
admin.add_view(view_opr.View_OPR(model_opr.Model_OPR, db.session, name='逾期應收帳款'))
app.run(host='192.168.88.80', port=7711, debug=True)
