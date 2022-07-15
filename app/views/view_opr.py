from flask_admin.contrib.sqla import ModelView
from app.models.model_opr import *


class View_OPR(ModelView):
    column_default_sort = ('index', True)
    column_display_pk = False
    page_size = 50
    can_set_page_size = True
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True
    can_export = True
    export_types = ['xlsx']
    columns = ('客戶代號', '客戶名稱', '日期', '結帳單號', '業務員代號', '發票號碼', '幣別', '原幣應收帳款', '原幣未收帳款', '匯率', '憑證號碼')
    column_list = columns
    column_details_list = columns
    column_searchable_list = columns
    column_sortable_list = columns
    column_filters = columns
    column_formatters = {'憑證號碼': list_sales_order}
