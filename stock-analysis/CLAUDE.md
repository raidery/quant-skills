# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this stock-analysis skill repository.

## Repository Overview

This is a quantitative finance skill for Claude Code, containing custom scripts for analyzing Chinese A-share market data using the akshare library. The skill provides real-time market analysis, stock recommendations, sector screening, and automated timed analysis.

## Project Structure

```
stock-analysis/
├── SKILL.md              # Skill documentation with AI decision guide
├── README.md             # User manual and quick start guide
├── SETUP.md              # Installation and setup documentation
├── config.json           # User preferences and configuration
├── install.py            # Installation script
├── start.bat             # Quick start script (Windows)
└── scripts/              # Analysis scripts directory
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
# Install dependencies
pip install akshare pandas

# Or run the installation script
python install.py
```

### Running Analyses
```bash
# Real-time market analysis
python scripts/quick_analysis.py

# Stock recommendations
python scripts/stock_recommend.py

# Morning market report
python scripts/morning_report.py

# Cron job optimized analysis
python scripts/cron_stock_analysis.py
```

### Testing the Connection
```bash
# Test akshare connection
python scripts/test_akshare.py
```

## Architecture

### Core Components

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

Stored in `config.json`:
- **Sectors**: Technology, liquor, aerospace, semiconductors, chips, aviation
- **Risk Level**: Medium
- **Investment Style**: Event-driven, medium-term
- **Screening Criteria**: Volume ratio > 1.5, price change 0-7%

## Important Notes

1. **Trading Hours**: Data only available during market hours (09:30-15:00 China time)
2. **Data Source**: akshare connects to Eastmoney API
3. **Network Dependency**: Requires internet connection for real-time data
4. **Timing**: Data may have 1-5 minute delay
5. **Dependencies**: Requires Python 3.8+, akshare, and pandas

## Development Workflow

When modifying the stock analysis skill:

1. Edit scripts in `scripts/` directory
2. Update configuration in `config.json` if needed
3. Test changes with sample data
4. Verify output formatting
5. Update documentation in `SKILL.md` and `README.md`

## Common Analysis Patterns

```python
# Basic real-time analysis
python scripts/quick_analysis.py

# Personalized stock recommendations
python scripts/stock_recommend.py

# Morning market overview
python scripts/morning_report.py

# Scheduled analysis (optimized for cron jobs)
python scripts/cron_stock_analysis.py
```

## Configuration Customization

Users can customize their investment preferences by editing `config.json`:

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