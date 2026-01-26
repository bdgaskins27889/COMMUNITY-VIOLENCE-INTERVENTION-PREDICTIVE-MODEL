"""
Census and Social Vulnerability Index Data Collection
Fetches socioeconomic data from Census API and CDC SVI
"""

import os
import pandas as pd
import requests
from typing import Optional, Dict, List
import time


class CensusDataCollector:
    """Collects socioeconomic data from US Census Bureau API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Census data collector
        
        Args:
            api_key: Census API key (get free at https://api.census.gov/data/key_signup.html)
        """
        self.api_key = api_key or os.getenv('CENSUS_API_KEY')
        self.base_url = "https://api.census.gov/data"
        
        # ACS 5-Year variables for violence prevention research
        self.variables = {
            'B19013_001E': 'median_household_income',
            'B23025_005E': 'unemployed',
            'B23025_003E': 'in_labor_force',
            'B17001_002E': 'poverty_count',
            'B01003_001E': 'total_population',
            'B15003_001E': 'education_total',
            'B15003_002E': 'education_no_school',
            'B15003_003E': 'education_nursery_4th',
            'B15003_004E': 'education_5th_6th',
            'B15003_005E': 'education_7th_8th',
            'B15003_006E': 'education_9th',
            'B15003_007E': 'education_10th',
            'B15003_008E': 'education_11th',
            'B15003_009E': 'education_12th_no_diploma',
            'B25002_003E': 'vacant_housing_units',
            'B25002_001E': 'total_housing_units'
        }
    
    def fetch_acs_data(
        self, 
        year: int, 
        state_fips: str, 
        county_fips: Optional[str] = None,
        geography: str = 'tract'
    ) -> pd.DataFrame:
        """
        Fetch American Community Survey data
        
        Args:
            year: Data year (e.g., 2021)
            state_fips: State FIPS code (e.g., '17' for Illinois)
            county_fips: County FIPS code (e.g., '031' for Cook County)
            geography: Geographic level ('tract', 'block group', 'county')
            
        Returns:
            DataFrame with ACS variables by census tract
        """
        print(f"Fetching ACS {year} data...")
        
        # Build variable list
        var_list = ','.join(self.variables.keys())
        
        # Build geography string
        if geography == 'tract':
            geo_str = f"tract:*"
            if county_fips:
                geo_str += f"&in=state:{state_fips}+county:{county_fips}"
            else:
                geo_str += f"&in=state:{state_fips}"
        elif geography == 'county':
            geo_str = f"county:{county_fips if county_fips else '*'}&in=state:{state_fips}"
        
        # Build request URL
        url = f"{self.base_url}/{year}/acs/acs5"
        params = {
            'get': var_list,
            'for': geo_str
        }
        
        if self.api_key:
            params['key'] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Convert to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            
            # Rename columns
            for old_name, new_name in self.variables.items():
                if old_name in df.columns:
                    df[new_name] = pd.to_numeric(df[old_name], errors='coerce')
            
            # Calculate derived variables
            df = self._calculate_derived_variables(df)
            
            # Create GEOID
            if 'tract' in df.columns:
                df['GEOID'] = df['state'] + df['county'] + df['tract']
            elif 'county' in df.columns:
                df['GEOID'] = df['state'] + df['county']
            
            print(f"Successfully fetched data for {len(df)} geographic units")
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Census data: {e}")
            raise
    
    def _calculate_derived_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived socioeconomic indicators"""
        
        # Unemployment rate
        if 'unemployed' in df.columns and 'in_labor_force' in df.columns:
            df['unemployment_rate'] = (
                df['unemployed'] / df['in_labor_force'] * 100
            ).fillna(0)
        
        # Poverty rate
        if 'poverty_count' in df.columns and 'total_population' in df.columns:
            df['poverty_rate'] = (
                df['poverty_count'] / df['total_population'] * 100
            ).fillna(0)
        
        # Education: Less than high school
        education_cols = [
            'education_no_school', 'education_nursery_4th', 'education_5th_6th',
            'education_7th_8th', 'education_9th', 'education_10th', 
            'education_11th', 'education_12th_no_diploma'
        ]
        
        if all(col in df.columns for col in education_cols):
            df['education_less_than_hs_count'] = df[education_cols].sum(axis=1)
            df['education_less_than_hs_pct'] = (
                df['education_less_than_hs_count'] / df['education_total'] * 100
            ).fillna(0)
        
        # Vacancy rate
        if 'vacant_housing_units' in df.columns and 'total_housing_units' in df.columns:
            df['vacancy_rate'] = (
                df['vacant_housing_units'] / df['total_housing_units'] * 100
            ).fillna(0)
        
        return df


class SVIDataCollector:
    """Collects CDC Social Vulnerability Index data"""
    
    def __init__(self):
        """Initialize SVI data collector"""
        self.base_url = "https://www.atsdr.cdc.gov/placeandhealth/svi/data"
        
        # SVI field mappings (2020 SVI)
        self.svi_fields = {
            'FIPS': 'GEOID',
            'RPL_THEMES': 'svi_overall',
            'RPL_THEME1': 'svi_socioeconomic',
            'RPL_THEME2': 'svi_household_composition',
            'RPL_THEME3': 'svi_minority_language',
            'RPL_THEME4': 'svi_housing_transportation',
            'E_TOTPOP': 'total_population_svi'
        }
    
    def fetch_svi_data(
        self, 
        year: int = 2020, 
        state_abbr: str = 'IL'
    ) -> pd.DataFrame:
        """
        Fetch CDC Social Vulnerability Index data
        
        Args:
            year: Data year (2020, 2018, 2016, 2014)
            state_abbr: State abbreviation (e.g., 'IL', 'NY')
            
        Returns:
            DataFrame with SVI scores by census tract
        """
        print(f"Fetching CDC SVI {year} data for {state_abbr}...")
        
        # Note: In production, this would download from CDC website
        # For now, we'll provide instructions for manual download
        
        print(f"""
        CDC SVI Data Download Instructions:
        1. Visit: https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html
        2. Select year: {year}
        3. Download state-level data for: {state_abbr}
        4. Extract CSV file to data/raw/ directory
        5. File should be named: SVI{year}_{state_abbr}_TRACT.csv
        """)
        
        # Try to load from local file if already downloaded
        filename = f"SVI{year}_{state_abbr}_TRACT.csv"
        local_path = os.path.join('data', 'raw', filename)
        
        if os.path.exists(local_path):
            print(f"Loading SVI data from {local_path}")
            df = pd.read_csv(local_path, dtype={'FIPS': str})
            
            # Select and rename relevant columns
            available_fields = {k: v for k, v in self.svi_fields.items() if k in df.columns}
            df = df[list(available_fields.keys())].rename(columns=available_fields)
            
            # Ensure GEOID is 11 digits (state + county + tract)
            df['GEOID'] = df['GEOID'].str.zfill(11)
            
            print(f"Successfully loaded SVI data for {len(df)} census tracts")
            return df
        else:
            print(f"SVI data file not found at {local_path}")
            print("Please download manually following the instructions above")
            return pd.DataFrame()
    
    def download_svi_data(self, year: int = 2020, state_abbr: str = 'IL', 
                          output_dir: str = 'data/raw') -> str:
        """
        Download SVI data from CDC website
        
        Args:
            year: Data year
            state_abbr: State abbreviation
            output_dir: Directory to save downloaded file
            
        Returns:
            Path to downloaded file
        """
        # CDC SVI download URL pattern
        url = f"https://svi.cdc.gov/Documents/Data/{year}/csv/states/{state_abbr}.csv"
        
        output_path = os.path.join(output_dir, f"SVI{year}_{state_abbr}_TRACT.csv")
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            print(f"Downloading SVI data from {url}...")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"SVI data saved to {output_path}")
            return output_path
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading SVI data: {e}")
            print("Please download manually from CDC website")
            raise


def fetch_all_socioeconomic_data(
    city_config: Dict,
    year: int = 2021,
    output_dir: str = 'data/raw',
    census_api_key: Optional[str] = None
) -> Dict[str, pd.DataFrame]:
    """
    Fetch all socioeconomic data for a city
    
    Args:
        city_config: City configuration dictionary
        year: Data year
        output_dir: Output directory
        census_api_key: Census API key
        
    Returns:
        Dictionary with 'census' and 'svi' DataFrames
    """
    results = {}
    
    # Fetch Census ACS data
    census_collector = CensusDataCollector(census_api_key)
    
    state_fips = city_config['census']['state_fips']
    county_fips = city_config['census'].get('county_fips')
    
    # Handle multiple counties (e.g., NYC)
    if isinstance(county_fips, list):
        dfs = []
        for county in county_fips:
            df = census_collector.fetch_acs_data(year, state_fips, county)
            dfs.append(df)
        census_df = pd.concat(dfs, ignore_index=True)
    else:
        census_df = census_collector.fetch_acs_data(year, state_fips, county_fips)
    
    results['census'] = census_df
    
    # Save Census data
    census_path = os.path.join(output_dir, f"{city_config['name']}_census_{year}.csv")
    census_df.to_csv(census_path, index=False)
    print(f"Census data saved to {census_path}")
    
    # Fetch SVI data
    svi_collector = SVIDataCollector()
    state_abbr = city_config['state']
    
    try:
        svi_df = svi_collector.fetch_svi_data(year=2020, state_abbr=state_abbr)
        if not svi_df.empty:
            results['svi'] = svi_df
            svi_path = os.path.join(output_dir, f"{city_config['name']}_svi_2020.csv")
            svi_df.to_csv(svi_path, index=False)
            print(f"SVI data saved to {svi_path}")
    except Exception as e:
        print(f"Could not fetch SVI data: {e}")
    
    return results
