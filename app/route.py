from app import app
from flask import redirect


@app.route('/static/sales_order/<path:form_no>')
def open_sales_order(form_no):
    form_type = form_no.split('-')[0]
    form_number = form_no.split('-')[1]
    return redirect('/static/sales_order.html?TH001={}&TH002={}'.format(form_type, form_number))
