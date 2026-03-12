# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a quantitative finance skills repository for Claude Code, containing custom skills for querying Chinese A-share market data. The repository contains two main skills:

1. **wencai**: Uses the pywencai library for natural language queries to Wencai (问财) platform
2. **stock-analysis**: Uses akshare library for real-time market analysis and stock recommendations

## Project Structure

```
quant-skills/
├── CLAUDE.md                 # This file - repository guidance
├── wencai/                   # Production wencai skill
│   ├── SKILL.md             # Skill documentation
│   ├── scripts/
│   │   └── check_environment.py
│   └── references/
│       ├── api_reference.md
│       └── query_examples.md
├── pywencai/                 # Development/testing directory for wencai
│   ├── TEST_GUIDE.md
│   ├── test_comprehensive.py
│   └── wencai/              # Skill source files
└── stock-analysis/           # Production stock analysis skill
    ├── SKILL.md             # Skill documentation with AI decision guide
    ├── README.md            # User manual and quick start guide
    ├── SETUP.md             # Installation and setup documentation
    ├── config.json          # User preferences and configuration
    ├── install.py           # Installation script
    ├── start.bat            # Quick start script (Windows)
    └── scripts/             # Analysis scripts directory
        ├── quick_analysis.py      # Real-time market analysis
        ├── stock_recommend.py     # Stock recommendation engine
        ├── morning_report.py      # Morning market report generator
        ├── cron_stock_analysis.py # Cron job optimized analysis
        ├── final_analysis.py      # Comprehensive analysis
        ├── recommend.py          # Stock recommendation filters
        ├── recommend2.py         # Relaxed condition recommendations
        ├── recommend3.py         # Name-based search recommendations
        ├── test_akshare.py       # Akshare connection testing
        ├── check_columns.py      # Data column validation
        ├── check_sectors.py      # Sector classification checking
        ├── simple_analysis.py    # Simplified analysis
        ├── analyze.py           # Core analysis functions
        └── quick_check.py       # Quick market check
```

## Key Commands

### Environment Setup
```bash
# For wencai skill
pip install pywencai
# Node.js v16+ is required (pywencai executes JS internally)

# For stock-analysis skill
pip install akshare pandas

# Or run the installation script for stock-analysis
python stock-analysis/install.py
```

### Testing the Skills

#### Wencai Skill
```bash
# Set cookie (required for all queries)
export WENCAI_COOKIE="your_cookie_here"

# Run test query
python pywencai/wencai/scripts/query_wencai.py
```

#### Stock Analysis Skill
```bash
# Test akshare connection
python stock-analysis/scripts/test_akshare.py

# Run real-time analysis
python stock-analysis/scripts/quick_analysis.py

# Generate stock recommendations
python stock-analysis/scripts/stock_recommend.py

# Generate morning report
python stock-analysis/scripts/morning_report.py
```

## Architecture

### Wencai Skill

The wencai skill enables natural language queries for Chinese A-share market data through the pywencai library.

**Core Components:**

1. **query_wencai.py** - Main query script with:
   - Cookie management (parameter > env var > config file)
   - Column name cleaning (removes date prefixes)
   - Smart column selection (prioritizes key financial data)
   - Markdown table output

2. **check_environment.py** - Validates:
   - Node.js v16+ installation
   - pywencai package availability

3. **SKILL.md** - Skill documentation with:
   - Quick start examples
   - Cookie authentication guide
   - Common query patterns
   - Best practices

**Data Flow:**
1. User provides natural language query (e.g., "涨停股", "ROE大于20%")
2. Script retrieves cookie from parameter/env/config
3. Calls pywencai.get() with query parameters
4. Cleans column names and selects key columns
5. Returns Markdown table (limited to max_rows)

### Stock Analysis Skill

The stock-analysis skill provides real-time market analysis, stock recommendations, sector screening, and automated timed analysis using the akshare library.

**Core Components:**

1. **Configuration Management** (`config.json`)
   - User investment preferences (sectors, risk level, style)
   - Trading rules (position limits, stop loss)
   - Data source settings
   - Alert configurations

2. **Analysis Scripts**
   - `quick_analysis.py`: Fast real-time market overview
   - `stock_recommend.py`: Personalized stock recommendations
   - `morning_report.py`: Pre-market analysis report
   - `cron_stock_analysis.py`: Optimized for scheduled execution

3. **Data Processing Layer**
   - Uses akshare library for real-time A-share data
   - Filters stocks based on user preferences
   - Calculates sector performance metrics
   - Applies technical screening criteria

### Data Flow

1. User initiates analysis request
2. Script loads user preferences from `config.json`
3. Connects to akshare data source
4. Retrieves real-time A-share market data
5. Filters stocks by sector preferences
6. Applies technical screening (volume ratio, price change)
7. Generates formatted output with recommendations

### User Preferences

Stored in `stock-analysis/config.json`:
- **Sectors**: Technology, liquor, aerospace, semiconductors, chips, aviation
- **Risk Level**: Medium
- **Investment Style**: Event-driven, medium-term
- **Screening Criteria**: Volume ratio > 1.5, price change 0-7%

## Important Notes

### Wencai Skill
1. **Node.js Dependency**: pywencai requires Node.js v16+ to execute internal JavaScript code
2. **Cookie Expiration**: Cookies expire periodically and must be refreshed
3. **Rate Limiting**: Use low-frequency queries to avoid being blocked by the service
4. **Data Delay**: Market data may have delays and is not real-time
5. **Column Cleaning**: The script automatically removes date prefixes like "20260309[涨跌幅]" → "涨跌幅"

### Stock Analysis Skill
1. **Trading Hours**: Data only available during market hours (09:30-15:00 China time)
2. **Data Source**: akshare connects to Eastmoney API
3. **Network Dependency**: Requires internet connection for real-time data
4. **Timing**: Data may have 1-5 minute delay
5. **Dependencies**: Requires Python 3.8+, akshare, and pandas

## Development Workflow

When modifying either skill:

### Wencai Skill
1. Edit files in `wencai/` directory (production source)
2. Test changes using scripts in `pywencai/` directory
3. Verify environment with `check_environment.py`
4. Test queries with valid cookie
5. Update documentation in SKILL.md and references/

### Stock Analysis Skill
1. Edit scripts in `stock-analysis/scripts/` directory
2. Update configuration in `stock-analysis/config.json` if needed
3. Test changes with sample data
4. Verify output formatting
5. Update documentation in `stock-analysis/SKILL.md` and `stock-analysis/README.md`

## Common Query Examples

### Wencai Skill
```python
# Basic query
query_wencai("今日涨停股")

# Filtered and sorted
query_wencai("ROE大于20%的股票", sort_key="ROE", sort_order="desc", max_rows=20)

# Multi-condition technical screening
query_wencai("涨幅大于1%，大单金额大于5000万，10日内ma10金叉ma60", loop=True)

# Non-stock queries
query_wencai("上证指数", query_type="zhishu")
```

### Stock Analysis Skill
```python
# Basic real-time analysis
python stock-analysis/scripts/quick_analysis.py

# Personalized stock recommendations
python stock-analysis/scripts/stock_recommend.py

# Morning market overview
python stock-analysis/scripts/morning_report.py

# Scheduled analysis (optimized for cron jobs)
python stock-analysis/scripts/cron_stock_analysis.py
```

## Configuration Customization

Users can customize their investment preferences by editing `stock-analysis/config.json`:

```json
{
  "user_preferences": {
    "investment": {
      "sectors": ["科技", "白酒", "航天"],
      "risk_level": "中等",
      "style": "事件驱动、中短线",
      "filter_conditions": {
        "volume_ratio_min": 1.5,
        "change_percent_min": 0,
        "change_percent_max": 7
      }
    }
  }
}
```