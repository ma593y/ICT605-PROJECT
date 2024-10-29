import pandas as pd
from tabulate import tabulate

# Load the preprocessed dataset
df = pd.read_parquet('datasets/_dataset.parquet')  # Adjust path if needed

# List of columns to inspect
columns_to_check = [
    'Year', 'Quarter', 'OriginCityMarketId', 'DestinationCityMarketId',
    'OriginCity', 'DestinationCity', 'OriginAirportId', 'DestinationAirportId', 
    'OriginAirportCode', 'DestinationAirportCode', 'RouteDistanceInMiles', 'PassengerCount', 
    'AverageFare', 'LargestCarrierCode', 'LargestCarrierMarketShare', 'LargestCarrierAverageFare', 
    'LowestFareCarrierCode', 'LowestFareMarketShare', 'LowestFare', 
    'OriginCityCoordinates', 'DestinationCityCoordinates', 'Route'
]

# Create a list to hold rows for the table
table_data = []

# Loop through each specified column and calculate required statistics
for column in columns_to_check:
    if column in df.columns:
        total_count = df[column].count()
        unique_count = df[column].nunique()
        table_data.append([column, total_count, unique_count])
    else:
        table_data.append([column, "Not found", "Not found"])

# Print the table using tabulate
print(tabulate(table_data, headers=["Column Name", "Total Count", "Unique Count"], tablefmt="grid"))

###########################################################################################################

# Combine specified pairs of columns and find unique values
unique_cities = pd.concat([df['OriginCity'], df['DestinationCity']]).unique()
unique_airports = pd.concat([df['OriginAirportCode'], df['DestinationAirportCode']]).unique()
unique_city_market_ids = pd.concat([df['OriginCityMarketId'], df['DestinationCityMarketId']]).unique()
unique_airport_ids = pd.concat([df['OriginAirportId'], df['DestinationAirportId']]).unique()
unique_carrier_codes = pd.concat([df['LargestCarrierCode'], df['LowestFareCarrierCode']]).unique()
unique_routes = df['Route'].unique()

# Count of unique values
table_data = [
    ["Unique Cities", len(unique_cities), unique_cities],
    ["Unique Airports", len(unique_airports), unique_airports],
    ["Unique City Market IDs", len(unique_city_market_ids), unique_city_market_ids],
    ["Unique Airport IDs", len(unique_airport_ids), unique_airport_ids],
    ["Unique Carrier Codes", len(unique_carrier_codes), unique_carrier_codes],
    ["Unique Routes", len(unique_routes), unique_routes]
]

# Print the results in a table
print(tabulate(table_data, headers=["Description", "Unique Count", "Unique Values (Sample)"], tablefmt="grid"))

###########################################################################################################

# Calculate the total passenger count
total_passenger_count = df['PassengerCount'].sum()

# Print the result
print(f"Total Passenger Count: {total_passenger_count}")

###########################################################################################################

# Aggregate PassengerCount by Year and sort by Year
passenger_count_by_year = df.groupby('Year')['PassengerCount'].sum().reset_index()
passenger_count_by_year = passenger_count_by_year.sort_values(by='Year')

# Calculate the total passenger count
total_passenger_count = passenger_count_by_year['PassengerCount'].sum()

# Add a row for the total passenger count using pd.concat
total_row = pd.DataFrame({'Year': ['Total'], 'PassengerCount': [total_passenger_count]})
passenger_count_by_year = pd.concat([passenger_count_by_year, total_row], ignore_index=True)

# Format PassengerCount column to avoid scientific notation and add commas
passenger_count_by_year['PassengerCount'] = passenger_count_by_year['PassengerCount'].apply(lambda x: f"{x:,.0f}")

# Print the result in a tabular format
print(tabulate(passenger_count_by_year, headers=["Year", "Total Passenger Count"], tablefmt="grid"))

###########################################################################################################

# Aggregate PassengerCount by DestinationCity and find the top 10 cities by arrivals
top_arrival_cities = df.groupby('DestinationCity')['PassengerCount'].sum().reset_index()
top_arrival_cities = top_arrival_cities.sort_values(by='PassengerCount', ascending=False).head(10)

# Print the result in tabular format
print("Top 10 Cities by Arrivals (Passenger Count):")
print(tabulate(top_arrival_cities, headers=["City", "Total Passenger Count"], tablefmt="grid"))

###########################################################################################################

# Aggregate PassengerCount by OriginCity and find the top 10 cities by departures
top_departure_cities = df.groupby('OriginCity')['PassengerCount'].sum().reset_index()
top_departure_cities = top_departure_cities.sort_values(by='PassengerCount', ascending=False).head(10)

# Print the result in tabular format
print("Top 10 Cities by Departures (Passenger Count):")
print(tabulate(top_departure_cities, headers=["City", "Total Passenger Count"], tablefmt="grid"))

###########################################################################################################

# Aggregate PassengerCount by DestinationAirportCode and find the top 10 airports by arrivals
top_arrival_airports = df.groupby('DestinationAirportCode')['PassengerCount'].sum().reset_index()
top_arrival_airports = top_arrival_airports.sort_values(by='PassengerCount', ascending=False).head(10)

# Print the result in tabular format
print("Top 10 Airports by Arrivals (Passenger Count):")
print(tabulate(top_arrival_airports, headers=["Airport Code", "Total Passenger Count"], tablefmt="grid"))

###########################################################################################################

# Aggregate PassengerCount by OriginAirportCode and find the top 10 airports by departures
top_departure_airports = df.groupby('OriginAirportCode')['PassengerCount'].sum().reset_index()
top_departure_airports = top_departure_airports.sort_values(by='PassengerCount', ascending=False).head(10)

# Print the result in tabular format
print("Top 10 Airports by Departures (Passenger Count):")
print(tabulate(top_departure_airports, headers=["Airport Code", "Total Passenger Count"], tablefmt="grid"))

###########################################################################################################

# Aggregate PassengerCount by Route and find the top 10 routes by passenger count
top_routes = df.groupby('Route')['PassengerCount'].sum().reset_index()
top_routes = top_routes.sort_values(by='PassengerCount', ascending=False).head(10)

# Print the result in tabular format
print("Top 10 Routes by Passenger Count:")
print(tabulate(top_routes, headers=["Route", "Total Passenger Count"], tablefmt="grid"))

###########################################################################################################

# Remove duplicate entries for each route, keeping only the first occurrence
unique_routes_df = df.drop_duplicates(subset=['Route'])

# Sort by RouteDistanceInMiles in descending order and get the top 10 longest routes
top_longest_routes = unique_routes_df.sort_values(by='RouteDistanceInMiles', ascending=False).head(10)

# Select only the relevant columns for display
top_longest_routes = top_longest_routes[['Route', 'RouteDistanceInMiles']]

# Print the result in tabular format
print("Top 10 Longest Routes by Distance (in Miles):")
print(tabulate(top_longest_routes, headers=["Route", "Route Distance (Miles)"], tablefmt="grid"))

###########################################################################################################

# Sort by RouteDistanceInMiles in ascending order and get the top 10 shortest routes
top_shortest_routes = unique_routes_df.sort_values(by='RouteDistanceInMiles').head(10)

# Select only the relevant columns for display
top_shortest_routes = top_shortest_routes[['Route', 'RouteDistanceInMiles']]

# Print the result in tabular format
print("Top 10 Shortest Routes by Distance (in Miles):")
print(tabulate(top_shortest_routes, headers=["Route", "Route Distance (Miles)"], tablefmt="grid"))

###########################################################################################################

