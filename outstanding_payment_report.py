import pandas as pd
from loguru import logger
from rich import print
from tabulate import tabulate

from config import db_cfg, mysql_url, opr_cfg
from dserp.acrta import ACRTA
from dserp.acrtb import ACRTB
from dserp.common import COMMON
from dserp.copma import COPMA
from dserp.dscma import DSCMA
from necessary_columns import change_columns, necessary_columns, ignore_record


class DannyReport:

    def __init__(self):
        self.report_df = self.get_report_df()
        self.print_table()
        self.export_html()
        self.export_db()

    @logger.catch
    def get_report_df(self):
        """
        Generate a report
        """
        report_df = self.get_merged_df()
        report_df = self.get_filter_df(report_df)
        report_df = self.get_output_df(report_df)
        return report_df

    @logger.catch
    def get_merged_df(self):
        """
        Merge some tables
        """
        mylist = ["acrta", "copma", "acrtb"]
        for i in mylist:
            globals()[i] = globals()[i.upper()](db_cfg)
            globals()[i].df = globals()[i].get_columns(necessary_columns[i])
            globals()[i].df.columns = globals()[i].translate(necessary_columns[i])

        merged_df = pd.merge(acrta.df, copma.df, on="客戶代號")
        merged_df = pd.merge(merged_df, acrtb.df, on=["結帳單別", "結帳單號"])
        merged_df.index += 1
        return merged_df

    @logger.catch
    def get_filter_df(self, df):
        """
        Filter tables
        """
        my_filters = ("確認碼 == 'Y' and 結案碼 =='N' and 結帳單別 in ['611', '612', '619']")
        filter_df = df.query(my_filters)
        return filter_df

    @logger.catch
    def get_output_df(self, df):
        """
        Custom Column for Output
        """
        output_df = pd.DataFrame()

        for k, v in change_columns['acrta']:
            output_df[k] = df[v]
        ### 新增自訂欄位、過濾重覆資料 ###
        output_df.insert(3, "結帳單號", df["結帳單別"].str.cat(df["結帳單號"], sep="-"))
        output_df.insert(7, "原幣應收帳款", df["應收金額"] + df["營業稅額"])
        output_df.insert(8, "原幣未收帳款", df["本幣應收金額"] + df["本幣營業稅額"] - df["本幣已收金額"])
        output_df.insert(
            len(output_df.columns),
            "憑證號碼",
            ["-".join(i) for i in zip(df["憑證單別"], df["憑證單號"])],
        )
        output_df.drop_duplicates("憑證號碼", inplace=True)

        ### 611、619單，發票號碼 顯示INVOCIE_NO ###
        output_df.loc[df["結帳單別"] == "611", "發票號碼"] = df["INVOICE_NO"]
        output_df.loc[df["結帳單別"] == "619", "發票號碼"] = df["INVOICE_NO"]

        ### 刪除金額過小記錄 ###
        for currency, limit in ignore_record:
            filter = output_df[(output_df["幣別"] == currency) & (output_df["原幣應收帳款"] < limit)].index
            output_df.drop(filter, inplace=True)

        ### 數值格式化(小數點後幾位) ###
        output_df = COMMON.object_to_float(output_df, ["原幣應收帳款", "原幣未收帳款"], 2)
        output_df = COMMON.object_to_float(output_df, ["匯率"], 4)
        output_df = output_df.reset_index(level=0, drop=True)  # 索引值重置為0

        return output_df

    @logger.catch
    def print_table(self):
        print(tabulate(self.report_df, self.report_df.columns, tablefmt="pretty"))

    @logger.catch
    def export_html(self):
        COMMON.export_html(self.report_df, "table.html")

    @logger.catch
    def export_db(self):
        tableName = "report"
        COMMON.df_to_mysql(self.report_df, mysql_url, tableName)


if __name__ == "__main__":
    DannyReport()
