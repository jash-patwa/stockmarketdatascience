# Vehicle Pricing Tracker - Setup & Usage Guide

This system automatically scrapes iseecars.com for vehicle pricing data (MSRP, invoice, destination fees) across multiple model years and maintains a weekly tracking spreadsheet.

## Features

- **Automated Scraping**: Extracts pricing data from iseecars.com for your vehicle list
- **Multi-Year Comparison**: Compares prices across 2024, 2025, and 2026 model years
- **Weekly Tracking**: Creates a new sheet in Excel for each week's data
- **Popular Trim Selection**: Automatically selects the most popular trim for each vehicle
- **Google Drive Integration**: Optionally fetch your vehicle list directly from Google Drive
- **Apples-to-Apples Comparison**: Ensures consistent trim selection for fair price comparisons

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Vehicle List

Create an Excel file with your 75 vehicles in this format:

| Make | Model |
|------|-------|
| GMC | Sierra 1500 |
| Toyota | Camry |
| Ford | F-150 |
| ... | ... |

### 3. Run the Tracker (Local File)

```bash
python main_tracker.py --vehicle-file "75_US_Vehicles_2025.xlsx" --output "vehicle_pricing_tracker.xlsx"
```

## Advanced Usage

### Using Google Drive

To fetch your vehicle list directly from Google Drive:

1. **Set up Google OAuth credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Drive API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials and save as `credentials.json` in the project directory

2. **Run with Google Drive:**
   ```bash
   python main_tracker.py --google-drive --vehicle-file "75_US_Vehicles_2025"
   ```

### Custom Model Years

```bash
python main_tracker.py --vehicle-file "75_US_Vehicles_2025.xlsx" \
    --model-years 2026 2025 2024 2023
```

### Specify Different Output File

```bash
python main_tracker.py --vehicle-file "75_US_Vehicles_2025.xlsx" \
    --output "/path/to/my_tracker.xlsx"
```

## Output File Structure

The tracker creates an Excel file with a sheet for each week in this format:

| Make | Model | Trim | MSRP | Invoice | Destination Fee | Model Year | Capture Date |
|------|-------|------|------|---------|-----------------|------------|--------------|
| GMC | Sierra 1500 | Base/Regular Cab | 31500 | 28750 | 1895 | 2026 | 2026-03-08 |
| Toyota | Camry | LE | 27100 | 24800 | 1285 | 2026 | 2026-03-08 |

## Data Extraction Details

### Most Popular Trim Selection

The system automatically selects the first trim in the list from iseecars.com, which is typically the base model or most common configuration. This ensures:

- Consistent comparisons week-to-week
- Focus on the most purchased variant
- Apples-to-apples pricing across model years

### Model Year Handling

The system attempts to scrape data for specified model years:
- Default: 2026, 2025, 2024
- If a model year isn't available on iseecars.com, it's skipped
- The latest available year is used in the main tracker sheet
- Full year-by-year data can be analyzed from the weekly sheets

### Destination Fees

Destination charges vary by vehicle and model year. The system captures these separately so you can analyze total cost of ownership accurately.

## Interpreting Your Data

### Price Comparison Example

If comparing a 2026 GMC Sierra 1500 from this week vs. last week:

```
Week 1 (2026-03-01):  MSRP: $31,500  Invoice: $28,750
Week 2 (2026-03-08):  MSRP: $31,800  Invoice: $28,900
Change:              +$300 MSRP     +$150 Invoice
```

### Year-over-Year Analysis

Compare the same trim across model years:

```
2024 Model Year: MSRP $29,500  Invoice $26,800
2025 Model Year: MSRP $30,200  Invoice $27,400
2026 Model Year: MSRP $31,500  Invoice $28,750
```

## Troubleshooting

### Issue: "No pricing table found"

- The vehicle may not be listed on iseecars.com
- Check the iseecars.com link manually: https://www.iseecars.com/car/make-model-price
- Verify the make and model spelling matches iseecars.com

### Issue: "Request timeout"

- The scraper includes a 2-second delay between requests to be respectful to servers
- Check your internet connection
- Try again later if iseecars.com is temporarily down

### Issue: "Google Drive authentication failed"

- Verify `credentials.json` is in the project directory
- Ensure the Google Drive API is enabled in your Google Cloud project
- Delete `token.pickle` and re-authenticate

### Issue: "File not found on Google Drive"

- Check that the filename matches exactly (case-sensitive)
- Ensure you have access to the file in Google Drive
- Verify it's an Excel file (.xlsx)

## Schedule Automation

To run this weekly, set up a scheduled task:

### Windows (Task Scheduler)
```
Program: python.exe
Arguments: C:\path\to\main_tracker.py --vehicle-file "75_US_Vehicles_2025.xlsx"
Trigger: Weekly (e.g., every Monday at 8 AM)
```

### Linux/Mac (Cron)
```bash
# Run every Monday at 8 AM
0 8 * * 1 cd /home/user/stockmarketdatascience && python main_tracker.py --vehicle-file "75_US_Vehicles_2025.xlsx"
```

## Data Accuracy Notes

- **Source**: iseecars.com pricing data
- **Update Frequency**: Depends on how often you run the tracker (recommended: weekly)
- **Model Availability**: Not all vehicles are available for all model years on iseecars.com
- **Trims**: Only the most popular trim is tracked to maintain consistency

## Advanced Features

### Generate Comparison Reports

After collecting data for several weeks:

```python
from main_tracker import VehiclePricingTracker

tracker = VehiclePricingTracker("75_US_Vehicles_2025.xlsx")
tracker.setup()
tracker.generate_comparison_report("vehicle_pricing_tracker.xlsx")
```

### Custom Analysis

Use Python to analyze the data:

```python
import pandas as pd

# Read all weeks of data
tracker_df = pd.read_excel("vehicle_pricing_tracker.xlsx", sheet_name=None)

# Concatenate all sheets
all_data = pd.concat(tracker_df.values(), ignore_index=True)

# Analyze price trends
price_trends = all_data.groupby(['Make', 'Model'])['MSRP'].agg(['min', 'max', 'mean'])
print(price_trends)
```

## Support & Questions

If you encounter issues:
1. Check the logs output by the tracker
2. Verify your vehicle list format matches the expected columns
3. Test a single vehicle manually at iseecars.com
4. Check internet connectivity

## License

This tracker is designed for personal use and data analysis. Always respect website terms of service when web scraping.
