from app import db
from flask import Markup, url_for


class Model_OPR(db.Model):
    __bind_key__ = 'opr'
    __tablename__ = 'report'
    index = db.Column(db.Integer, primary_key=True)
    客戶代號 = db.Column(db.String(80))
    客戶名稱 = db.Column(db.String(80))
    日期 = db.Column(db.String(80))
    結帳單號 = db.Column(db.String(80))
    業務員代號 = db.Column(db.String(80))
    發票號碼 = db.Column(db.String(80))
    幣別 = db.Column(db.String(80))
    原幣應收帳款 = db.Column(db.String(80))
    原幣未收帳款 = db.Column(db.String(80))
    匯率 = db.Column(db.String(80))
    憑證號碼 = db.Column(db.String(80))


def list_sales_order(view, context, model, name):
    if model.憑證號碼:
        return Markup('<a href="{}" target="_blank">{}</a>'.format(url_for('open_sales_order', form_no=model.憑證號碼),
                                                                   model.憑證號碼))
    else:
        return ''


# db.create_all()
