import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

# Load the preprocessed dataset
df = pd.read_parquet('datasets/_dataset.parquet')  # Adjust path if needed

# Calculate unique counts for each metric
unique_count_year = df['Year'].nunique()
unique_count_quarter = df['Quarter'].nunique()
unique_cities_count = len(pd.concat([df['OriginCity'], df['DestinationCity']]).unique())
unique_count_origin_city = df['OriginCity'].nunique()
unique_count_dest_city = df['DestinationCity'].nunique()
unique_airports_count = len(pd.concat([df['OriginAirportCode'], df['DestinationAirportCode']]).unique())
unique_count_origin_airport_code = df['OriginAirportCode'].nunique()
unique_count_dest_airport_code = df['DestinationAirportCode'].nunique()
unique_carrier_codes_count = len(pd.concat([df['LargestCarrierCode'], df['LowestFareCarrierCode']]).unique())
unique_count_largest_carrier = df['LargestCarrierCode'].nunique()
unique_count_lowest_fare_carrier = df['LowestFareCarrierCode'].nunique()
unique_routes_count = df['Route'].nunique()

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Data Analysis Dashboard"

# Helper function to create an indicator
def create_indicator(value, title):
    return go.Figure(go.Indicator(
        mode="number",
        value=value,
        title={'text': title}
    ))

# Layout for the Homepage
home_layout = html.Div([
    html.H1("Welcome to the Data Analysis Dashboard", className="text-center my-4", style={"color": "#1d3557"}),
    
    dbc.Container([
        # Introduction Section
        html.H2("Introduction", className="my-3", style={"color": "#457b9d"}),
        html.P("This project provides a comprehensive analysis focused on [specific case]. The case revolves around understanding key metrics, trends, and insights within the data."),
        
        # Problem Definition Section
        html.H2("Problem Definition", className="my-3", style={"color": "#457b9d"}),
        html.P("The central problem is to uncover patterns and trends offering insights into [central theme]. This analysis provides actionable conclusions for decision-making."),

        # Goal Section
        html.H2("Goal", className="my-3", style={"color": "#457b9d"}),
        html.P("Our goal is to utilize data-driven methods to explore and validate hypotheses around the dataset, delivering clear and insightful visualizations."),

        # Narrative Section
        html.H2("Narrative / Storyboard", className="my-3", style={"color": "#457b9d"}),
        html.P("This dashboard narrates the story of the dataset, including patterns, findings, and insights. We start with general statistics, explore trends, and conclude with recommendations."),

        # Target Audience
        html.H2("Target Audience", className="my-3", style={"color": "#457b9d"}),
        html.P("This dashboard is tailored for data analysts, business decision-makers, and stakeholders looking to derive insights from [specific dataset]."),

        # Dataset Summary
        html.H2("Dataset Summary", className="my-3", style={"color": "#457b9d"}),
        html.P("The dataset contains information on [data description]. Key fields include [important columns], covering various dimensions and aggregates."),

        # Analysis Summary
        html.H2("Analysis Summary", className="my-3", style={"color": "#457b9d"}),
        html.P("Our data exploration included data cleaning, transformation, and outlier detection. Key findings reveal [summary of findings]."),

        # Hypothesis Section
        html.H2("Hypothesis", className="my-3", style={"color": "#457b9d"}),
        html.P("Our main hypothesis is that [hypothesis statement]. By analyzing [fields], we aim to validate or invalidate this hypothesis."),

        # FAQs / Help Section
        html.H2("FAQs / Help", className="my-3", style={"color": "#457b9d"}),
        html.P("For questions, refer to our FAQ section for guidance and troubleshooting tips."),
    ]),

    # Navigation Link to Graphs
    html.Div([
        dbc.Button("View Graphs", href="/graphs", color="primary", className="mr-2"),
    ], className="text-center my-4")
])

# Layout for Graphs Page
graphs_layout = html.Div([
    html.H1("Data Visualizations", className="text-center my-4", style={"color": "#1d3557"}),
    
    # Example Graph 1
    html.Div([
        html.H3("Graph 1: Passenger Count Trends", style={"color": "#457b9d"}),
        dcc.Graph(id="graph-1", figure={}),  # Replace with actual figure
    ], className="my-4"),
    
    # Example Graph 2
    html.Div([
        html.H3("Graph 2: Average Fare Trends", style={"color": "#457b9d"}),
        dcc.Graph(id="graph-2", figure={}),  # Replace with actual figure
    ], className="my-4"),
])

# Layout for Data Summary Page
data_summary_layout = html.Div([
    html.H1("Data Summary", className="text-center my-4", style={"color": "#1d3557"}),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=create_indicator(unique_count_year, "Unique Year Count")), md=4),
        dbc.Col(dcc.Graph(figure=create_indicator(unique_count_quarter, "Unique Quarter Count")), md=4),
        dbc.Col(dcc.Graph(figure=create_indicator(unique_cities_count, "Unique Cities (combined OriginCity and DestinationCity)")), md=4),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=create_indicator(unique_count_origin_city, "Unique OriginCity Count")), md=4),
        dbc.Col(dcc.Graph(figure=create_indicator(unique_count_dest_city, "Unique DestinationCity Count")), md=4),
        dbc.Col(dcc.Graph(figure=create_indicator(unique_airports_count, "Unique Airports (combined OriginAirportCode and DestinationAirportCode)")), md=4),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=create_indicator(unique_count_origin_airport_code, "Unique OriginAirportCode Count")), md=4),
        dbc.Col(dcc.Graph(figure=create_indicator(unique_count_dest_airport_code, "Unique DestinationAirportCode Count")), md=4),
        dbc.Col(dcc.Graph(figure=create_indicator(unique_carrier_codes_count, "Unique Carrier Codes (combined LargestCarrierCode and LowestFareCarrierCode)")), md=4),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(figure=create_indicator(unique_count_largest_carrier, "Unique LargestCarrierCode Count")), md=4),
        dbc.Col(dcc.Graph(figure=create_indicator(unique_count_lowest_fare_carrier, "Unique LowestFareCarrierCode Count")), md=4),
        dbc.Col(dcc.Graph(figure=create_indicator(unique_routes_count, "Unique Routes Count")), md=4),
    ], className="mb-4"),
])

# App Layout with Navigation
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    
    # Navbar with links to Home, Graphs, and Data Summary
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Graphs", href="/graphs")),
            dbc.NavItem(dbc.NavLink("Data Summary", href="/data-summary")),
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
    else:
        return home_layout

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
