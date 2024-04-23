import plotly.graph_objs as go


def line_graph(ema_data):
    selected_subdomain = 'Business'  # Replace 'YourSelectedSubdomain' with the desired subdomain
    selected_window_size = 4  # Replace 4 with the desired EMA window size

    # Filter data for the selected subdomain and window size
    filtered_data = ema_data[
        (ema_data['Subdomain'] == selected_subdomain) & (ema_data[f'EMA_{selected_window_size}_days'].notna())]

    # Create a trace for the selected data
    trace = go.Scatter(
        x=filtered_data['Time'],
        y=filtered_data[f'EMA_{selected_window_size}_days'],
        mode='lines',
        name=f'{selected_subdomain} - EMA {selected_window_size} days'
    )

    layout = go.Layout(
        title='Sentiment Line Graph',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Sentiment Value', range=[0, 100])
    )

    # Create figure
    fig = go.Figure(data=[trace], layout=layout)

    # Show figure
    fig.show()


def gauge_chart(categorical_ema):
    # Define available Subdomains and EMA window sizes
    subdomains = categorical_ema['Subdomain'].unique()
    ema_window_sizes = ['EMA_4_days', 'EMA_12_days', 'EMA_30_days']

    # Define labels for EMA window sizes
    window_labels = {'EMA_4_days': 'Daily', 'EMA_12_days': 'Weekly', 'EMA_30_days': 'Monthly'}

    # Define initial Subdomain and EMA window size
    initial_subdomain = subdomains[0]
    initial_ema_window_size = ema_window_sizes[0]

    # Initial Subdomain and EMA window size
    selected_subdomain = initial_subdomain
    selected_ema_window_size = initial_ema_window_size

    # Filter data for selected Subdomain and EMA window size
    filtered_data = categorical_ema[(categorical_ema['Subdomain'] == selected_subdomain)]

    # Create gauge chart
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=filtered_data[selected_ema_window_size].iloc[0],
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 20], 'color': "red"},
                   {'range': [20, 40], 'color': "orange"},
                   {'range': [40, 60], 'color': "yellow"},
                   {'range': [60, 80], 'color': "lightgreen"},
                   {'range': [80, 100], 'color': "green"}]}))

    # Add label underneath
    gauge.add_annotation(
        text=f"{selected_subdomain}",
        x=0.5,
        y=-0.3,
        showarrow=False,
        font=dict(size=16)
    )

    # Update layout
    gauge.update_layout(
        title={'text': f"<b>{window_labels[selected_ema_window_size]} Fear and Greed Index</b>"},
        width=600,
        height=400,
        margin=dict(t=100)
    )

    # Show chart
    gauge.show()
