#!/usr/bin/env python3
"""
Main script to scrape vehicle pricing from iseecars.com and update tracking spreadsheet.
"""

import argparse
import logging
from datetime import datetime
from vehicle_list import get_vehicle_list
from iseecars_scraper import IseecarsPrice
from excel_tracker import VehiclePriceTracker

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_best_model_year(available_years, preferred_years=[2026, 2025, 2024]):
    """
    Select the best model year from available options.
    Prefers 2026, then 2025, then 2024.
    """
    for year in preferred_years:
        if year in available_years:
            return year
    return available_years[0] if available_years else None

def process_vehicle_data(brand, model, scraper):
    """
    Scrape and process data for a single vehicle.

    Returns a dict with the most popular trim for the best available model year.
    """
    logger.info(f"Processing {brand} {model}...")

    # Try to scrape multiple years
    pricing_data_list = scraper.scrape_multiple_years(brand, model)

    if not pricing_data_list:
        logger.warning(f"No data found for {brand} {model}")
        return None

    # Find the best model year (prefer 2026, then 2025, then 2024)
    available_years = [d['model_year'] for d in pricing_data_list]
    best_year = get_best_model_year(available_years)

    # Get data for the best year
    best_data = next((d for d in pricing_data_list if d['model_year'] == best_year), None)

    if not best_data:
        return None

    # Get the most popular trim (first in the list)
    most_popular = scraper.get_most_popular_trim(best_data)

    return most_popular

def scrape_all_vehicles(output_file='vehicle_pricing_tracker.xlsx', model_years=[2024, 2025, 2026]):
    """
    Scrape pricing data for all top 75 vehicles and update the Excel tracker.

    Args:
        output_file: Name of the Excel file to create/update
        model_years: List of model years to attempt to scrape
    """
    vehicles = get_vehicle_list()
    scraper = IseecarsPrice()
    tracker = VehiclePriceTracker(output_file)

    # Load or create the tracker
    tracker.load_tracker()

    # Scrape data for all vehicles
    scraped_data = []

    for vehicle in vehicles:
        try:
            brand = vehicle['brand']
            model = vehicle['model']
            rank = vehicle['rank']

            pricing = process_vehicle_data(brand, model, scraper)

            if pricing:
                # Add rank information
                pricing['rank'] = rank
                scraped_data.append(pricing)
                logger.info(f"✓ {brand} {model}: ${pricing.get('msrp', 'N/A')} MSRP")
            else:
                logger.warning(f"✗ {brand} {model}: No pricing data found")

        except Exception as e:
            logger.error(f"Error processing {vehicle['brand']} {vehicle['model']}: {e}")
            continue

    # Add the weekly sheet to the tracker
    if scraped_data:
        tracker.add_weekly_sheet(scraped_data)
        tracker.save()
        logger.info(f"✓ Tracker saved to {output_file}")
        logger.info(f"✓ Scraped pricing for {len(scraped_data)} out of {len(vehicles)} vehicles")
    else:
        logger.error("No data was scraped successfully")

    return scraped_data

def scrape_single_vehicle(brand, model, output_file='vehicle_pricing_tracker.xlsx', model_years=[2024, 2025, 2026]):
    """
    Scrape pricing data for a single vehicle for testing.

    Args:
        brand: Vehicle brand
        model: Vehicle model
        output_file: Name of the Excel file to create/update
        model_years: List of model years to attempt to scrape
    """
    scraper = IseecarsPrice()
    tracker = VehiclePriceTracker(output_file)

    # Load or create the tracker
    tracker.load_tracker()

    logger.info(f"Scraping {brand} {model}...")

    pricing = process_vehicle_data(brand, model, scraper)

    if pricing:
        pricing['rank'] = 0  # No rank for single vehicle test
        tracker.add_weekly_sheet([pricing])
        tracker.save()
        logger.info(f"✓ Data saved to {output_file}")
        return pricing
    else:
        logger.error(f"No pricing data found for {brand} {model}")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scrape vehicle pricing from iseecars.com and update tracking spreadsheet'
    )
    parser.add_argument(
        '--single',
        nargs=2,
        metavar=('BRAND', 'MODEL'),
        help='Scrape a single vehicle (e.g., --single Ford F-150)'
    )
    parser.add_argument(
        '--output',
        default='vehicle_pricing_tracker.xlsx',
        help='Output Excel file name (default: vehicle_pricing_tracker.xlsx)'
    )
    parser.add_argument(
        '--years',
        default='2024,2025,2026',
        help='Model years to scrape (comma-separated, default: 2024,2025,2026)'
    )

    args = parser.parse_args()

    # Parse model years
    model_years = [int(y.strip()) for y in args.years.split(',')]

    if args.single:
        # Single vehicle mode (for testing)
        brand, model = args.single
        result = scrape_single_vehicle(brand, model, args.output, model_years)
        if result:
            print(f"\n✓ Successfully scraped {brand} {model}")
            print(f"  Model Year: {result['model_year']}")
            print(f"  Trim: {result['trim']}")
            print(f"  MSRP: ${result['msrp']:,.2f}" if result['msrp'] else "  MSRP: N/A")
            print(f"  Invoice: ${result['invoice']:,.2f}" if result['invoice'] else "  Invoice: N/A")
            print(f"  Destination Fee: ${result['destination_fee']:,.2f}" if result['destination_fee'] else "  Destination Fee: N/A")
    else:
        # Batch mode (all 75 vehicles)
        logger.info(f"Starting batch scrape of all vehicles...")
        logger.info(f"Output file: {args.output}")
        logger.info(f"Model years: {model_years}")
        scrape_all_vehicles(args.output, model_years)
