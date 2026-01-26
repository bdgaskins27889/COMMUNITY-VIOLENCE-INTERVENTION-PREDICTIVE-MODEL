"""
Crime Data Collection Module
Fetches crime data from city open data portals using Socrata API
"""

import os
import pandas as pd
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sodapy import Socrata
import time


class CrimeDataCollector:
    """Collects crime data from municipal open data portals"""
    
    def __init__(self, city_config: Dict[str, Any], app_token: Optional[str] = None):
        """
        Initialize crime data collector
        
        Args:
            city_config: City-specific configuration dictionary
            app_token: Socrata app token for higher rate limits
        """
        self.city_config = city_config
        self.city_name = city_config['name']
        self.crime_config = city_config['crime_data']
        self.app_token = app_token
        
        # Initialize Socrata client
        if self.crime_config['source'] == 'socrata':
            self.client = Socrata(
                self.crime_config['domain'],
                self.app_token,
                timeout=30
            )
    
    def fetch_crime_data(
        self, 
        start_date: str, 
        end_date: str,
        limit: int = 100000,
        violent_only: bool = True
    ) -> pd.DataFrame:
        """
        Fetch crime data for specified date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            limit: Maximum number of records to fetch
            violent_only: If True, filter for violent crimes only
            
        Returns:
            DataFrame containing crime records
        """
        print(f"Fetching crime data for {self.city_name}...")
        print(f"Date range: {start_date} to {end_date}")
        
        # Build query
        date_field = self.crime_config['date_field']
        where_clause = f"{date_field} >= '{start_date}' AND {date_field} <= '{end_date}'"
        
        # Filter for violent crimes if requested
        if violent_only:
            type_field = self.crime_config['type_field']
            violent_types = self.crime_config['violent_crimes']
            violent_filter = " OR ".join([f"{type_field}='{crime}'" for crime in violent_types])
            where_clause += f" AND ({violent_filter})"
        
        try:
            # Fetch data using Socrata API
            results = self.client.get(
                self.crime_config['dataset_id'],
                where=where_clause,
                limit=limit
            )
            
            # Convert to DataFrame
            df = pd.DataFrame.from_records(results)
            
            if df.empty:
                print(f"Warning: No data returned for {self.city_name}")
                return df
            
            # Standardize column names
            df = self._standardize_columns(df)
            
            # Clean and validate data
            df = self._clean_data(df)
            
            print(f"Successfully fetched {len(df)} crime records")
            return df
            
        except Exception as e:
            print(f"Error fetching crime data: {e}")
            raise
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names across different cities"""
        
        rename_map = {
            self.crime_config['date_field']: 'date',
            self.crime_config['lat_field']: 'latitude',
            self.crime_config['lon_field']: 'longitude',
            self.crime_config['type_field']: 'crime_type'
        }
        
        df = df.rename(columns=rename_map)
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate crime data"""
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Convert coordinates to numeric
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        
        # Remove records with missing critical fields
        initial_count = len(df)
        df = df.dropna(subset=['date', 'latitude', 'longitude'])
        removed_count = initial_count - len(df)
        
        if removed_count > 0:
            print(f"Removed {removed_count} records with missing critical fields")
        
        # Validate coordinates (basic bounds check)
        df = df[
            (df['latitude'].between(-90, 90)) & 
            (df['longitude'].between(-180, 180))
        ]
        
        # Add metadata
        df['city'] = self.city_name
        df['data_source'] = f"{self.crime_config['domain']}/{self.crime_config['dataset_id']}"
        df['fetch_date'] = datetime.now()
        
        return df
    
    def fetch_recent_data(self, days: int = 365) -> pd.DataFrame:
        """
        Fetch crime data for the most recent N days
        
        Args:
            days: Number of days to look back
            
        Returns:
            DataFrame containing recent crime records
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.fetch_crime_data(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
    
    def save_to_csv(self, df: pd.DataFrame, output_path: str):
        """Save crime data to CSV file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
    
    def close(self):
        """Close Socrata client connection"""
        if hasattr(self, 'client'):
            self.client.close()


class ShotSpotterCollector:
    """Collects ShotSpotter gunfire detection data"""
    
    def __init__(self, city_config: Dict[str, Any], app_token: Optional[str] = None):
        """Initialize ShotSpotter data collector"""
        self.city_config = city_config
        self.city_name = city_config['name']
        
        if 'shotspotter_data' not in city_config:
            raise ValueError(f"ShotSpotter data not configured for {self.city_name}")
        
        self.shotspotter_config = city_config['shotspotter_data']
        self.app_token = app_token
        
        # Initialize Socrata client
        self.client = Socrata(
            self.shotspotter_config['domain'],
            self.app_token,
            timeout=30
        )
    
    def fetch_shotspotter_data(
        self, 
        start_date: str, 
        end_date: str,
        limit: int = 50000
    ) -> pd.DataFrame:
        """Fetch ShotSpotter alert data"""
        
        print(f"Fetching ShotSpotter data for {self.city_name}...")
        
        date_field = self.shotspotter_config['date_field']
        where_clause = f"{date_field} >= '{start_date}' AND {date_field} <= '{end_date}'"
        
        try:
            results = self.client.get(
                self.shotspotter_config['dataset_id'],
                where=where_clause,
                limit=limit
            )
            
            df = pd.DataFrame.from_records(results)
            
            if df.empty:
                print(f"Warning: No ShotSpotter data returned")
                return df
            
            # Standardize columns
            rename_map = {
                self.shotspotter_config['date_field']: 'date',
                self.shotspotter_config['lat_field']: 'latitude',
                self.shotspotter_config['lon_field']: 'longitude'
            }
            df = df.rename(columns=rename_map)
            
            # Clean data
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
            df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
            df = df.dropna(subset=['date', 'latitude', 'longitude'])
            
            df['city'] = self.city_name
            df['fetch_date'] = datetime.now()
            
            print(f"Successfully fetched {len(df)} ShotSpotter alerts")
            return df
            
        except Exception as e:
            print(f"Error fetching ShotSpotter data: {e}")
            raise
    
    def close(self):
        """Close Socrata client connection"""
        if hasattr(self, 'client'):
            self.client.close()


def fetch_all_crime_data(city_name: str, start_date: str, end_date: str, 
                         output_dir: str, app_token: Optional[str] = None):
    """
    Convenience function to fetch all crime-related data for a city
    
    Args:
        city_name: Name of the city
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        output_dir: Directory to save output files
        app_token: Socrata app token
    """
    from ..utils.config import get_city_config
    
    city_config = get_city_config(city_name)
    
    # Fetch crime data
    crime_collector = CrimeDataCollector(city_config, app_token)
    crime_df = crime_collector.fetch_crime_data(start_date, end_date)
    
    if not crime_df.empty:
        output_path = os.path.join(output_dir, f"{city_name}_crime_data.csv")
        crime_collector.save_to_csv(crime_df, output_path)
    
    crime_collector.close()
    
    # Fetch ShotSpotter data if available
    if 'shotspotter_data' in city_config:
        try:
            shotspotter_collector = ShotSpotterCollector(city_config, app_token)
            shotspotter_df = shotspotter_collector.fetch_shotspotter_data(start_date, end_date)
            
            if not shotspotter_df.empty:
                output_path = os.path.join(output_dir, f"{city_name}_shotspotter_data.csv")
                shotspotter_collector.save_to_csv(shotspotter_df, output_path)
            
            shotspotter_collector.close()
        except Exception as e:
            print(f"ShotSpotter data not available or error occurred: {e}")
    
    print(f"\nData collection complete for {city_name}")
