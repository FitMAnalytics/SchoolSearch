import requests
import pandas as pd

# Replace with your U.S. Census Bureau API key
API_KEY = "ea4cf4edca163a7682936c1f208a8cee356d74f1"

# Define API endpoint and parameters
BASE_URL = "https://api.census.gov/data/2021/acs/acs5"
PARAMS = {
    "get": "NAME,B19013_001E",  # B19013_001E: Median household income in the past 12 months
    "for": "zip code tabulation area:*",  # Fetch data for all ZCTAs
    "in": "state:27",  # State FIPS code for Minnesota
    "key": API_KEY
}

# Make the API request
response = requests.get(BASE_URL, params=PARAMS)

if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Convert to a DataFrame for easy manipulation
    columns = data[0]  # First row contains column names
    rows = data[1:]    # Subsequent rows contain data
    df = pd.DataFrame(rows, columns=columns)

    # Rename columns for clarity
    df = df.rename(columns={
        "NAME": "ZCTA_Name",
        "B19013_001E": "Median_Income",
        "zip code tabulation area": "ZCTA"
    })

    # Convert income to numeric and handle missing values
    df["Median_Income"] = pd.to_numeric(df["Median_Income"], errors="coerce")

    # Display the first few rows
    print(df.head())

    # Save to CSV
    df.to_csv("minnesota_income_by_zip.csv", index=False)
    print("Data saved to minnesota_income_by_zip.csv")
else:
    print(f"Error: {response.status_code}, {response.text}")
