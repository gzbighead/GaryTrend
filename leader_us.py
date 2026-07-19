#!/usr/bin/env python3
"""
美股龙头候选捕捉
每天运行，逻辑：
1. 从ETF趋势系统识别正在启动的板块（多头比例↑的板块）
2. 在标普500对应GICS板块的个股里计算虹吸比例
3. 虹吸比例（5日均值/60日均值）≥ 3倍 + Supertrend多头
4. 按虹吸比例从高到低排列输出
"""

import os
import datetime
import requests
import numpy as np
import yfinance as yf

from watchlist_sp500 import get_stocks_by_etf_sector
from watchlist_us import WATCHLIST_US, classify_us
from engine import (
    fetch_daily, calc_supertrend, calc_ma,
    scan_symbol, calc_sector_state, calc_sector_trend,
)

# ─── 配置 ──────────────────────────────────────────────────────────────────
EMAIL_TO   = ["garyfocus@hotmail.com", "hua@ceic.ca"]
EMAIL_FROM = "美股龙头捕捉 <gary@ceic.ca>"

ST_PERIOD     = 10
ST_MULTIPLIER = 3.0
MA_PERIOD     = 20

# 虹吸比例阈值：5日均值 ≥ N倍60日均值
SIPHON_THRESHOLD = 3.0

# 板块启动阈值：多头比例 ≥ X% 且5日方向为↑或↑↑
SECTOR_BULL_MIN  = 50  # 多头比例至少50%
ACTIVE_DIRECTIONS = {"↑", "↑↑"}

# 用SPY成交额代表大盘
MARKET_PROXY = "SPY"

# ─── 计算虹吸比例 ──────────────────────────────────────────────────────────
def calc_siphon_ratio(symbol, market_turnover_series):
    """
    计算个股的虹吸比例：个股成交额 / 大盘成交额
    返回 {5日均值, 60日均值, 倍数} 或 None
    """
    df = fetch_daily(symbol)
    if df is None or len(df) < 65:
        return None

    close  = df["Close"].values.astype(float)
    volume = df["Volume"].values.astype(float)

    # 个股成交额（收盘价 × 成交量）
    turnover = close * volume

    # 对齐大盘数据日期
    stock_dates  = [str(d)[:10] for d in df.index]
    market_dates = list(market_turnover_series.keys())

    # 计算虹吸比例序列
    ratios = []
    for i, date in enumerate(stock_dates):
        if date in market_turnover_series and market_turnover_series[date] > 0:
            ratios.append(turnover[i] / market_turnover_series[date])
        else:
            ratios.append(np.nan)

    ratios = np.array(ratios)
    valid  = ratios[~np.isnan(ratios)]

    if len(valid) < 65:
        return None

    ma60 = np.mean(valid[-60:])
    ma5  = np.mean(valid[-5:])

    if ma60 == 0:
        return None

    multiple = round(ma5 / ma60, 2)
    return {
        "ma5":      round(ma5, 8),
        "ma60":     round(ma60, 8),
        "multiple": multiple,
    }

# ─── 获取大盘成交额序列 ────────────────────────────────────────────────────
def get_market_turnover():
    """用SPY的成交额作为大盘基准，返回 {date_str: turnover} 字典"""
    df = fetch_daily(MARKET_PROXY)
    if df is None:
        return {}
    close  = df["Close"].values.astype(float)
    volume = df["Volume"].values.astype(float)
    dates  = [str(d)[:10] for d in df.index]
    return {dates[i]: close[i] * volume[i] for i in range(len(dates))}

# ─── 判断当前多头状态和Supertrend ─────────────────────────────────────────
def get_stock_trend(symbol):
    """返回当前Supertrend趋势和距趋势线距离"""
    df = fetch_daily(symbol)
    if df is None:
        return None, None
    trend_arr, st_arr = calc_supertrend(df, ST_PERIOD, ST_MULTIPLIER)
    close = df["Close"].values.astype(float)
    n     = len(close)
    t     = trend_arr[n-1]
    s     = st_arr[n-1]
    c     = close[n-1]
    if np.isnan(t) or np.isnan(s):
        return None, None
    st_dist = round((c - s) / s * 100, 1)
    return int(t), st_dist

# ─── 识别正在启动的ETF板块 ────────────────────────────────────────────────
def find_active_sectors():
    """
    扫描ETF趋势系统，找出多头比例≥阈值且方向向上的板块
    返回: [etf板块名, ...]
    """
    print("[扫描ETF板块状态]")
    results = []
    for symbol, name in WATCHLIST_US:
        try:
            r = scan_symbol(symbol, name, classify_us, signal_days=3, trend_days=60)
            if r:
                results.append(r)
        except Exception as e:
            pass

    sector_state = calc_sector_state(results)
    sector_trend = calc_sector_trend(results, days=60)

    active = []
    for sec, stat in sector_state.items():
        pct       = stat["pct"]
        direction = sector_trend.get(sec, {}).get("direction", "→")
        if pct >= SECTOR_BULL_MIN and direction in ACTIVE_DIRECTIONS:
            active.append({
                "sector":    sec,
                "pct":       pct,
                "direction": direction,
            })
            print(f"  启动板块: {sec} {pct}% {direction}")

    return active

# ─── 主扫描逻辑 ────────────────────────────────────────────────────────────
def scan_leaders(active_sectors, market_turnover):
    """
    在启动板块对应的SP500个股里找龙头候选
    返回候选列表
    """
    # 收集需要扫描的个股（去重）
    candidates = {}  # symbol -> {name, sectors}
    for sec_info in active_sectors:
        etf_sector = sec_info["sector"]
        stocks     = get_stocks_by_etf_sector(etf_sector)
        for symbol, info in stocks.items():
            name = info["name"]
            if symbol not in candidates:
                candidates[symbol] = {"name": name, "sectors": []}
            candidates[symbol]["sectors"].append(etf_sector)

    print(f"\n[扫描个股] 共{len(candidates)}只候选")

    results = []
    for symbol, info in candidates.items():
        try:
            # 计算虹吸比例
            siphon = calc_siphon_ratio(symbol, market_turnover)
            if siphon is None:
                continue

            # 虹吸比例不达标，跳过
            if siphon["multiple"] < SIPHON_THRESHOLD:
                continue

            # 获取Supertrend状态
            trend, st_dist = get_stock_trend(symbol)
            if trend != 1:  # 必须是多头
                continue

            results.append({
                "symbol":    symbol,
                "name":      info["name"],
                "sectors":   info["sectors"],
                "multiple":  siphon["multiple"],
                "st_dist":   st_dist,
            })
            print(f"  ✓ {symbol} {info['name']} 虹吸{siphon['multiple']}倍 ST+{st_dist}%")

        except Exception as e:
            print(f"  {symbol}: 错误 {e}")

    # 按虹吸倍数从高到低排序
    results.sort(key=lambda x: x["multiple"], reverse=True)
    return results

# ─── 生成HTML邮件 ──────────────────────────────────────────────────────────
def build_html(report_date, active_sectors, leaders):

    def siphon_color(m):
        if m >= 8:  return "#c0392b"
        if m >= 5:  return "#e67e22"
        if m >= 3:  return "#856404"
        return "#555"

    def siphon_bg(m):
        if m >= 8:  return "#fdecea"
        if m >= 5:  return "#fef5e7"
        if m >= 3:  return "#fef9e7"
        return "#f9f9f9"

    th  = 'style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:left;border-bottom:1px solid #ddd;"'
    thc = 'style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:center;border-bottom:1px solid #ddd;"'
    thr = 'style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:right;border-bottom:1px solid #ddd;"'

    # 启动板块
    sector_rows = ""
    for s in active_sectors:
        dir_col = "#c0392b" if s["direction"] == "↑↑" else "#856404"
        sector_rows += (
            f'<tr>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;font-weight:bold;">{s["sector"]}</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;">{s["pct"]}%</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;font-weight:bold;color:{dir_col};">{s["direction"]}</td>'
            f'</tr>'
        )
    if not sector_rows:
        sector_rows = '<tr><td colspan="3" style="padding:10px;color:#aaa;text-align:center;">无启动板块</td></tr>'

    # 龙头候选
    leader_rows = ""
    for i, r in enumerate(leaders):
        bg  = "#ffffff" if i % 2 == 0 else "#f9f9f9"
        mc  = siphon_color(r["multiple"])
        mbg = siphon_bg(r["multiple"])
        sc  = "#c0392b" if (r["st_dist"] or 0) > 0 else "#1a56db"
        secs = " / ".join(r["sectors"])
        leader_rows += (
            f'<tr style="background:{bg};">'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;font-weight:bold;white-space:nowrap;">{r["symbol"]}</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;font-size:12px;">{r["name"]}</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;font-size:11px;color:#888;">{secs}</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;background:{mbg};color:{mc};font-weight:bold;">{r["multiple"]}x</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:right;font-weight:bold;color:{sc};">{r["st_dist"]:+.1f}%</td>'
            f'</tr>'
        )
    if not leader_rows:
        leader_rows = '<tr><td colspan="5" style="padding:10px;color:#aaa;text-align:center;">今日无龙头候选</td></tr>'

    return f"""<table width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0" border="0"
           style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#222;padding:16px;">
      <tr><td>
        <h2 style="margin:0 0 4px;font-size:17px;">🏆 美股龙头候选</h2>
        <p style="margin:0 0 16px;color:#888;font-size:12px;">温哥华时间 {report_date}</p>

        <!-- 启动板块 -->
        <div style="margin-bottom:20px;">
          <div style="background:#e8f0fe;border-left:4px solid #1a56db;padding:10px 14px;border-radius:4px 4px 0 0;">
            <span style="font-size:14px;font-weight:bold;color:#1a56db;">📡 当前启动板块</span>
          </div>
          <table width="100%" cellpadding="0" cellspacing="0" border="0"
                 style="border-collapse:collapse;font-size:13px;border:1px solid #ddd;border-top:none;">
            <thead><tr><th {th}>板块</th><th {thc}>多头比例</th><th {thc}>方向</th></tr></thead>
            <tbody>{sector_rows}</tbody>
          </table>
        </div>

        <!-- 龙头候选 -->
        <div style="margin-bottom:20px;">
          <div style="background:#fdecea;border-left:4px solid #c0392b;padding:10px 14px;border-radius:4px 4px 0 0;">
            <span style="font-size:14px;font-weight:bold;color:#c0392b;">
              🏆 龙头候选（虹吸≥{SIPHON_THRESHOLD}倍 + Supertrend多头，共{len(leaders)}只）
            </span>
          </div>
          <table width="100%" cellpadding="0" cellspacing="0" border="0"
                 style="border-collapse:collapse;font-size:13px;border:1px solid #ddd;border-top:none;">
            <thead><tr>
              <th {th}>代码</th><th {th}>名称</th><th {th}>板块</th>
              <th {thc}>虹吸倍数</th><th {thr}>趋势线</th>
            </tr></thead>
            <tbody>{leader_rows}</tbody>
          </table>
        </div>

        <!-- 说明 -->
        <div style="background:#f9f9f9;border-radius:4px;padding:10px 14px;font-size:11px;color:#888;line-height:1.6;">
          虹吸倍数 = 个股5日成交额均值 ÷ 60日均值（相对SPY） ÷ 基准值<br>
          ≥3倍：异常资金介入 · ≥5倍：强势启动 · ≥8倍：爆发阶段（需谨慎追高）
        </div>

      </td></tr>
    </table>
    </td></tr></table>"""

# ─── 发邮件 ────────────────────────────────────────────────────────────────
def send_email(html, report_date, leader_count):
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        print("[邮件] 未设置RESEND_API_KEY")
        return
    subject = f"美股龙头候选 {report_date}" + (f" · {leader_count}只" if leader_count else " · 今日无信号")
    res = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"from": EMAIL_FROM, "to": EMAIL_TO, "subject": subject, "html": html},
    )
    print(f"[邮件] {'成功' if res.status_code==200 else '失败'} {res.status_code}")

# ─── 主流程 ────────────────────────────────────────────────────────────────
def main():
    now         = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-7)))
    report_date = now.strftime("%Y-%m-%d")
    print(f"[开始] 美股龙头捕捉 {report_date}")

    # 1. 获取大盘成交额基准
    print("[获取大盘成交额]")
    market_turnover = get_market_turnover()
    if not market_turnover:
        print("[错误] 无法获取大盘数据")
        return

    # 2. 找出启动板块
    active_sectors = find_active_sectors()
    if not active_sectors:
        print("[结果] 当前无启动板块，不发送邮件")
        return

    # 3. 扫描龙头候选
    leaders = scan_leaders(active_sectors, market_turnover)
    print(f"\n[完成] 找到{len(leaders)}只龙头候选")

    # 4. 生成报告并发邮件（有无候选都发，让用户知道系统在运行）
    html = build_html(report_date, active_sectors, leaders)
    send_email(html, report_date, len(leaders))

if __name__ == "__main__":
    main()
