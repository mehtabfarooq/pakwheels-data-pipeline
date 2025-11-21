import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
import urllib

st.set_page_config(layout="wide") 

##Connecting to database
server = st.secrets["DB_SERVER"]
database = st.secrets["DB_NAME"]
username = st.secrets["DB_USER"]
password = st.secrets["DB_PASSWORD"]
table_name = st.secrets["DB_TABLE_NAME"]

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=no;"
)

# URL encode the ODBC string
params = urllib.parse.quote_plus(connection_string)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


def runDbQuery(query):
    result = pd.read_sql(query, engine)
    return result





all_listing = runDbQuery(f"SELECT * FROM {table_name};")
total_listings = len(all_listing)
st.header(f"List of {total_listings} used cars currently availibe:", divider="gray")
st.dataframe(all_listing)


col1, col2 = st.columns(2)
with col1:
    #Analysis 1: Number of card avalible in each city:
    st.header("Analysis 1: Number of card avalible in each city:", divider="gray")

    # Prepare your data
    analysis_1 = runDbQuery(f"SELECT City, COUNT(City) AS Cars_per_city FROM {table_name} GROUP BY City;")
    analysis_1_x = analysis_1['City']
    analysis_1_y = analysis_1['Cars_per_city']

    # Create the Matplotlib figure and axes
    fig, ax = plt.subplots()

    # Plot the bar chart
    ax.bar(analysis_1_x, analysis_1_y, color='skyblue')
    ax.set_xlabel("City")
    ax.set_ylabel("Number of Cars")
    ax.set_title("Number of Cars in Each City")
    ax.set_xticklabels(analysis_1_x, rotation=90, ha='right')

    # Display the chart in Streamlit
    st.pyplot(fig)
with col2:
    #Analysis 2: Number of listed availbile per modal year
    st.header("Analysis 2: Number of listed availbile per model year:", divider="gray")
    analysis_2 = runDbQuery(f"SELECT [Model Year], COUNT([Model Year]) AS Cars_per_model FROM {table_name} GROUP BY [Model Year];")
    analysis_2_x = analysis_2['Model Year']
    analysis_2_x = analysis_2_x.astype(str)
    analysis_2_y = analysis_2['Cars_per_model']

    fig2, ax2 = plt.subplots()

    ax2.bar(analysis_2_x, analysis_2_y, color='skyblue')
    ax2.set_xlabel("Model Year")
    ax2.set_ylabel("Number of Cars per model")
    ax2.set_title("Number of Cars in per model year")
    ax2.set_xticklabels(analysis_2_x, rotation=90, ha='right')

    # Display the chart in Streamlit
    st.pyplot(fig2)



col1, col2 = st.columns(2)
with col1:
    #Analysis 3: Percentage of cars in each transmission type
    st.header("Analysis 3: Percentage of cars in each transmission type", divider="gray")
    analysis_3 = runDbQuery(f"SELECT [Transmission Type], COUNT([Transmission Type]) AS Cars_per_transmission_type FROM {table_name} GROUP BY [Transmission Type];")
    analysis_3_x = analysis_3['Transmission Type']
    analysis_3_y = analysis_3['Cars_per_transmission_type']
    total_cars = analysis_3['Cars_per_transmission_type'].sum()

    fig3, ax3 = plt.subplots()
    ax3.set_title(f'Percentage of cars per transmission type. Total Cars {total_cars}')
    ax3.pie(analysis_3_y, explode=None, labels=analysis_3_x, autopct='%1.1f%%', shadow=False, startangle=90)
    ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig3)
with col2:
    #Analysis 4: Number of cars availble in each engine type
    st.header("Analysis 4: Percentage of cars availble in each engine type", divider="gray")

    analysis_4 = runDbQuery(f"SELECT [Fuel Type], COUNT([Fuel Type]) AS Cars_per_fuel_type FROM {table_name} GROUP BY [Fuel Type];")
    analysis_4_x = analysis_4['Fuel Type']
    analysis_4_y = analysis_4['Cars_per_fuel_type']
    total_carss = analysis_4['Cars_per_fuel_type'].sum()

    fig4, ax4 = plt.subplots()
    ax4.set_title(f'Percentage of cars per fuele type. Total Cars {total_carss}')
    ax4.pie(analysis_4_y, explode=None, labels=analysis_4_x, autopct='%1.1f%%', shadow=False, startangle=90)
    ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig4)

