"""
Main orchestrator for vehicle pricing tracker.
Coordinates scraping, data processing, and Excel updates.
"""

import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import logging

from iseecars_scraper import ISeeCarsScraperPriceScraper, ISeeCarsScraperError
from excel_tracker import VehicleExcelTracker, ExcelTrackerError
from google_drive_handler import GoogleDriveHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VehiclePricingTrackerError(Exception):
    """Base exception for vehicle pricing tracker."""
    pass


class VehiclePricingTracker:
    """Main orchestrator for vehicle pricing tracking."""

    def __init__(self, vehicle_source: str, use_google_drive: bool = False):
        """
        Initialize the tracker.

        Args:
            vehicle_source: Path to vehicle Excel file or Google Drive file name
            use_google_drive: Whether to fetch vehicle list from Google Drive
        """
        self.vehicle_source = vehicle_source
        self.use_google_drive = use_google_drive
        self.local_vehicle_file = None
        self.scraper = ISeeCarsScraperPriceScraper(delay=2.0)
        self.tracker = None

    def setup(self) -> bool:
        """
        Set up the tracker (load vehicle data).

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.use_google_drive:
                if not self._download_from_google_drive():
                    return False
            else:
                self.local_vehicle_file = self.vehicle_source

            # Load vehicle list
            self.tracker = VehicleExcelTracker(self.local_vehicle_file)
            return True

        except Exception as e:
            logger.error(f"Setup error: {e}")
            return False

    def _download_from_google_drive(self) -> bool:
        """Download vehicle file from Google Drive."""
        try:
            drive = GoogleDriveHandler()
            file_id = drive.find_file_by_name(self.vehicle_source)

            if not file_id:
                logger.error(f"Could not find {self.vehicle_source} in Google Drive")
                return False

            # Download to local temp file
            self.local_vehicle_file = f"temp_{self.vehicle_source}"
            return drive.download_file(file_id, self.local_vehicle_file)

        except Exception as e:
            logger.error(f"Error downloading from Google Drive: {e}")
            return False

    def scrape_all_vehicles(self, model_years: Optional[List[int]] = None) -> Dict[str, Dict]:
        """
        Scrape pricing data for all vehicles.

        Args:
            model_years: List of model years to scrape

        Returns:
            Dictionary mapping vehicle names to pricing data
        """
        if not self.tracker:
            raise VehiclePricingTrackerError("Tracker not initialized. Call setup() first.")

        if model_years is None:
            model_years = [2026, 2025, 2024]

        pricing_data = {}
        vehicles = self.tracker.get_vehicle_list()

        logger.info(f"Starting to scrape {len(vehicles)} vehicles...")

        for idx, (make, model) in enumerate(vehicles, 1):
            logger.info(f"[{idx}/{len(vehicles)}] Scraping {make} {model}...")

            try:
                year_data = self.scraper.get_pricing_data(make, model, model_years)

                # Extract most popular trim for each year
                for year, trims in year_data.items():
                    popular_trim = self.scraper.get_most_popular_trim(trims)
                    if popular_trim:
                        vehicle_key = f"{make} {model}"
                        if vehicle_key not in pricing_data:
                            pricing_data[vehicle_key] = {}

                        pricing_data[vehicle_key][year] = popular_trim

            except ISeeCarsScraperError as e:
                logger.warning(f"Failed to scrape {make} {model}: {e}")
                continue

        logger.info(f"Successfully scraped {len(pricing_data)} vehicles")
        return pricing_data

    def update_tracker(self, output_path: str,
                      pricing_data: Dict[str, Dict],
                      week_date: Optional[datetime] = None) -> bool:
        """
        Update the weekly tracking Excel file.

        Args:
            output_path: Path to save the tracker Excel file
            pricing_data: Dictionary of pricing data from scrape_all_vehicles()
            week_date: Date for this week's tracking (defaults to today)

        Returns:
            True if successful, False otherwise
        """
        if not self.tracker:
            raise VehiclePricingTrackerError("Tracker not initialized. Call setup() first.")

        try:
            # Flatten pricing data for Excel update
            flattened_data = self._flatten_pricing_data(pricing_data)

            # Update the tracker
            self.tracker.add_weekly_data(output_path, week_date, flattened_data)
            logger.info(f"Updated tracker at {output_path}")
            return True

        except ExcelTrackerError as e:
            logger.error(f"Error updating tracker: {e}")
            return False

    def _flatten_pricing_data(self, pricing_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Flatten multi-year pricing data for Excel.
        Takes the latest available model year for each vehicle.

        Args:
            pricing_data: Dictionary from scrape_all_vehicles()

        Returns:
            Flattened dictionary with single entry per vehicle
        """
        flattened = {}

        for vehicle_key, year_dict in pricing_data.items():
            if year_dict:
                # Get the latest (highest) model year
                latest_year = max(year_dict.keys())
                trim_data = year_dict[latest_year]

                make, model = vehicle_key.split(' ', 1)
                flattened[vehicle_key] = {
                    'make': make,
                    'model': model,
                    'trim': trim_data.get('trim', 'N/A'),
                    'msrp': trim_data.get('msrp', 0),
                    'invoice': trim_data.get('invoice', 0),
                    'destination_fee': trim_data.get('destination_fee', 0),
                    'model_year': latest_year
                }

        return flattened

    def generate_comparison_report(self, output_path: str) -> bool:
        """
        Generate a comparison report across model years.

        Args:
            output_path: Path to the tracker Excel file with weekly data

        Returns:
            True if successful, False otherwise
        """
        try:
            comparison = self.tracker.compare_model_years(output_path)
            logger.info("Comparison report generated")
            logger.info(comparison)
            return True

        except Exception as e:
            logger.error(f"Error generating comparison report: {e}")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Vehicle Pricing Tracker for iseecars.com'
    )
    parser.add_argument(
        '--vehicle-file',
        required=False,
        default='75_US_Vehicles_2025.xlsx',
        help='Path to vehicle Excel file or Google Drive file name'
    )
    parser.add_argument(
        '--google-drive',
        action='store_true',
        help='Fetch vehicle file from Google Drive'
    )
    parser.add_argument(
        '--output',
        required=False,
        default='vehicle_pricing_tracker.xlsx',
        help='Output path for the tracking Excel file'
    )
    parser.add_argument(
        '--model-years',
        nargs='+',
        type=int,
        default=[2026, 2025, 2024],
        help='Model years to scrape (default: 2026 2025 2024)'
    )
    parser.add_argument(
        '--skip-scrape',
        action='store_true',
        help='Skip scraping (only update from cached data)'
    )

    args = parser.parse_args()

    logger.info("Starting Vehicle Pricing Tracker")
    logger.info(f"Vehicle source: {args.vehicle_file}")
    logger.info(f"Output file: {args.output}")
    logger.info(f"Model years: {args.model_years}")

    try:
        # Initialize tracker
        tracker = VehiclePricingTracker(args.vehicle_file, args.google_drive)

        # Setup
        if not tracker.setup():
            logger.error("Failed to setup tracker")
            return 1

        # Scrape data
        if not args.skip_scrape:
            pricing_data = tracker.scrape_all_vehicles(args.model_years)
        else:
            logger.info("Skipping scrape step")
            pricing_data = {}

        # Update tracker
        if pricing_data:
            if not tracker.update_tracker(args.output, pricing_data):
                logger.error("Failed to update tracker")
                return 1

        logger.info("Vehicle Pricing Tracker completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
