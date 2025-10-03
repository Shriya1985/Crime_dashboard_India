import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_excel("Modified_Crime_Dataset_India.xlsx", sheet_name="Sheet1")

# Page setup
st.set_page_config(page_title="Crime Dashboard India", layout="wide")
st.title("🚔 Crime Analytics Dashboard - India")

# --- Sidebar filters
st.sidebar.header("Filter Options")
city = st.sidebar.multiselect("Select City:", df["City"].unique())
crime_type = st.sidebar.multiselect("Select Crime Type:", df["Crime Description"].unique())
year = st.sidebar.multiselect("Select Year:", df["Year"].unique())

# Apply filters
filtered_df = df.copy()
if city:
    filtered_df = filtered_df[filtered_df["City"].isin(city)]
if crime_type:
    filtered_df = filtered_df[filtered_df["Crime Description"].isin(crime_type)]
if year:
    filtered_df = filtered_df[filtered_df["Year"].isin(year)]

# --- KPI Cards
total_cases = len(filtered_df)
closed_cases = len(filtered_df[filtered_df["Case Closed"] == "Yes"])
open_cases = total_cases - closed_cases

col1, col2, col3 = st.columns(3)
col1.metric("Total Cases", f"{total_cases:,}")
col2.metric("Closed Cases", f"{closed_cases:,}")
col3.metric("Open Cases", f"{open_cases:,}")

# --- Charts
col4, col5 = st.columns(2)

with col4:
    fig_city = px.bar(filtered_df.groupby("City")["Report Number"].count().reset_index(),
                      x="City", y="Report Number", color="City",
                      title="Crimes by City")
    st.plotly_chart(fig_city, use_container_width=True)

with col5:
    fig_domain = px.pie(filtered_df, names="Crime Domain",
                        title="Crime Distribution by Domain")
    st.plotly_chart(fig_domain, use_container_width=True)

# Extra Charts
col6, col7 = st.columns(2)

with col6:
    fig_gender = px.histogram(filtered_df, x="Victim Gender", color="Victim Gender",
                              title="Victim Gender Distribution")
    st.plotly_chart(fig_gender, use_container_width=True)

with col7:
    fig_weapon = px.bar(filtered_df.groupby("Weapon Used")["Report Number"].count().reset_index(),
                        x="Weapon Used", y="Report Number",
                        title="Weapons Used in Crimes")
    st.plotly_chart(fig_weapon, use_container_width=True)

# --- Data Table
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head(50))
