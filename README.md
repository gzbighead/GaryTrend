# GaryPOWER Weekly - 市场趋势报告系统

每天自动运行，输出美股和A股的趋势报告，包含：
- 最近3日信号（空转多 / 多转空 / 多头调整）
- 当前状态截面（多头/空头/板块分布）
- 60天趋势方向
- AI综合判断

## 文件结构

```
garypower-weekly/
├── engine.py          # 计算引擎（美股A股共用）
├── watchlist_us.py    # 美股清单 + 自动分类
├── watchlist_a.py     # A股清单 + 自动分类
├── report_us.py       # 美股报告主程序
├── report_a.py        # A股报告主程序
├── worker.js          # Cloudflare Worker触发器
├── wrangler.toml      # Worker配置
└── .github/workflows/
    ├── report_us.yml  # 美股 GitHub Actions
    └── report_a.yml   # A股 GitHub Actions
```

## 架构

```
Cloudflare Worker (cron)
    ├── UTC 23:30 周日至周四 → repository_dispatch: run_report_a  → report_a.py
    └── UTC 00:00 周二至周六 → repository_dispatch: run_report_us → report_us.py
```

## 部署步骤

### 1. GitHub仓库

- 新建仓库 `garypower-weekly`
- 上传所有文件
- 在 Settings → Secrets → Actions 添加：
  - `RESEND_API_KEY`：Resend邮件API Key
  - `ANTHROPIC_API_KEY`：Claude API Key

### 2. Cloudflare Worker

```bash
npm install -g wrangler
wrangler login
wrangler deploy
```

在 Cloudflare Workers 控制台 → Settings → Variables 添加加密变量：
- `GITHUB_TOKEN`：GitHub Personal Access Token（需要 `repo` 权限）
- `GITHUB_OWNER`：你的GitHub用户名
- `GITHUB_REPO`：`garypower-weekly`

### 3. 手动测试

Worker部署后，访问以下URL手动触发：
```
https://garypower-trigger.your-subdomain.workers.dev/?target=us
https://garypower-trigger.your-subdomain.workers.dev/?target=a
```

## 扩充清单

直接在 `watchlist_us.py` 或 `watchlist_a.py` 末尾加一行：
```python
("AAPL", "苹果"),          # 自动识别为个股
("XLK",  "科技行业ETF"),   # 自动归类为科技板块
```
无需改任何其他文件。

## 参数调整

在 `report_us.py` / `report_a.py` 顶部：
```python
SIGNAL_DAYS = 3   # 信号回看天数（今天/昨天/前天）
TREND_DAYS  = 60  # 趋势回看天数
```
