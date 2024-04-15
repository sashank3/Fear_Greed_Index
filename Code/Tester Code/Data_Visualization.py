import pygal
import pandas as pd
from pygal.style import LightColorizedStyle


# Load the data from the CSV file
df = pd.read_csv('ema_results.csv')

# Iterate over each subdomain
for subdomain in df['Subdomain'].unique():
    # Filter data for the current subdomain
    subdomain_data = df[df['Subdomain'] == subdomain]

    # Select the data for EMA_7_days, EMA_21_days, and EMA_60_days
    ema_7_days = subdomain_data['EMA_7_days'].iloc[0]
    ema_21_days = subdomain_data['EMA_21_days'].iloc[0]
    ema_60_days = subdomain_data['EMA_60_days'].iloc[0]

    # Create a new gauge chart
    gauge_chart = pygal.SolidGauge(half_pie=True, inner_radius=0.70, style=LightColorizedStyle)

    # Add the data to the gauge chart
    gauge_chart.add('EMA_7_days', [{'value': ema_7_days, 'max_value': 100}])
    gauge_chart.add('EMA_21_days', [{'value': ema_21_days, 'max_value': 100}])
    gauge_chart.add('EMA_60_days', [{'value': ema_60_days, 'max_value': 100}])

    # Customize the gauge chart
    gauge_chart.title = f'EMA Values for {subdomain}'
    gauge_chart.range = [0, 100]
    gauge_chart.legend_at_bottom = False
    gauge_chart.legend_box_size = 10

    # Save the chart to a file
    file_name = f'{subdomain}_ema_gauge_chart.svg'
    gauge_chart.render_to_file(file_name)

    # Display the chart
    gauge_chart.render_in_browser()
