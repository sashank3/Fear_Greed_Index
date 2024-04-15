import pandas as pd
import plotly.graph_objects as go

# Load the data from the CSV file
df = pd.read_csv('ema_results.csv')

# Initialize an empty list to store gauge charts
charts = []

# Iterate over each subdomain
for subdomain in df['Subdomain'].unique():
    # Filter data for the current subdomain
    subdomain_data = df[df['Subdomain'] == subdomain]

    # Select the data for EMA_7_days, EMA_21_days, and EMA_60_days
    ema_7_days = subdomain_data['EMA_7_days'].iloc[0]
    ema_21_days = subdomain_data['EMA_21_days'].iloc[0]
    ema_60_days = subdomain_data['EMA_60_days'].iloc[0]

    label_7_days = subdomain_data['Label_7_days'].iloc[0]
    label_21_days = subdomain_data['Label_21_days'].iloc[0]
    label_60_days = subdomain_data['Label_60_days'].iloc[0]

    # Create a gauge chart for the current subdomain
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        domain={'x': [0, 0.25], 'y': [0, 1]},
        mode='gauge+number',
        value=ema_7_days,
        title={'text': 'Daily', 'font': {'color': 'white'}},  # Title font color
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#000000"},  # Teal
            'steps': [
                {'range': [0, 20], 'color': '#ff6666'},  # Light red
                {'range': [20, 45], 'color': '#ffcc66'},  # Light orange
                {'range': [45, 55], 'color': '#D3D3D3'},  # Grey
                {'range': [55, 79], 'color': '#ffff66'},  # Light yellow
                {'range': [79, 100], 'color': '#66ff66'}  # Light green
            ],
        }
    ))
    fig.add_trace(go.Indicator(
        domain={'x': [0.35, 0.6], 'y': [0, 1]},
        mode='gauge+number',
        value=ema_21_days,
        title={'text': 'Weekly', 'font': {'color': 'white'}},  # Title font color
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#000000"},  # Teal
            'steps': [
                {'range': [0, 20], 'color': '#ff6666'},  # Light red
                {'range': [20, 45], 'color': '#ffcc66'},  # Light orange
                {'range': [45, 55], 'color': '#D3D3D3'},  # Grey
                {'range': [55, 79], 'color': '#ffff66'},  # Light yellow
                {'range': [79, 100], 'color': '#66ff66'}  # Light green
            ],
        }
    ))
    fig.add_trace(go.Indicator(
        domain={'x': [0.7, 0.95], 'y': [0, 1]},
        mode='gauge+number',
        value=ema_60_days,
        title={'text': 'Monthly', 'font': {'color': 'white'}},  # Title font color
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#000000"},  # Teal
            'steps': [
                {'range': [0, 20], 'color': '#ff6666'},  # Light red
                {'range': [20, 45], 'color': '#ffcc66'},  # Light orange
                {'range': [45, 55], 'color': '#D3D3D3'},  # Grey
                {'range': [55, 79], 'color': '#ffff66'},  # Light yellow
                {'range': [79, 100], 'color': '#66ff66'}  # Light green
            ],
        }
    ))
    fig.update_layout(title_text=subdomain, height=300, width=800, margin=dict(l=50, r=50, t=50, b=50),
                      font=dict(color='white'))  # Title font color

    # Add labels below each gauge chart
    fig.update_layout(
        annotations=[
            dict(
                x=0.125,  # Adjust position for the Daily gauge chart
                y=0,  # Adjust position for the Daily gauge chart
                showarrow=False,
                text= label_7_days,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="bottom",
                font=dict(color='white', size=16)  # Label font color
            ),
            dict(
                x=0.475,
                y=0,  # Adjust position for the Weekly gauge chart
              showarrow=False,
              text=label_21_days,
              xref="paper",
              yref="paper",
              xanchor="center",
              yanchor="bottom",
              font=dict(color='white', size=16)  # Label font color
            ),
            dict(
                x=0.825,  # Adjust position for the Monthly gauge chart
                y=0,  # Adjust position for the Monthly gauge chart
                showarrow=False,
                text=label_60_days,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="bottom",
                font=dict(color='white', size=16)  # Label font color
            )
        ]
    )

    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black')

    # Append the gauge chart to the list
    charts.append(fig)

# Display the gauge charts
for chart in charts:
    chart.show()