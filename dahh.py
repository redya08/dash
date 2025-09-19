
import streamlit as st
import pandas as pd

# ===============================
# 1. Load Data
# ===============================
customer = pd.read_csv("customer.csv")
product = pd.read_csv("product.csv")
store = pd.read_csv("store.csv")
transaction = pd.read_csv("transaction.csv")

# Debug: tampilkan kolom tiap tabel
st.write("Kolom di customer.csv:", customer.columns.tolist())
st.write("Kolom di product.csv:", product.columns.tolist())
st.write("Kolom di store.csv:", store.columns.tolist())
st.write("Kolom di transaction.csv:", transaction.columns.tolist())

# Pastikan kolom yang dipakai untuk merge benar
df = transaction.copy()

if "customer_id" in transaction.columns and "customer_id" in customer.columns:
    df = df.merge(customer, on="customer_id", how="left")

if "product_id" in transaction.columns and "product_id" in product.columns:
    df = df.merge(product, on="product_id", how="left")

if "store_id" in transaction.columns and "store_id" in store.columns:
    df = df.merge(store, on="store_id", how="left")

# Pastikan tanggal dalam format datetime
if "transaction_date" in df.columns:
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

# Hitung total sales
if all(x in df.columns for x in ["quantity", "price"]):
    df["total_sales"] = df["quantity"] * df["price"]

# ===============================
# 2. Dashboard Layout
# ===============================
st.title("📊 Dashboard Analisis Penjualan Retail")

if not df.empty:
    # Ringkasan KPI
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${df['total_sales'].sum():,.0f}")
    col2.metric("Total Transaksi", f"{df['transaction_id'].nunique():,}")
    col3.metric("Total Customer", f"{df['customer_id'].nunique():,}")

    # ===============================
    # 3. Analisis Penjualan
    # ===============================
    st.header("📈 Analisis Penjualan")

    if "transaction_date" in df.columns:
        monthly_sales = df.groupby(df["transaction_date"].dt.to_period("M"))["total_sales"].sum()
        st.subheader("Penjualan Bulanan")
        st.line_chart(monthly_sales)

    if "product_name" in df.columns:
        top_products = df.groupby("product_name")["total_sales"].sum().sort_values(ascending=False).head(10)
        st.subheader("Top 10 Produk Terlaris")
        st.bar_chart(top_products)

    # ===============================
    # 4. Analisis Customer
    # ===============================
    st.header("🧑‍🤝‍🧑 Analisis Customer")

    if "gender" in df.columns:
        gender_dist = df["gender"].value_counts()
        st.subheader("Distribusi Gender Customer")
        st.bar_chart(gender_dist)

    if "customer_id" in df.columns:
        customer_spending = df.groupby("customer_id")["total_sales"].sum()
        st.subheader("Top 10 Customer Berdasarkan Pengeluaran")
        st.bar_chart(customer_spending.sort_values(ascending=False).head(10))

    # ===============================
    # 5. Analisis Store
    # ===============================
    st.header("🏬 Analisis Store")

    if "store_name" in df.columns:
        store_sales = df.groupby("store_name")["total_sales"].sum().sort_values(ascending=False)
        st.subheader("Revenue per Store")
        st.bar_chart(store_sales)
else:
    st.error("DataFrame kosong. Periksa kembali kolom kunci untuk merge.")
