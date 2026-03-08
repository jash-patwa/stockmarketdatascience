"""
Example usage of the Vehicle Pricing Tracker.

This script demonstrates how to:
1. Scrape pricing data for a specific vehicle
2. Update the weekly tracker
3. Generate comparison reports
"""

from main_tracker import VehiclePricingTracker
from iseecars_scraper import ISeeCarsScraperPriceScraper
from datetime import datetime
import json


def example_1_scrape_single_vehicle():
    """Example: Scrape pricing data for a single vehicle."""
    print("=" * 60)
    print("Example 1: Scrape Single Vehicle")
    print("=" * 60)

    scraper = ISeeCarsScraperPriceScraper()

    # Scrape GMC Sierra 1500
    make = "GMC"
    model = "Sierra 1500"
    model_years = [2026, 2025, 2024]

    try:
        data = scraper.get_pricing_data(make, model, model_years)

        for year, trims in data.items():
            print(f"\n{year} {make} {model}:")
            print(f"  Found {len(trims)} trims")

            # Show the most popular trim
            popular_trim = scraper.get_most_popular_trim(trims)
            if popular_trim:
                print(f"  Most Popular Trim: {popular_trim['trim']}")
                print(f"    MSRP: ${popular_trim.get('msrp', 'N/A'):,.0f}")
                print(f"    Invoice: ${popular_trim.get('invoice', 'N/A'):,.0f}")
                print(f"    Destination Fee: ${popular_trim.get('destination_fee', 'N/A'):,.0f}")

    except Exception as e:
        print(f"Error: {e}")


def example_2_full_tracker_update():
    """Example: Run the full tracker with a vehicle file."""
    print("\n" + "=" * 60)
    print("Example 2: Full Tracker Update")
    print("=" * 60)

    # NOTE: This requires a valid Excel file with vehicle data
    vehicle_file = "75_US_Vehicles_2025.xlsx"
    output_file = "vehicle_pricing_tracker.xlsx"

    try:
        tracker = VehiclePricingTracker(vehicle_file, use_google_drive=False)

        if not tracker.setup():
            print("Failed to set up tracker")
            return

        print(f"Loaded vehicles: {len(tracker.tracker.get_vehicle_list())}")

        # Scrape data for model years 2026, 2025, 2024
        print("Starting scrape...")
        pricing_data = tracker.scrape_all_vehicles([2026, 2025, 2024])

        print(f"Scraped data for {len(pricing_data)} vehicles")

        # Update the tracker
        if pricing_data:
            tracker.update_tracker(output_file, pricing_data, datetime.now())
            print(f"Tracker updated at {output_file}")
        else:
            print("No pricing data was scraped")

    except Exception as e:
        print(f"Error: {e}")


def example_3_inspect_pricing_data():
    """Example: Inspect the structure of pricing data."""
    print("\n" + "=" * 60)
    print("Example 3: Inspect Pricing Data Structure")
    print("=" * 60)

    scraper = ISeeCarsScraperPriceScraper()

    try:
        data = scraper.get_pricing_data("Ford", "F-150", [2026])

        for year, trims in data.items():
            print(f"\n{year} Ford F-150:")
            print(f"Total trims available: {len(trims)}")

            if trims:
                print("\nFirst 3 trims:")
                for i, trim in enumerate(trims[:3]):
                    print(f"\n  Trim {i + 1}: {trim.get('trim', 'Unknown')}")
                    print(f"    MSRP: ${trim.get('msrp', 0):,.2f}")
                    print(f"    Invoice: ${trim.get('invoice', 0):,.2f}")
                    print(f"    Destination Fee: ${trim.get('destination_fee', 0):,.2f}")

    except Exception as e:
        print(f"Error: {e}")


def example_4_price_comparison():
    """Example: Compare prices across model years for a vehicle."""
    print("\n" + "=" * 60)
    print("Example 4: Price Comparison Across Model Years")
    print("=" * 60)

    scraper = ISeeCarsScraperPriceScraper()

    try:
        data = scraper.get_pricing_data("Toyota", "Camry", [2026, 2025, 2024])

        print("\nToyota Camry - Popular Trim Price Comparison:")
        print(f"{'Year':<10} {'Trim':<20} {'MSRP':<15} {'Invoice':<15} {'Dest Fee':<15}")
        print("-" * 75)

        for year in sorted(data.keys(), reverse=True):
            trims = data[year]
            popular = scraper.get_most_popular_trim(trims)

            if popular:
                trim_name = popular.get('trim', 'N/A')[:19]
                msrp = f"${popular.get('msrp', 0):,.0f}"
                invoice = f"${popular.get('invoice', 0):,.0f}"
                dest_fee = f"${popular.get('destination_fee', 0):,.0f}"

                print(f"{year:<10} {trim_name:<20} {msrp:<15} {invoice:<15} {dest_fee:<15}")

    except Exception as e:
        print(f"Error: {e}")


def example_5_calculate_depreciation():
    """Example: Calculate depreciation across model years."""
    print("\n" + "=" * 60)
    print("Example 5: Price Trend Analysis")
    print("=" * 60)

    scraper = ISeeCarsScraperPriceScraper()

    vehicles = [
        ("Honda", "Civic"),
        ("Chevrolet", "Silverado 1500"),
        ("Nissan", "Altima"),
    ]

    try:
        for make, model in vehicles:
            data = scraper.get_pricing_data(make, model, [2026, 2025, 2024])

            msrps = {}
            for year in sorted(data.keys()):
                trims = data[year]
                popular = scraper.get_most_popular_trim(trims)
                if popular:
                    msrps[year] = popular.get('msrp', 0)

            print(f"\n{make} {model}:")
            print(f"  2024 MSRP: ${msrps.get(2024, 'N/A'):,.0f}")
            print(f"  2025 MSRP: ${msrps.get(2025, 'N/A'):,.0f}")
            print(f"  2026 MSRP: ${msrps.get(2026, 'N/A'):,.0f}")

            # Calculate year-over-year changes
            if 2024 in msrps and 2025 in msrps:
                change_24_25 = msrps[2025] - msrps[2024]
                pct_change = (change_24_25 / msrps[2024] * 100) if msrps[2024] > 0 else 0
                print(f"  2024→2025 Change: +${change_24_25:,.0f} ({pct_change:+.1f}%)")

            if 2025 in msrps and 2026 in msrps:
                change_25_26 = msrps[2026] - msrps[2025]
                pct_change = (change_25_26 / msrps[2025] * 100) if msrps[2025] > 0 else 0
                print(f"  2025→2026 Change: +${change_25_26:,.0f} ({pct_change:+.1f}%)")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("\nVehicle Pricing Tracker - Usage Examples\n")

    # Run examples
    example_1_scrape_single_vehicle()
    example_3_inspect_pricing_data()
    example_4_price_comparison()
    example_5_calculate_depreciation()

    # NOTE: example_2_full_tracker_update() requires a valid Excel file
    print("\n" + "=" * 60)
    print("Note: example_2_full_tracker_update() requires your Excel file")
    print("      To run it, uncomment the line below and ensure you have")
    print("      your vehicle list in '75_US_Vehicles_2025.xlsx'")
    print("=" * 60)
    # example_2_full_tracker_update()
