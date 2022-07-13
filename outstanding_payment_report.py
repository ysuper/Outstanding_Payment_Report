import pandas as pd

from config import db_cfg, opr_cfg
from dserp.acrta import ACRTA
from dserp.acrtb import ACRTB
from dserp.common import COMMON
from dserp.copma import COPMA
from dserp.dscma import DSCMA
from necessary_columns import necessary_columns, change_columns

if __name__ == "__main__":
    # mylist = ["acrta", "copma", "dscma", "acrtb"]
    mylist = ["acrta", "copma", "acrtb"]
    for i in mylist:
        locals()[i] = locals()[i.upper()](db_cfg)
        locals()[i].df = locals()[i].get_columns(necessary_columns[i])
        locals()[i].df.columns = locals()[i].translate(necessary_columns[i])

    merge_df = pd.merge(acrta.df, copma.df, on="客戶代號")
    # merge_df = pd.merge(merge_df, dscma.df, left_on="收款業務員", right_on="登入者代號")
    merge_df = pd.merge(merge_df, acrtb.df, on=["結帳單別", "結帳單號"])
    merge_df.index += 1
    my_filters = ("客戶代號 == 'CAS90014' and 確認碼 == 'Y' and 結案碼 =='N' and 結帳單別 in ['611', '612', '619']")
    merge_df = merge_df.query(my_filters)

    output_df = pd.DataFrame()
    for k, v in change_columns:
        output_df[k] = merge_df[v]
    output_df.insert(3, "結帳單號", merge_df['結帳單別'].str.cat(merge_df['結帳單號'], sep='-'))
    output_df.insert(7, "原幣應收帳款", merge_df['應收金額'] + merge_df['營業稅額'])
    output_df.insert(8, "原幣未收帳款", merge_df['本幣應收金額'] + merge_df['本幣營業稅額'] - merge_df['本幣已收金額'])
    output_df.insert(len(output_df.columns), "憑證號碼", ['-'.join(i) for i in zip(merge_df['憑證單別'], merge_df['憑證單號'])])
    output_df = COMMON.object_to_float(output_df, ["原幣應收帳款", "原幣未收帳款"], 2)
    output_df = COMMON.object_to_float(output_df, ["匯率"], 4)
    output_df.drop_duplicates("憑證號碼")
    output_df = output_df.reset_index(level=0, drop=True)
    # print(output_df)
    print(output_df.to_string(index=False))

    COMMON.export_html(output_df, "table.html")
    engine = 'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(opr_cfg["opr_user"], opr_cfg["opr_password"],
                                                                opr_cfg["opr_host"], opr_cfg["opr_port"],
                                                                opr_cfg["opr_db"], opr_cfg["opr_charset"])
    tableName = "report"
    COMMON.df_to_mysql(output_df, engine, tableName)
