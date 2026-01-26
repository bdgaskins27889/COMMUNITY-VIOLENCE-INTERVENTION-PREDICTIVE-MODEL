"""
Spatial Aggregation Module
Aggregates crime and environmental data to neighborhood level
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import requests
from typing import Optional, Dict
import os


class SpatialAggregator:
    """Aggregates point-level data to neighborhood boundaries"""
    
    def __init__(self, boundaries_gdf: gpd.GeoDataFrame):
        """
        Initialize spatial aggregator
        
        Args:
            boundaries_gdf: GeoDataFrame with neighborhood boundaries
        """
        self.boundaries = boundaries_gdf
        self.neighborhood_id_col = self._identify_id_column()
        
        print(f"Initialized with {len(self.boundaries)} neighborhoods")
    
    def _identify_id_column(self) -> str:
        """Identify the neighborhood ID column"""
        possible_names = ['community', 'area_numbe', 'area_num_1', 'neighborhood', 
                         'name', 'GEOID', 'id']
        for col in self.boundaries.columns:
            if any(name.lower() in col.lower() for name in possible_names):
                return col
        return self.boundaries.columns[0]
    
    def aggregate_points_to_neighborhoods(
        self, 
        points_df: pd.DataFrame,
        lat_col: str = 'latitude',
        lon_col: str = 'longitude',
        aggregation: str = 'count'
    ) -> pd.DataFrame:
        """
        Aggregate point data to neighborhoods
        
        Args:
            points_df: DataFrame with point data (must have lat/lon)
            lat_col: Name of latitude column
            lon_col: Name of longitude column
            aggregation: Aggregation method ('count', 'sum', 'mean')
            
        Returns:
            DataFrame with aggregated values by neighborhood
        """
        print(f"Aggregating {len(points_df)} points to neighborhoods...")
        
        # Create GeoDataFrame from points
        geometry = [Point(xy) for xy in zip(points_df[lon_col], points_df[lat_col])]
        points_gdf = gpd.GeoDataFrame(points_df, geometry=geometry, crs='EPSG:4326')
        
        # Ensure same CRS
        if self.boundaries.crs != points_gdf.crs:
            points_gdf = points_gdf.to_crs(self.boundaries.crs)
        
        # Spatial join
        joined = gpd.sjoin(
            points_gdf, 
            self.boundaries, 
            how='left', 
            predicate='within'
        )
        
        # Count points per neighborhood
        if aggregation == 'count':
            agg_df = joined.groupby(self.neighborhood_id_col).size().reset_index(name='count')
        elif aggregation == 'sum':
            agg_df = joined.groupby(self.neighborhood_id_col).sum().reset_index()
        elif aggregation == 'mean':
            agg_df = joined.groupby(self.neighborhood_id_col).mean().reset_index()
        
        # Merge back with boundaries to include neighborhoods with zero counts
        result = self.boundaries[[self.neighborhood_id_col]].merge(
            agg_df, 
            on=self.neighborhood_id_col, 
            how='left'
        )
        
        if aggregation == 'count':
            result['count'] = result['count'].fillna(0).astype(int)
        
        print(f"Aggregated to {len(result)} neighborhoods")
        return result
    
    def aggregate_temporal_spatial(
        self,
        points_df: pd.DataFrame,
        date_col: str = 'date',
        lat_col: str = 'latitude',
        lon_col: str = 'longitude',
        temporal_unit: str = 'week'
    ) -> pd.DataFrame:
        """
        Aggregate points by both time and space
        
        Args:
            points_df: DataFrame with point data
            date_col: Name of date column
            lat_col: Latitude column
            lon_col: Longitude column
            temporal_unit: Time unit ('week', 'month', 'day')
            
        Returns:
            DataFrame with counts by neighborhood and time period
        """
        print(f"Performing temporal-spatial aggregation...")
        
        # Ensure date is datetime
        points_df[date_col] = pd.to_datetime(points_df[date_col])
        
        # Create temporal grouping
        if temporal_unit == 'week':
            points_df['time_period'] = points_df[date_col].dt.to_period('W')
        elif temporal_unit == 'month':
            points_df['time_period'] = points_df[date_col].dt.to_period('M')
        elif temporal_unit == 'day':
            points_df['time_period'] = points_df[date_col].dt.to_period('D')
        
        # Create GeoDataFrame
        geometry = [Point(xy) for xy in zip(points_df[lon_col], points_df[lat_col])]
        points_gdf = gpd.GeoDataFrame(points_df, geometry=geometry, crs='EPSG:4326')
        
        # Ensure same CRS
        if self.boundaries.crs != points_gdf.crs:
            points_gdf = points_gdf.to_crs(self.boundaries.crs)
        
        # Spatial join
        joined = gpd.sjoin(points_gdf, self.boundaries, how='left', predicate='within')
        
        # Group by neighborhood and time period
        agg_df = joined.groupby([self.neighborhood_id_col, 'time_period']).size().reset_index(name='count')
        
        # Convert period to string for easier handling
        agg_df['time_period'] = agg_df['time_period'].astype(str)
        
        print(f"Created {len(agg_df)} neighborhood-time observations")
        return agg_df
    
    def calculate_density(
        self,
        counts_df: pd.DataFrame,
        count_col: str = 'count'
    ) -> pd.DataFrame:
        """
        Calculate density (count per square km)
        
        Args:
            counts_df: DataFrame with counts by neighborhood
            count_col: Name of count column
            
        Returns:
            DataFrame with density column added
        """
        # Calculate area in square kilometers
        boundaries_proj = self.boundaries.to_crs('EPSG:3857')  # Web Mercator for area calc
        boundaries_proj['area_sqkm'] = boundaries_proj.geometry.area / 1_000_000
        
        # Merge area with counts
        result = counts_df.merge(
            boundaries_proj[[self.neighborhood_id_col, 'area_sqkm']],
            on=self.neighborhood_id_col,
            how='left'
        )
        
        # Calculate density
        result['density'] = result[count_col] / result['area_sqkm']
        result['density'] = result['density'].fillna(0)
        
        return result


class BoundaryLoader:
    """Loads neighborhood boundary data"""
    
    @staticmethod
    def load_boundaries(city_config: Dict, cache_dir: str = 'data/boundaries') -> gpd.GeoDataFrame:
        """
        Load neighborhood boundaries for a city
        
        Args:
            city_config: City configuration dictionary
            cache_dir: Directory to cache boundary files
            
        Returns:
            GeoDataFrame with neighborhood boundaries
        """
        city_name = city_config['name']
        boundary_config = city_config['boundaries']
        
        print(f"Loading boundaries for {city_name}...")
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Check for cached file
        cache_file = os.path.join(cache_dir, f"{city_name.lower().replace(' ', '_')}_boundaries.geojson")
        
        if os.path.exists(cache_file):
            print(f"Loading cached boundaries from {cache_file}")
            gdf = gpd.read_file(cache_file)
        else:
            # Download from URL
            url = boundary_config['url']
            print(f"Downloading boundaries from {url}")
            
            try:
                gdf = gpd.read_file(url)
                
                # Save to cache
                gdf.to_file(cache_file, driver='GeoJSON')
                print(f"Boundaries cached to {cache_file}")
                
            except Exception as e:
                print(f"Error loading boundaries: {e}")
                raise
        
        # Ensure CRS is set
        if gdf.crs is None:
            gdf = gdf.set_crs('EPSG:4326')
        
        print(f"Loaded {len(gdf)} neighborhood boundaries")
        return gdf
    
    @staticmethod
    def load_census_tracts(
        state_fips: str,
        county_fips: Optional[str] = None,
        year: int = 2021,
        cache_dir: str = 'data/boundaries'
    ) -> gpd.GeoDataFrame:
        """
        Load census tract boundaries from Census Bureau
        
        Args:
            state_fips: State FIPS code
            county_fips: County FIPS code (optional)
            year: Census year
            cache_dir: Cache directory
            
        Returns:
            GeoDataFrame with census tract boundaries
        """
        print(f"Loading census tract boundaries...")
        
        # Census tract boundary URL
        url = f"https://www2.census.gov/geo/tiger/TIGER{year}/TRACT/tl_{year}_{state_fips}_tract.zip"
        
        cache_file = os.path.join(
            cache_dir, 
            f"census_tracts_{state_fips}_{county_fips if county_fips else 'all'}_{year}.geojson"
        )
        
        if os.path.exists(cache_file):
            print(f"Loading cached tracts from {cache_file}")
            gdf = gpd.read_file(cache_file)
        else:
            try:
                gdf = gpd.read_file(url)
                
                # Filter by county if specified
                if county_fips:
                    gdf = gdf[gdf['COUNTYFP'] == county_fips]
                
                # Save to cache
                os.makedirs(cache_dir, exist_ok=True)
                gdf.to_file(cache_file, driver='GeoJSON')
                print(f"Tracts cached to {cache_file}")
                
            except Exception as e:
                print(f"Error loading census tracts: {e}")
                raise
        
        print(f"Loaded {len(gdf)} census tracts")
        return gdf


def create_neighborhood_features(
    crime_df: pd.DataFrame,
    boundaries_gdf: gpd.GeoDataFrame,
    start_date: str,
    end_date: str,
    temporal_unit: str = 'week'
) -> pd.DataFrame:
    """
    Create neighborhood-level features from crime data
    
    Args:
        crime_df: Crime incident DataFrame
        boundaries_gdf: Neighborhood boundaries
        start_date: Start date for analysis
        end_date: End date for analysis
        temporal_unit: Temporal aggregation unit
        
    Returns:
        DataFrame with neighborhood features
    """
    aggregator = SpatialAggregator(boundaries_gdf)
    
    # Filter date range
    crime_df['date'] = pd.to_datetime(crime_df['date'])
    mask = (crime_df['date'] >= start_date) & (crime_df['date'] <= end_date)
    crime_filtered = crime_df[mask].copy()
    
    # Temporal-spatial aggregation
    features_df = aggregator.aggregate_temporal_spatial(
        crime_filtered,
        temporal_unit=temporal_unit
    )
    
    # Calculate density
    features_df = aggregator.calculate_density(features_df)
    
    return features_df
