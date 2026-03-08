# Vehicle Pricing Tracker - Quick Start

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Your Vehicle List
Create an Excel file named `75_US_Vehicles_2025.xlsx` with columns:
- **Make** (e.g., "GMC", "Toyota", "Ford")
- **Model** (e.g., "Sierra 1500", "Camry", "F-150")

Example:
```
| Make        | Model           |
|-------------|-----------------|
| GMC         | Sierra 1500     |
| Toyota      | Camry           |
| Ford        | F-150           |
| Honda       | Civic           |
| Chevrolet   | Silverado 1500  |
```

### 3. Run the Tracker
```bash
python main_tracker.py --vehicle-file "75_US_Vehicles_2025.xlsx"
```

This creates `vehicle_pricing_tracker.xlsx` with weekly pricing data.

## Output File

The tracker creates sheets like:
- **Week_2026-03-08** (first run date)
- **Week_2026-03-15** (second run date)
- etc.

Each sheet contains:
| Make | Model | Trim | MSRP | Invoice | Destination Fee | Model Year | Capture Date |
|------|-------|------|------|---------|-----------------|------------|--------------|
| GMC | Sierra 1500 | Base | $31,500 | $28,750 | $1,895 | 2026 | 2026-03-08 |

## Next Steps

### Option A: Use Google Drive (Recommended for convenience)

1. **Set up Google OAuth:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project and enable Google Drive API
   - Create Desktop credentials and download as `credentials.json`

2. **Upload your vehicle list to Google Drive** and save the file name

3. **Run with Google Drive:**
   ```bash
   python main_tracker.py --google-drive --vehicle-file "75_US_Vehicles_2025"
   ```

### Option B: Schedule Weekly Runs

#### Linux/Mac (using cron):
```bash
# Edit crontab
crontab -e

# Add this line to run every Monday at 8 AM
0 8 * * 1 cd /path/to/stockmarketdatascience && python main_tracker.py --vehicle-file "75_US_Vehicles_2025.xlsx"
```

#### Windows (using Task Scheduler):
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Weekly, Monday, 8:00 AM
4. Set action: `python.exe main_tracker.py --vehicle-file "75_US_Vehicles_2025.xlsx"`
5. Set start in: `C:\path\to\stockmarketdatascience`

### Option C: Analyze Data

Run the example scripts to see data analysis patterns:
```bash
python example_usage.py
```

## Testing

### Test with a Single Vehicle
```python
from iseecars_scraper import ISeeCarsScraperPriceScraper

scraper = ISeeCarsScraperPriceScraper()
data = scraper.get_pricing_data("Toyota", "Camry", [2026])

for year, trims in data.items():
    print(f"Found {len(trims)} trims for {year}")
    best = scraper.get_most_popular_trim(trims)
    print(f"Popular trim: {best['trim']}")
    print(f"  MSRP: ${best['msrp']:,.0f}")
    print(f"  Invoice: ${best['invoice']:,.0f}")
    print(f"  Destination: ${best['destination_fee']:,.0f}")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `No pricing table found` | Vehicle may not be on iseecars.com or spelling is incorrect |
| `Connection timeout` | Check internet, try again later, or increase delay |
| `Import error` | Run `pip install -r requirements.txt` |
| `File not found` | Verify Excel file path and format |
| `Google Drive auth fails` | Delete `token.pickle` and re-authenticate |

## Data Notes

- **Default Model Years:** 2026, 2025, 2024 (customize with `--model-years`)
- **Trim Selection:** Most popular trim (typically base model) for consistency
- **Update Frequency:** Recommend weekly to track price changes
- **Data Source:** iseecars.com real-time pricing

## File Structure

```
stockmarketdatascience/
├── main_tracker.py              # Main entry point
├── iseecars_scraper.py          # Web scraper
├── excel_tracker.py             # Excel management
├── google_drive_handler.py      # Google Drive integration
├── example_usage.py             # Usage examples
├── requirements.txt             # Dependencies
├── config.template.json         # Configuration template
├── 75_US_Vehicles_2025.xlsx     # Your vehicle list (you create this)
├── vehicle_pricing_tracker.xlsx # Output tracker (auto-generated)
├── README.md                    # Main documentation
├── QUICK_START.md              # This file
└── VEHICLE_TRACKER_GUIDE.md    # Detailed guide
```

## Common Commands

```bash
# Run with default settings
python main_tracker.py

# Run specific vehicle file
python main_tracker.py --vehicle-file "my_vehicles.xlsx"

# Scrape specific model years
python main_tracker.py --model-years 2026 2025 2024 2023

# Specify output file
python main_tracker.py --output "my_tracker.xlsx"

# Fetch from Google Drive
python main_tracker.py --google-drive --vehicle-file "VehicleList"

# Combine options
python main_tracker.py --google-drive --vehicle-file "75_US_Vehicles_2025" --output "tracker_2026.xlsx" --model-years 2026 2025
```

## Understanding the Data

### MSRP vs Invoice
- **MSRP:** Manufacturer Suggested Retail Price (what you see advertised)
- **Invoice:** Dealer cost (what dealer paid for the car)
- **Difference:** Typical dealer markup (profit margin)

### Destination Fee
- Also called "doc fee" or "delivery charge"
- Varies by manufacturer and location
- Usually $500-$2,000
- Included in total cost of ownership

### Price Trends
Compare week-to-week to see:
- Price increases/decreases
- Model year transitions
- Seasonal promotions
- Inventory adjustments

## Next: Detailed Analysis

Once you have multiple weeks of data, use Python/Excel to:
- Calculate average price changes
- Identify which models hold value best
- Track trim-specific pricing
- Analyze destination fee variations
- Create pivot tables for comparisons

See [VEHICLE_TRACKER_GUIDE.md](VEHICLE_TRACKER_GUIDE.md) for advanced features.

## Support

For detailed information, see:
- [VEHICLE_TRACKER_GUIDE.md](VEHICLE_TRACKER_GUIDE.md) - Full documentation
- [example_usage.py](example_usage.py) - Code examples
- [config.template.json](config.template.json) - Configuration options

Enjoy tracking your vehicle pricing data! 🚗📊
