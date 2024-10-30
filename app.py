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
    app.run_server(debug=True)
