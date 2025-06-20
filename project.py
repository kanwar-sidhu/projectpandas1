import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/leonism/sample-superstore/refs/heads/master/data/superstore.csv'
    df = pd.read_csv(url)
    
    # Data cleaning
    df['Postal Code'] = df['Postal Code'].fillna('N/A').astype(str)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    # Calculate profit margin
    df['Profit Margin'] = df['Profit'] / df['Sales']
    
    return df

df = load_data()

# Streamlit app
st.title('Superstore Sales Performance Analysis')
st.write("This app analyzes the Superstore dataset to uncover insights into sales, profitability, and customer behavior.")

# Data Cleaning Section
st.header("1. Data Cleaning")
st.write(f"- Dataset contains {df.shape[0]} rows and {df.shape[1]} columns")
st.write("- Missing values handled in Postal Code column (filled with 'N/A')")
st.write("- Data types corrected (Postal Code to string, dates to datetime)")
st.write(f"- Found {df.duplicated().sum()} duplicate rows (none removed)")

# Exploratory Data Analysis
st.header("2. Exploratory Data Analysis")

## Basic Metrics
st.subheader("2.1 Basic Metrics")
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
avg_order_value = df.groupby('Order ID')['Sales'].sum().mean()

st.write(f"- Total Sales: ${total_sales:,.2f}")
st.write(f"- Total Profit: ${total_profit:,.2f}")
st.write(f"- Average Order Value: ${avg_order_value:,.2f}")

## Product Analysis
st.subheader("2.2 Product Analysis")
highest_sales_product = df.loc[df['Sales'].idxmax(), 'Product Name']
highest_profit_product = df.loc[df['Profit'].idxmax(), 'Product Name']
category_profit = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)

st.write(f"- Product with highest sales: {highest_sales_product}")
st.write(f"- Product with highest profit: {highest_profit_product}")
st.write("- Profit by category:")
for category, profit in category_profit.items():
    st.write(f"  - {category}: ${profit:,.2f}")

## Regional Performance
st.subheader("2.3 Regional Performance")
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
region_profit_margin = df.groupby('Region').apply(lambda x: x['Profit'].sum() / x['Sales'].sum()).sort_values(ascending=False)
city_sales = df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(1)

st.write("- Sales by region:")
for region, sales in region_sales.items():
    st.write(f"  - {region}: ${sales:,.2f}")

st.write("\n- Profit margin by region:")
for region, margin in region_profit_margin.items():
    st.write(f"  - {region}: {margin:.2%}")

st.write(f"- Top city by sales: {city_sales.index[0]} (${city_sales.iloc[0]:,.2f})")

## Customer Insights
st.subheader("2.4 Customer Insights")
avg_orders = df.groupby('Customer ID')['Order ID'].nunique().mean()
top_customers = df.groupby(['Customer ID', 'Customer Name'])['Sales'].sum().sort_values(ascending=False).head(5)

st.write(f"- Average number of orders per customer: {avg_orders:.2f}")
st.write("- Top 5 customers by spending:")
for i, ((customer_id, name), sales) in enumerate(top_customers.items(), 1):
    st.write(f"  {i}. {name} (ID: {customer_id}): ${sales:,.2f}")

## Discounts & Profitability
st.subheader("2.5 Discounts & Profitability")
avg_discount = df.groupby('Category')['Discount'].mean().sort_values(ascending=False)
subcat_profit_margin = df.groupby('Sub-Category')['Profit Margin'].mean().sort_values()
lowest_margin_subcat = subcat_profit_margin.idxmin()

st.write("- Average discount by category:")
for category, discount in avg_discount.items():
    st.write(f"  - {category}: {discount:.2%}")

st.write(f"\n- Sub-category with lowest profit margin: {lowest_margin_subcat} ({subcat_profit_margin.min():.2%})")

# Display raw data option
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(df)