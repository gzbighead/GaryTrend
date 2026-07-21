#!/usr/bin/env python3
"""
美股龙头候选捕捉
每天运行，逻辑：
1. 从ETF趋势系统识别正在启动的板块（多头比例↑的板块）
2. 找到板块启动点（多头比例首次≥50%的日期）
3. 在标普500对应GICS板块的个股里，找当前Supertrend多头的个股
4. 按bull_days从长到短排列，最长的就是率先启动的龙头
"""

import os
import datetime
import requests
import numpy as np
import yfinance as yf

from watchlist_sp500 import get_stocks_by_sector
from watchlist_us import WATCHLIST_US, classify_us
from engine import (
    fetch_daily, calc_supertrend, calc_ma, safe,
    scan_symbol, calc_sector_state, calc_sector_trend,
)

# ─── 配置 ──────────────────────────────────────────────────────────────────
EMAIL_TO   = ["garyfocus@hotmail.com"]
EMAIL_FROM = "趋势分析 - 美股龙头捕捉 <gary@ceic.ca>"

ST_PERIOD     = 10
ST_MULTIPLIER = 3.0
MA_PERIOD     = 20
TREND_DAYS    = 60

# 板块启动阈值
SECTOR_BULL_MIN  = 50   # 多头比例首次≥50%为板块启动点
ACTIVE_DIRECTIONS = {"↑", "↑↑"}  # 当前方向必须向上

# ─── 计算个股bull_days和转多日期 ──────────────────────────────────────────
def get_stock_bull_info(symbol):
    """
    返回:
      trend     : 当前趋势 1=多头 -1=空头
      bull_days : 多头持续交易日数
      bull_since: 多头起始日期字符串
      st_dist   : 距趋势线距离%
    """
    df = fetch_daily(symbol)
    if df is None:
        return None

    trend_arr, st_arr = calc_supertrend(df, ST_PERIOD, ST_MULTIPLIER)
    close = df["Close"].values.astype(float)
    dates = df.index
    n     = len(close)

    last_i = n - 1
    t      = safe(trend_arr[last_i])
    if t is None:
        return None

    t = int(t)

    # 计算距趋势线距离
    s      = safe(st_arr[last_i])
    c      = float(close[last_i])
    st_dist = round((c - s) / s * 100, 1) if s else None

    # 如果当前不是多头，直接返回
    if t != 1:
        return {"trend": t, "bull_days": 0, "bull_since": None, "st_dist": st_dist}

    # 往前找连续多头起点
    start_i = last_i
    for i in range(last_i - 1, -1, -1):
        v = safe(trend_arr[i])
        if v == 1:
            start_i = i
        else:
            break

    bull_days = last_i - start_i + 1
    start_date = dates[start_i]
    bull_since = start_date.strftime("%Y-%m-%d") if hasattr(start_date, "strftime") else str(start_date)[:10]

    return {
        "trend":     t,
        "bull_days": bull_days,
        "bull_since": bull_since,
        "st_dist":   st_dist,
    }

# ─── 找板块启动点 ──────────────────────────────────────────────────────────
def find_sector_launch_date(sector_series):
    """
    从板块60天多头比例序列里，找首次≥50%的日期
    sector_series: [{date, pct, ...}, ...] 按日期从旧到新
    返回日期字符串或None
    """
    for pt in sector_series:
        if pt["pct"] >= SECTOR_BULL_MIN:
            return pt["date"]
    return None

# ─── 识别正在启动的ETF板块 ────────────────────────────────────────────────
def find_active_sectors(results):
    """
    从ETF扫描结果里找当前多头比例≥50%且方向向上的板块
    同时返回每个板块的60天序列（用于找启动点）
    """
    sector_state = calc_sector_state(results)
    sector_trend = calc_sector_trend(results, days=TREND_DAYS)

    active = []
    for sec, stat in sector_state.items():
        pct       = stat["pct"]
        st_info   = sector_trend.get(sec, {})
        direction = st_info.get("direction", "→")
        series    = st_info.get("series", [])

        if pct >= SECTOR_BULL_MIN and direction in ACTIVE_DIRECTIONS:
            launch_date = find_sector_launch_date(series)
            active.append({
                "sector":      sec,
                "pct":         pct,
                "direction":   direction,
                "launch_date": launch_date,
            })
            print(f"  启动板块: {sec} {pct}% {direction} 启动点:{launch_date}")

    return active

# ─── 主扫描逻辑 ────────────────────────────────────────────────────────────
def scan_leaders(active_sectors):
    """
    在启动板块对应的SP500个股里找龙头
    逻辑：当前多头 + bull_days从长到短排列 = 率先启动的龙头
    """
    leaders_by_sector = {}

    for sec_info in active_sectors:
        etf_sector   = sec_info["sector"]
        launch_date  = sec_info["launch_date"]
        stocks       = get_stocks_by_sector(etf_sector)

        if not stocks:
            continue

        print(f"\n  [{etf_sector}] 扫描{len(stocks)}只个股，板块启动点:{launch_date}")

        candidates = []
        for symbol, info in stocks.items():
            try:
                bull_info = get_stock_bull_info(symbol)
                if bull_info is None:
                    continue
                if bull_info["trend"] != 1:
                    continue  # 只要当前多头

                candidates.append({
                    "symbol":    symbol,
                    "name":      info["name"],
                    "sector":    info["sector"],
                    "bull_days": bull_info["bull_days"],
                    "bull_since":bull_info["bull_since"],
                    "st_dist":   bull_info["st_dist"],
                })
                print(f"    ✓ {symbol} 多头{bull_info['bull_days']}天 自{bull_info['bull_since']}")

            except Exception as e:
                print(f"    {symbol}: 错误 {e}")

        # 按bull_days从长到短排列
        candidates.sort(key=lambda x: x["bull_days"], reverse=True)
        leaders_by_sector[etf_sector] = {
            "launch_date": launch_date,
            "pct":         sec_info["pct"],
            "direction":   sec_info["direction"],
            "candidates":  candidates,
        }

    return leaders_by_sector

# ─── 生成HTML ──────────────────────────────────────────────────────────────
def build_html(report_date, leaders_by_sector):

    th  = 'style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:left;border-bottom:1px solid #ddd;"'
    thr = 'style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:right;border-bottom:1px solid #ddd;"'
    thc = 'style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:center;border-bottom:1px solid #ddd;"'

    sections = ""
    for etf_sector, data in leaders_by_sector.items():
        candidates  = data["candidates"]
        launch_date = data["launch_date"]
        pct         = data["pct"]
        direction   = data["direction"]
        dir_col     = "#c0392b" if direction == "↑↑" else "#856404"

        rows = ""
        for i, r in enumerate(candidates[:3]):  # 只显示前3名
            bg     = "#ffffff" if i % 2 == 0 else "#f9f9f9"
            st_col = "#c0392b" if (r["st_dist"] or 0) > 0 else "#1a56db"
            # 第一名特别标注
            rank   = "🏆" if i == 0 else f"{i+1}"
            rows += (
                f'<tr style="background:{bg};">'
                f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;font-weight:bold;">{rank}</td>'
                f'<td style="padding:7px 10px;border-bottom:1px solid #eee;font-weight:bold;white-space:nowrap;">{r["symbol"]}</td>'
                f'<td style="padding:7px 10px;border-bottom:1px solid #eee;font-size:12px;color:#555;">{r["name"]}</td>'
                f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;font-weight:bold;color:#1a7340;">{r["bull_days"]}天</td>'
                f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;color:#888;font-size:12px;">{r["bull_since"]}</td>'
                f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:right;font-weight:bold;color:{st_col};">{r["st_dist"]:+.1f}%</td>'
                f'</tr>'
            )

        if not rows:
            rows = '<tr><td colspan="6" style="padding:10px;color:#aaa;text-align:center;">无多头个股</td></tr>'

        total = len(candidates)
        sections += f"""
        <div style="margin-bottom:24px;">
          <table width="100%" cellpadding="0" cellspacing="0" border="0">
            <tr><td style="background:#fdecea;border-left:4px solid #c0392b;padding:10px 14px;border-radius:4px 4px 0 0;">
              <span style="font-size:14px;font-weight:bold;color:#c0392b;">
                {etf_sector} · 多头{pct}% <span style="color:{dir_col};">{direction}</span>
              </span>
              <span style="font-size:12px;color:#888;margin-left:12px;">
                板块启动: {launch_date or '未知'} · 多头个股: {total}只
              </span>
            </td></tr>
          </table>
          <table width="100%" cellpadding="0" cellspacing="0" border="0"
                 style="border-collapse:collapse;font-size:13px;border:1px solid #ddd;border-top:none;">
            <thead><tr>
              <th {thc}>排名</th>
              <th {th}>代码</th>
              <th {th}>名称</th>
              <th {thc}>多头天数</th>
              <th {thc}>转多日期</th>
              <th {thr}>趋势线</th>
            </tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>"""

    if not sections:
        sections = '<p style="color:#aaa;text-align:center;padding:20px;">今日无启动板块</p>'

    return f"""<table width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr><td align="center">
    <table width="620" cellpadding="0" cellspacing="0" border="0"
           style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#222;padding:16px;">
      <tr><td>
        <h2 style="margin:0 0 4px;font-size:17px;">🏆 美股龙头候选</h2>
        <p style="margin:0 0 6px;color:#888;font-size:12px;">温哥华时间 {report_date}</p>
        <p style="margin:0 0 20px;color:#aaa;font-size:11px;">
          逻辑：板块启动后，Supertrend多头持续时间最长的个股 = 率先启动的龙头
        </p>
        {sections}
      </td></tr>
    </table>
    </td></tr></table>"""

# ─── 发邮件 ────────────────────────────────────────────────────────────────
def send_email(html, report_date, sector_count):
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        print("[邮件] 未设置RESEND_API_KEY")
        return
    subject = f"美股龙头候选 {report_date} · {sector_count}个启动板块"
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

    # 1. 扫描ETF清单，获取板块状态
    print("[扫描ETF板块]")
    results = []
    for symbol, name in WATCHLIST_US:
        try:
            r = scan_symbol(symbol, name, classify_us, signal_days=3, trend_days=TREND_DAYS)
            if r:
                results.append(r)
        except Exception as e:
            print(f"  {symbol}: {e}")

    print(f"  ETF扫描完成: {len(results)}只")

    # 2. 找启动板块
    print("[识别启动板块]")
    active_sectors = find_active_sectors(results)

    if not active_sectors:
        print("[结果] 当前无启动板块")
        html = build_html(report_date, {})
        send_email(html, report_date, 0)
        return

    # 3. 扫描个股，找龙头
    print("[扫描个股]")
    leaders_by_sector = scan_leaders(active_sectors)

    # 4. 生成报告
    total_leaders = sum(len(v["candidates"]) for v in leaders_by_sector.values())
    print(f"\n[完成] {len(active_sectors)}个启动板块，{total_leaders}只多头个股")

    html = build_html(report_date, leaders_by_sector)
    send_email(html, report_date, len(active_sectors))

if __name__ == "__main__":
    main()
