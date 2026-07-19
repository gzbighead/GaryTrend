#!/usr/bin/env python3
"""
A股趋势报告
每天运行，输出：
  - 今天/昨天/前天 信号汇总
  - 当前状态截面（多头/空头/板块分布）
  - 60天趋势方向
  - AI综合判断
"""

import os
import datetime
import requests

from watchlist_a import WATCHLIST_A, classify_a
from engine import (
    scan_symbol, calc_state, calc_sector_state,
    calc_signals, calc_trend_series, calc_sector_trend,
    last_n_days,
)

# ─── 配置 ──────────────────────────────────────────────────────────────────
EMAIL_TO   = ["garyfocus@hotmail.com"]
EMAIL_FROM = "A股趋势报告 <messenger@ceic.ca>"
SIGNAL_DAYS = 3   # 信号回看天数：今天/昨天/前天
TREND_DAYS  = 60  # 趋势回看天数

# ─── 工具函数 ──────────────────────────────────────────────────────────────
def fmt_val(v, decimals=3):
    return f"{v:.{decimals}f}" if v is not None else "-"

def trend_emoji(t):
    return "多头" if t == 1 else "空头"

def trend_cell_style(t):
    """多头红色，空头蓝色，色弱友好"""
    if t == 1:
        return 'style="padding:6px 8px;text-align:center;background:#fdecea;color:#c0392b;font-weight:bold;"'
    return 'style="padding:6px 8px;text-align:center;background:#e8f0fe;color:#1a56db;font-weight:bold;"'

def pct_color(pct):
    if pct >= 70: return "#1a7340"
    if pct >= 50: return "#2e7d32"
    if pct >= 30: return "#856404"
    return "#922b21"

def pct_bg(pct):
    if pct >= 70: return "#e6f4ea"
    if pct >= 50: return "#f0f7f0"
    if pct >= 30: return "#fef9e7"
    return "#fdecea"

def dir_color(d):
    return "#1a7340" if "↑" in d else ("#922b21" if "↓" in d else "#888")

# ─── 组织AI prompt ─────────────────────────────────────────────────────────
def build_prompt(report_date, signal_dates, signals_by_date,
                 current_state, sector_state, trend_series, sector_trend, results):
    lines = []
    lines.append(f"以下是A股市场截至 {report_date} 的技术面扫描数据。")
    lines.append("请根据数据给出市场分析和投资建议，重点关注趋势方向和板块轮动。")
    lines.append("")

    # 信号
    lines.append("【最近3日信号】")
    for date in signal_dates:
        sigs = signals_by_date[date]
        bull_n = len(sigs["空转多"])
        bear_n = len(sigs["多转空"])
        adj_n  = len(sigs["多头调整"])
        lines.append(f"{date}: 空转多{bull_n}个 多转空{bear_n}个 多头调整{adj_n}个")
        if sigs["空转多"]:
            lines.append("  空转多: " + ", ".join(f"{r['symbol']}({r['name']})" for r in sigs["空转多"]))
        if sigs["多转空"]:
            lines.append("  多转空: " + ", ".join(f"{r['symbol']}({r['name']})" for r in sigs["多转空"]))
    lines.append("")

    # 当前状态
    s = current_state
    t = s["total"]
    lines.append("【当前状态】")
    lines.append(f"多头: {s['bull']}只({round(s['bull']/t*100) if t else 0}%) "
                 f"多头调整: {s['adj']}只 "
                 f"空头: {s['bear']}只({round(s['bear']/t*100) if t else 0}%) "
                 f"共{t}只")
    lines.append("")

    # 板块状态
    lines.append("【板块多头比例（当前）】")
    sorted_sec = sorted(sector_state.items(), key=lambda x: x[1]["pct"], reverse=True)
    for sec, stat in sorted_sec:
        direction = sector_trend.get(sec, {}).get("direction", "-")
        lines.append(f"  {sec:<12} {stat['pct']:>3}%  {direction}  ({stat['bull']}/{stat['total']}只)")
    lines.append("")

    # 60天趋势（取每周五或每5个点一个，避免数据过多）
    lines.append("【60天多头比例趋势（每5日一个采样点）】")
    sampled = trend_series[::5] + ([trend_series[-1]] if trend_series else [])
    for pt in sampled:
        lines.append(f"  {pt['date']}  多头{pt['bull_pct']}%  ({pt['bull']}/{pt['total']})")
    lines.append("")

    # 指数和个股状态
    lines.append("【指数和核心个股（当前状态）】")
    for r in results:
        if r["layer"] not in ("index", "stock"): continue
        snap = r["snapshots"][-1] if r["snapshots"] else None
        if not snap: continue
        t_str  = "多头" if snap["trend"] == 1 else "空头"
        st_str = f"趋势线距离{snap['st_dist']:+.1f}%" if snap["st_dist"] is not None else ""
        lines.append(f"  {r['symbol']:<8} {r['name']:<16} {t_str}  {st_str}")
    lines.append("")

    lines.append("分析原则：")
    lines.append("- 只基于以上技术面数据，不引用任何外部信息或个人假设")
    lines.append("- 重点从资金流动角度解读：板块间的强弱对比反映了资金在往哪里走、在回避什么")
    lines.append("- 寻找数据内部的逻辑关联，而不是孤立描述每个板块")
    lines.append("- 指出数据之间的矛盾或异常，这往往是最有价值的信号")
    lines.append("- 结论必须能从数据中找到直接依据，不做无根据的推测")
    lines.append("")
    lines.append("请用中文输出分析报告，结构如下：")
    lines.append("")
    lines.append("1. 资金流向判断")
    lines.append("   - 资金正在流入哪类资产（进攻/防御/现金）")
    lines.append("   - 依据：哪些板块同步转强或转弱，形成什么组合")
    lines.append("   - 这个资金流向组合历史上通常出现在市场的什么阶段")
    lines.append("")
    lines.append("2. 板块轮动逻辑")
    lines.append("   - 强势板块和弱势板块之间有什么内在关联")
    lines.append("   - 有没有异常信号：某板块的走势与整体方向不符，说明什么")
    lines.append("   - 哪个板块的变化最值得警惕或关注，为什么")
    lines.append("")
    lines.append("3. 关键标的的位置")
    lines.append("   - 列出上证指数，深圳成指，创业板综合指数以及科创板的最新收盘指数")
    lines.append("   - 指数距趋势线的距离意味着什么（多空博弈的边界在哪）")
    lines.append("")
    lines.append("4. 操作建议")
    lines.append("   - 基于以上资金流向判断，现在应该做什么、等什么信号")
    lines.append("   - 趋势跟踪原则：资本保护优先，只在右侧确认后入场，不抄底")
    lines.append("   - 在发现某个标的趋势确定性高的时候，可以直接推荐 ")           
    lines.append("")
    lines.append("风格：态度鲜明，直接给结论，说清楚依据。没有100%正确的投资，只有废话才能100%正确。分析可以错，但不能模糊。不写'需要观察''存在可能''或许'这类股评式的模糊表达。每一个判断都要有明确立场。")

    return "\n".join(lines)

# ─── 调用Claude API ────────────────────────────────────────────────────────
def call_claude(prompt):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "（未设置ANTHROPIC_API_KEY）"
    res = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key":         api_key,
            "anthropic-version": "2023-06-01",
            "content-type":      "application/json",
        },
        json={
            "model":      "claude-sonnet-4-5",
            "max_tokens": 2000,
            "messages":   [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    if res.status_code == 200:
        return res.json()["content"][0]["text"]
    return f"（API调用失败：{res.status_code}）"

# ─── 生成HTML ──────────────────────────────────────────────────────────────
def build_html(report_date, signal_dates, signals_by_date,
               current_state, sector_state, trend_series, sector_trend,
               results, ai_text):

    # ── Zoho移动端兼容：用table属性控制宽度，不依赖CSS flex/max-width ──

    def section_header(emoji, title):
        return f"""<table width="100%" cellpadding="0" cellspacing="0" border="0">
          <tr><td style="background:#e8f0fe;border-left:4px solid #1a56db;padding:10px 14px;border-radius:4px 4px 0 0;">
            <span style="font-size:14px;font-weight:bold;color:#1a56db;">{emoji} {title}</span>
          </td></tr></table>"""

    def wrap_table(header_html, body_html):
        return f"""<div style="margin-bottom:20px;">
          {header_html}
          <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-size:13px;border:1px solid #ddd;border-top:none;">
            {body_html}
          </table></div>"""

    # ── AI分析 ──
    ai_html  = ai_text.replace("\n\n", "</p><p style='margin:8px 0;'>").replace("\n", "<br>")
    ai_block = f"""<div style="background:#f8f9ff;border-left:4px solid #1a56db;border-radius:4px;padding:14px;margin-bottom:20px;">
      <div style="font-size:13px;font-weight:bold;color:#1a56db;margin-bottom:8px;">🤖 A股市场分析</div>
      <div style="font-size:13px;line-height:1.7;color:#333;"><p style="margin:0">{ai_html}</p></div>
    </div>"""

    # ── 状态概况：用table代替flex ──
    s        = current_state
    t        = s["total"]
    bull_pct = round(s["bull"]/t*100) if t else 0
    bear_pct = round(s["bear"]/t*100) if t else 0
    adj_pct  = round(s["adj"]/t*100)  if t else 0
    state_cards = f"""<table width="100%" cellpadding="6" cellspacing="4" border="0" style="margin-bottom:20px;">
      <tr>
        <td width="25%" style="background:#fdecea;border-radius:8px;padding:12px;text-align:center;">
          <div style="font-size:22px;font-weight:bold;color:#c0392b;">{s['bull']}</div>
          <div style="font-size:11px;color:#c0392b;margin-top:2px;">多头 {bull_pct}%</div>
        </td>
        <td width="25%" style="background:#fef9e7;border-radius:8px;padding:12px;text-align:center;">
          <div style="font-size:22px;font-weight:bold;color:#856404;">{s['adj']}</div>
          <div style="font-size:11px;color:#856404;margin-top:2px;">调整 {adj_pct}%</div>
        </td>
        <td width="25%" style="background:#e8f0fe;border-radius:8px;padding:12px;text-align:center;">
          <div style="font-size:22px;font-weight:bold;color:#1a56db;">{s['bear']}</div>
          <div style="font-size:11px;color:#1a56db;margin-top:2px;">空头 {bear_pct}%</div>
        </td>
        <td width="25%" style="background:#f0f0f0;border-radius:8px;padding:12px;text-align:center;">
          <div style="font-size:22px;font-weight:bold;color:#555;">{t}</div>
          <div style="font-size:11px;color:#555;margin-top:2px;">总扫描</div>
        </td>
      </tr>
    </table>"""

    # ── 信号表格：标的单独一行，避免挤压 ──
    signal_rows = ""
    sig_labels  = {
        "空转多":   ("#c0392b", "#fdecea"),
        "多转空":   ("#1a56db", "#e8f0fe"),
        "多头调整": ("#856404", "#fef9e7"),
    }
    for date in signal_dates:
        sigs    = signals_by_date[date]
        has_any = any(sigs[k] for k in sigs)
        # 日期行
        signal_rows += f'<tr><td colspan="2" style="padding:8px 10px;border-bottom:1px solid #eee;background:#f9f9f9;font-weight:bold;font-size:13px;">{date}</td></tr>'
        if not has_any:
            signal_rows += f'<tr><td colspan="2" style="padding:6px 10px;border-bottom:1px solid #eee;color:#aaa;font-size:12px;">无信号</td></tr>'
            continue
        for sig_type, (color, bg) in sig_labels.items():
            items = sigs[sig_type]
            if not items: continue
            # 信号类型行
            signal_rows += f'<tr><td colspan="2" style="padding:6px 10px;border-bottom:1px solid #f0f0f0;background:{bg};color:{color};font-weight:bold;font-size:12px;">{sig_type} · {len(items)}只</td></tr>'
            # 每个标的单独一行
            for r in items:
                signal_rows += f'<tr><td width="8" style="border-bottom:1px solid #f5f5f5;"></td><td style="padding:4px 10px;border-bottom:1px solid #f5f5f5;font-size:12px;color:#555;">{r["symbol"]} {r["name"]}</td></tr>'

    signal_table = wrap_table(
        section_header("📡", f"最近{SIGNAL_DAYS}日信号"),
        f'<tbody>{signal_rows}</tbody>'
    )

    # ── 板块表格 ──
    sorted_sec  = sorted(sector_state.items(), key=lambda x: x[1]["pct"], reverse=True)
    sector_rows = ""
    for sec, stat in sorted_sec:
        st_trend  = sector_trend.get(sec, {})
        direction = st_trend.get("direction", "-")
        count     = st_trend.get("count", stat.get("total", 0))
        bg        = pct_bg(stat["pct"])
        col       = pct_color(stat["pct"])
        dc        = dir_color(direction)
        sector_rows += (
            f'<tr>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;font-weight:bold;">{sec}</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;background:{bg};color:{col};font-weight:bold;">{stat["pct"]}%</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;font-weight:bold;color:{dc};">{direction}</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;color:#888;font-size:12px;">{stat["bull"]}/{count}</td>'
            f'</tr>'
        )

    sector_table = wrap_table(
        section_header("🏭", "板块多头比例"),
        f'<thead><tr>'
        f'<th style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:left;border-bottom:1px solid #ddd;">板块</th>'
        f'<th style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:center;border-bottom:1px solid #ddd;">多头%</th>'
        f'<th style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:center;border-bottom:1px solid #ddd;">5日</th>'
        f'<th style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:center;border-bottom:1px solid #ddd;">ETF</th>'
        f'</tr></thead>'
        f'<tbody>{sector_rows}</tbody>'
    )

    # ── 60天趋势表格 ──
    sampled    = trend_series[::5]
    if trend_series and (not sampled or sampled[-1] != trend_series[-1]):
        sampled.append(trend_series[-1])
    trend_rows = ""
    for i, pt in enumerate(sampled):
        row_bg = "#ffffff" if i % 2 == 0 else "#f9f9f9"
        col    = pct_color(pt["bull_pct"])
        bgc    = pct_bg(pt["bull_pct"])
        trend_rows += (
            f'<tr style="background:{row_bg};">'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;font-size:12px;">{pt["date"]}</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;background:{bgc};color:{col};font-weight:bold;">{pt["bull_pct"]}%</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;color:#c0392b;font-size:12px;">{pt["bull"]}</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;color:#856404;font-size:12px;">{pt["adj"]}</td>'
            f'<td style="padding:7px 10px;border-bottom:1px solid #eee;text-align:center;color:#1a56db;font-size:12px;">{pt["bear"]}</td>'
            f'</tr>'
        )

    trend_table = wrap_table(
        section_header("📈", "60天多头比例趋势"),
        f'<thead><tr>'
        f'<th style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:left;border-bottom:1px solid #ddd;">日期</th>'
        f'<th style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:center;border-bottom:1px solid #ddd;">多头%</th>'
        f'<th style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:center;border-bottom:1px solid #ddd;">多头</th>'
        f'<th style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:center;border-bottom:1px solid #ddd;">调整</th>'
        f'<th style="padding:7px 10px;background:#f5f5f5;font-size:12px;color:#666;text-align:center;border-bottom:1px solid #ddd;">空头</th>'
        f'</tr></thead>'
        f'<tbody>{trend_rows}</tbody>'
    )

    # ── 指数和个股表格：4列，去掉均线距离 ──
    def index_stock_rows(layer):
        rows = ""
        for r in results:
            if r["layer"] != layer: continue
            snap = r["snapshots"][-1] if r["snapshots"] else None
            if not snap: continue
            t_label = trend_emoji(snap["trend"])
            t_bg    = "#fdecea" if snap["trend"] == 1 else "#e8f0fe"
            t_col   = "#c0392b" if snap["trend"] == 1 else "#1a56db"
            st_d    = f'{snap["st_dist"]:+.1f}%' if snap["st_dist"] is not None else "-"
            st_col  = "#c0392b" if (snap.get("st_dist") or 0) > 0 else "#1a56db"
            rows += (
                f'<tr>'
                f'<td style="padding:7px 8px;border-bottom:1px solid #eee;font-weight:bold;font-size:12px;white-space:nowrap;">{r["symbol"]}</td>'
                f'<td style="padding:7px 8px;border-bottom:1px solid #eee;color:#555;font-size:12px;">{r["name"]}</td>'
                f'<td style="padding:7px 8px;border-bottom:1px solid #eee;text-align:center;background:{t_bg};color:{t_col};font-weight:bold;font-size:12px;white-space:nowrap;">{t_label}</td>'
                f'<td style="padding:7px 8px;border-bottom:1px solid #eee;text-align:right;font-weight:bold;color:{st_col};font-size:12px;white-space:nowrap;">{st_d}</td>'
                f'</tr>'
            )
        return rows

    th_style = 'style="padding:7px 8px;background:#f5f5f5;font-size:12px;color:#666;text-align:left;border-bottom:1px solid #ddd;"'
    thc_style = 'style="padding:7px 8px;background:#f5f5f5;font-size:12px;color:#666;text-align:center;border-bottom:1px solid #ddd;"'
    thr_style = 'style="padding:7px 8px;background:#f5f5f5;font-size:12px;color:#666;text-align:right;border-bottom:1px solid #ddd;"'

    index_table = wrap_table(
        section_header("📌", "指数状态"),
        f'<thead><tr><th {th_style}>代码</th><th {th_style}>名称</th><th {thc_style}>趋势</th><th {thr_style}>趋势线</th></tr></thead>'
        f'<tbody>{index_stock_rows("index")}</tbody>'
    )

    stock_table = wrap_table(
        section_header("⭐", "核心个股状态"),
        f'<thead><tr><th {th_style}>代码</th><th {th_style}>名称</th><th {thc_style}>趋势</th><th {thr_style}>趋势线</th></tr></thead>'
        f'<tbody>{index_stock_rows("stock")}</tbody>'
    )

    return f"""<table width="100%" cellpadding="0" cellspacing="0" border="0">
    <tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0" border="0" style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#222;padding:16px;">
      <tr><td>
        <h2 style="margin:0 0 4px;font-size:17px;">📈 A股市场趋势报告</h2>
        <p style="margin:0 0 16px;color:#888;font-size:12px;">北京时间 {report_date}</p>
        {ai_block}
        {state_cards}
        {signal_table}
        {sector_table}
        {trend_table}
        {index_table}
        {stock_table}
      </td></tr>
    </table>
    </td></tr></table>"""

# ─── 发邮件 ────────────────────────────────────────────────────────────────
def send_email(html, report_date):
    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        print("[邮件] 未设置RESEND_API_KEY")
        return
    res = requests.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "from":    EMAIL_FROM,
            "to":      EMAIL_TO,
            "subject": f"投资分析 - A股趋势报告 {report_date}",
            "html":    html,
        },
    )
    print(f"[邮件] {'成功' if res.status_code==200 else '失败'} {res.status_code}")

# ─── 主流程 ────────────────────────────────────────────────────────────────
def main():
    now         = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    report_date = now.strftime("%Y-%m-%d")
    print(f"[开始] A股报告 {report_date} 共{len(WATCHLIST_A)}只")

    # 1. 扫描所有标的
    results = []
    for symbol, name in WATCHLIST_A:
        try:
            r = scan_symbol(symbol, name, classify_a, SIGNAL_DAYS, TREND_DAYS)
            if r is None:
                print(f"  {symbol}: 数据不足，跳过")
                continue
            results.append(r)
            print(f"  {symbol} [{r['layer']}/{r['sector']}] OK")
        except Exception as e:
            print(f"  {symbol}: 错误 {e}")

    print(f"[扫描完成] {len(results)}只")

    # 2. 取最近3个交易日的日期
    all_dates    = sorted({s["date"] for r in results for s in r["snapshots"]})
    signal_dates = list(reversed(all_dates[-SIGNAL_DAYS:])) if len(all_dates) >= SIGNAL_DAYS else list(reversed(all_dates))

    # 3. 按日期计算信号
    signals_by_date = {date: calc_signals(results, date) for date in signal_dates}

    # 4. 当前状态
    current_state = calc_state(results)
    sector_state  = calc_sector_state(results)

    # 5. 60天趋势
    trend_series  = calc_trend_series(results, TREND_DAYS)
    sector_trend  = calc_sector_trend(results, TREND_DAYS)

    # 6. 调用AI
    prompt      = build_prompt(report_date, signal_dates, signals_by_date,
                               current_state, sector_state, trend_series, sector_trend, results)
    print("[调用Claude API]")
    ai_text     = call_claude(prompt)
    print("[AI完成]")

    # 7. 生成HTML并发邮件
    html = build_html(report_date, signal_dates, signals_by_date,
                      current_state, sector_state, trend_series, sector_trend,
                      results, ai_text)
    send_email(html, report_date)

if __name__ == "__main__":
    main()
