Outstanding_Payment_Report

config.py
=========
```python
from urllib.parse import quote_plus

db_cfg = dict(
    server="erp_db_ip",
    username="erp_db_username",
    password=quote_plus("erp_db_password"),
    db_name="erp_db_name",
)

opr_cfg = dict(
    opr_host="mysql_db_ip",
    opr_user="mysql_db_user",
    opr_password="mysql_db_password",
    opr_port="mysql_db_port",
    opr_db="mysql_db_name",
    opr_charset="utf8",
)

mysql_url = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(
    opr_cfg["opr_user"],
    opr_cfg["opr_password"],
    opr_cfg["opr_host"],
    opr_cfg["opr_port"],
    opr_cfg["opr_db"],
    opr_cfg["opr_charset"],
)
```