import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
from datetime import datetime

# ---------------------------------------
# 🔌 Connect to MongoDB
# ---------------------------------------
#client = MongoClient("mongodb://root:example@localhost:27017/?authSource=admin")
client = MongoClient("mongodb://root:example@mongo:27017/?authSource=admin")
db = client["uberstreaming"]
collection = db["bookings"]

# ---------------------------------------
# 📥 Load Data
# ---------------------------------------
@st.cache_data(ttl=30)   # refresh every 30 seconds
def load_data():
    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)

    # Convert date & time
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Booking_Value"] = pd.to_numeric(df["Booking_Value"], errors="coerce")
    df["Ride_Distance"] = pd.to_numeric(df["Ride_Distance"], errors="coerce")

    # Extract day, month, year
    df["Day"] = df["Date"].dt.day
    df["Month"] = df["Date"].dt.month
    df["Year"] = df["Date"].dt.year
    return df

df = load_data()

st.title("🚖 Real-Time Uber Booking Streaming Dashboard")
st.markdown("Live analytics dashboard powered by **Kafka + Spark Structured Streaming + MongoDB + Streamlit**")

# ---------------------------------------
# Sidebar Filters
# ---------------------------------------
st.sidebar.header("🔎 Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].dropna().unique()),
    default=sorted(df["Year"].dropna().unique())
)

month_filter = st.sidebar.multiselect(
    "Select Month",
    options=sorted(df["Month"].dropna().unique()),
    default=sorted(df["Month"].dropna().unique())
)

day_filter = st.sidebar.multiselect(
    "Select Day",
    options=sorted(df["Day"].dropna().unique()),
    default=sorted(df["Day"].dropna().unique())
)

vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type",
    options=sorted(df["Vehicle_Type"].dropna().unique()),
    default=sorted(df["Vehicle_Type"].dropna().unique())
)

status_filter = st.sidebar.multiselect(
    "Booking Status",
    options=sorted(df["Booking_Status"].dropna().unique()),
    default=sorted(df["Booking_Status"].dropna().unique())
)

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    options=sorted(df["Payment_Method"].dropna().unique()),
    default=sorted(df["Payment_Method"].dropna().unique())
)

# ---------------------------------------
# Apply Filters
# ---------------------------------------
filtered_df = df[
    (df["Year"].isin(year_filter)) &
    (df["Month"].isin(month_filter)) &
    (df["Day"].isin(day_filter)) &
    (df["Vehicle_Type"].isin(vehicle_filter)) &
    (df["Booking_Status"].isin(status_filter)) &
    (df["Payment_Method"].isin(payment_filter))
]

st.subheader("📊 Filtered Data Overview")
st.dataframe(filtered_df.head(20))

# ---------------------------------------
# KPIs
# ---------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Bookings", len(filtered_df))
col2.metric("Avg Booking Value", round(filtered_df["Booking_Value"].mean(), 2))
col3.metric("Avg Ride Distance (km)", round(filtered_df["Ride_Distance"].mean(), 2))

# ---------------------------------------
# Charts
# ---------------------------------------

# --- Bookings by Vehicle Type ---
st.subheader("🚘 Bookings by Vehicle Type")
fig_vehicle = px.bar(
    filtered_df.groupby("Vehicle_Type").size().reset_index(name="Count"),
    x="Vehicle_Type",
    y="Count",
    text="Count",
)
st.plotly_chart(fig_vehicle, use_container_width=True)

# --- Booking Status ---
st.subheader("📌 Booking Status Distribution")
fig_status = px.pie(
    filtered_df,
    names="Booking_Status",
    title="Booking Status Breakdown"
)
st.plotly_chart(fig_status, use_container_width=True)

# --- Payment Method ---
st.subheader("💳 Payment Method Distribution")
fig_payment = px.pie(
    filtered_df,
    names="Payment_Method",
    title="Payment Methods"
)
st.plotly_chart(fig_payment, use_container_width=True)

# --- Time-series Bookings ---
st.subheader("📈 Bookings Over Time")
if not filtered_df.empty:
    fig_timeseries = px.line(
        filtered_df.groupby("Date").size().reset_index(name="Count"),
        x="Date",
        y="Count",
        title="Daily Booking Count"
    )
    st.plotly_chart(fig_timeseries, use_container_width=True)
else:
    st.info("No data available for selected filters.")

# --- Average Booking Value by Vehicle Type ---
st.subheader("💰 Avg Booking Value by Vehicle Type")
fig_value = px.bar(
    filtered_df.groupby("Vehicle_Type")["Booking_Value"].mean().reset_index(),
    x="Vehicle_Type",
    y="Booking_Value",
    title="Average Booking Value",
)
st.plotly_chart(fig_value, use_container_width=True)

# --- Average Ride Distance by Vehicle Type ---
st.subheader("🚴 Avg Ride Distance by Vehicle Type")
fig_distance = px.bar(
    filtered_df.groupby("Vehicle_Type")["Ride_Distance"].mean().reset_index(),
    x="Vehicle_Type",
    y="Ride_Distance",
    title="Average Ride Distance",
)
st.plotly_chart(fig_distance, use_container_width=True)

st.success("Dashboard updated successfully! 🚀")
