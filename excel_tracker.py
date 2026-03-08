"""
Excel tracker for weekly vehicle pricing data.
Manages reading vehicle lists and updating weekly tracking spreadsheets.
"""

import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExcelTrackerError(Exception):
    """Base exception for Excel tracker."""
    pass


class VehicleExcelTracker:
    """Manages vehicle pricing data in Excel format."""

    def __init__(self, excel_path: str):
        """
        Initialize the tracker.

        Args:
            excel_path: Path to the Excel file containing vehicle list
        """
        self.excel_path = excel_path
        self.vehicles = []
        self._load_vehicles()

    def _load_vehicles(self) -> None:
        """Load vehicle list from Excel file."""
        try:
            df = pd.read_excel(self.excel_path)
            logger.info(f"Loaded {len(df)} vehicles from {self.excel_path}")

            # Normalize column names
            df.columns = df.columns.str.strip().str.lower()

            # Extract make and model from different possible column names
            self.vehicles = []
            for idx, row in df.iterrows():
                vehicle = {}

                # Try to find make column
                if 'make' in df.columns:
                    vehicle['make'] = row['make']
                elif 'brand' in df.columns:
                    vehicle['make'] = row['brand']

                # Try to find model column
                if 'model' in df.columns:
                    vehicle['model'] = row['model']

                if 'make' in vehicle and 'model' in vehicle:
                    self.vehicles.append(vehicle)

            logger.info(f"Extracted {len(self.vehicles)} vehicles")

        except Exception as e:
            logger.error(f"Error loading vehicles from {self.excel_path}: {e}")
            raise ExcelTrackerError(f"Failed to load vehicles: {str(e)}")

    def create_weekly_tracker(self, output_path: str) -> None:
        """
        Create a new weekly tracker Excel file.

        Args:
            output_path: Path to save the tracker file
        """
        wb = Workbook()
        wb.remove(wb.active)  # Remove default sheet

        logger.info(f"Created new tracker at {output_path}")

    def add_weekly_data(self, output_path: str, week_date: Optional[datetime] = None,
                       pricing_data: Dict[str, Dict] = None) -> None:
        """
        Add or update weekly pricing data in the tracker.

        Args:
            output_path: Path to the tracker Excel file
            week_date: Date for this week's data (defaults to today)
            pricing_data: Dictionary mapping vehicle name to pricing info
        """
        if week_date is None:
            week_date = datetime.now()

        if pricing_data is None:
            pricing_data = {}

        # Create sheet name from week date
        sheet_name = f"Week_{week_date.strftime('%Y-%m-%d')}"

        try:
            # Load existing workbook or create new one
            if self._file_exists(output_path):
                wb = load_workbook(output_path)
            else:
                wb = Workbook()
                if 'Sheet' in wb.sheetnames:
                    wb.remove(wb['Sheet'])

            # Create or get the weekly sheet
            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                ws.delete_rows(1, ws.max_row)
            else:
                ws = wb.create_sheet(sheet_name)

            # Write headers
            headers = ['Make', 'Model', 'Trim', 'MSRP', 'Invoice', 'Destination Fee',
                      'Model Year', 'Capture Date']
            ws.append(headers)

            # Style headers
            self._style_header_row(ws)

            # Write data rows
            for vehicle in self.vehicles:
                vehicle_key = f"{vehicle['make']} {vehicle['model']}"
                if vehicle_key in pricing_data:
                    data = pricing_data[vehicle_key]
                    row = [
                        data.get('make', vehicle['make']),
                        data.get('model', vehicle['model']),
                        data.get('trim', 'N/A'),
                        data.get('msrp', 0),
                        data.get('invoice', 0),
                        data.get('destination_fee', 0),
                        data.get('model_year', 'N/A'),
                        week_date.strftime('%Y-%m-%d')
                    ]
                    ws.append(row)

            # Auto-adjust column widths
            self._auto_adjust_columns(ws)

            # Save workbook
            wb.save(output_path)
            logger.info(f"Added weekly data to {output_path} in sheet '{sheet_name}'")

        except Exception as e:
            logger.error(f"Error adding weekly data: {e}")
            raise ExcelTrackerError(f"Failed to add weekly data: {str(e)}")

    def _style_header_row(self, ws) -> None:
        """Style the header row."""
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment

    def _auto_adjust_columns(self, ws) -> None:
        """Auto-adjust column widths based on content."""
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except TypeError:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width

    def _file_exists(self, path: str) -> bool:
        """Check if file exists."""
        import os
        return os.path.exists(path)

    def get_vehicle_list(self) -> List[Tuple[str, str]]:
        """
        Get list of vehicles as (make, model) tuples.

        Returns:
            List of (make, model) tuples
        """
        return [(v['make'], v['model']) for v in self.vehicles]

    def compare_model_years(self, output_path: str, week_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        Create a comparison DataFrame of prices across model years.

        Args:
            output_path: Path to the tracker file
            week_date: Date to filter by (optional)

        Returns:
            DataFrame with model year comparisons
        """
        try:
            # Read all sheets
            all_data = []
            xlsx = pd.ExcelFile(output_path)

            for sheet_name in xlsx.sheet_names:
                df = pd.read_excel(output_path, sheet_name=sheet_name)
                all_data.append(df)

            combined = pd.concat(all_data, ignore_index=True)

            # Group by Make, Model, Trim and create comparison
            comparison = combined.pivot_table(
                index=['Make', 'Model', 'Trim'],
                columns='Model Year',
                values=['MSRP', 'Invoice', 'Destination Fee'],
                aggfunc='first'
            )

            return comparison

        except Exception as e:
            logger.error(f"Error comparing model years: {e}")
            return pd.DataFrame()
