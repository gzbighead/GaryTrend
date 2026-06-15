#!/usr/bin/env python3
"""
计算引擎 - 美股和A股共用
负责：拉取数据、计算Supertrend、计算MA20、生成每日快照
"""

import numpy as np
import yfinance as yf

# ─── 参数 ──────────────────────────────────────────────────────────────────
ST_PERIOD     = 10
ST_MULTIPLIER = 3.0
MA_PERIOD     = 20
HISTORY_DAYS  = 90   # 拉取历史长度，覆盖60天趋势 + 计算缓冲

# ─── 基础计算 ──────────────────────────────────────────────────────────────
def fetch_daily(symbol):
    df = yf.Ticker(symbol).history(period="6mo", interval="1d")
    if df.empty or len(df) < ST_PERIOD + MA_PERIOD + 5:
        return None
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df.columns:
            df[col] = df[col].astype(float)
    return df

def calc_atr(df, period):
    high  = df["High"].values
    low   = df["Low"].values
    close = df["Close"].values
    n     = len(close)
    tr    = np.zeros(n)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr[i] = max(high[i]-low[i], abs(high[i]-close[i-1]), abs(low[i]-close[i-1]))
    atr    = np.zeros(n)
    atr[0] = np.mean(tr[:period])
    k      = 1.0 / period
    for i in range(1, n):
        atr[i] = tr[i]*k + atr[i-1]*(1-k)
    atr[:period] = np.nan
    return atr

def calc_supertrend(df, period, multiplier):
    high  = df["High"].values
    low   = df["Low"].values
    close = df["Close"].values
    n     = len(close)
    atr   = calc_atr(df, period)
    hl2   = (high + low) / 2.0
    ub    = hl2 + multiplier * atr
    lb    = hl2 - multiplier * atr
    upper = np.copy(ub)
    lower = np.copy(lb)
    trend = np.full(n, np.nan)
    st    = np.full(n, np.nan)
    for i in range(period, n):
        if np.isnan(atr[i]): continue
        if np.isnan(trend[i-1]):
            trend[i] = 1 if close[i] > ub[i] else -1
            st[i]    = lower[i] if trend[i]==1 else upper[i]
            continue
        upper[i] = ub[i] if (ub[i] < upper[i-1] or close[i-1] > upper[i-1]) else upper[i-1]
        lower[i] = lb[i] if (lb[i] > lower[i-1] or close[i-1] < lower[i-1]) else lower[i-1]
        if   close[i] > upper[i-1]: trend[i] = 1
        elif close[i] < lower[i-1]: trend[i] = -1
        else:                        trend[i] = trend[i-1]
        st[i] = lower[i] if trend[i]==1 else upper[i]
    return trend, st

def calc_ma(df, period):
    return df["Close"].astype(float).rolling(period).mean().values

def safe(v):
    try:
        f = float(v)
        return None if np.isnan(f) else f
    except:
        return None

# ─── 单标的扫描：返回每日快照数组 ─────────────────────────────────────────
def scan_symbol(symbol, name, classify_fn, signal_days=3, trend_days=60):
    """
    返回:
      layer   : index / stock / etf
      sector  : 板块名（ETF）或 None
      snapshots: 按日期从旧到新的快照列表，每个快照包含：
                 date / close / trend(1/-1) / st / ma20 / st_dist% / ma_dist%
    """
    df = fetch_daily(symbol)
    if df is None:
        return None

    trend_arr, st_arr = calc_supertrend(df, ST_PERIOD, ST_MULTIPLIER)
    ma_arr            = calc_ma(df, MA_PERIOD)
    close_arr         = df["Close"].values.astype(float)
    dates             = df.index
    n                 = len(close_arr)

    # 需要的最大回溯天数 = trend_days（60天趋势） + signal_days（信号窗口）
    needed = trend_days + signal_days
    start  = max(0, n - needed)

    snapshots = []
    for i in range(start, n):
        t = safe(trend_arr[i])
        if t is None: continue
        c  = float(close_arr[i])
        s  = safe(st_arr[i])
        m  = safe(ma_arr[i])
        dt = dates[i]
        date_str  = dt.strftime("%Y-%m-%d") if hasattr(dt, "strftime") else str(dt)[:10]
        st_dist   = round((c - s) / s * 100, 2) if s else None
        ma_dist   = round((c - m) / m * 100, 2) if m else None

        # 信号：对比前一天
        prev_t = safe(trend_arr[i-1]) if i > 0 else None
        signal = None
        if prev_t is not None:
            if prev_t == -1 and t == 1:
                signal = "空转多"
            elif prev_t == 1 and t == -1:
                signal = "多转空"
            elif t == 1:
                prev_c  = float(close_arr[i-1]) if i > 0 else c
                prev_m  = safe(ma_arr[i-1]) if i > 0 else m
                if m and prev_m and c < m and prev_c >= prev_m:
                    signal = "多头调整"

        snapshots.append({
            "date":    date_str,
            "close":   round(c, 3),
            "trend":   int(t),
            "st":      round(s, 3) if s else None,
            "ma20":    round(m, 3) if m else None,
            "st_dist": st_dist,
            "ma_dist": ma_dist,
            "signal":  signal,   # 空转多 / 多转空 / 多头调整 / None
        })

    layer, sector = classify_fn(symbol, name)
    return {
        "symbol":    symbol,
        "name":      name,
        "layer":     layer,
        "sector":    sector,
        "snapshots": snapshots,
    }

# ─── 从快照数组提取最近N个交易日的数据 ───────────────────────────────────
def last_n_days(snapshots, n):
    """取最近n个交易日快照"""
    return snapshots[-n:] if len(snapshots) >= n else snapshots

def get_snapshot_at(snapshots, offset=0):
    """offset=0最新，offset=1前一天，以此类推"""
    idx = len(snapshots) - 1 - offset
    return snapshots[idx] if 0 <= idx < len(snapshots) else None

# ─── 全局状态统计（某一天） ────────────────────────────────────────────────
def calc_state(results, date=None):
    """
    统计某一天所有标的的多头/调整/空头数量
    date=None 表示取最新一天
    返回: {bull, adj, bear, total}
    """
    bull = adj = bear = 0
    for r in results:
        snaps = r["snapshots"]
        if not snaps: continue
        if date:
            snap = next((s for s in snaps if s["date"] == date), None)
        else:
            snap = snaps[-1]
        if not snap: continue
        t  = snap["trend"]
        md = snap["ma_dist"]
        if t == 1 and md is not None and md >= 0:
            bull += 1
        elif t == 1:
            adj += 1
        else:
            bear += 1
    total = bull + adj + bear
    return {"bull": bull, "adj": adj, "bear": bear, "total": total}

# ─── 板块状态统计（某一天） ───────────────────────────────────────────────
def calc_sector_state(results, date=None):
    """
    统计各板块某一天的多头比例
    返回: {板块名: {bull, total, pct}}
    """
    sectors = {}
    for r in results:
        if r["layer"] != "etf" or not r["sector"]: continue
        sec   = r["sector"]
        snaps = r["snapshots"]
        if not snaps: continue
        if date:
            snap = next((s for s in snaps if s["date"] == date), None)
        else:
            snap = snaps[-1]
        if not snap: continue
        if sec not in sectors:
            sectors[sec] = {"bull": 0, "total": 0}
        sectors[sec]["total"] += 1
        if snap["trend"] == 1:
            sectors[sec]["bull"] += 1
    for sec in sectors:
        t = sectors[sec]["total"]
        b = sectors[sec]["bull"]
        sectors[sec]["pct"] = round(b / t * 100) if t else 0
    return sectors

# ─── 信号统计（某一天） ───────────────────────────────────────────────────
def calc_signals(results, date):
    """
    统计某一天触发各类信号的标的
    返回: {空转多: [...], 多转空: [...], 多头调整: [...]}
    """
    out = {"空转多": [], "多转空": [], "多头调整": []}
    for r in results:
        snap = next((s for s in r["snapshots"] if s["date"] == date), None)
        if not snap or not snap["signal"]: continue
        sig = snap["signal"]
        if sig in out:
            out[sig].append({
                "symbol": r["symbol"],
                "name":   r["name"],
                "layer":  r["layer"],
                "sector": r["sector"],
                "close":  snap["close"],
                "st":     snap["st"],
                "ma20":   snap["ma20"],
            })
    return out

# ─── 60天趋势：取每个交易日的全局多头比例 ────────────────────────────────
def calc_trend_series(results, days=60):
    """
    取最近days个交易日，每天计算多头占比
    返回: [{date, bull_pct, bull, adj, bear, total}, ...]
    """
    # 收集所有日期
    all_dates = sorted({
        s["date"]
        for r in results
        for s in r["snapshots"]
    })
    # 取最近days天
    recent_dates = all_dates[-days:] if len(all_dates) >= days else all_dates

    series = []
    for date in recent_dates:
        state = calc_state(results, date)
        t     = state["total"]
        pct   = round(state["bull"] / t * 100) if t else 0
        series.append({
            "date":     date,
            "bull_pct": pct,
            **state,
        })
    return series

# ─── 60天板块趋势 ─────────────────────────────────────────────────────────
def calc_sector_trend(results, days=60):
    """
    取最近days个交易日，每天计算各板块多头比例
    返回: {板块名: [{date, pct}, ...]}
    并计算每个板块的周变化方向
    """
    all_dates = sorted({
        s["date"]
        for r in results
        for s in r["snapshots"]
    })
    recent_dates = all_dates[-days:] if len(all_dates) >= days else all_dates

    # 板块列表
    sector_names = sorted({
        r["sector"]
        for r in results
        if r["layer"] == "etf" and r["sector"]
    })

    out = {}
    for sec in sector_names:
        sec_results = [r for r in results if r["sector"] == sec]
        series = []
        for date in recent_dates:
            total = bull = 0
            for r in sec_results:
                snap = next((s for s in r["snapshots"] if s["date"] == date), None)
                if not snap: continue
                total += 1
                if snap["trend"] == 1: bull += 1
            pct = round(bull / total * 100) if total else 0
            series.append({"date": date, "pct": pct, "bull": bull, "total": total})

        # 计算5天变化方向
        if len(series) >= 5:
            delta = series[-1]["pct"] - series[-5]["pct"]
        elif len(series) >= 2:
            delta = series[-1]["pct"] - series[0]["pct"]
        else:
            delta = 0

        if   delta >= 15: direction = "↑↑"
        elif delta >= 5:  direction = "↑"
        elif delta <= -15:direction = "↓↓"
        elif delta <= -5: direction = "↓"
        else:             direction = "→"

        count = len(sec_results)
        out[sec] = {"series": series, "direction": direction, "count": count}

    return out
