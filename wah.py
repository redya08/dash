
import streamlit as st
import pandas as pd

# Load data
customer = pd.read_csv("customer.csv")
product = pd.read_csv("product.csv")
store = pd.read_csv("store.csv")
transaction = pd.read_csv("transaction.csv")

# Merge data
df = transaction.merge(customer, left_on="customer_id", right_on="id", how="left")                 .merge(product, left_on="product_id", right_on="id", how="left", suffixes=("_cust", "_prod"))                 .merge(store, left_on="store_id", right_on="id", how="left", suffixes=("", "_store"))

# Streamlit dashboard
st.title("📊 Sales Dashboard")

st.subheader("Preview Data")
st.dataframe(df.head())

# Chart: Distribusi transaksi per kota
st.subheader("Jumlah Transaksi per Kota")
city_counts = df['city'].value_counts()
st.bar_chart(city_counts)

# Chart: Distribusi berdasarkan gender
st.subheader("Distribusi Transaksi berdasarkan Gender")
gender_counts = df['gender'].value_counts()
st.bar_chart(gender_counts)

# Chart: Total penjualan per jenis toko
st.subheader("Total Penjualan per Jenis Toko")
store_sales = df.groupby("type")['total'].sum()
st.bar_chart(store_sales)

# Chart: Produk dengan total penjualan tertinggi
st.subheader("Top 10 Produk dengan Penjualan Tertinggi")
top_products = df.groupby("product_id")['total'].sum().nlargest(10)
st.bar_chart(top_products)
