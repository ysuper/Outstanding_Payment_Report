from config import db_cfg
from app import app
from urllib.parse import unquote_plus
from decimal import Decimal
from flask_cors import CORS
from flasgger import Swagger
import pymssql
import json

CORS(app)
Swagger(app)


def get_ERP_table(sqlcmd):

    host = db_cfg["server"]
    port = '1433'
    user = db_cfg["username"]
    password = unquote_plus(db_cfg["password"])
    dbname = db_cfg["db_name"]

    db = pymssql.connect(host=host, port=port, user=user, password=password, database=dbname)
    cursor = db.cursor()

    try:
        cursor.execute(sqlcmd)
        results = cursor.fetchall()
        items = [dict(zip([key[0] for key in cursor.description], row)) for row in results]
        json_string = json.dumps(items, indent=4, ensure_ascii=False, cls=AdvancedJSONEncoder)
    except Exception as e:
        print(e)
    finally:
        db.close()
    return json_string


class AdvancedJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
