import pandas as pd
from loguru import logger
from rich import print
from tabulate import tabulate
from datetime import datetime

from config import db_cfg
from dserp.acrta import ACRTA
from dserp.acrtc import ACRTC
from dserp.copma import COPMA
from dserp.common import COMMON
from necessary_columns import change_columns, necessary_columns, to_list_official, cc_list_official
from outstanding_payment_report import DannyReport
from sendmail import Email


# 溢收結帳單 未確認報表
class SalesReport1(DannyReport):

    def __init__(self):
        self.report_df = self.get_report_df()
        self.print_table()
        self.export_html()

    @logger.catch
    def get_merged_df(self):
        """
        Merge some tables
        """
        mylist = ["acrta", "copma"]
        for i in mylist:
            globals()[i] = globals()[i.upper()](db_cfg)
            globals()[i].df = globals()[i].get_columns(necessary_columns[i])
            globals()[i].df.columns = globals()[i].translate(necessary_columns[i])

        merged_df = pd.merge(acrta.df, copma.df, on="客戶代號")
        merged_df.index += 1
        return merged_df

    @logger.catch
    def get_filter_df(self, df):
        """
        Filter tables
        """
        my_filters = ("確認碼 == 'N' and 結帳單別 == '621'")
        filter_df = df.query(my_filters)
        return filter_df

    @logger.catch
    def get_output_df(self, df):
        """
        Custom Column for Output
        """
        output_df = pd.DataFrame()

        for k, v in change_columns['acrta']:
            if v in ('客戶代號', '客戶簡稱', '結帳日期', '幣別'):  # 只取需要的欄位
                output_df[k] = df[v]

        ### 新增自訂欄位 ###
        output_df.insert(3, "結帳單號", df["結帳單別"].str.cat(df["結帳單號"], sep="-"))
        output_df.insert(5, "原幣應收帳款", df["應收金額"] + df["營業稅額"])

        ## 數值格式化(小數點後幾位) ###
        output_df = COMMON.object_to_float(output_df, ["原幣應收帳款"], 2)
        output_df = output_df.reset_index(level=0, drop=True)  # 索引值重置為0

        return output_df


# 收款單 未確認報表
class SalesReport2(DannyReport):

    def __init__(self):
        self.report_df = self.get_report_df()
        self.print_table()
        self.export_html()

    @logger.catch
    def get_merged_df(self):
        """
        Merge some tables
        """
        mylist = ["acrtc", "copma"]
        for i in mylist:
            globals()[i] = globals()[i.upper()](db_cfg)
            globals()[i].df = globals()[i].get_columns(necessary_columns[i])
            globals()[i].df.columns = globals()[i].translate(necessary_columns[i])

        merged_df = pd.merge(acrtc.df, copma.df, on="客戶代號")
        merged_df.index += 1
        return merged_df

    @logger.catch
    def get_filter_df(self, df):
        """
        Filter tables
        """
        my_filters = ("確認碼 == 'N' and 收款單別 == '631'")
        filter_df = df.query(my_filters)
        return filter_df

    @logger.catch
    def get_output_df(self, df):
        """
        Custom Column for Output
        """
        output_df = pd.DataFrame()

        for k, v in change_columns['acrtc']:
            output_df[k] = df[v]

        ### 新增自訂欄位 ###
        output_df.insert(3, "收款單號", df["收款單別"].str.cat(df["收款單號"], sep="-"))

        ## 數值格式化(小數點後幾位) ###
        output_df = COMMON.object_to_float(output_df, ["原幣金額"], 2)
        output_df = output_df.reset_index(level=0, drop=True)  # 索引值重置為0

        return output_df


class SendSalesReport:

    def __init__(self, official=True):
        report1 = SalesReport1()
        report2 = SalesReport2()
        report1_html = Email.to_html(report1.report_df, '溢收結帳單 未確認報表')
        report1_htm2 = Email.to_html(report2.report_df, '收款單 未確認報表')
        body = report1_html + report1_htm2
        sender = 'noreply@automodules.com'
        if official:
            to_list = to_list_official
            cc_list = cc_list_official
        else:
            to_list = []
            cc_list = ['ysuper.liang@automodules.com']
        subject = '沖帳提醒 - {}'.format(datetime.now().strftime('%Y/%m/%d'))
        mail_dict = {'from': sender, 'to': to_list, 'cc': cc_list, 'subject': subject, 'body': body}
        mail = Email(mail_dict)
        mail.sendmail()


if __name__ == '__main__':
    # SalesReport1()
    # SalesReport2()
    SendSalesReport(official=False)
