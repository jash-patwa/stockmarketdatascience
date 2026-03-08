# stockmarketdatascience

## Projects

### 1. Indian Stock Market Data Science
Data science techniques on Indian stock market data NSE.

This project draws useful conclusions regarding overnight and intraday returns in the Indian Stock market.
The data is imported from python library nsepy for nifty50 index as well as midcap and smallcap indices.

The notebook includes:
- Daily return schedule calculations to identify which days of the week the stock market advances or declines
- Histogram showing return distribution and boxplots of volume distribution on yearly basis
- Analysis showing that major portion of returns in the Indian stock market are overnight rather than intraday

### 2. Vehicle Pricing Tracker (US Vehicles)
Weekly tracking of vehicle MSRP, invoice prices, and destination fees from iseecars.com.

This feature allows you to:
- Extract pricing data for your vehicle list from iseecars.com
- Compare prices across model years (2024, 2025, 2026, etc.)
- Track pricing changes week-by-week
- Maintain a weekly tracking spreadsheet with historical data
- Analyze price trends and year-over-year changes

**Quick Start:**
```bash
python main_tracker.py --vehicle-file "75_US_Vehicles_2025.xlsx" --output "vehicle_pricing_tracker.xlsx"
```

For detailed setup and usage, see [VEHICLE_TRACKER_GUIDE.md](VEHICLE_TRACKER_GUIDE.md)

