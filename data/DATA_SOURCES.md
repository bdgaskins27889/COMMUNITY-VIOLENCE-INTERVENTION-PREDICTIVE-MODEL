# Data Sources Documentation

## Verified Public Data Sources

### 1. Chicago Crime Data

**Source:** City of Chicago Data Portal - Crimes 2001 to Present  
**URL:** https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2  
**API Endpoint:** Socrata Open Data API (SODA)  
**Dataset ID:** `ijzp-q8t2`  
**Update Frequency:** Daily (minus most recent 7 days)  
**Records:** 8.48+ million crime incidents  
**Time Range:** 2001 - Present  

**Key Fields:**
- `id` - Unique identifier
- `case_number` - CPD Records Division Number
- `date` - Incident date/time
- `block` - Partially redacted address (block level)
- `iucr` - Illinois Uniform Crime Reporting code
- `primary_type` - Primary crime classification
- `description` - Detailed crime description
- `location_description` - Location type
- `arrest` - Whether arrest was made
- `domestic` - Domestic violence indicator
- `beat` - Police beat
- `district` - Police district
- `ward` - City council ward
- `latitude` / `longitude` - Geographic coordinates

**API Access:**
```
Base URL: https://data.cityofchicago.org/resource/ijzp-q8t2.json
Authentication: Optional (app token recommended for higher limits)
Format: JSON, CSV, XML
Query Language: SoQL (Socrata Query Language)
```

**Example Query:**
```
https://data.cityofchicago.org/resource/ijzp-q8t2.json?$where=date>'2024-01-01'&primary_type=HOMICIDE
```

---

### 2. Census Data - American Community Survey (ACS)

**Source:** U.S. Census Bureau  
**API:** Census Data API  
**URL:** https://www.census.gov/data/developers/data-sets/acs-5year.html  
**Dataset:** ACS 5-Year Estimates  

**Key Variables:**
- Median household income
- Unemployment rate
- Poverty rate
- Educational attainment
- Population demographics
- Housing characteristics

**API Access:**
```
Base URL: https://api.census.gov/data/{year}/acs/acs5
Authentication: API key required (free)
Geographic Level: Tract, Block Group, ZIP Code
```

---

### 3. CDC Social Vulnerability Index (SVI)

**Source:** CDC/ATSDR  
**URL:** https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html  
**Format:** CSV, Shapefile, Geodatabase  
**Update:** Annual  
**Geographic Level:** Census Tract  

**Key Themes:**
1. Socioeconomic Status
2. Household Composition & Disability
3. Minority Status & Language
4. Housing Type & Transportation

**Variables:**
- Overall SVI score (0-1)
- Theme-specific scores
- Percentile rankings
- Raw variable counts

---

### 4. OpenStreetMap (OSM) Data

**Source:** OpenStreetMap Foundation  
**API:** Overpass API  
**URL:** https://overpass-api.de/  
**License:** Open Database License (ODbL)  

**Infrastructure Features:**
- Schools
- Parks and recreation
- Transit stations
- Commercial establishments
- Healthcare facilities
- Religious institutions

**API Access:**
```
Endpoint: https://overpass-api.de/api/interpreter
Query Language: Overpass QL
Format: JSON, XML
```

---

### 5. Chicago Abandoned Buildings

**Source:** City of Chicago Data Portal  
**URL:** https://data.cityofchicago.org/Buildings/311-Service-Requests-Vacant-and-Abandoned-Building/7nii-7srd  
**API Endpoint:** Socrata SODA API  
**Dataset ID:** `7nii-7srd`  
**Update Frequency:** Daily  

**Key Fields:**
- Service request number
- Request date
- Address
- Status
- Latitude/Longitude

---

### 6. ShotSpotter Alerts (Chicago)

**Source:** City of Chicago Data Portal  
**URL:** https://data.cityofchicago.org/Public-Safety/Violence-Reduction-Shotspotter-Alerts/3h7q-7mdb  
**API Endpoint:** Socrata SODA API  
**Dataset ID:** `3h7q-7mdb`  
**Update Frequency:** Daily  

**Key Fields:**
- Alert date/time
- Number of rounds detected
- Location (latitude/longitude)
- Community area
- Beat

---

## Multi-City Adaptability

### Additional City Data Portals

**New York City:**
- NYC Open Data: https://opendata.cityofnewyork.us/
- NYPD Complaint Data: https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date/5uac-w243

**Los Angeles:**
- LA Open Data: https://data.lacity.org/
- Crime Data: https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8

**Philadelphia:**
- OpenDataPhilly: https://opendataphilly.org/
- Crime Incidents: https://opendataphilly.org/datasets/crime-incidents/

**Baltimore:**
- Open Baltimore: https://data.baltimorecity.gov/
- Crime Data: https://data.baltimorecity.gov/datasets/part-1-crime-data/

**Seattle:**
- Seattle Open Data: https://data.seattle.gov/
- Crime Data: https://data.seattle.gov/Public-Safety/SPD-Crime-Data-2008-Present/tazs-3rd5

---

## Data Collection Strategy

### Phase 1: Chicago Implementation
1. Crime incidents (2020-present)
2. ShotSpotter alerts
3. Abandoned buildings
4. Census tract boundaries
5. ACS socioeconomic data
6. CDC SVI data
7. OSM infrastructure features

### Phase 2: Multi-City Expansion
1. Identify city-specific data portals
2. Map equivalent datasets
3. Standardize field names and schemas
4. Create city-specific configuration files
5. Test data pipeline for each city

---

## Ethical Considerations

### Data Limitations
- Crime data reflects reported incidents only (underreporting bias)
- Geographic precision limited to block level (privacy protection)
- 7-day lag in Chicago data (operational constraint)
- Reporting practices vary by jurisdiction

### Privacy Safeguards
- No individual-level identifiers
- Addresses redacted to block level
- Neighborhood-level aggregation only
- Minimum population thresholds for analysis

---

## Data Quality Checks

### Validation Steps
1. Check for missing coordinates
2. Verify date ranges
3. Validate geographic boundaries
4. Identify duplicate records
5. Assess completeness of key fields
6. Cross-reference with official statistics

### Data Cleaning
1. Remove records with invalid coordinates
2. Standardize date/time formats
3. Handle missing values appropriately
4. Filter for relevant crime types
5. Geocode missing locations where possible

---

*Last Updated: January 23, 2026*
