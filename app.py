import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from prophet import Prophet
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Set page configuration
st.set_page_config(page_title="Supplier Performance Dashboard", layout="wide")

# Title of the dashboard
st.title("📊 Supplier Performance Dashboard")

# Connect to SQLite database
conn = sqlite3.connect("supplier.db")
df_suppliers = pd.read_sql("SELECT * FROM Suppliers", conn)
conn.close()

# Display supplier data
st.subheader("📄 Supplier Data")
st.dataframe(df_suppliers)

# Sidebar Filters
st.sidebar.title("🔍 Filters")
supplier_choice = st.sidebar.selectbox("Select Supplier", df_suppliers["CompanyName"].unique())
city_filter = st.sidebar.multiselect("Filter by City", df_suppliers["City"].unique(), default=df_suppliers["City"].unique())

# Filter Data
filtered_data = df_suppliers[(df_suppliers["CompanyName"] == supplier_choice) & (df_suppliers["City"].isin(city_filter))]
st.subheader(f"Details for {supplier_choice}")
st.write(filtered_data)

# Visualization (Bar Chart)
fig = px.bar(filtered_data, x="City", y="SupplierID", title=f"{supplier_choice} Performance")
st.plotly_chart(fig)

# --- Future Trend Prediction ---
st.subheader("📈 Future Trend Prediction")

# Check if 'OrderDate' and 'Amount' exist in the supplier data.
if 'OrderDate' not in df_suppliers.columns or 'Amount' not in df_suppliers.columns:
    st.info("Time series data not found in supplier data. Simulating data for forecasting.")
    import numpy as np
    # Simulate data for the last 365 days
    date_range = pd.date_range(start='2022-01-01', periods=365, freq='D')
    simulated_data = pd.DataFrame({'ds': date_range, 'y': np.random.randint(100, 1000, size=365)})
    forecast_data = simulated_data
else:
    # If your data already has these columns, aggregate them.
    df_suppliers['OrderDate'] = pd.to_datetime(df_suppliers['OrderDate'], errors='coerce')
    forecast_data = df_suppliers.groupby('OrderDate')['Amount'].sum().reset_index()
    forecast_data.columns = ['ds', 'y']

from prophet import Prophet

# Train Prophet Model
model = Prophet()
model.fit(forecast_data)

# Predict the next 6 months
future = model.make_future_dataframe(periods=6, freq='M')
forecast = model.predict(future)

# Plot the forecast
fig_forecast = model.plot(forecast)
st.pyplot(fig_forecast)


# --- Supplier Clustering ---
st.subheader("🎯 Supplier Clustering")

# Example: Using 'SupplierID' (just for demonstration) and a simulated 'CustomerRating'
features = df_suppliers[['SupplierID']].copy()
import numpy as np
df_suppliers['CustomerRating'] = np.random.uniform(1, 5, size=len(df_suppliers))
features['CustomerRating'] = df_suppliers['CustomerRating']

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42)
df_suppliers['Cluster'] = kmeans.fit_predict(features_scaled)

import plotly.express as px
fig_cluster = px.scatter(df_suppliers, x="SupplierID", y="CustomerRating", 
                         color=df_suppliers["Cluster"].astype(str),
                         hover_data=['CompanyName'], 
                         title="Supplier Clustering")
st.plotly_chart(fig_cluster)

