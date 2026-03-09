# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a quantitative finance skills repository for Claude Code, containing custom skills for querying Chinese A-share market data using the pywencai library.

## Project Structure

```
quant-skills/
├── wencai/                    # Production wencai skill
│   ├── SKILL.md              # Skill documentation
│   ├── scripts/
│   │   └── check_environment.py
│   └── references/
│       ├── api_reference.md
│       └── query_examples.md
└── pywencai/                  # Development/testing directory
    ├── TEST_GUIDE.md
    ├── test_comprehensive.py
    └── wencai/               # Skill source files
```

## Key Commands

### Environment Verification
```bash
# Check if Node.js v16+ and pywencai are installed
python wencai/scripts/check_environment.py
```

### Testing the Skill
```bash
# Set cookie (required for all queries)
export WENCAI_COOKIE="your_cookie_here"

# Run test query
python pywencai/wencai/scripts/query_wencai.py
```

### Installing Dependencies
```bash
# Install pywencai library
pip install pywencai

# Node.js v16+ is required (pywencai executes JS internally)
# Install from: https://nodejs.org/
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

**Cookie Authentication:**
- Required for all queries
- Priority: function parameter > WENCAI_COOKIE env var > ~/.wencai/config.json
- Obtain from https://www.iwencai.com/ (F12 > Network > Copy Cookie header)

**Query Types Supported:**
- stock (default) - A-share stocks
- zhishu - Indices
- fund - Funds
- conbond - Convertible bonds
- hkstock, usstock, threeboard, etc.

## Important Notes

1. **Node.js Dependency**: pywencai requires Node.js v16+ to execute internal JavaScript code
2. **Cookie Expiration**: Cookies expire periodically and must be refreshed
3. **Rate Limiting**: Use low-frequency queries to avoid being blocked by the service
4. **Data Delay**: Market data may have delays and is not real-time
5. **Column Cleaning**: The script automatically removes date prefixes like "20260309[涨跌幅]" → "涨跌幅"

## Development Workflow

When modifying the wencai skill:

1. Edit files in `wencai/` directory (production source)
2. Test changes using scripts in `pywencai/` directory
3. Verify environment with `check_environment.py`
4. Test queries with valid cookie
5. Update documentation in SKILL.md and references/

## Common Query Examples

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
