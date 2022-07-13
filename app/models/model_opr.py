from app import db


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


# db.create_all()
