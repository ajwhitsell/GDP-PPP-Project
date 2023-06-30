import pandas as pd
from dash import dcc, dash, html, Input, Output 
import os
from dash_bootstrap_components import themes
import plotly.express as px


PATH = os.path.join(os.getcwd(), 'data/World_GDP_PC.csv')

data = pd.read_csv(PATH)
data = data[~data['Country Name'].isin(
    ['North America', 'Faroe Islands', 'Cayman Islands', 
     'Bermuda', 'Bahamas, The', 'demographic dividen', 
     'Isle of Man', 'Pre-demographic dividend'
     'Early-demographic dividend','Post-demographic dividend',
     'Channel Islands','Hong Kong SAR, China', 'Macao SAR, China'])]
data['Country Name'] = data['Country Name'].replace('Brunei Darussalam', 'Brunei')

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'background': 'linear-gradient(to bottom, #4169E1, #87CEEB)',  # Gradient from light blue to dark blue
        'height': '100vh',  # Set the height of the container to fill the viewport
        'padding': '20px'  # Add padding for better spacing
    },
    className="container",
    children=[
        html.Div(
            className="title-container",
            children=[
                html.H1('Top 10 GDP Per Capita (1961-2021)', style={'textAlign': 'center'})
            ], 
        ),
        html.Div(
            className="description-container",
            children=[
                html.P("Gross Domestic Product (GDP) is the monetary value of all finished goods and services made within a country during a specific period. GDP provides an economic snapshot of a country, used to estimate the size of an economy and growth rate.This dataset contains the GDP based on Purchasing Power Parity (PPP).", style={'textAlign': 'center'}),
                html.P("GDP comparisons using PPP are arguably more useful than those using nominal GDP when assessing a nation's domestic market because PPP takes into account the relative cost of local goods, services and inflation rates of the country, rather than using international market exchange rates which may distort the real differences in per capita income.", style={'textAlign': 'center'})
            ]
        ),
        html.Div(
            className="animated-chart",
            children=[
                dcc.Graph(
                    id='animated-gdp-graph',
                    config={'displayModeBar': False},  # Hide the plotly mode bar
                    ),
                dcc.Interval(
                    id='interval-component',
                    interval=500,  # Update the graph every .5 second
                    n_intervals=0
                )
            ]
        ),
        html.Div(
            className="dropdown-chart",
            children=[
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': col, 'value': col} for col in data.columns[5:-1]],  # Assuming the first column is country names
                    value=data.columns[-2],  # Assuming the initial value is the first year column
                    className="mb-3"
                ),
                dcc.Graph(
                    id='dropdown-gdp-graph',
                    config={'displayModeBar': False},  # Hide the plotly mode bar
                    ),
            ]
        )
    ]
)

@app.callback(
    Output('animated-gdp-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_animated_graph(n):
    year_index = n % len(data.columns[5:-1])  # Get the index of the current year
    selected_year = data.columns[5:-1][year_index]  # Get the selected year

    sorted_data = data.sort_values(selected_year, ascending=False)  # Sort the data in descending order
    top_10_data = sorted_data.head(10)  # Select the first 10 rows (highest values)

    top_10_data = top_10_data[::-1]  # Reverse the order of the top 10 rows

    colors = px.colors.qualitative.G10[:10]

    figure = {
        'data': [
            {
                'x': top_10_data[selected_year],
                'y': top_10_data['Country Name'],
                'type': 'bar',
                'orientation': 'h',
                'marker': {
                    'color': colors, # Assign colors to each bar
                    'line': {'color': 'silver', 'width': 1},# Assign colors to each bar
                     }  # Assign colors to each bar
            }
        ],
        'layout': {
            'title': f'Top 10 GDP - {selected_year}',
            'xaxis': {'title': 'GDP Per Capita in USD'},
            'yaxis': {
                'showticklabels': True,  # Show the y-axis tick labels
                'showline': False,  # Remove the y-axis line
                'zeroline': False  # Remove the y-axis zero line
            },
            'margin': {'l': 150}, # Adjust the left margin to accommodate longer country names
            'plot_bgcolor': 'rgb(248, 248, 255)',  # Set the background color for the chart
            'paper_bgcolor': 'rgb(248, 248, 255)',  # Set the background color for the chart's paper
            'annotations': [
                {
                    'text': 'Information collected from World Bank Historical Data. (Accessed 30 June 2023)',
                    'showarrow': False,
                    'xref': 'paper',
                    'yref': 'paper',
                    'x': 0,
                    'y': -0.2,
                    'font': {'size': 10, 'color': 'gray'}
                }
            ]
        }
    }

    return figure

@app.callback(
    Output('dropdown-gdp-graph', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_dropdown_graph(selected_year):
    sorted_data = data.sort_values(selected_year, ascending=False)  # Sort the data in descending order
    top_10_data = sorted_data.head(10)  # Select the first 10 rows (highest values)
    top_10_data = top_10_data[::-1]

    colors = px.colors.qualitative.G10[:10]  

    figure = {
        'data': [
            {
                'x': top_10_data[selected_year],
                'y': top_10_data['Country Name'],
                'type': 'bar',
                'orientation': 'h',
                'marker': {
                    'color': colors,
                    'line': {'color': 'silver', 'width': 1},# Assign colors to each bar
                    }  
            }
        ],
        'layout': {
            'title': f'Top 10 GDP - {selected_year}',
            'xaxis': {'title': 'GDP Per Capita in USD'},
            'yaxis': {
                'showticklabels': True,  # Show the y-axis tick labels
                'showline': False,  # Remove the y-axis line
                'zeroline': False  # Remove the y-axis zero line
            },
            'margin': {'l': 150},  # Adjust the left margin to accommodate longer country names
            'plot_bgcolor': 'rgb(248, 248, 255)',  # Set the background color for the chart
            'paper_bgcolor': 'rgb(248, 248, 255)',  # Set the background color for the chart's paper
            'annotations': [
                {
                    'text': 'Information collected from World Bank Historical Data. (Accessed 30 June 2023)',
                    'showarrow': False,
                    'xref': 'paper',
                    'yref': 'paper',
                    'x': 0,
                    'y': -0.2,
                    'font': {'size': 10, 'color': 'gray'}
                }
            ]
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)