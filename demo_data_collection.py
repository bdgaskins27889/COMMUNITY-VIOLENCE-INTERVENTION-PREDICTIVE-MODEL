"""
Demo Script: Data Collection for CVI Risk Predictor
Demonstrates fetching real crime data from Chicago Data Portal
"""

import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_collection.crime_data import CrimeDataCollector
from src.utils.config import get_city_config

def main():
    """
    Demo: Fetch recent crime data for Chicago
    """
    print("=" * 70)
    print("CVI RISK PREDICTOR - DATA COLLECTION DEMO")
    print("=" * 70)
    print()
    
    # Configuration
    city_name = 'chicago'
    days_back = 30  # Fetch last 30 days of data
    
    print(f"📍 City: {city_name.title()}")
    print(f"📅 Time Period: Last {days_back} days")
    print()
    
    # Get city configuration
    print("Loading city configuration...")
    city_config = get_city_config(city_name)
    print(f"✓ Configuration loaded for {city_config['name']}")
    print()
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    print(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print()
    
    # Initialize collector
    print("Initializing data collector...")
    collector = CrimeDataCollector(city_config)
    print("✓ Collector initialized")
    print()
    
    # Fetch crime data
    print("Fetching crime data from Chicago Data Portal...")
    print("(This may take a minute depending on data volume)")
    print()
    
    try:
        crime_df = collector.fetch_crime_data(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            violent_only=True,
            limit=10000  # Limit for demo
        )
        
        if not crime_df.empty:
            print("=" * 70)
            print("DATA COLLECTION SUCCESSFUL!")
            print("=" * 70)
            print()
            
            # Display summary statistics
            print("📊 SUMMARY STATISTICS")
            print("-" * 70)
            print(f"Total Records:        {len(crime_df):,}")
            print(f"Date Range:           {crime_df['date'].min()} to {crime_df['date'].max()}")
            print(f"Unique Crime Types:   {crime_df['crime_type'].nunique()}")
            print()
            
            print("Crime Type Distribution:")
            print(crime_df['crime_type'].value_counts().to_string())
            print()
            
            print("Sample Records:")
            print(crime_df[['date', 'crime_type', 'latitude', 'longitude']].head(10).to_string())
            print()
            
            # Save to CSV
            output_dir = os.path.join('data', 'raw')
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f'chicago_crime_demo_{datetime.now().strftime("%Y%m%d")}.csv')
            
            collector.save_to_csv(crime_df, output_file)
            print(f"✓ Data saved to: {output_file}")
            print()
            
            print("=" * 70)
            print("DEMO COMPLETE!")
            print("=" * 70)
            print()
            print("Next Steps:")
            print("1. Review the saved CSV file")
            print("2. Run spatial aggregation to create neighborhood-level features")
            print("3. Train machine learning models")
            print("4. Generate risk predictions")
            print()
            
        else:
            print("⚠️  No data returned. This may be due to:")
            print("   - API rate limits")
            print("   - Network connectivity issues")
            print("   - Date range with no violent crimes")
            print()
            
    except Exception as e:
        print(f"❌ Error during data collection: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check internet connectivity")
        print("2. Verify Chicago Data Portal is accessible")
        print("3. Consider using a Socrata app token for higher rate limits")
        print()
    
    finally:
        collector.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
