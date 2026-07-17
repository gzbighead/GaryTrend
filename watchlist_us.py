# ─── 美股观察清单 ─────────────────────────────────────────────────────────
# 格式: ("代码", "名称")
# 直接加到列表，系统自动分类，无需手动排序
# 原则：每板块选成交量大、规模大的主流活跃ETF，保证数据代表性

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
    ("IWF",  "罗素1000成长ETF-iShares"),
    ("IWD",  "罗素1000价值ETF-iShares"),
    ("VUG",  "成长ETF-Vanguard"),
    ("VTV",  "价值ETF-Vanguard"),

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
    ("FTEC", "科技ETF-Fidelity"),
    ("IGV",  "软件ETF-iShares"),
    ("SKYY", "云计算ETF-First Trust"),
    ("CLOU", "云计算ETF-Global X"),
    ("WCLD", "云计算ETF-WisdomTree"),
    ("BUG",  "网络安全ETF-Global X"),
    ("HACK", "网络安全ETF-ETFMG"),
    ("CIBR", "网络安全ETF-First Trust"),
    ("IHAK", "网络安全ETF-iShares"),
    ("PNQI", "纳斯达克互联网ETF-Invesco"),
    ("FDN",  "道琼斯互联网ETF-First Trust"),

    # ── 半导体ETF ─────────────────────────────────────────────────────────
    ("SMH",  "半导体ETF-VanEck"),
    ("SOXX", "费城半导体ETF-iShares"),
    ("XSD",  "标普半导体ETF-SPDR"),
    ("PSI",  "半导体ETF-Invesco"),
    ("SOXQ", "费城半导体ETF-Invesco"),
    ("USD",  "半导体ETF-ProShares"),
    ("FTXL", "纳斯达克半导体ETF-First Trust"),

    # ── 人工智能ETF ───────────────────────────────────────────────────────
    ("BOTZ", "机器人与AI ETF-Global X"),
    ("ROBO", "机器人ETF-ROBO Global"),
    ("IRBO", "机器人AI ETF-iShares"),
    ("AIQ",  "AI大数据ETF-Global X"),
    ("ARKQ", "自动化ETF-ARK"),
    ("ARKW", "下一代互联网ETF-ARK"),
    ("ARKK", "创新ETF-ARK"),
    ("ARKG", "基因组革命ETF-ARK"),
    ("THNQ", "AI ETF-ROBO Global"),
    ("CHAT", "生成式AI ETF-Roundhill"),

    # ── 金融ETF ───────────────────────────────────────────────────────────
    ("XLF",  "金融行业ETF-SPDR"),
    ("VFH",  "金融ETF-Vanguard"),
    ("IYF",  "金融ETF-iShares"),
    ("FNCL", "金融ETF-Fidelity"),
    ("KBE",  "银行ETF-SPDR KBW"),
    ("KRE",  "地区银行ETF-SPDR KBW"),
    ("IAT",  "美国地区银行ETF-iShares"),
    ("KIE",  "保险ETF-SPDR KBW"),
    ("IAK",  "美国保险ETF-iShares"),
    ("IAI",  "证券经纪ETF-iShares"),
    ("KBWB", "银行ETF-Invesco KBW"),
    ("FAS",  "三倍做多金融ETF-Direxion"),

    # ── 医疗医药ETF ───────────────────────────────────────────────────────
    ("XLV",  "医疗保健ETF-SPDR"),
    ("VHT",  "医疗保健ETF-Vanguard"),
    ("IYH",  "美国医疗ETF-iShares"),
    ("FHLC", "医疗保健ETF-Fidelity"),
    ("IBB",  "生物科技ETF-iShares"),
    ("XBI",  "标普生物科技ETF-SPDR"),
    ("BBH",  "生物科技ETF-VanEck"),
    ("ARKG", "基因组革命ETF-ARK"),
    ("IHE",  "医药ETF-iShares"),
    ("IHI",  "医疗器械ETF-iShares"),
    ("IHF",  "医疗保险ETF-iShares"),
    ("PTH",  "医疗保健ETF-Invesco"),
    ("GNOM", "基因组学ETF-Global X"),

    # ── 能源ETF ───────────────────────────────────────────────────────────
    ("XLE",  "能源ETF-SPDR"),
    ("VDE",  "能源ETF-Vanguard"),
    ("IYE",  "美国能源ETF-iShares"),
    ("FENY", "能源ETF-Fidelity"),
    ("OIH",  "油服ETF-VanEck"),
    ("XOP",  "油气勘探ETF-SPDR"),
    ("FCG",  "天然气ETF-First Trust"),
    ("UNG",  "天然气ETF"),
    ("USL",  "12月原油ETF"),
    ("ERX",  "2倍做多能源ETF-Direxion"),

    # ── 新能源ETF ─────────────────────────────────────────────────────────
    ("TAN",  "太阳能ETF-Invesco"),
    ("ICLN", "清洁能源ETF-iShares"),
    ("QCLN", "清洁能源ETF-First Trust"),
    ("FAN",  "风能ETF-First Trust"),
    ("ACES", "清洁能源ETF-ALPS"),
    ("CNRG", "清洁能源ETF-SPDR"),
    ("NLR",  "铀与核能ETF-VanEck"),
    ("URA",  "铀ETF-Global X"),
    ("URNM", "铀矿ETF-Sprott"),
    ("LIT",  "锂电池ETF-Global X"),
    ("BATT", "电池科技ETF-Amplify"),
    ("DRIV", "电动车ETF-Global X"),
    ("IDRV", "电动车ETF-iShares"),

    # ── 消费ETF ───────────────────────────────────────────────────────────
    ("XLP",  "必需消费ETF-SPDR"),
    ("XLY",  "非必需消费ETF-SPDR"),
    ("VCR",  "非必需消费ETF-Vanguard"),
    ("VDC",  "必需消费ETF-Vanguard"),
    ("IYC",  "消费服务ETF-iShares"),
    ("FDIS", "非必需消费ETF-Fidelity"),
    ("FSTA", "必需消费ETF-Fidelity"),
    ("RTH",  "零售ETF-VanEck"),
    ("XRT",  "标普零售ETF-SPDR"),
    ("ITB",  "房屋建筑ETF-iShares"),
    ("XHB",  "标普房屋建筑商ETF-SPDR"),
    ("AWAY", "旅游ETF-ETFMG"),
    ("JETS", "航空ETF-US Global"),

    # ── 工业ETF ───────────────────────────────────────────────────────────
    ("XLI",  "工业ETF-SPDR"),
    ("VIS",  "工业ETF-Vanguard"),
    ("IYJ",  "美国工业ETF-iShares"),
    ("FIDU", "工业ETF-Fidelity"),
    ("IYT",  "运输ETF-iShares"),
    ("ITA",  "航空航天国防ETF-iShares"),
    ("PPA",  "航空航天国防ETF-Invesco"),
    ("XAR",  "标普航空航天ETF-SPDR"),
    ("DFEN", "三倍做多航空航天ETF-Direxion"),
    ("PKB",  "建筑与施工ETF-Invesco"),
    ("PAVE", "基础设施ETF-Global X"),

    # ── 原材料ETF ─────────────────────────────────────────────────────────
    ("XLB",  "原材料ETF-SPDR"),
    ("VAW",  "原材料ETF-Vanguard"),
    ("IYM",  "基础材料ETF-iShares"),
    ("FMAT", "原材料ETF-Fidelity"),
    ("XME",  "金属与矿产ETF-SPDR"),
    ("PICK", "金属与矿产ETF-iShares"),
    ("COPX", "铜矿ETF-Global X"),
    ("REMX", "稀土ETF-VanEck"),
    ("WOOD", "木材ETF-iShares"),
    ("LIT",  "锂ETF-Global X"),

    # ── 贵金属ETF ─────────────────────────────────────────────────────────
    ("GLD",  "黄金ETF-SPDR"),
    ("IAU",  "黄金ETF-iShares"),
    ("SGOL", "黄金ETF-Aberdeen"),
    ("BAR",  "黄金ETF-GraniteShares"),
    ("AAAU", "黄金ETF-Goldman Sachs"),
    ("GLDM", "黄金ETF-SPDR迷你版"),
    ("SLV",  "白银ETF-iShares"),
    ("SIVR", "白银ETF-Aberdeen"),
    ("PPLT", "铂金ETF-Aberdeen"),
    ("PALL", "钯金ETF-Aberdeen"),
    ("GDX",  "黄金矿商ETF-VanEck"),
    ("GDXJ", "初级黄金矿商ETF-VanEck"),
    ("RING", "黄金矿商ETF-iShares"),
    ("SIL",  "白银矿商ETF-Global X"),

    # ── 大宗商品ETF ───────────────────────────────────────────────────────
    ("DBC",  "商品指数ETF-Invesco"),
    ("GSG",  "商品ETF-iShares"),
    ("PDBC", "多元化商品ETF-Invesco"),
    ("USCI", "商品指数ETF-US Commodity"),
    ("DBA",  "农业ETF-Invesco"),
    ("MOO",  "农业企业ETF-VanEck"),
    ("CORN", "玉米ETF-Teucrium"),
    ("WEAT", "小麦ETF-Teucrium"),
    ("SOYB", "大豆ETF-Teucrium"),
    ("USO",  "原油ETF-United States"),
    ("BNO",  "布伦特原油ETF"),
    ("DBO",  "原油ETF-Invesco"),

    # ── 债券ETF ───────────────────────────────────────────────────────────
    ("AGG",  "综合债券ETF-iShares"),
    ("BND",  "综合债券ETF-Vanguard"),
    ("BOND", "主动债券ETF-PIMCO"),
    ("TLT",  "20年以上国债ETF-iShares"),
    ("TLH",  "10-20年国债ETF-iShares"),
    ("IEF",  "7-10年国债ETF-iShares"),
    ("IEI",  "3-7年国债ETF-iShares"),
    ("SHY",  "1-3年国债ETF-iShares"),
    ("GOVT", "美国国债ETF-iShares"),
    ("TIP",  "通胀保护债券ETF-iShares"),
    ("SCHP", "通胀保护债券ETF-Schwab"),
    ("HYG",  "高收益债券ETF-iShares"),
    ("JNK",  "高收益债券ETF-SPDR"),
    ("USHY", "高收益债券ETF-iShares"),
    ("LQD",  "投资级公司债ETF-iShares"),
    ("VCIT", "中期公司债ETF-Vanguard"),
    ("VCSH", "短期公司债ETF-Vanguard"),
    ("EMB",  "新兴市场债券ETF-iShares"),
    ("MUB",  "市政债券ETF-iShares"),
    ("BNDX", "国际债券ETF-Vanguard"),

    # ── 房地产ETF ─────────────────────────────────────────────────────────
    ("IYR",  "美国房地产ETF-iShares"),
    ("VNQ",  "不动产ETF-Vanguard"),
    ("XLRE", "房地产ETF-SPDR"),
    ("ICF",  "美国房地产ETF-iShares"),
    ("SCHH", "美国房地产ETF-Schwab"),
    ("REM",  "抵押房地产ETF-iShares"),
    ("FRI",  "标普REIT ETF-First Trust"),
    ("URE",  "2倍做多房地产ETF-ProShares"),
    ("REZ",  "住宅房地产ETF-iShares"),
    ("INDS", "工业房地产ETF-Pacer"),

    # ── 公用事业ETF ───────────────────────────────────────────────────────
    ("XLU",  "公用事业ETF-SPDR"),
    ("VPU",  "公用事业ETF-Vanguard"),
    ("IDU",  "美国公用事业ETF-iShares"),
    ("FUTY", "公用事业ETF-Fidelity"),
    ("IYZ",  "美国电信ETF-iShares"),
    ("XLC",  "通信服务ETF-SPDR"),
    ("VOX",  "通信服务ETF-Vanguard"),
    ("FCOM", "通信服务ETF-Fidelity"),

    # ── 杠杆ETF ───────────────────────────────────────────────────────────
    ("TQQQ", "三倍做多纳指ETF-ProShares"),
    ("SOXL", "三倍做多半导体ETF-Direxion"),
    ("UPRO", "三倍做多标普500ETF-ProShares"),
    ("TECL", "三倍做多科技ETF-Direxion"),
    ("LABU", "三倍做多生物科技ETF-Direxion"),
    ("TNA",  "三倍做多小盘股ETF-Direxion"),
    ("SSO",  "2倍做多标普500ETF-ProShares"),
    ("QLD",  "2倍做多纳指ETF-ProShares"),
    ("DDM",  "2倍做多道指ETF-ProShares"),
    ("UWM",  "2倍做多罗素2000ETF-ProShares"),
    ("UYG",  "2倍做多金融ETF-ProShares"),
    ("UYM",  "2倍做多基础材料ETF-ProShares"),
    ("DRN",  "三倍做多房地产ETF-Direxion"),
    ("DFEN", "三倍做多航空航天ETF-Direxion"),
    ("ERX",  "2倍做多能源ETF-Direxion"),
    ("FNGU", "三倍做多科技龙头ETF-MicroSectors"),

    # ── 恐慌/波动率ETF ────────────────────────────────────────────────────
    ("VXX",  "标普500短期期货恐慌ETN-iPath"),
    ("VIXY", "短期期货恐慌ETF-ProShares"),
    ("UVXY", "1.5倍做多恐慌ETF-ProShares"),
]

# ─── 指数代码白名单 ────────────────────────────────────────────────────────
INDEX_CODES_US = {
    "SPY", "QQQ", "IWM", "DIA", "VOO", "IVV",
    "VTI", "MDY", "IJH", "IJR", "IWB", "IWV", "OEF",
    "IWF", "IWD", "VUG", "VTV",
}

# ─── ETF板块关键词（顺序敏感，具体词优先于宽泛词）────────────────────────
SECTOR_KEYWORDS_US = {
    "半导体":   ["半导体", "Semiconductor", "费城半导体"],
    "科技":     ["科技", "Tech", "技术", "软件", "Software", "云计算", "Cloud",
                 "网络安全", "Cyber", "信息科技", "互联网", "Internet"],
    "人工智能": ["人工智能", "AI", "机器人", "Robot", "自动化", "Autonom",
                 "创新", "Innovat", "基因组", "Genom", "生成式"],
    "新能源":   ["太阳能", "Solar", "清洁能源", "Clean", "风能", "Wind",
                 "铀", "核能", "Uranium", "Nuclear", "锂", "Lithium",
                 "电动车", "Electric", "电池", "Battery"],
    "医疗医药": ["医疗", "医药", "生物科技", "Health", "Biotech", "Pharma",
                 "Medical", "基因", "Gene", "器械", "Device", "保险ETF-iShares"],
    "金融":     ["金融", "银行", "Financial", "Bank", "保险", "Insurance", "证券", "Broker"],
    "能源":     ["能源", "石油", "Energy", "Oil", "天然气", "Gas", "原油"],
    "消费":     ["消费", "Consumer", "零售", "Retail", "房屋建筑", "Homebuilder",
                 "旅游", "Travel", "航空ETF"],
    "工业":     ["工业", "运输", "Industrial", "Transport", "基础设施", "Infrastructure",
                 "建筑", "Construction"],
    "原材料":   ["原材料", "材料", "金属", "矿", "铜", "稀土", "木材",
                 "Material", "Metal", "Mining", "Copper", "Rare Earth"],
    "贵金属":   ["黄金", "白银", "铂金", "钯金", "Gold", "Silver", "Platinum",
                 "Palladium", "黄金矿", "白银矿", "Gold Miner"],
    "大宗商品": ["商品", "Commodity", "农业", "Agriculture", "玉米", "小麦",
                 "大豆", "Corn", "Wheat", "Soybean"],
    "债券":     ["债券", "Bond", "国债", "Treasury", "高收益", "High Yield",
                 "公司债", "Corporate", "市政", "Municipal", "通胀保护"],
    "房地产":   ["房地产", "Real Estate", "REIT", "不动产", "住宅", "Residential"],
    "公用事业": ["公用", "电信", "Utility", "Telecom", "通信服务", "Communication"],
    "恐慌":     ["恐慌", "波动", "Volatility", "VIX"],
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
