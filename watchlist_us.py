# ─── 美股观察清单 ─────────────────────────────────────────────────────────
# 格式: ("代码", "名称")
# 直接加到列表，系统自动分类，无需手动排序

WATCHLIST_US = [
    # ── 指数 ──────────────────────────────────────────────────────────────
    ("SPY",  "标普500ETF-SPDR"),
    ("QQQ",  "纳指100ETF-Invesco"),
    ("IWM",  "罗素2000ETF-iShares"),
    ("DIA",  "道指ETF-SPDR"),
    ("VOO",  "标普500ETF-Vanguard"),
    ("IVV",  "标普500ETF-iShares"),
    ("VTI",  "全市场ETF-Vanguard"),
    ("MDY",  "标普中型股400ETF-SPDR"),
    ("IJH",  "标普中型股ETF-iShares"),
    ("IJR",  "标普小盘股ETF-iShares"),
    ("IWB",  "罗素1000ETF-iShares"),
    ("IWV",  "罗素3000ETF-iShares"),
    ("OEF",  "标普100ETF-iShares"),

    # ── 个股 ──────────────────────────────────────────────────────────────
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
    ("DDOG", "Datadog"),
    ("AEP",  "美国电力"),

    # ── 科技ETF ───────────────────────────────────────────────────────────
    ("XLK",  "科技行业ETF-SPDR"),
    ("VGT",  "信息科技ETF-Vanguard"),
    ("IYW",  "美国科技ETF-iShares"),
    ("IGV",  "软件指数ETF-iShares"),
    ("SKYY", "云计算ETF-First Trust"),
    ("CLOU", "云计算ETF-Global X"),
    ("BUG",  "网络安全ETF-Global X"),
    ("HACK", "网络安全ETF-ETFMG"),
    ("CIBR", "网络安全ETF-First Trust"),

    # ── 半导体ETF ─────────────────────────────────────────────────────────
    ("SMH",  "半导体ETF-VanEck"),
    ("SOXX", "费城半导体ETF-iShares"),
    ("XSD",  "标普半导体ETF-SPDR"),
    ("PSI",  "半导体ETF-Invesco"),
    ("SOXQ", "费城半导体ETF-Invesco"),

    # ── 人工智能ETF ───────────────────────────────────────────────────────
    ("BOTZ", "机器人与AI ETF-Global X"),
    ("ROBO", "机器人ETF-ROBO Global"),
    ("IRBO", "机器人AI ETF-iShares"),
    ("AIQ",  "AI大数据ETF-Global X"),
    ("ARKQ", "自动化ETF-ARK"),
    ("ARKW", "下一代互联网ETF-ARK"),
    ("ARKK", "创新ETF-ARK"),

    # ── 金融ETF ───────────────────────────────────────────────────────────
    ("XLF",  "金融行业ETF-SPDR"),
    ("VFH",  "金融ETF-Vanguard"),
    ("IYF",  "金融ETF-iShares"),
    ("KBE",  "银行ETF-SPDR KBW"),
    ("KRE",  "地区银行ETF-SPDR KBW"),
    ("KIE",  "保险ETF-SPDR KBW"),
    ("IAI",  "证券经纪ETF-iShares"),

    # ── 医疗医药ETF ───────────────────────────────────────────────────────
    ("XLV",  "医疗保健ETF-SPDR"),
    ("VHT",  "医疗保健ETF-Vanguard"),
    ("IBB",  "生物科技ETF-iShares"),
    ("XBI",  "标普生物科技ETF-SPDR"),
    ("IHE",  "医药ETF-iShares"),
    ("IHI",  "医疗器械ETF-iShares"),
    ("BBH",  "生物科技ETF-VanEck"),
    ("ARKG", "基因组革命ETF-ARK"),

    # ── 能源ETF ───────────────────────────────────────────────────────────
    ("XLE",  "能源ETF-SPDR"),
    ("VDE",  "能源ETF-Vanguard"),
    ("OIH",  "油服ETF-VanEck"),
    ("XOP",  "油气勘探ETF-SPDR"),
    ("FCG",  "天然气ETF-First Trust"),
    ("UNG",  "天然气ETF"),

    # ── 新能源ETF ─────────────────────────────────────────────────────────
    ("TAN",  "太阳能ETF-Invesco"),
    ("ICLN", "清洁能源ETF-iShares"),
    ("QCLN", "清洁能源ETF-First Trust"),
    ("FAN",  "风能ETF-First Trust"),
    ("NLR",  "铀与核能ETF-VanEck"),
    ("URA",  "铀ETF-Global X"),
    ("LIT",  "锂电池ETF-Global X"),

    # ── 消费ETF ───────────────────────────────────────────────────────────
    ("XLP",  "必需消费ETF-SPDR"),
    ("XLY",  "非必需消费ETF-SPDR"),
    ("VCR",  "非必需消费ETF-Vanguard"),
    ("VDC",  "必需消费ETF-Vanguard"),
    ("RTH",  "零售ETF-VanEck"),
    ("XRT",  "标普零售ETF-SPDR"),
    ("ITB",  "房屋建筑ETF-iShares"),
    ("XHB",  "标普房屋建筑商ETF-SPDR"),

    # ── 工业ETF ───────────────────────────────────────────────────────────
    ("XLI",  "工业ETF-SPDR"),
    ("VIS",  "工业ETF-Vanguard"),
    ("IYT",  "运输ETF-iShares"),
    ("ITA",  "航空航天与国防ETF-iShares"),
    ("PPA",  "航空航天与国防ETF-Invesco"),
    ("XAR",  "标普航空航天ETF-SPDR"),

    # ── 原材料ETF ─────────────────────────────────────────────────────────
    ("XLB",  "原材料ETF-SPDR"),
    ("VAW",  "原材料ETF-Vanguard"),
    ("IYM",  "基础材料ETF-iShares"),
    ("XME",  "金属与矿产ETF-SPDR"),
    ("GLD",  "黄金ETF-SPDR"),
    ("IAU",  "黄金ETF-iShares"),
    ("SLV",  "白银ETF-iShares"),
    ("COPX", "铜矿ETF-Global X"),
    ("REMX", "稀土ETF-VanEck"),

    # ── 大宗商品ETF ───────────────────────────────────────────────────────
    ("DBC",  "商品指数ETF-Invesco"),
    ("GSG",  "商品ETF-iShares"),
    ("PDBC", "多元化商品ETF-Invesco"),
    ("DBA",  "农业ETF-Invesco"),
    ("MOO",  "农业企业ETF-VanEck"),
    ("CORN", "玉米ETF-Teucrium"),
    ("WEAT", "小麦ETF-Teucrium"),
    ("USO",  "原油ETF"),
    ("BNO",  "布伦特原油ETF"),

    # ── 债券ETF ───────────────────────────────────────────────────────────
    ("AGG",  "综合债券ETF-iShares"),
    ("BND",  "综合债券ETF-Vanguard"),
    ("TLT",  "20年以上国债ETF-iShares"),
    ("IEF",  "7-10年国债ETF-iShares"),
    ("SHY",  "1-3年国债ETF-iShares"),
    ("TIP",  "通胀保护债券ETF-iShares"),
    ("HYG",  "高收益债券ETF-iShares"),
    ("JNK",  "高收益债券ETF-SPDR"),
    ("LQD",  "投资级公司债ETF-iShares"),
    ("EMB",  "新兴市场债券ETF-iShares"),
    ("MUB",  "市政债券ETF-iShares"),
    ("BNDX", "国际债券ETF-Vanguard"),

    # ── 房地产ETF ─────────────────────────────────────────────────────────
    ("IYR",  "美国房地产ETF-iShares"),
    ("VNQ",  "不动产ETF-Vanguard"),
    ("XLRE", "房地产ETF-SPDR"),
    ("ICF",  "美国房地产ETF-iShares"),
    ("FRI",  "标普REIT ETF-First Trust"),
    ("URE",  "2倍做多房地产ETF-ProShares"),

    # ── 公用事业ETF ───────────────────────────────────────────────────────
    ("XLU",  "公用事业ETF-SPDR"),
    ("VPU",  "公用事业ETF-Vanguard"),
    ("IDU",  "美国公用事业ETF-iShares"),
    ("IYZ",  "美国电信ETF-iShares"),
    ("XLC",  "通信服务ETF-SPDR"),

    # ── 杠杆ETF ───────────────────────────────────────────────────────────
    ("TQQQ", "三倍做多纳指ETF-ProShares"),
    ("SOXL", "三倍做多半导体ETF-Direxion"),
    ("UPRO", "三倍做多标普500ETF-ProShares"),
    ("TECL", "三倍做多科技ETF-Direxion"),
    ("FAS",  "三倍做多金融ETF-Direxion"),
    ("LABU", "三倍做多生物科技ETF-Direxion"),
    ("TNA",  "三倍做多小盘股ETF-Direxion"),
    ("ERX",  "2倍做多能源ETF-Direxion"),
    ("SSO",  "2倍做多标普500ETF-ProShares"),
    ("QLD",  "2倍做多纳指ETF-ProShares"),
    ("DDM",  "2倍做多道指ETF-ProShares"),
    ("UWM",  "2倍做多罗素2000ETF-ProShares"),
    ("UYG",  "2倍做多金融ETF-ProShares"),
    ("UYM",  "2倍做多基础材料ETF-ProShares"),
    ("DRN",  "三倍做多房地产ETF-Direxion"),

    # ── 恐慌/波动率ETF ────────────────────────────────────────────────────
    ("VXX",  "标普500短期期货恐慌ETN-iPath"),
    ("VIXY", "短期期货恐慌ETF-ProShares"),
    ("UVXY", "1.5倍做多恐慌ETF-ProShares"),
]

# ─── 指数代码白名单 ────────────────────────────────────────────────────────
INDEX_CODES_US = {
    "SPY", "QQQ", "IWM", "DIA", "VOO", "IVV",
    "VTI", "MDY", "IJH", "IJR", "IWB", "IWV", "OEF",
}

# ─── ETF板块关键词（顺序敏感，具体词优先于宽泛词）────────────────────────
SECTOR_KEYWORDS_US = {
    "半导体":   ["半导体", "Semiconductor", "费城半导体"],
    "科技":     ["科技", "Tech", "技术", "软件", "Software", "云计算", "Cloud", "网络安全", "Cyber", "信息科技"],
    "人工智能": ["人工智能", "AI", "机器人", "Robot", "自动化", "创新", "互联网", "基因组"],
    "新能源":   ["太阳能", "Solar", "清洁能源", "Clean", "风能", "Wind", "铀", "核能", "锂", "Lithium"],
    "医疗医药": ["医疗", "医药", "生物科技", "Health", "Biotech", "Pharma", "Medical", "基因"],
    "金融":     ["金融", "银行", "Financial", "Bank", "保险", "证券"],
    "能源":     ["能源", "石油", "Energy", "Oil", "天然气", "Gas"],
    "消费":     ["消费", "Consumer", "零售", "Retail", "房屋建筑", "Homebuilder"],
    "工业":     ["工业", "运输", "Industrial", "Transport", "航空航天", "Aerospace"],
    "原材料":   ["原材料", "材料", "金属", "矿", "黄金", "白银", "铜", "稀土", "Material", "Metal", "Gold", "Silver", "Mining"],
    "大宗商品": ["商品", "Commodity", "农业", "Agriculture", "玉米", "小麦", "原油", "Oil", "布伦特"],
    "债券":     ["债券", "Bond", "国债", "Treasury", "高收益", "公司债", "市政", "Municipal"],
    "房地产":   ["房地产", "Real Estate", "REIT", "不动产"],
    "公用事业": ["公用", "电信", "Utility", "Telecom", "通信服务"],
    "恐慌":     ["恐慌", "波动", "VIX", "Volatility"],
    "杠杆":     ["倍做多", "倍做空", "三倍", "两倍", "2倍", "3x", "2x"],
}


def classify_us(symbol, name):
    """返回 (层级, 板块): 层级=index/stock/etf, 板块=ETF时的板块名"""
    if symbol in INDEX_CODES_US:
        return "index", None
    if "ETF" in name.upper() or "ETN" in name.upper():
        for sector, keywords in SECTOR_KEYWORDS_US.items():
            for kw in keywords:
                if kw in name or kw in symbol:
                    return "etf", sector
        return "etf", "其他"
    return "stock", None
