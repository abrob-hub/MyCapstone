# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=int(min_payload),  # Convert to integer
        max=int(max_payload),  # Convert to integer
        step=1000,  # Increment of the slider
        marks={i: str(i) for i in range(int(min_payload), int(max_payload) + 1, 1000)},  # Add marks for each 1000 kg
        value=[int(min_payload), int(max_payload)]  # Default range
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches for All Sites'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_fail = filtered_df['class'].value_counts().reset_index()
        success_fail.columns = ['class', 'count']
        fig = px.pie(
            success_fail,
            names='class',
            values='count',
            title=f'Success vs Failure for {entered_site}'
        )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)', 
        y='class', 
        color='Booster Version Category',
        title=f'Scatter plot of Payload Mass vs Launch Success for {entered_site if entered_site != "ALL" else "All Sites"}',
        labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Launch Success'}
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
