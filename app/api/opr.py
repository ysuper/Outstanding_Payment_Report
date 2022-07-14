from app import app
from .connect import get_ERP_table


@app.route('/erp/get/COPTH/<TH001>/<TH002>', methods=['GET'])
def get_COPTH(TH001, TH002):
    """
    回傳 COPTH(銷貨單單身) 相關資料
    ---
    tags:
      - ERP COPTH API
    parameters:
      - name: TH001
        in: path
        type: string
        required: true
      - name: TH002
        in: path
        type: string
        required: true
    responses:
      200:
        description: "(範例)TH001:231 TH002:20220711001"
    """

    sql = "SELECT * FROM COPTH where TH001 = '{}' and TH002 = '{}'".format(TH001, TH002)

    return get_ERP_table(sql)
