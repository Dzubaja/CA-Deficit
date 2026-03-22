# Project: NBS External Sector Dashboard

## What This Project Is

A complete data pipeline + interactive Streamlit dashboard built on publicly available economic data from the National Bank of Serbia (NBS). The pipeline downloads 27 Excel files, extracts and cleans heterogeneous data into a structured SQLite database, and the dashboard presents Serbia's current account, balance of payments, FDI, and external position through professional visualizations.

---

## Who This Is For

Branko — Head of Treasury at a bank in Serbia. Not a professional developer, but understands logic, structure, and data deeply. Builds practical tools to solve real problems. Learns by building.

### Coding Principles (follow these strictly)

1. **Keep it simple** — working solution over perfect architecture
2. **Modular code** — clear functions, no monolithic scripts
3. **Readability > cleverness** — clear variable names, short comments only where useful
4. **Minimal dependencies** — prefer standard libraries
5. **No overengineering** — no enterprise patterns, no unnecessary abstractions

### Preferred Stack

- **Data:** Python (pandas, numpy)
- **Viz:** Plotly (preferred), Matplotlib for simple cases
- **Apps/UI:** Streamlit (default)
- **Storage:** CSV/Excel first, SQLite when needed
- **Avoid:** Complex frameworks, heavy ORMs, abstract architectures

### UI/UX Expectations

- Think like an executive user
- Filters at top, key metrics immediately visible, clear charts
- "Can this be understood in 5 seconds?"
- Minimize clicks, single focus per view
- Premium dark theme — professional, business-grade, not generic

### How to Respond

- Short explanation, then full working code, then run instructions
- For complex tasks: break into steps, build incrementally
- Highlight where parameters can be changed
- Suggest improvements, but don't overcomplicate
- If debugging: explain simply, show exact fix, provide corrected code
- If multiple options: recommend ONE best option

---

## Folder Structure

```
c:/Branko/AI Projects/1. Contex folder/
├── CLAUDE.md                              # This file — full project context for Claude
├── about-me.md                            # User profile and preferences
├── CLAUDE memory remember.docx            # Previous conversation memory
│
└── nbs_dashboard/                         # Main project
    ├── app.py                             # Streamlit dashboard (main entry point)
    ├── config.py                          # Source URLs, paths, file registry
    ├── run_pipeline.py                    # Pipeline orchestrator (download → extract → clean)
    ├── README.md                          # Project documentation
    │
    ├── .streamlit/
    │   └── config.toml                    # Streamlit theme config (dark navy theme)
    │
    ├── dashboard/                         # Dashboard application layer
    │   ├── __init__.py
    │   ├── data_loader.py                 # SQL queries → pandas DataFrames
    │   ├── charts.py                      # All Plotly chart functions (19 charts)
    │   └── styles.py                      # Custom CSS + KPI card HTML generator
    │
    ├── scripts/                           # Data pipeline
    │   ├── download.py                    # Downloads Excel files from NBS website
    │   ├── schema.py                      # SQLite DDL — creates all tables and indexes
    │   ├── extract.py                     # Parses Excel files → raw tables
    │   └── clean.py                       # Standardizes raw → clean tables
    │
    └── data/
        ├── raw_excel/                     # Downloaded .xls/.xlsx files (27 files)
        └── db/
            └── nbs_external_sector.db     # SQLite database (~7 MB, ~46K records)
```

---

## Running the Project

### Data Pipeline
```bash
cd nbs_dashboard
python run_pipeline.py                # full pipeline (download + extract + clean)
python run_pipeline.py --skip-download # skip download, re-extract + re-clean
python run_pipeline.py --force         # re-download everything from NBS
```

### Dashboard
```bash
cd nbs_dashboard
streamlit run app.py
# or: python -m streamlit run app.py
```
Opens at http://localhost:8501

---

## Dashboard Architecture

### app.py — Main Streamlit Application

The entry point. Loads all data via `@st.cache_data`, renders the header, KPI cards, filters, and 5 tabs:

1. **Current Account** — CA balance bar chart (with optional CA/GDP line), stacked components, waterfall decomposition, area evolution
2. **Trade & Financing** — Exports vs Imports bars, FDI coverage ratio, Financial Account components line chart
3. **External Position** — FX reserves trend, external debt trend, key vulnerability indicators (CA/GDP, reserves, debt, coverage)
4. **Component Rankings** — Horizontal bars ranked by value, YoY change chart, historical table
5. **FDI Deep Dive** — Dedicated section with 3 sub-tabs (see below)

**Global filters** (applied across tabs):
- Year range slider (min–max from CA data)
- View mode: "Absolute (EUR mn)" or "% of GDP"

**KPI cards** (top row, always visible):
- Current Account, Trade Balance, Services Surplus, FDI Net Inflow, NBS FX Reserves

### FDI Deep Dive Tab (Tab 5)

Has its own KPI row (Inflows, Outflows, Net FDI, CA Coverage) and 3 sub-tabs:

**By Country:**
- Stacked bar: top N countries (configurable: 5/10/15/20), rest grouped as "Other"
- Concentration chart: top 5 share as % of total over time
- Pivot table: countries × years

**By Sector:**
- Stacked bar: 18 NACE sectors over time (shortened names for readability)
- Horizontal bar: latest year sector breakdown
- Pivot table: sectors × years

**Analytics:**
- Inflows vs Outflows (bar + net line)
- YoY growth (absolute bars + % line on dual axis)
- FDI coverage of CA deficit (bars + 3-yr rolling average + 100% reference line)
- Cumulative FDI inflows (area chart)
- Summary metrics row: avg annual inflow, latest growth, concentration, total cumulative

---

## Design System

### Theme (`.streamlit/config.toml`)
```
primaryColor = "#00D4FF"        (cyan accent)
backgroundColor = "#060B18"     (deep navy)
secondaryBackgroundColor = "#0F1629"  (card surfaces)
textColor = "#E2E8F0"           (light gray)
font = Inter (Google Fonts)
```

### Color Palette (`charts.py` → `COLORS`)
```python
"cyan": "#00D4FF"       # Primary accent, neutral KPIs, FX reserves
"purple": "#7C5CFC"     # Secondary accent, concentration, portfolio
"teal/green": "#06D6A0" # Positive values, inflows, exports, services
"red": "#FF6B8A"        # Negative values, deficits, imports, goods
"gold": "#FBBF24"       # Secondary lines (CA/GDP ratio, trade balance, growth %)
"orange": "#FB923C"     # External debt, other investment, primary income
"magenta": "#FF006E"    # Alert accent (negative card glow)
"pink": "#EC4899"       # FDI country palette
"blue": "#3B82F6"       # FDI palette
"muted": "#8B95A8"      # Secondary text, axis labels
"dim": "#5A6478"        # Tertiary text, subtitles
"bg": "#060B18"         # Page background
"card": "#0F1629"       # Card/surface background
"grid": "rgba(255,255,255,0.04)"  # Chart gridlines
```

### Component-Specific Colors
```python
COMPONENT_COLORS = {
    "Goods": "#FF6B8A",
    "Services": "#06D6A0",
    "Primary Income": "#FB923C",
    "Secondary Income": "#00D4FF",
}
FA_COLORS = {
    "FA.FDI": "#00D4FF",
    "FA.PORTFOLIO": "#7C5CFC",
    "FA.OTHER": "#FB923C",
    "FA.RESERVES": "#FBBF24",
}
```

### KPI Card Styling
- Gradient background: `linear-gradient(145deg, #0F1629, #131A2E)`
- Colored top accent bar (3px): green→teal for positive, red→magenta for negative, cyan→purple for neutral
- Text glow (text-shadow) on values
- Hover lift animation (`translateY(-2px)`)
- Font: Inter 800 (value), 600 (label), 500 (sub-text)
- Separator: middot (`&middot;`) between unit and sub-text

### Chart Styling
- Transparent backgrounds (blend into page)
- Spline curves (smooth lines)
- Rounded bar corners (`cornerradius: 3-4`)
- Gradient area fills on trend charts (FX reserves, external debt, cumulative FDI)
- Dark hover tooltips matching card color
- Custom hover templates with bold values
- Marker dots with dark border (`line=dict(width=2, color="#060B18")`)
- Legend: horizontal, above chart, muted text
- All titles bold (`<b>` tags)

### Tab Styling
- Pill-style container with dark background
- Selected tab: gradient highlight (cyan → purple at 12% opacity)
- Inactive tabs: muted gray text

### Divider
- Gradient horizontal rule: transparent → cyan → purple → transparent

---

## Data Pipeline Details

### config.py
Central configuration. Defines:
- `PROJECT_DIR`, `DATA_DIR`, `RAW_EXCEL_DIR`, `DB_PATH`
- `BASE_EN` / `BASE_SR` — NBS base URLs for English and Serbian documents
- `SOURCES` — list of 27 tuples: `(filename, url, category, description, frequency, methodology)`

Categories: `bop`, `services`, `tourism`, `fdi`, `external_debt`, `iip`, `fx_reserves`, `fx_rates`, `macro`

### run_pipeline.py
Orchestrates the full pipeline in steps:
1. Create database schema
2. Download source files (skip existing, `--force` to re-download)
3. Extract Excel → raw SQLite tables
4. Clean raw → standardized tables
5. Print verification summary

**Important:** Sets `PYTHONIOENCODING=utf-8` and reconfigures stdout for Windows compatibility with Serbian Cyrillic text.

**Idempotent:** Every run clears raw tables, metadata, and clean tables before re-inserting. Safe to re-run.

### scripts/download.py
- Downloads all 27 Excel files from NBS using urllib
- Browser-like User-Agent header (NBS requires it)
- SSL verification disabled (NBS endpoints sometimes have cert issues)
- 0.5s delay between requests (polite scraping)
- Skips files that already exist on disk

### scripts/schema.py
Creates the full SQLite schema:
- 1 `metadata` table (source tracking)
- 8 `raw_*` tables (data as-extracted)
- 8 `clean_*` tables (standardized, dashboard-ready)
- Indexes on `date` and `indicator_code` fields

### scripts/extract.py
The most complex file. Handles heterogeneous NBS Excel layouts:

**Three extraction strategies:**
1. **Standard matrix** — rows = indicators, columns = periods (most BOP, services, debt files)
2. **Transposed** — years in rows, indicators in columns, with optional month sub-rows (FX reserves, FX rates, macro, bank liabilities)
3. **Grouped sub-columns** — FDI by_country files with multiple sub-columns per year (Assets/Liabilities/Net)

**Key functions:**
- `_find_header_row()` — scans for rows with year/date values (skips col 0 to avoid false positives from transposed data)
- `_detect_layout()` — determines if col 0 has item codes or is empty, returns (indicator_col, data_start_col)
- `_normalize_period()` — converts various date formats to strings: "2007", "2025-03", "2025-12-31"
- `_month_from_text()` — maps English and Serbian Cyrillic month names to numbers
- `_extract_auto()` — tries standard matrix first, falls back to transposed with year+month detection
- `_extract_fdi_grouped()` — dedicated extractor for FDI by_country files with grouped sub-columns per year
- `extract_matrix()` — main matrix extractor with support for extra columns (country, sector)

**Routing logic in `extract_file()`:**
- `fdi` + `by_country` → `_extract_fdi_grouped()` (handles Assets/Liabilities/Net sub-columns)
- `fx_reserves`, `macro`, `fx_rates`, `ext_debt_by_creditor` → `_extract_auto()`
- Services/tourism `by_country` → extra country column
- `by_activity` / `branch_of_activity` → extra sector column
- Everything else → standard matrix with auto-detected layout

### scripts/clean.py
Transforms raw tables into dashboard-ready clean tables:

**Period parsing:**
- Handles: pure years, YYYY-MM, quarters (Q1-Q4, I-IV), month names (English + Serbian Cyrillic), ISO dates, European dates (31.12.2010.)
- All dates normalized to ISO format: `YYYY-MM-DD` (annual → YYYY-01-01, monthly → YYYY-MM-01)

**Value parsing:**
- European format support: `1.234,56` → `1234.56`
- Handles: nan, "...", "-", "n/a", empty strings

**BOP indicator mapping (`BOP_CODE_MAP`):**
- Maps raw text labels → `(indicator_code, indicator_name, sub_indicator)`
- Codes: CA, CA.GOODS, CA.SERVICES, CA.PRIMARY_INCOME, CA.SECONDARY_INCOME, KA, FA, FA.FDI, FA.PORTFOLIO, FA.OTHER, FA.DERIVATIVES, FA.RESERVES, EO
- Sub-indicators: credit, debit, net

**FDI cleaning (special handling):**
- by_country files: indicator_raw = "Assets"/"Liabilities"/"Net" → mapped to direction field; indicator set to "FDI"; country_or_sector = country name
- by_activity files: indicator_raw = NACE sector description → kept as indicator; direction = "liabilities" (NBS activity files show inward FDI only); sub-items ("of which:") and totals filtered out
- Order of checks: "net" before "asset" in direction detection (the Net header "FDI, net (=assets - liabilities)" contains the word "asset")

**Data quality filters:**
- Rejects dates before 1990-01-01 (catches Excel epoch errors → 1970-01-01)
- Rejects empty indicator names
- Cleans currency codes (removes "(100)", newlines; skips "COL_" placeholders)
- Handles Cyrillic in indicator codes (`re.UNICODE` flag)

---

## Dashboard Data Layer

### dashboard/data_loader.py

All SQL queries return pandas DataFrames ready for charting. Key functions:

**BOP & Trade:**
- `get_ca_annual()` — CA from `bop_annual_2007_2025.xls` only
- `get_ca_components_annual()` — Derives goods as residual: `CA - Services - Primary - Secondary` (avoids duplicate row issues)
- `get_ca_gdp_ratio()` — Merges CA with GDP from macro table
- `get_fa_components_annual()` — FA.FDI, FA.PORTFOLIO, FA.OTHER, FA.RESERVES
- `get_fdi_coverage()` — `|net FDI| / |CA deficit| * 100` (from BOP data)
- `get_goods_trade_annual()` — Exports/imports from credit/debit
- `get_fx_reserves()` — "Total (1 to 4)" and "Total (5+6)" indicators, annual end-of-year
- `get_external_debt_total()` — `debtor_type='total' AND maturity='total'`
- `get_gdp()` — From `indicator_name LIKE '%БДП (у млн евра)%'` (Serbian Cyrillic)
- `get_latest_kpis()` — Dict with year, ca, goods, services, fdi, fx_reserves
- `get_component_ranking()` — Sorted by absolute value with YoY change

**FDI Deep Dive:**
- `get_fdi_by_country(flow_or_position, top_n)` — Liabilities by country, groups small countries into "Other"
- `get_fdi_by_sector(flow_or_position)` — Liabilities by NACE sector, filters to uppercase main sectors
- `get_fdi_total_flows()` — Total flows pivot: Inflows (liabilities), Outflows (assets), Net FDI
- `get_fdi_concentration(top_n)` — Top N share as % of total FDI per year
- `get_fdi_yoy_growth()` — Year-over-year inflow change (absolute + %)
- `get_fdi_ca_coverage()` — Net FDI / CA deficit from the by_country data (more accurate than BOP)

**Helper constants:**
- `_FDI_AGGREGATES` — set of regional aggregates to exclude when listing individual countries (TOTAL, EUROPE, ASIA, EU-27, etc.)
- `_shorten_sector()` — maps full NACE names to short labels (e.g., "MANUFACTURING" → "Manufacturing")

### dashboard/charts.py

19 Plotly chart functions, all using `_base_layout()` for consistent dark theme:

**Current Account (4 charts):** `ca_trend_chart`, `ca_components_stacked`, `ca_waterfall`, `component_share_chart`

**Trade & Financing (3 charts):** `trade_chart`, `fa_components_chart`, `fdi_coverage_chart`

**External Position (2 charts):** `fx_reserves_chart`, `external_debt_chart`

**Rankings (2 charts):** `component_ranking_chart`, `yoy_change_chart`

**FDI Deep Dive (7 charts):** `fdi_total_flows_chart`, `fdi_by_country_chart`, `fdi_by_sector_chart`, `fdi_concentration_chart`, `fdi_yoy_growth_chart`, `fdi_ca_coverage_chart`, `fdi_sector_latest_chart`

**Country/sector color palettes:** `_COUNTRY_PALETTE` (11 colors), `_SECTOR_PALETTE` (18 colors)

### dashboard/styles.py

- `CUSTOM_CSS` — full CSS block injected via `st.markdown(unsafe_allow_html=True)`:
  - Google Fonts import (Inter)
  - KPI card styling with gradient backgrounds, colored top accents, hover effects
  - Tab styling (pill-style, gradient selected state)
  - Dashboard title with gradient text (white → cyan)
  - Section headers with bottom border
  - Gradient divider (hr)
  - Styled `st.metric` cards
  - Hidden Streamlit branding (header, footer, menu)

- `kpi_card(label, value, unit, css_class, sub_text)` — HTML generator for KPI cards

---

## Database Schema

### Metadata
| Table | Purpose |
|-------|---------|
| `metadata` | Source file registry: filename, URL, category, frequency, methodology, download_date, file_size, sheets_parsed |

### Raw Layer (8 tables)
Data as-extracted from Excel. Preserves original labels and string values.

| Table | Key Fields |
|-------|-----------|
| `raw_bop` | indicator_raw, period_raw, value_raw, unit_raw |
| `raw_services` | indicator_raw, country, period_raw, value_raw |
| `raw_fdi` | indicator_raw, country_or_sector, period_raw, value_raw |
| `raw_external_debt` | indicator_raw, period_raw, value_raw |
| `raw_iip` | indicator_raw, period_raw, value_raw |
| `raw_fx_reserves` | indicator_raw, period_raw, value_raw |
| `raw_fx_rates` | currency, period_raw, value_raw |
| `raw_macro` | indicator_raw, period_raw, value_raw |

### Clean Layer (8 tables)
Standardized, typed, indexed. Ready for dashboard queries.

| Table | Key Fields | Records |
|-------|-----------|---------|
| `clean_bop` | date, frequency, indicator_code, indicator_name, sub_indicator, value, unit | ~8,570 |
| `clean_services` | date, frequency, service_type, country, direction, value, unit | ~6,280 |
| `clean_fdi` | date, frequency, flow_or_position, indicator, country_or_sector, direction, value, unit | ~14,870 |
| `clean_external_debt` | date, frequency, debtor_type, creditor_type, maturity, value, unit | ~2,630 |
| `clean_iip` | date, frequency, indicator, direction, value, unit | ~1,590 |
| `clean_fx_reserves` | date, frequency, indicator, value, unit | ~750 |
| `clean_fx_rates` | date, frequency, currency, rate_type, value, unit | ~1,430 |
| `clean_macro` | date, frequency, indicator_code, indicator_name, value, unit | ~10,310 |

**Total: ~46,400 clean records**

### clean_fdi Direction Values
- `assets` — Serbian investment abroad (outflows)
- `liabilities` — Foreign investment into Serbia (inflows)
- `net` — Assets minus Liabilities (negative = net inflow in BPM6)

### clean_fdi Data Sources
| Source | File | Years | Sub-columns | Records |
|--------|------|-------|-------------|---------|
| Flows by country | `fdi_flows_by_country_2010_2024.xls` | 2010-2024 | Assets, Liabilities, Net | ~11,000 |
| Flows by activity | `fdi_flows_by_activity_2010_2024.xls` | 2010-2024 | Liabilities only | ~1,100 |
| Positions by country | `fdi_positions_by_country_2020_2024.xls` | 2020-2024 | Assets, Liabilities | ~2,470 |
| Positions by activity | `fdi_positions_by_activity_2020_2024.xls` | 2020-2024 | Liabilities only | ~300 |

---

## Data Sources

27 Excel files from NBS, organized by category:

| Category | Files | Time Range | Frequency | Methodology |
|----------|-------|------------|-----------|-------------|
| Balance of Payments | 5 | 1997-2026 | Annual + Monthly | BPM5, BPM6 |
| Services | 3 | 2007-2025 | Annual + Monthly | BPM6 |
| Tourism | 2 | 2007-2025 | Annual | BPM6 |
| FDI | 4 | 2010-2024 | Annual | BPM6 |
| External Debt | 4 | 2000-2025 | Quarterly | BPM6 |
| IIP | 1 | 2013-Q3 2025 | Quarterly | BPM6 |
| FX Reserves | 2 | 2002-2026 | Monthly | — |
| FX Rates | 2 | 1997-2025 | Daily + Monthly | — |
| Macro Indicators | 4 | 2000-2025 | Annual + Quarterly | — |

Source page: https://www.nbs.rs/sr_RS/finansijsko_trziste/informacije-za-investitore-i-analiticare/

---

## Key Technical Decisions

1. **Two-layer database (raw + clean)** — preserves original data for debugging while providing standardized data for dashboards
2. **SQLite** — lightweight, single-file, no server needed, perfect for this scale
3. **Auto-detection of Excel layouts** — NBS files are heterogeneous; the parser adapts instead of hardcoding
4. **Dedicated FDI grouped-column extractor** — FDI by_country files have 3 sub-columns per year (Assets/Liabilities/Net); the generic matrix extractor can't handle this, so `_extract_fdi_grouped()` was written specifically
5. **Column 0 skip in header detection** — prevents misidentifying transposed data rows as header rows
6. **Serbian Cyrillic month mapping** — NBS publishes in both Serbian and English; both are handled
7. **Date < 1990 filter** — catches Excel epoch errors (some cells parse to 1970-01-01)
8. **EUR millions as standard unit** — most NBS external sector data is in EUR mn
9. **BPM6 indicator codes** — CA, CA.GOODS, FA.FDI etc. for structured querying
10. **Goods derived as residual** — `CA - Services - Primary - Secondary` avoids duplicate row issues in BOP files
11. **Direction detection order** — "net" checked before "asset" because the Net header "FDI, net (=assets - liabilities)" contains "asset"
12. **Premium dark theme** — deep navy background, vibrant accent colors, Inter font, gradient effects — designed for executive-level presentation

---

## Dependencies

```
pandas
openpyxl
xlrd
streamlit
plotly
```

All other imports are Python stdlib (sqlite3, urllib, ssl, json, re, datetime, pathlib).

---

## Data Refresh

- NBS publishes monthly BOP data around the 15th of each month
- Full refresh: `python run_pipeline.py --force`
- Add new sources: edit `SOURCES` list in `config.py`, then run pipeline
- Pipeline is idempotent — safe to re-run anytime

---

## Key Data Points (as of 2024)

| Metric | Value |
|--------|-------|
| Current Account | -3,788 EUR mn (deficit) |
| Trade Balance (Goods) | negative (large deficit) |
| Services Surplus | positive |
| FDI Inflows | 5,231 EUR mn |
| FDI Outflows | 628 EUR mn |
| Net FDI | 4,602 EUR mn |
| FDI Top 5 Concentration | 76% |
| FDI Coverage of CA Deficit | 122% |
| Top FDI Country | China (1,691 EUR mn) |
| Top FDI Sector | Mining (1,455 EUR mn) |
| NBS FX Reserves | ~29,400 EUR mn |

---

## Known Limitations

- Some NBS files not fully parsed (`ext_debt_by_debtor_creditor` has complex multi-level row hierarchy)
- FX rate data from the "movements" file has limited extraction due to complex daily format
- Macro indicators are in Serbian Cyrillic (indicator_name field); indicator_code is auto-generated
- BOP annual files for 1997-2006 use BPM5 methodology; 2007+ uses BPM6 (not directly comparable)
- The `intl_reserves_fx_liquidity.xls` and `private_sector_debt.xls` files have layouts not yet handled
- FDI by_activity files only contain liabilities (inward FDI); outward FDI by sector is not available from NBS in this format
- FDI positions data only covers 2020-2024 (shorter range than flows 2010-2024)
