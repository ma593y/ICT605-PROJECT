# ICT605-PROJECT - Dash App

This project provides an interactive Data Analysis Dashboard that explores trends and patterns in U.S. domestic airline flight routes, fares, and passenger volumes from 1993 to 2024. Built using Dash and Plotly, the dashboard enables users to visualize and analyze essential metrics such as fare variations, route demand, and passenger behavior. By leveraging a robust dataset, this tool empowers stakeholders to derive actionable insights, validate hypotheses, and make data-driven decisions for pricing and route optimization in the airline industry.

Follow the instructions below to set up and run the application on your local machine.

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Running the App](#running-the-app)
4. [Folder Structure](#folder-structure)

## Requirements

- Python 3.7 or higher

## Installation

1. **Clone the repository:**

    ```bash
    git clone --branch submission https://github.com/ma593y/ICT605-PROJECT.git
    cd ICT605-PROJECT
    ```

2. **Set up a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    venv\Scripts\activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the App

1. **Start the Dash server:**

    ```bash
    python app.py
    ```

2. **Access the app in your web browser:**

    Open your browser and go to `http://127.0.0.1:8050`. The Dash app should now be accessible at this address.

## Folder Structure

- **app.py**: Main file to run the Dash app.
- **datasets/**: Contains data files used by the app.
- **files/**: Stores additional files related to the project.
- **requirements.txt**: Python dependencies for the project.
- **README.md**: Main documentation file.
