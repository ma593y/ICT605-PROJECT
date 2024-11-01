import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load the preprocessed dataset
df = pd.read_parquet('datasets/_dataset.parquet')  # Adjust path if needed

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Data Analysis Dashboard"

# Layout for the Homepage
home_layout = html.Div([
    html.H1("Welcome to the US Airline Data Analysis Dashboard", className="text-center my-4", style={"color": "#1d3557"}),
    
    dbc.Container([
        # Introduction Section
        html.H2("Introduction", className="my-3", style={"color": "#457b9d"}),
        html.P(
            "The airline industry is influenced by numerous factors such as fares, passenger volumes, and routes, which play a crucial role in determining business performance and customer satisfaction. "
            "This dashboard explores key metrics from 1993 to 2024, aiming to enhance data-driven decision-making for stakeholders."
        ),
        
        # Problem Definition Section
        html.H2("Problem Definition", className="my-3", style={"color": "#457b9d"}),
        html.P(
            "The core problem centers on identifying patterns in U.S. domestic air travel to support strategic actions. By visualizing trends, routes, and fare dynamics, the dashboard will facilitate "
            "informed decisions in pricing and route optimization, ultimately improving competitiveness and operational efficiency."
        ),

        # Goal Section
        html.H2("Goal", className="my-3", style={"color": "#457b9d"}),
        html.P(
            "Our primary goal is to use interactive data visualization to provide insights into fare trends, route demands, and passenger behavior. This dashboard will help users validate hypotheses, "
            "analyze patterns, and engage with the data for better strategic planning."
        ),

        # Narrative Section
        html.H2("Narrative / Storyboard", className="my-3", style={"color": "#457b9d"}),
        html.P(
            "The dashboard guides users through a comprehensive analysis journey. Beginning with an overview, it explores travel trends, busy routes, fare patterns, and seasonal variations. Key events, "
            "such as the 2008 recession and COVID-19, are highlighted to show their impacts on air travel trends, leading to a final summary of actionable insights."
        ),

        # Target Audience
        html.H2("Target Audience", className="my-3", style={"color": "#457b9d"}),
        html.P(
            "This system is designed for data analysts, business stakeholders, and industry strategists who aim to understand domestic airline performance trends, optimize pricing strategies, "
            "and make data-informed decisions in the U.S. airline market."
        ),

        # Dataset Summary
        html.H2("Dataset Summary", className="my-3", style={"color": "#457b9d"}),
        html.P(
            "The dataset comprises over 244,000 records with fields on cities, airports, routes, distances, fare averages, and more, spanning 1993 to 2024. Data cleaning reduced irrelevant fields, "
            "ensuring accurate insights into market share, fare dynamics, and passenger trends."
        ),

        # Analysis Summary
        html.H2("Analysis Summary", className="my-3", style={"color": "#457b9d"}),
        html.P(
            "Key analyses included: descriptive statistics, trend analysis (examining yearly, seasonal, and event-driven trends), comparative analysis of fares by route and carrier, and "
            "regional analysis ranking the busiest airports, cities, and routes."
        ),

        # Hypothesis Section
        html.H2("Hypotheses", className="my-3", style={"color": "#457b9d"}),
        html.Ul([
            html.Li("Fare-Distance Relationship: Fares tend to increase with route distance, though pricing strategies vary by carrier."),
            html.Li("Seasonal Demand Effects: Passenger volume and fare pricing are higher in summer and autumn, with dips in winter."),
            html.Li("Competitive Influence on Fares: Routes with more carriers show unexpected fare increases, potentially due to high demand or premium services."),
        ]),

        # FAQs / Help Section
        html.H2("FAQs / Help", className="my-3", style={"color": "#457b9d"}),
        html.P(
            "For questions, refer to our FAQ section for guidance and troubleshooting tips."
        ),
    ]),
])

########################################################################################

import dash_daq as daq

# Load the data
df_graphs = pd.read_parquet("datasets/_dataset_graphs.parquet")

# Split 'Geocoded_City1' into 'start_lat' and 'start_lon'
df_graphs[["start_lat", "start_lon"]] = df_graphs["Geocoded_City1"].str.split(", ", expand=True)

# Split 'Geocoded_City2' into 'end_lat' and 'end_lon'
df_graphs[["end_lat", "end_lon"]] = df_graphs["Geocoded_City2"].str.split(", ", expand=True)

# Convert the latitude and longitude columns to numeric
df_graphs["start_lat"] = pd.to_numeric(df_graphs["start_lat"])
df_graphs["start_lon"] = pd.to_numeric(df_graphs["start_lon"])
df_graphs["end_lat"] = pd.to_numeric(df_graphs["end_lat"])
df_graphs["end_lon"] = pd.to_numeric(df_graphs["end_lon"])


# Remove "Metropolitan Area" from city names
def remove_metropolitan(route):
    return route.replace("(Metropolitan Area)", "").strip()

df_graphs["city1"] = df_graphs["city1"].apply(remove_metropolitan)
df_graphs["city2"] = df_graphs["city2"].apply(remove_metropolitan)

# Create a new column for the route to make selection easier
df_graphs["route"] = df_graphs["city1"] + " - " + df_graphs["city2"]

# Define the layout of the app
graphs_layout = html.Div(
    [
        html.H1("US Airline Dashboard", id="header"),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        id="year-dropdown",
                        options=sorted(
                            [
                                {"label": year, "value": year}
                                for year in df_graphs["Year"].unique()
                            ],
                            key=lambda x: x["value"],
                        ),
                        placeholder="Select a year",
                        multi=True,
                    ),
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "margin-right": "2%",
                        "vertical-align": "top",
                    },
                ),
                html.Div(
                    dcc.Dropdown(
                        id="source-city-dropdown",
                        options=sorted(
                            [
                                {"label": source, "value": source}
                                for source in df_graphs["city1"].unique()
                            ],
                            key=lambda x: x["label"],
                        ),
                        placeholder="Select a source city",
                        multi=True,
                    ),
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "margin-right": "2%",
                        "vertical-align": "top",
                    },
                ),
                html.Div(
                    dcc.Dropdown(
                        id="destination-city-dropdown",
                        options=sorted(
                            [
                                {"label": destination, "value": destination}
                                for destination in df_graphs["city2"].unique()
                            ],
                            key=lambda x: x["label"],
                        ),
                        placeholder="Select a destination city",
                        multi=True,
                    ),
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flex-wrap": "wrap",
                "bgcolor": "rgba(150, 150, 150, 0.5)",
            },
        ),
        html.Br(),
        # Div for Route Map and Box Plot
        html.Div(
            [
                # Dive For Route Map & Dropdown
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    # Text for the button
                                    "Source City & Routes   ",
                                ),
                                # Button for source city
                                daq.BooleanSwitch(
                                    id="source-dest-btn",
                                    on=False,
                                ),
                                html.Div(
                                    # Text for the button
                                    "   Destination City",
                                ),
                            ],
                            style={
                                "width": "100%",
                                "height": "33px",
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                                "border": "1px solid #D3D3D3",  # Border color and thickness
                                "border-radius": "4px",  # Rounded corners
                                "font-color": "lightgrey",
                            },
                        ),
                        html.Br(),
                        dcc.Graph(
                            id="route-map", style={"height": "70vh", "width": "100%"}
                        ),
                    ],
                    style={
                        "width": "49%",
                        "display": "inline-block",
                        "margin-right": "2%",
                        "vertical-align": "top",
                    },
                ),
                # Dive For Box Plot & Dropdown
                html.Div(
                    [
                        # Dropdown for Box Plot selection
                        html.Div(
                            dcc.Dropdown(
                                id="route-dropdown",
                                options=[
                                    {"label": route, "value": route}
                                    for route in df_graphs["route"].unique()
                                ],
                                placeholder="Select routes for box plot",
                                multi=True,
                            ),
                            style={
                                "width": "100%",
                            },
                        ),
                        html.Br(),
                        # Box Plot
                        dcc.Graph(
                            id="box-plot", style={"height": "70vh", "width": "100%"}
                        ),
                    ],
                    style={
                        "width": "49%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
            ],
        ),
        html.Br(),
        # Div for Sankey Diagram
        html.Div(
            [
                html.Div(
                    [
                        # Dropdown for plot options
                        html.Label("Select Plot Type:"),
                        dcc.RadioItems(
                            id="sankey-selector",
                            options=[
                                {"label": "Passengers", "value": "psg"},
                                {"label": "Fare (Carrier Large)", "value": "fare_lg"},
                                {"label": "Fare (Carrier Low)", "value": "fare_low"},
                            ],
                            value="psg",  # Default option
                            inline=True,
                        ),
                    ],
                    style={
                        "width": "100%",
                        "height": "33px",
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                        "border": "1px solid #D3D3D3",  # Border color and thickness
                        "border-radius": "4px",  # Rounded corners
                        "font-color": "lightgrey",
                    },
                ),
                html.Br(),
                dcc.Graph(id="sankey-di", style={"height": "70vh", "width": "100%"}),
            ]
        ),
    ],
)

# Define the callback
@app.callback(
    # Outputs
    Output("route-map", "figure"),
    Output("box-plot", "figure"),
    Output("sankey-di", "figure"),
    # Inputs
    Input("year-dropdown", "value"),
    Input("source-city-dropdown", "value"),
    Input("destination-city-dropdown", "value"),
    Input("source-dest-btn", "on"),
    Input("route-dropdown", "value"),
    Input("sankey-selector", "value"),
)
def update_graph(
    year_selected,
    source_city_selected,
    destination_city_selected,
    is_dest,
    selected_routes,
    sankey_selector,
):

    # Default selections for filters
    if year_selected is None or len(year_selected) == 0:
        year_selected = df_graphs["Year"].unique()
    if source_city_selected is None or len(source_city_selected) == 0:
        source_city_selected = df_graphs["city1"].unique()
    if destination_city_selected is None or len(destination_city_selected) == 0:
        destination_city_selected = df_graphs["city2"].unique()

    # Filter the data
    df_graphs_year = df_graphs[
        df_graphs["Year"].isin(year_selected)
        & df_graphs["city1"].isin(source_city_selected)
        & df_graphs["city2"].isin(destination_city_selected)
    ]

    # Group data by city and aggregate necessary fields
    df_graphs_source = (
        df_graphs_year.groupby(["city1", "start_lat", "start_lon"])
        .agg(
            {
                "passengers": "mean",
                "airport_1": "first",
            }
        )
        .reset_index()
    )

    # Count the number of flights
    source_flight_count = df_graphs_year["city1"].value_counts().reset_index()
    source_flight_count.columns = ["city1", "flight_count"]

    # Merge the flight count back to the aggregated data
    df_graphs_source = df_graphs_source.merge(source_flight_count, on="city1", how="left")
    df_graphs_source["hover_text"] = (
        "From: "
        + df_graphs_source["city1"]
        + "<br>Total Flights: "
        + df_graphs_source["flight_count"].astype(str)
        + "<br>Avg. Passengers: "
        + df_graphs_source["passengers"].round().astype(str)
        + "<br>Airport: "
        + df_graphs_source["airport_1"]
    )

    df_graphs_dest = (
        df_graphs_year.groupby(["city2", "end_lat", "end_lon"])
        .agg(
            {
                "passengers": "mean",
                "airport_2": "first",
            }
        )
        .reset_index()
    )

    dest_flight_count = df_graphs_year["city2"].value_counts().reset_index()
    dest_flight_count.columns = ["city2", "flight_count"]

    df_graphs_dest = df_graphs_dest.merge(dest_flight_count, on="city2", how="left")

    df_graphs_dest["hover_text"] = (
        "To: "
        + df_graphs_dest["city2"]
        + "<br>Total Flights: "
        + df_graphs_dest["flight_count"].astype(str)
        + "<br>Avg. Passengers: "
        + df_graphs_dest["passengers"].round().astype(str)
        + "<br>Airport: "
        + df_graphs_dest["airport_2"]
    )

    unique_source_cities = df_graphs_source["city1"].unique()
    unique_dest_cities = df_graphs_dest["city2"].unique()
    color_scale = px.colors.qualitative.Plotly
    source_city_colors = {
        city: color_scale[i % len(color_scale)]
        for i, city in enumerate(unique_source_cities)
    }
    dest_city_colors = {
        city: color_scale[i % len(color_scale)]
        for i, city in enumerate(unique_dest_cities)
    }

    # Map figure
    map_fig = go.Figure()

    if is_dest:
        map_fig.add_trace(
            go.Scattergeo(
                locationmode="USA-states",
                lon=df_graphs_dest["end_lon"],
                lat=df_graphs_dest["end_lat"],
                hoverinfo="text",
                text=df_graphs_dest["hover_text"],
                mode="markers",
                marker=dict(
                    size=df_graphs_dest["flight_count"],
                    sizemode="area",
                    sizeref=2.0 * max(df_graphs_dest["flight_count"]) / (25.0**2),
                    color="rgba(0, 0, 0, 0)",  # Transparent fill color
                    line=dict(
                        color=[dest_city_colors[city] for city in df_graphs_dest["city2"]],
                        width=2,  # Set the width of the circle outline
                    ),
                ),
            )
        )
    else:
        map_fig.add_trace(
            go.Scattergeo(
                locationmode="USA-states",
                lon=df_graphs_source["start_lon"],
                lat=df_graphs_source["start_lat"],
                hoverinfo="text",
                text=df_graphs_source["hover_text"],
                mode="markers",
                marker=dict(
                    size=df_graphs_source["flight_count"],
                    sizemode="area",
                    sizeref=2.0 * max(df_graphs_source["flight_count"]) / (25.0**2),
                    color=[source_city_colors[city] for city in df_graphs_source["city1"]],
                ),
            )
        )

        for i, row in df_graphs_year.iterrows():
            map_fig.add_trace(
                go.Scattergeo(
                    locationmode="USA-states",
                    lon=[row["start_lon"], row["end_lon"], None],
                    lat=[row["start_lat"], row["end_lat"], None],
                    mode="lines",
                    line=dict(width=1, color=source_city_colors[row["city1"]]),
                    opacity=0.5,
                )
            )

    map_fig.update_layout(
        title={
            "text": "Routes Map",
            "y": 0.95,  # Adjust y-position slightly (range from 0 to 1, where 1 is the top of the plot area)
            "x": 0.5,  # Center title horizontally
            "xanchor": "center",
            "yanchor": "top",
        },
        showlegend=False,
        geo=go.layout.Geo(
            scope="north america",
            # projection_type="azimuthal equal area",
            showland=True,
            landcolor="rgb(30, 30, 30)",
            countrycolor="rgb(60, 60, 60)",
            lakecolor="rgb(40, 40, 40)",
            bgcolor="rgb(20, 20, 20)",
            lonaxis=dict(range=[-130, -60]),
            lataxis=dict(range=[20, 55]),
        ),
        paper_bgcolor="rgba(150, 150, 150, 0.5)",
        font=dict(color="black"),
        margin=dict(l=0, r=0, t=0, b=0),  # Removes extra margins
    )

    # Box Plot
    if selected_routes is None or len(selected_routes) == 0:
        selected_routes = (
            df_graphs_year.groupby("route")["fare"].mean().nlargest(3).index.tolist()
        )  # Default to top 3 if none selected
        filtered_data = df_graphs_year[df_graphs_year["route"].isin(selected_routes)].copy()
        box_title = "Fare Distribution of Top Route(s)"
    else:
        filtered_data = df_graphs[df_graphs["route"].isin(selected_routes)].copy()
        box_title = "Fare Distribution by Selected Routes"

    box_plot_fig = px.box(
        filtered_data,
        x="route",
        y="fare",
        color="route",
        title=box_title,
    )
    box_plot_fig.update_layout(
        yaxis_title="Fare ($)",
        paper_bgcolor="rgba(150, 150, 150, 0.5)",
        font=dict(
            color="black",
        ),
        legend=dict(
            title="Route(s)",
            orientation="h",
            x=0.5,
            y=-0.1,
            xanchor="center",
            yanchor="middle",
        ),
        xaxis=dict(
            title=None,
            showticklabels=False,
        ),
        margin=dict(r=20),
    ),

    ## Sankey Diagram

    # Map city names to indices
    all_cities = list(set(df_graphs_year["city1"]).union(set(df_graphs_year["city2"])))
    city_to_index = {city: i for i, city in enumerate(all_cities)}

    # Assign colors to each city from the color_scale
    node_colors = {
        city: color_scale[i % len(color_scale)] for i, city in enumerate(all_cities)
    }

    # Set link colors to match source node colors
    link_colors = [node_colors[df_graphs_year["city1"].iloc[i]] for i in range(len(df_graphs_year))]

    # Define nodes and links for Sankey diagram
    node_labels = all_cities  # Labels for the Sankey nodes (unique cities)

    # Convert DataFrame into sources, targets, and values for the Sankey plot
    sources = [city_to_index[city] for city in df_graphs_year["city1"]]
    targets = [city_to_index[city] for city in df_graphs_year["city2"]]
    
    if sankey_selector == "psg":
        values = df_graphs_year["passengers"].tolist()
        sankey_title = "Passenger Flow Between Cities"
    elif sankey_selector == "fare_lg":
        values = df_graphs_year["fare_lg"].tolist()
        sankey_title = "Fare (Large Carrier) Flow Between Cities"
    elif sankey_selector == "fare_low":
        values = df_graphs_year["fare_low"].value_counts().tolist()
        sankey_title = "Fare (Large Carrier) Flow Between Cities"
    else:
        values = df_graphs_year["passengers"].tolist()
        sankey_title = "Passenger Flow Between Cities"

    # Define a label for the hover text based on the sankey_selector
    hover_label = {
        "psg": "Passengers",
        "fare_lg": "Fare (Large Carrier)",
        "fare_low": "Fare (Low Carrier)",
    }.get(sankey_selector, "Passengers")  # Default to "Passengers" if no match



    # Create Sankey figure
    sankey_fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=node_labels,  # City names
                    color=[node_colors[city] for city in node_labels],  # Node colors
                ),
                link=dict(
                    source=sources,  # Indices of source cities
                    target=targets,  # Indices of target cities
                    value=values,  # Number of passengers
                    color=link_colors,  # Color of the links
                    hovertemplate="From: %{source.label}<br />"
                    +"To: %{target.label}<br />"
                    + "{hover_label}: %{value}<br />"
                ),
            )
        ]
    )

    sankey_fig.update_layout(
        title_text=sankey_title,
        font_size=12,
    )

    return map_fig, box_plot_fig, sankey_fig


########################################################################################

# Calculate unique counts and titles dynamically
unique_counts = {
    "Unique Year Count": df['Year'].nunique(),
    "Unique Quarter Count": df['Quarter'].nunique(),
    "Unique Cities Count": len(pd.concat([df['OriginCity'], df['DestinationCity']]).unique()),
    "Unique OriginCity Count": df['OriginCity'].nunique(),
    "Unique DestinationCity Count": df['DestinationCity'].nunique(),
    "Unique Airports Count": len(pd.concat([df['OriginAirportCode'], df['DestinationAirportCode']]).unique()),
    "Unique OriginAirportCode Count": df['OriginAirportCode'].nunique(),
    "Unique DestinationAirportCode Count": df['DestinationAirportCode'].nunique(),
    "Unique Carrier Codes Count": len(pd.concat([df['LargestCarrierCode'], df['LowestFareCarrierCode']]).unique()),
    "Unique LargestCarrierCode Count": df['LargestCarrierCode'].nunique(),
    "Unique LowestFareCarrierCode Count": df['LowestFareCarrierCode'].nunique(),
    "Unique Routes Count": df['Route'].nunique(),
    "Total Records Count": len(df),
    "Total Passenger Count": df['PassengerCount'].sum()
}

# Helper function to create an indicator graph with responsive height
def create_indicator(value, title):
    fig = go.Figure(go.Indicator(
        mode="number",
        value=value,
        title={'text': title}
    ))

    # Set margins to zero to avoid extra spacing
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig

# Helper function to create a card for each indicator with fixed height
def create_card(title, value):
    return dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                figure=create_indicator(value, title),
                config={'displayModeBar': False},
                style={"height": "100%", "width": "100%"}  # Ensures graph fills the card body
            )
        ]),
        className="shadow-sm mb-4",
        style={"height": "200px"}  # Fixed height for the card
    )

# Dynamic Data Summary Layout
data_summary_layout = dbc.Container([
    html.H1("Data Summary", className="text-center my-4", style={"color": "#1d3557"}),

    # Generate cards for each unique count dynamically
    dbc.Row(
        [
            dbc.Col(create_card(title, value), md=4)
            for title, value in unique_counts.items()
        ],
        className="mb-4"
    )
], fluid=True)

# Helper function to generate top 10 graphs
def generate_top_10_figures():
    figures = []

    # Top 10 Cities by Arrivals
    top_arrival_cities = df.groupby('DestinationCity')['PassengerCount'].sum().reset_index()
    top_arrival_cities = top_arrival_cities.sort_values(by='PassengerCount').tail(10)
    fig5 = px.bar(top_arrival_cities, x='PassengerCount', y='DestinationCity', orientation='h',
                  title="Top 10 Busiest Cities by Arrivals (Passenger Count)",
                  color='PassengerCount', color_continuous_scale='Blues')
    fig5.update_layout(title_font_size=20, xaxis_title="Passenger Count", yaxis_title="City")
    figures.append(fig5)

    # Top 10 Cities by Departures
    top_departure_cities = df.groupby('OriginCity')['PassengerCount'].sum().reset_index()
    top_departure_cities = top_departure_cities.sort_values(by='PassengerCount').tail(10)
    fig6 = px.bar(top_departure_cities, x='PassengerCount', y='OriginCity', orientation='h',
                  title="Top 10 Busiest Cities by Departures (Passenger Count)",
                  color='PassengerCount', color_continuous_scale='Oranges')
    fig6.update_layout(title_font_size=20, xaxis_title="Passenger Count", yaxis_title="City")
    figures.append(fig6)

    # Top 10 Airports by Arrivals
    top_arrival_airports = df.groupby('DestinationAirportCode')['PassengerCount'].sum().reset_index()
    top_arrival_airports = top_arrival_airports.sort_values(by='PassengerCount').tail(10)
    fig7 = px.bar(top_arrival_airports, x='PassengerCount', y='DestinationAirportCode', orientation='h',
                  title="Top 10 Busiest Airports by Arrivals (Passenger Count)",
                  color='PassengerCount', color_continuous_scale='Blues')
    fig7.update_layout(title_font_size=20, xaxis_title="Passenger Count", yaxis_title="Airport Code")
    figures.append(fig7)

    # Top 10 Airports by Departures
    top_departure_airports = df.groupby('OriginAirportCode')['PassengerCount'].sum().reset_index()
    top_departure_airports = top_departure_airports.sort_values(by='PassengerCount').tail(10)
    fig8 = px.bar(top_departure_airports, x='PassengerCount', y='OriginAirportCode', orientation='h',
                  title="Top 10 Busiest Airports by Departures (Passenger Count)",
                  color='PassengerCount', color_continuous_scale='Oranges')
    fig8.update_layout(title_font_size=20, xaxis_title="Passenger Count", yaxis_title="Airport Code")
    figures.append(fig8)

    # Top 10 Routes by Passenger Count
    top_routes = df.groupby('Route')['PassengerCount'].sum().reset_index()
    top_routes = top_routes.sort_values(by='PassengerCount').tail(10)
    fig9 = px.bar(top_routes, x='PassengerCount', y='Route', orientation='h',
                  title="Top 10 Busiest Routes by Passenger Count",
                  color='PassengerCount', color_continuous_scale='Blues')
    fig9.update_layout(title_font_size=20, xaxis_title="Passenger Count", yaxis_title="Route")
    figures.append(fig9)

    # Top 10 Longest Routes
    unique_routes_df = df.drop_duplicates(subset=['Route'])
    top_longest_routes = unique_routes_df.sort_values(by='RouteDistanceInMiles').tail(10)
    fig10 = px.bar(top_longest_routes, x='RouteDistanceInMiles', y='Route', orientation='h',
                   title="Top 10 Longest Routes by Distance (Miles)", color_discrete_sequence=['teal'])
    fig10.update_layout(title_font_size=20, xaxis_title="Route Distance (Miles)", yaxis_title="Route")
    figures.append(fig10)

    # Top 10 Shortest Routes
    top_shortest_routes = unique_routes_df.sort_values(by='RouteDistanceInMiles').head(10)
    fig11 = px.bar(top_shortest_routes, x='RouteDistanceInMiles', y='Route', orientation='h',
                   title="Top 10 Shortest Routes by Distance (Miles)", color_discrete_sequence=['salmon'])
    fig11.update_layout(title_font_size=20, xaxis_title="Route Distance (Miles)", yaxis_title="Route")
    figures.append(fig11)

    return figures

# Generate the figures for top 10 graphs
top_10_figures = generate_top_10_figures()

# Layout for Top 10 Graphs Page
top_10_layout = html.Div([
    html.H1("Top 10 Data Visualizations", className="text-center my-4", style={"color": "#1d3557"}),

    dbc.Container([
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=fig), html.Hr(style={"border-top": "5px solid #ddd"})], md=12) for fig in top_10_figures
            ],
            className="g-4"
        )
    ])
])

# Trend Graph Definitions
def create_trend_figures(df):
    figures = []

    # Passenger Count by Year with Average Line
    passenger_count_by_year = df.groupby('Year')['PassengerCount'].sum().reset_index()
    average_count = passenger_count_by_year['PassengerCount'].mean()
    fig1 = px.line(passenger_count_by_year, x='Year', y='PassengerCount', title="Passengers Trend Over Years")
    fig1.update_traces(mode='lines+markers', line=dict(color='gray'))
    fig1.add_shape(type="line", x0=passenger_count_by_year['Year'].min(), x1=passenger_count_by_year['Year'].max(),
                   y0=average_count, y1=average_count, line=dict(dash="dash", color="red"))
    fig1.add_annotation(x=passenger_count_by_year['Year'].max(), y=average_count, text=f"Avg: {average_count:.0f}", showarrow=False)
    fig1.update_layout(title_font_size=20, xaxis_title="Year", yaxis_title="Passenger Count (Log Scale)", yaxis_type="log")
    figures.append(fig1)

    # Passenger Count Trends by Distance Category
    df['DistanceCategory'] = pd.cut(df['RouteDistanceInMiles'], bins=[0, 500, 1500, 3000], labels=['Short', 'Medium', 'Long'])
    trend_data = df.groupby(['Year', 'DistanceCategory'])['PassengerCount'].sum().reset_index()
    distance_colors = {"Short": "dodgerblue", "Medium": "orange", "Long": "green"}
    fig2 = px.line(trend_data, x='Year', y='PassengerCount', color='DistanceCategory',
                   title="Passenger Count Trends by Route Distance Category Over Time",
                   line_shape='spline', markers=True, color_discrete_map=distance_colors)
    figures.append(fig2)

    # Yearly Trend of Passenger Count with Annotations
    passenger_trend = df.groupby('Year')['PassengerCount'].sum().reset_index()
    fig3 = px.line(passenger_trend, x='Year', y='PassengerCount', title="Yearly Trend of Passenger Count",
                   line_shape='spline', markers=True)
    peak_year = passenger_trend.loc[passenger_trend['PassengerCount'].idxmax()]
    low_year = passenger_trend.loc[passenger_trend['PassengerCount'].idxmin()]
    fig3.add_annotation(x=peak_year['Year'], y=peak_year['PassengerCount'], text="Peak", showarrow=True, arrowhead=2)
    fig3.add_annotation(x=low_year['Year'], y=low_year['PassengerCount'], text="Lowest", showarrow=True, arrowhead=2)
    figures.append(fig3)

    # Yearly Trend of Average Fare with Annotations
    fare_trend = df.groupby('Year')['AverageFare'].mean().reset_index()
    fig4 = px.line(fare_trend, x='Year', y='AverageFare', title="Yearly Trend of Average Fare",
                   line_shape='spline', markers=True, color_discrete_sequence=['indianred'])
    peak_fare = fare_trend.loc[fare_trend['AverageFare'].idxmax()]
    low_fare = fare_trend.loc[fare_trend['AverageFare'].idxmin()]
    fig4.add_annotation(x=peak_fare['Year'], y=peak_fare['AverageFare'], text="Highest Fare", showarrow=True, arrowhead=2)
    fig4.add_annotation(x=low_fare['Year'], y=low_fare['AverageFare'], text="Lowest Fare", showarrow=True, arrowhead=2)
    figures.append(fig4)

    # Passenger Count Trends by Quarter
    quarterly_trends = df.groupby(['Year', 'Quarter']).agg({'PassengerCount': 'sum', 'AverageFare': 'mean'}).reset_index()
    quarterly_trends['Quarter'] = "Q" + quarterly_trends['Quarter'].astype(str)
    quarter_colors = {"Q1": "royalblue", "Q2": "orange", "Q3": "green", "Q4": "red"}
    fig5 = px.line(quarterly_trends, x='Year', y='PassengerCount', color='Quarter',
                   title="Passenger Count Trends by Quarter Over Time",
                   color_discrete_map=quarter_colors, line_shape="linear")
    figures.append(fig5)

    # Average Fare Trends by Quarter
    fig6 = px.line(quarterly_trends, x='Year', y='AverageFare', color='Quarter',
                   title="Average Fare Trends by Quarter Over Time",
                   color_discrete_map=quarter_colors, line_shape="linear")
    figures.append(fig6)

    return figures

# Generate trend figures
trend_figures = create_trend_figures(df)

# Layout for Trend Analysis Page
trend_layout = html.Div([
    html.H1("Trend Analysis", className="text-center my-4", style={"color": "#1d3557"}),

    dbc.Container([
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=fig), html.Hr(style={"border-top": "5px solid #ddd"})], md=12) for fig in trend_figures
            ],
            className="g-4"
        )
    ])
])

# App Layout with Navigation
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    
    # Navbar with links to Home, Graphs, and Data Summary
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Data Summary", href="/data-summary")),
            dbc.NavItem(dbc.NavLink("Top 10 Graphs", href="/top-10")),
            dbc.NavItem(dbc.NavLink("Trend Analysis", href="/trend-analysis")),
            dbc.NavItem(dbc.NavLink("Graphs", href="/graphs")),
        ],
        brand="Data Analysis Dashboard",
        brand_href="/",
        color="dark",
        dark=True,
        className="mb-4"
    ),
    
    # Content container that changes based on the URL
    html.Div(id="page-content")
])

# Callback to update page layout based on URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/graphs":
        return graphs_layout
    elif pathname == "/data-summary":
        return data_summary_layout
    elif pathname == "/top-10":
        return top_10_layout
    elif pathname == "/trend-analysis":
        return trend_layout
    else:
        return home_layout

# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
