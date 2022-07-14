necessary_columns = {
    "acrta": [
        "TA001",  # 結帳單別
        "TA002",  # 結帳單號
        "TA003",  # 結帳日期
        "TA004",  # 客戶代號
        "TA005",  # 收款業務員
        "TA009",  # 幣別
        "TA010",  # 匯率
        "TA015",  # 發票號碼(訖)
        "TA025",  # 確認碼
        "TA027",  # 結案碼
        "TA029",  # 應收金額
        "TA030",  # 營業稅額
        "TA036",  # INVOICE_NO
        "TA041",  # 本幣應收金額
        "TA042",  # 本幣營業稅額
        "TA058",  # 本幣已收金額
    ],
    "copma": [
        "MA001",  # 客戶代號
        "MA002",  # 客戶簡稱
    ],
    # "dscma": [
    #     "MA001",  # 登入者代號
    #     "MA002",  # 登入者名稱
    # ],
    "acrtb": [
        "TB001",  # 結帳單別
        "TB002",  # 結帳單號
        "TB005",  # 憑證單別
        "TB006",  # 憑證單號
        "TB007",  # 憑證序號
        # "TB008",  # 憑證日期
    ],
}

change_columns = [
    ('客戶代號', '客戶代號'),
    ('客戶名稱', '客戶簡稱'),
    ('日期', '結帳日期'),
    # ('結帳單號', '結帳單號'),
    ('業務員代號', '收款業務員'),
    ('發票號碼', '發票號碼(訖)'),
    ('幣別', '幣別'),
    # ('原幣應收帳款', '原幣應收帳款'),
    # ('原幣未收帳款', '原幣未收帳款'),
    ('匯率', '匯率'),
    # ('憑證號碼', '憑證號碼'),
]

ignore_record = [
    ('USD', 10000),
    ('EUR', 9500),
    ('NTD', 300000),
]
