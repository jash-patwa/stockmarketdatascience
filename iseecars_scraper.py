import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IseecarsPrice(object):
    """Scraper for pricing data from iseecars.com"""

    def __init__(self):
        self.base_url = "https://www.iseecars.com/car/{brand}-{model}-price"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def format_url(self, brand, model, model_year=None):
        """Format the URL for a specific vehicle."""
        brand_formatted = brand.lower().replace(" ", "-")
        model_formatted = model.lower().replace(" ", "-")
        url = self.base_url.format(brand=brand_formatted, model=model_formatted)

        if model_year:
            url += f"?model_year={model_year}"

        return url

    def scrape_vehicle_pricing(self, brand, model, model_year=2026):
        """
        Scrape pricing data for a vehicle.

        Returns:
            dict: Contains pricing data for all trims
        """
        url = self.format_url(brand, model, model_year)
        logger.info(f"Scraping {model_year} {brand} {model} from {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the pricing table
            pricing_data = self._extract_pricing_table(soup, brand, model, model_year)

            return pricing_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error scraping {brand} {model}: {e}")
            return None

    def _extract_pricing_table(self, soup, brand, model, model_year):
        """Extract pricing table from the page."""
        # Look for the pricing table
        table = soup.find('table', {'class': ['table', 'pricing-table']})

        if not table:
            # Try alternative table selectors
            tables = soup.find_all('table')
            if tables:
                table = tables[0]

        if not table:
            logger.warning(f"No pricing table found for {brand} {model}")
            return None

        trims_data = []
        rows = table.find_all('tr')

        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 4:
                try:
                    trim_name = cols[0].get_text(strip=True)
                    msrp = self._clean_price(cols[1].get_text(strip=True))
                    invoice = self._clean_price(cols[2].get_text(strip=True))
                    destination_fee = self._clean_price(cols[3].get_text(strip=True))

                    trims_data.append({
                        'trim': trim_name,
                        'msrp': msrp,
                        'invoice': invoice,
                        'destination_fee': destination_fee
                    })
                except Exception as e:
                    logger.warning(f"Error parsing row for {brand} {model}: {e}")
                    continue

        if trims_data:
            return {
                'brand': brand,
                'model': model,
                'model_year': model_year,
                'trims': trims_data,
                'scraped_date': datetime.now().isoformat()
            }

        return None

    def _clean_price(self, price_str):
        """Clean and convert price string to float."""
        if not price_str:
            return None

        # Remove currency symbols and commas
        cleaned = price_str.replace('$', '').replace(',', '').strip()

        try:
            return float(cleaned)
        except ValueError:
            return None

    def scrape_multiple_years(self, brand, model, years=[2024, 2025, 2026]):
        """
        Scrape pricing data for multiple model years.

        Returns:
            list: List of pricing data for each year
        """
        all_data = []

        for year in years:
            data = self.scrape_vehicle_pricing(brand, model, year)
            if data:
                all_data.append(data)

            # Be nice to the server - add delay between requests
            time.sleep(1)

        return all_data

    def get_most_popular_trim(self, pricing_data):
        """
        Get the most popular trim (first trim in the list).

        Returns:
            dict: Pricing data for the most popular trim
        """
        if not pricing_data or 'trims' not in pricing_data:
            return None

        if pricing_data['trims']:
            trim = pricing_data['trims'][0]
            return {
                'brand': pricing_data['brand'],
                'model': pricing_data['model'],
                'model_year': pricing_data['model_year'],
                'trim': trim['trim'],
                'msrp': trim['msrp'],
                'invoice': trim['invoice'],
                'destination_fee': trim['destination_fee'],
                'scraped_date': pricing_data['scraped_date']
            }

        return None

    def scrape_batch(self, vehicles, model_years=[2024, 2025, 2026]):
        """
        Scrape pricing data for a batch of vehicles.

        Args:
            vehicles: List of dicts with 'brand' and 'model' keys
            model_years: List of model years to scrape

        Returns:
            dict: Keyed by vehicle (brand-model) with pricing data
        """
        results = {}

        for vehicle in vehicles:
            brand = vehicle['brand']
            model = vehicle['model']
            key = f"{brand}-{model}".lower()

            vehicle_data = self.scrape_multiple_years(brand, model, model_years)
            results[key] = vehicle_data

        return results
