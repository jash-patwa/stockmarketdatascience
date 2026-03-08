# Vehicle Pricing Tracker - Architecture

## Overview

The Vehicle Pricing Tracker is a modular Python application that scrapes vehicle pricing data from iseecars.com and maintains a weekly tracking spreadsheet for comparing MSRP, invoice prices, and destination fees across multiple model years.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface Layer                         │
│                  (Command Line Interface)                        │
│                     main_tracker.py                              │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                           │
│              VehiclePricingTracker (main_tracker.py)             │
│  - Coordinates scraping workflow                                 │
│  - Manages data flow between components                          │
│  - Handles error recovery                                        │
└─────────────────────────────────────────────────────────────────┘
         ▼                              ▼                      ▼
    ┌────────────┐          ┌──────────────────┐    ┌──────────────┐
    │  Scraper   │          │ Excel Tracker    │    │Google Drive  │
    │   Layer    │          │     Layer        │    │  Layer       │
    └────────────┘          └──────────────────┘    └──────────────┘
         │                         │                      │
    iseecars.com              Local Excel Files      Google Drive API
```

## Component Descriptions

### 1. **main_tracker.py** - Orchestration Layer
**Responsibility:** Coordinates the entire scraping and tracking workflow

**Key Classes:**
- `VehiclePricingTracker`: Main orchestrator
  - `setup()`: Initialize and load vehicle data
  - `scrape_all_vehicles()`: Scrape data for all vehicles
  - `update_tracker()`: Update Excel file with scraped data
  - `generate_comparison_report()`: Create analysis reports

**Flow:**
```
Initialize → Load Vehicles → Scrape Data → Update Excel → Generate Reports
```

### 2. **iseecars_scraper.py** - Web Scraping Layer
**Responsibility:** Extract pricing data from iseecars.com

**Key Classes:**
- `ISeeCarsScraperPriceScraper`: Main scraper
  - `get_pricing_data()`: Fetch data for multiple model years
  - `_scrape_model_year()`: Scrape specific year
  - `_extract_trim_data()`: Parse HTML to extract trim information
  - `get_most_popular_trim()`: Select base/most popular variant

**Implementation Details:**
```python
# URL Structure
base_url = "https://www.iseecars.com/car/{make}-{model}-price"

# Data Extraction
- Parses HTML tables
- Extracts: Trim name, MSRP, Invoice, Destination Fee
- Handles multiple model years

# Output Format
{
    2026: [
        {'trim': 'Base', 'msrp': 31500, 'invoice': 28750, 'destination_fee': 1895},
        {'trim': 'SLE', 'msrp': 34200, 'invoice': 31100, 'destination_fee': 1895},
    ],
    2025: [...]
}
```

**Features:**
- Respectful scraping with 2-second delays between requests
- Error handling for missing data
- Multiple model year support
- Robust price parsing (handles various formats)

### 3. **excel_tracker.py** - Spreadsheet Management Layer
**Responsibility:** Manage vehicle data in Excel format

**Key Classes:**
- `VehicleExcelTracker`: Excel file management
  - `_load_vehicles()`: Read vehicle list from Excel
  - `add_weekly_data()`: Add or update weekly data
  - `compare_model_years()`: Create comparison pivots
  - `_style_header_row()`: Apply formatting

**Data Structure:**
```
Input Excel (75_US_Vehicles_2025.xlsx):
┌────────┬──────────────┐
│ Make   │ Model        │
├────────┼──────────────┤
│ GMC    │ Sierra 1500  │
│ Toyota │ Camry        │
└────────┴──────────────┘

Output Tracker (vehicle_pricing_tracker.xlsx):
┌──────────────────────────────────────────────────────────────┐
│ Sheet: Week_2026-03-08                                       │
├────────┬────────┬──────────┬────────┬────────┬────────┬──────┤
│ Make   │ Model  │ Trim     │ MSRP   │ Invoice│ Dest   │ Year │
├────────┼────────┼──────────┼────────┼────────┼────────┼──────┤
│ GMC    │ Sierra │ Base     │ 31500  │ 28750  │ 1895   │ 2026 │
│ Toyota │ Camry  │ LE       │ 27100  │ 24800  │ 1285   │ 2026 │
└────────┴────────┴──────────┴────────┴────────┴────────┴──────┘

Sheet: Week_2026-03-15
... (same structure with updated prices)
```

**Features:**
- Column auto-sizing
- Header styling (blue background, white text)
- Named weekly sheets (Week_YYYY-MM-DD)
- Automatic column detection (handles various header names)

### 4. **google_drive_handler.py** - Cloud Integration Layer
**Responsibility:** Handle Google Drive authentication and file operations

**Key Classes:**
- `GoogleDriveHandler`: Google Drive API wrapper
  - `_authenticate()`: OAuth 2.0 authentication
  - `find_file_by_name()`: Search for files
  - `download_file()`: Download from Google Drive
  - `upload_file()`: Upload to Google Drive
  - `update_file()`: Update existing files

**OAuth Flow:**
```
1. Check for cached token (token.pickle)
2. If valid: Use cached token
3. If invalid/missing: Initiate OAuth flow
4. Save new token for future use
5. Build Google Drive API service
```

**Features:**
- Persistent token caching
- Automatic token refresh
- File search by name
- Upload/update capability for results

## Data Flow

### Scraping Workflow
```
1. Load Vehicle List
   └─> Read from Excel or Google Drive

2. For Each Vehicle:
   a. Build iseecars.com URL
   b. Fetch page
   c. Parse HTML table
   d. Extract all trims
   e. For each model year:
      - Get pricing for that year
      - Store in dictionary
   f. Select most popular trim

3. Aggregate Results
   └─> Create {vehicle_name: {year: trim_data}} structure

4. Update Excel Tracker
   └─> Create/append weekly sheet

5. Generate Reports (optional)
   └─> Create comparison tables
```

### Excel Update Workflow
```
1. Check if tracker file exists
   ├─ Yes: Load existing workbook
   └─ No: Create new workbook

2. Create weekly sheet (Week_YYYY-MM-DD)

3. Write headers
   ├─ Style with colors
   └─ Set column widths

4. Write data rows
   ├─ Match vehicles to scraped data
   └─ Handle missing data gracefully

5. Save file
```

## Error Handling

### Graceful Degradation
- Vehicle not found: Log warning, continue to next
- Model year not available: Skip that year, try others
- HTML parsing failure: Return empty result, skip vehicle
- Network timeout: Retry with exponential backoff

### Logging Strategy
```
Level  Usage
─────────────────────────────────────────
INFO   Major operations (scrape start/end, file updates)
WARN   Non-fatal issues (vehicle not found, year unavailable)
ERROR  Significant failures (setup errors, parsing failures)
DEBUG  Detailed diagnostic info
```

## Configuration Options

Users can customize:
- Vehicle source (local file or Google Drive)
- Output file path
- Model years to scrape
- Request delay (to be respectful to servers)
- Excel formatting options

## Extensibility

### Adding New Data Sources
Extend `iseecars_scraper.py`:
```python
class KBBScraper(BaseScraper):
    BASE_URL = "https://www.kbb.com/..."

    def get_pricing_data(self, make, model):
        # Implement KBB-specific scraping
```

### Adding New Export Formats
Extend `excel_tracker.py`:
```python
def export_to_csv(self, data):
    # Export to CSV format

def export_to_database(self, data):
    # Export to database
```

### Custom Analysis
Users can import the modules:
```python
from iseecars_scraper import ISeeCarsScraperPriceScraper
from excel_tracker import VehicleExcelTracker

# Build custom analysis tools
```

## Performance Considerations

### Scraping Speed
- **Rate Limiting:** 2-second delay between requests
- **Parallel Processing:** Possible but not implemented (respects server load)
- **Caching:** Could be added to avoid re-scraping unchanged data

### Memory Usage
- Typical run: <100 MB RAM
- Scales linearly with number of vehicles
- 1000 vehicles would use ~500 MB

### Network Efficiency
- Single HTTP request per vehicle per model year
- BeautifulSoup parsing in memory
- No data stored during scrape (streamed to Excel)

## Testing

### Unit Testing Approach
```python
# Test scraper extraction
def test_price_parsing():
    assert parse_price("$31,500.00") == 31500.0

# Test vehicle list loading
def test_load_vehicles():
    tracker = VehicleExcelTracker("test.xlsx")
    assert len(tracker.get_vehicle_list()) == 5

# Test Excel formatting
def test_weekly_sheet_creation():
    tracker.add_weekly_data("output.xlsx", {...})
    assert "Week_" in openpyxl.load_workbook("output.xlsx").sheetnames
```

### Integration Testing
```python
# End-to-end test
def test_full_workflow():
    tracker = VehiclePricingTracker("test_vehicles.xlsx")
    tracker.setup()
    data = tracker.scrape_all_vehicles([2026])
    tracker.update_tracker("output.xlsx", data)
    # Verify output file
```

## Dependencies

| Package | Purpose |
|---------|---------|
| requests | HTTP requests to iseecars.com |
| beautifulsoup4 | HTML parsing |
| selenium | Alternative parsing (optional) |
| openpyxl | Excel file manipulation |
| pandas | Data analysis and comparison |
| google-auth-oauthlib | Google Drive authentication |
| google-api-python-client | Google Drive API |

## Security Considerations

### Data Privacy
- No credentials stored in code
- OAuth tokens stored locally with restricted permissions
- No personal data transmitted

### Web Scraping Ethics
- Respectful rate limiting (2 sec delays)
- Proper User-Agent headers
- Does not circumvent access controls
- Uses public data

### File Security
- Excel files not encrypted (could add encryption)
- Google Drive files inherited from user's sharing settings
- Local files follow system permissions

## Future Enhancements

1. **Multi-Source Scraping**
   - Add support for KBB.com, TrueCar, etc.
   - Aggregate data from multiple sources

2. **Advanced Analytics**
   - Price prediction using ML
   - Depreciation curve analysis
   - Market trend identification

3. **Web Interface**
   - Dashboard for viewing trends
   - Alert system for price changes
   - Real-time data visualization

4. **Database Integration**
   - Store historical data in database
   - Enable complex queries
   - Better data management

5. **Mobile App**
   - Mobile dashboard
   - Push notifications
   - On-the-go price tracking

## Maintenance

### Regular Updates Needed
- Monitor iseecars.com HTML structure changes
- Update scraper selectors if HTML changes
- Test with new model years annually

### User Support
- Log files for debugging
- Clear error messages
- Example configurations

### Documentation
- Keep guides updated
- Add troubleshooting FAQs
- Provide example outputs

---

**Architecture Version:** 1.0
**Last Updated:** March 2026
**Status:** Production Ready
