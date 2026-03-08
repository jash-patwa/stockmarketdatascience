# Vehicle Pricing Tracker - iseecars.com Scraper

A Python-based system to scrape vehicle pricing data from iseecars.com and maintain a weekly tracking spreadsheet for the top 75 US vehicles.

## Overview

This system:
- Scrapes MSRP, Invoice Price, and Destination Fees from iseecars.com
- Tracks the most popular trim for each vehicle
- Compares prices across model years (2024, 2025, 2026)
- Creates a weekly Excel spreadsheet with pricing data
- Allows year-over-year price comparisons

## Features

✅ **Automated Scraping** - Extract pricing data from iseecars.com
✅ **Weekly Tracking** - New tabs for each week's data
✅ **Model Year Comparison** - Track prices across 2024, 2025, and 2026
✅ **Most Popular Trim** - Automatically selects the first (most popular) trim
✅ **Excel Organization** - Professional formatting with currency, totals, and comparisons
✅ **Error Handling** - Robust logging and error management

## Files

### Core Modules

- **`vehicle_list.py`** - List of top 75 US vehicles with make, model, trims, and sales data
- **`iseecars_scraper.py`** - Web scraper for iseecars.com pricing data
- **`excel_tracker.py`** - Excel workbook manager for tracking pricing data
- **`scrape_vehicle_prices.py`** - Main execution script

### Configuration

- **`requirements.txt`** - Python dependencies

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `requests` - HTTP library for web scraping
- `beautifulsoup4` - HTML parsing
- `openpyxl` - Excel workbook management
- `pandas` - Data manipulation
- `lxml` - XML/HTML processing

### 2. Verify Setup

```bash
python3 scrape_vehicle_prices.py --help
```

## Usage

### Option 1: Test with a Single Vehicle

Test the scraper with a single vehicle to verify it's working:

```bash
python3 scrape_vehicle_prices.py --single Ford F-150
```

This will:
- Scrape pricing for the 2026, 2025, and 2024 Ford F-150
- Select the best available model year (preferring 2026)
- Extract the most popular trim's pricing
- Create `vehicle_pricing_tracker.xlsx` with a test sheet

### Option 2: Scrape All 75 Vehicles

Scrape pricing data for all top 75 vehicles and create a weekly tracker:

```bash
python3 scrape_vehicle_prices.py
```

This will:
- Scrape all 75 vehicles
- Create a new weekly sheet in the Excel file
- Each vehicle gets the best available model year
- Save all data to `vehicle_pricing_tracker.xlsx`

### Options

```bash
# Specify custom output file
python3 scrape_vehicle_prices.py --output my_tracker.xlsx

# Specify custom model years to scrape (comma-separated)
python3 scrape_vehicle_prices.py --years 2025,2026

# Test with a single vehicle and custom output
python3 scrape_vehicle_prices.py --single GMC Sierra --output gmc_test.xlsx
```

## Excel File Structure

### Metadata Sheet
- Overview and description of the tracker
- Lists the columns used

### Weekly Sheets
Each week's data goes into a sheet named `Week_YYYY_MM_DD`:

| Column | Description |
|--------|-------------|
| Rank | Vehicle rank (1-75) |
| Brand | Vehicle manufacturer |
| Model | Vehicle model name |
| Trim | Most popular trim level |
| Model Year | Best available model year |
| MSRP | Manufacturer Suggested Retail Price |
| Invoice | Dealer invoice price |
| Destination Fee | Destination/delivery fee |
| Total Cost | MSRP + Destination Fee |
| Scraped Date | Date/time data was scraped |

### Comparisons Sheet
Year-over-year price comparison showing:
- 2024, 2025, 2026 MSRP values
- Price changes between years

## How It Works

### 1. URL Structure
The scraper uses iseecars.com's pricing pages:
```
https://www.iseecars.com/car/{brand}-{model}-price?model_year={year}
```

### 2. Data Extraction
- Finds the pricing table on the page
- Extracts trim name, MSRP, invoice, and destination fee
- Cleans prices (removes $ and commas)

### 3. Model Year Selection
For each vehicle, the system attempts to scrape 2024, 2025, and 2026 in that order:
- If 2026 data is available, uses it
- Falls back to 2025 if 2026 unavailable
- Falls back to 2024 if 2025 unavailable

### 4. Trim Selection
The most popular trim is assumed to be the first trim listed on iseecars.com.

## Weekly Workflow

1. **Run the scraper** - `python3 scrape_vehicle_prices.py`
2. **Review the Excel file** - Open `vehicle_pricing_tracker.xlsx`
3. **New week** - A new sheet is automatically created with the week's date
4. **Compare years** - Use the Comparisons sheet to see price changes

## Troubleshooting

### No Data Scraped
- Check your internet connection
- Verify iseecars.com is accessible
- Check logs for specific vehicle errors

### Incomplete Pricing Data
- Some vehicles may not have all trim levels available on iseecars.com
- Some model years may not be listed yet
- The scraper logs which vehicles had issues

### Excel File Issues
- Close the file before re-running the scraper
- The script automatically overwrites weekly sheets if they already exist

### Slow Scraping
- The script adds 1-second delays between requests to be polite
- Full batch scraping (75 vehicles × 3 years) takes ~5-10 minutes

## Customization

### Adding/Removing Vehicles

Edit `vehicle_list.py` to modify the vehicle list:

```python
{
    "rank": 1,
    "brand": "Ford",
    "model": "F-150",
    "trims": ["F-150", "Raptor"],
    "segment": "Full-Size Truck",
    "sales": 828832
}
```

### Changing Model Years

Edit the year preference order in `scrape_vehicle_prices.py`:

```python
preferred_years=[2027, 2026, 2025, 2024]
```

### Custom Excel Formatting

Modify `excel_tracker.py` to change:
- Column widths
- Header colors
- Number formats
- Font styles

## Limitations

- iseecars.com may change their website structure (scraper may need updates)
- Some vehicles may not have complete pricing data
- Page scraping depends on consistent HTML structure
- Request delays may affect total execution time

## Notes

- Always respect robots.txt and website terms of service
- The scraper includes polite delays between requests
- Test with a single vehicle first before batch operations
- Keep Excel file closed while running the scraper

## Example Output

```
$ python3 scrape_vehicle_prices.py --single Ford F-150

✓ Successfully scraped Ford F-150
  Model Year: 2026
  Trim: F-150
  MSRP: $28,485.00
  Invoice: $26,400.00
  Destination Fee: $1,695.00
```

## Support

For issues or improvements, check the scraper logs and verify:
1. Website accessibility
2. HTML structure hasn't changed
3. Required dependencies are installed
4. Python version is 3.6+
