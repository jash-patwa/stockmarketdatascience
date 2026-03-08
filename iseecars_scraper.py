"""
iseecars.com pricing data scraper for vehicle tracking.
Extracts MSRP, invoice price, and destination fees for specific model years.
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ISeeCarsScraperError(Exception):
    """Base exception for ISeeCars scraper."""
    pass


class ISeeCarsScraperPriceScraper:
    """Scraper for iseecars.com pricing data."""

    BASE_URL = "https://www.iseecars.com/car"

    def __init__(self, delay: float = 2.0):
        """
        Initialize scraper.

        Args:
            delay: Delay between requests in seconds to be respectful to the server
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def build_url(self, make: str, model: str) -> str:
        """Build the iseecars.com URL for a vehicle."""
        make_model = f"{make}-{model}".lower().replace(" ", "-")
        return f"{self.BASE_URL}/{make_model}-price"

    def get_pricing_data(self, make: str, model: str,
                        model_years: Optional[List[int]] = None) -> Dict[int, List[Dict]]:
        """
        Get pricing data for a vehicle across model years.

        Args:
            make: Vehicle make (e.g., 'GMC')
            model: Vehicle model (e.g., 'Sierra 1500')
            model_years: List of model years to scrape. If None, uses default (2026, 2025, 2024)

        Returns:
            Dictionary with model year as key and list of trim data as value.
            Each trim has: {'trim': str, 'msrp': float, 'invoice': float, 'destination_fee': float}
        """
        if model_years is None:
            model_years = [2026, 2025, 2024]

        results = {}
        url = self.build_url(make, model)

        logger.info(f"Fetching data for {make} {model}...")

        try:
            # Fetch the page
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract available model years from the page
            available_years = self._extract_model_years(soup)
            logger.info(f"Available model years: {available_years}")

            # Request data for each model year
            for year in model_years:
                if year in available_years:
                    pricing_data = self._scrape_model_year(make, model, year)
                    if pricing_data:
                        results[year] = pricing_data

            time.sleep(self.delay)

        except Exception as e:
            logger.error(f"Error fetching data for {make} {model}: {e}")
            raise ISeeCarsScraperError(f"Failed to scrape {make} {model}: {str(e)}")

        return results

    def _extract_model_years(self, soup: BeautifulSoup) -> List[int]:
        """Extract available model years from the page."""
        years = []

        # Look for year selectors or year references in the page
        year_patterns = re.findall(r'\b(20\d{2})\b', soup.get_text())
        unique_years = sorted(set(int(y) for y in year_patterns if 2020 <= int(y) <= 2030))

        return unique_years

    def _scrape_model_year(self, make: str, model: str, model_year: int) -> Optional[List[Dict]]:
        """
        Scrape pricing data for a specific model year.

        Args:
            make: Vehicle make
            model: Vehicle model
            model_year: Model year to scrape

        Returns:
            List of trim data or None if not found
        """
        url = self.build_url(make, model)

        try:
            # Add model year parameter if needed
            params = {'year': model_year}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            trim_data = self._extract_trim_data(soup)

            if not trim_data:
                logger.warning(f"No trim data found for {make} {model} {model_year}")
                return None

            return trim_data

        except Exception as e:
            logger.warning(f"Could not scrape {make} {model} {model_year}: {e}")
            return None

    def _extract_trim_data(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract trim pricing data from the page.

        Returns:
            List of dictionaries with trim, msrp, invoice, destination_fee
        """
        trim_data = []

        # Look for price tables - the structure may vary, so we try multiple selectors
        table = soup.find('table', class_=re.compile(r'price|trim', re.I))

        if not table:
            # Try finding any table that contains pricing information
            all_tables = soup.find_all('table')
            for t in all_tables:
                if self._looks_like_pricing_table(t):
                    table = t
                    break

        if not table:
            logger.warning("Could not find pricing table")
            return []

        rows = table.find_all('tr')
        headers = self._extract_headers(rows[0] if rows else None)

        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 3:
                trim_info = self._parse_trim_row(cells, headers)
                if trim_info:
                    trim_data.append(trim_info)

        return trim_data

    def _looks_like_pricing_table(self, table: BeautifulSoup) -> bool:
        """Check if a table contains pricing information."""
        text = table.get_text().lower()
        return any(keyword in text for keyword in ['msrp', 'invoice', 'price', 'trim'])

    def _extract_headers(self, header_row: Optional[BeautifulSoup]) -> Dict[str, int]:
        """Extract column headers and their indices."""
        headers = {}
        if not header_row:
            return headers

        cells = header_row.find_all(['th', 'td'])
        for idx, cell in enumerate(cells):
            text = cell.get_text().strip().lower()
            if 'trim' in text:
                headers['trim'] = idx
            elif 'msrp' in text:
                headers['msrp'] = idx
            elif 'invoice' in text:
                headers['invoice'] = idx
            elif 'destination' in text or 'dest' in text:
                headers['destination_fee'] = idx

        return headers

    def _parse_trim_row(self, cells: List, headers: Dict[str, int]) -> Optional[Dict]:
        """Parse a single row of trim pricing data."""
        try:
            trim_info = {}

            # Extract trim name
            if 'trim' in headers:
                trim_info['trim'] = cells[headers['trim']].get_text().strip()
            else:
                trim_info['trim'] = cells[0].get_text().strip()

            # Extract MSRP
            if 'msrp' in headers:
                trim_info['msrp'] = self._parse_price(cells[headers['msrp']].get_text())

            # Extract Invoice
            if 'invoice' in headers:
                trim_info['invoice'] = self._parse_price(cells[headers['invoice']].get_text())

            # Extract Destination Fee
            if 'destination_fee' in headers:
                trim_info['destination_fee'] = self._parse_price(cells[headers['destination_fee']].get_text())
            else:
                trim_info['destination_fee'] = 0.0

            # Validate that we have pricing data
            if trim_info.get('msrp') or trim_info.get('invoice'):
                return trim_info

            return None

        except Exception as e:
            logger.debug(f"Error parsing trim row: {e}")
            return None

    def _parse_price(self, price_str: str) -> float:
        """Parse a price string to float."""
        # Remove currency symbols and commas
        cleaned = re.sub(r'[$,]', '', price_str.strip())
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def get_most_popular_trim(self, trim_data: List[Dict]) -> Optional[Dict]:
        """
        Get the most popular trim from a list.
        By default, assumes the first trim is the base/most popular model.
        Can be customized with market research.

        Args:
            trim_data: List of trim dictionaries

        Returns:
            The most popular trim dictionary or None
        """
        if not trim_data:
            return None

        # The first trim in the list is typically the base model (most popular)
        return trim_data[0]
