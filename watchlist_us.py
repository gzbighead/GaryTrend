# ─── 美股观察清单 ─────────────────────────────────────────────────────────
# 格式: ("代码", "名称")
# 直接加到列表，系统自动分类，无需手动排序

WATCHLIST_US = [
    # 指数
    ("SPY",  "标普500ETF"),
    ("QQQ",  "纳指100ETF"),
    ("IWM",  "罗素2000ETF"),
    ("DIA",  "道指ETF"),
    ("VOO",  "标普500ETF-Vanguard"),

    # 个股
    ("NVDA", "英伟达"),
    ("PLTR", "Palantir"),
    ("TSLA", "特斯拉"),
    ("MSFT", "微软"),
    ("AAPL", "苹果"),
    ("AMZN", "亚马逊"),
    ("AMD",  "美国超微公司"),
    ("ARM",  "ARM Holding"),
    ("MRVL", "迈威尔"),
    ("CRWD", "CrowdStrike"),
    ("RKLB", "火箭实验室"),

    # ETF
    ("XLK",  "科技行业精选指数ETF-SPDR"),
    ("SMH",  "半导体指数ETF-VanEck"),
    ("IGV",  "软件指数ETF-iShares"),
    ("TQQQ", "三倍做多纳指ETF-ProShares"),
    ("SOXL", "三倍做多半导体ETF-Direxion"),
    ("UPRO", "三倍做多标普500ETF-ProShares"),
    ("XLF",  "金融行业ETF-SPDR"),
    ("XLE",  "能源指数ETF-SPDR"),
    ("XLV",  "医疗保健ETF-SPDR"),
    ("XLI",  "工业指数ETF-SPDR"),
    ("XLU",  "公用事业ETF-SPDR"),
    ("XLP",  "日常消费品ETF-SPDR"),
    ("XLY",  "非必需消费ETF-SPDR"),
    ("XLB",  "原物料ETF-SPDR"),
    ("XME",  "标普金属与矿产业ETF-SPDR"),
    ("GLD",  "黄金ETF-SPDR"),
    ("SLV",  "白银ETF-iShares"),
    ("TAN",  "太阳能ETF-Invesco"),
    ("IYR",  "美国房地产指数ETF-iShares"),
    ("URE",  "2倍做多房地产ETF-ProShares"),
    ("IBB",  "生物科技指数ETF-iShares"),
    ("ITA",  "航空航天与国防ETF-iShares"),
    ("IWO",  "罗素2000成长股指数ETF-iShares"),
    ("IYM",  "基础材料ETF-iShares"),
    ("IYZ",  "美国电信ETF-iShares"),
    ("KBE",  "银行指数ETF-SPDR KBW"),
    ("OIH",  "石油服务指数ETF-VanEck"),
    ("SSO",  "2倍做多标普500ETF-ProShares"),
    ("TNA",  "三倍做多小盘股ETF-Direxion"),
    ("UWM",  "罗素2000指数ETF-ProShares两倍做多"),
    ("DDM",  "2倍做多道指ETF-Proshares"),
    ("DRN",  "三倍做多房地产ETF-Direxion"),
    ("FAS",  "三倍做多金融指数ETF-Direxion"),
    ("NLR",  "铀与核能ETF-VanEck"),
    ("MOO",  "农业企业指数ETF-VanEck"),
    ("DBC",  "商品指数ETF-Invesco"),
    ("DBA",  "Invesco德银农业ETF"),
]

# ─── 指数代码白名单 ────────────────────────────────────────────────────────
INDEX_CODES_US = {"SPY", "QQQ", "IWM", "DIA", "VOO", "IVV"}

# ─── ETF板块关键词（顺序敏感，具体词优先于宽泛词）────────────────────────
SECTOR_KEYWORDS_US = {
    "半导体":   ["半导体", "Semiconductor"],
    "科技":     ["科技", "Tech", "技术", "软件", "Software"],
    "人工智能": ["人工智能", "AI"],
    "新能源":   ["太阳能", "Solar", "清洁能源", "铀", "核能"],
    "医疗医药": ["医疗", "医药", "生物科技", "Health", "Biotech", "Pharma"],
    "金融":     ["金融", "银行", "Financial", "Bank"],
    "能源":     ["能源", "石油", "Energy", "Oil"],
    "消费":     ["消费", "Consumer", "零售", "Retail"],
    "工业":     ["工业", "运输", "Industrial", "Transport"],
    "原材料":   ["原材料", "材料", "金属", "矿", "黄金", "白银", "Material", "Metal", "Gold", "Silver", "商品"],
    "房地产":   ["房地产", "Real Estate", "REIT"],
    "国防航天": ["航空", "国防", "Defense", "Aerospace"],
    "公用事业": ["公用", "电信", "Utility", "Telecom"],
    "农业":     ["农业", "Agriculture"],
    "杠杆":     ["倍做多", "倍做空", "三倍", "两倍", "2倍"],
}

def classify_us(symbol, name):
    """返回 (层级, 板块): 层级=index/stock/etf, 板块=ETF时的板块名"""
    if symbol in INDEX_CODES_US:
        return "index", None
    if "ETF" in name.upper():
        for sector, keywords in SECTOR_KEYWORDS_US.items():
            for kw in keywords:
                if kw in name or kw in symbol:
                    return "etf", sector
        return "etf", "其他"
    return "stock", None
