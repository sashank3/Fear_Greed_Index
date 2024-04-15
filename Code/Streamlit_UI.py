import streamlit as st
import altair as alt


def generate_line_chart(sentiment_df):
    # Select category for line chart
    selected_category = st.selectbox("Select a category for the line chart:", sentiment_df['Subdomain'].unique())

    # Filter data for the selected category
    category_data = sentiment_df[sentiment_df['Subdomain'] == selected_category]

    # Create line chart
    line_chart = alt.Chart(category_data).mark_line().encode(
        x='Time',
        y='Sentiment',

        color='Subdomain',
        tooltip=['Time', 'Sentiment', 'Subdomain']
    ).properties(
        width=800,
        height=400
    )

    return line_chart


def generate_gauge_chart(categorical_ema):
    # Select subdomain for gauge chart
    selected_subdomain = st.selectbox("Select a subdomain for the gauge chart:", categorical_ema['Subdomain'].unique())

    # Filter data for the selected subdomain
    subdomain_data = categorical_ema[categorical_ema['Subdomain'] == selected_subdomain]

    # Convert 'EMA_12_Days' column to string data type
    subdomain_data['EMA_12_days'] = subdomain_data['EMA_12_days'].astype(str)

    # Create gauge chart
    gauge_chart = alt.Chart(subdomain_data).mark_bar().encode(
        x='Subdomain',
        y='EMA_12_days',
        color=alt.Color('Label_12_days', scale=alt.Scale(scheme='set1'), type='nominal'),  # Specify data type
        tooltip=['Subdomain', 'EMA_12_days', 'Label_12_days']
    ).properties(
        width=400,
        height=200
    )

    return gauge_chart



def run_streamlit_app(sentiment_df, categorical_ema):
    st.title("Sentiment Analysis Dashboard")

    st.header("Gauge Chart")
    gauge_chart = generate_gauge_chart(categorical_ema)
    st.altair_chart(gauge_chart, use_container_width=True)

    st.header("Line Chart")
    line_chart = generate_line_chart(sentiment_df)
    st.altair_chart(line_chart, use_container_width=True)


