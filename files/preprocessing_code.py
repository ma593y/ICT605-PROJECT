import json
import pandas as pd

# Specify the data types for geocoded coordinate columns to treat them as strings
dtype = {'Geocoded_City1': 'string', 'Geocoded_City2': 'string'}

# Load the dataset
df = pd.read_csv('US Airline Flight Routes and Fares 1993-2024.csv', dtype=dtype)

# Convert all column names to pascal case
df.columns = [
    'TableId', 'Year', 'Quarter', 'OriginCityMarketId', 'DestinationCityMarketId',
    'OriginCity', 'DestinationCity', 'OriginAirportId', 'DestinationAirportId', 
    'OriginAirportCode', 'DestinationAirportCode', 'RouteDistanceInMiles', 'PassengerCount', 
    'AverageFare', 'LargestCarrierCode', 'LargestCarrierMarketShare', 'LargestCarrierAverageFare', 
    'LowestFareCarrierCode', 'LowestFareMarketShare', 'LowestFare', 
    'OriginCityCoordinates', 'DestinationCityCoordinates', 'RouteId'
]

# Display rows with any missing values
missing_values_df = df[df.isna().any(axis=1)]
# print(missing_values_df)

# Count the records before dropping missing values
initial_count = len(df)
print(f"Record count before dropping missing values: {initial_count}")

# Count of rows with missing values
print(f"Number of rows with missing values: {len(missing_values_df)}")

# Drop rows with any missing values
df = df.dropna()

# Count the records after dropping missing values
final_count = len(df)
print(f"Record count after dropping missing values: {final_count}")

df = df.drop(columns=['TableId', 'RouteId'])

# Create a new "Route" column by combining "OriginAirportCode" and "DestinationAirportCode"
df['Route'] = df['OriginAirportCode'] + '-' + df['DestinationAirportCode']

# print(json.dumps(list(df.columns), indent=4))

# Save the dataset in csv format and parquet format
df.to_parquet('../datasets/_dataset.parquet', index=False)
df.to_csv('../datasets/_dataset.csv', index=False)