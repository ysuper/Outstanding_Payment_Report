from app import app
from config import opr_cfg

app.config['SECRET_KEY'] = '80689917'
app.config['FLASK_ADMIN_SWATCH'] = 'spacelab'
app.config['SQLALCHEMY_BINDS'] = {
    'opr':
        'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format( \
            opr_cfg["opr_user"], \
            opr_cfg["opr_password"], \
            opr_cfg["opr_host"], \
            opr_cfg["opr_port"], \
            opr_cfg["opr_db"], \
            opr_cfg["opr_charset"] \
        )
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['WTF_CSRF_ENABLED'] = False
