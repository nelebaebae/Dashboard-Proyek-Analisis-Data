import streamlit as st
import pandas as pd

# Title and description
st.title("Dashboard Proyek Analisis Data")
st.write("""
Ini adalah dashboard yang menampilkan analisis data terkait korelasi ulasan produk, metode pembayaran, 
dan waktu pengiriman produk.
""")

# Load data directly from your GitHub repository
@st.cache
def load_data():
    base_url = "https://raw.githubusercontent.com/nelebaebae/Dashboard-Proyek-Analisis-Data/main/"
    
    customers_df = pd.read_csv(base_url + "customers_dataset.csv")
    order_items_df = pd.read_csv(base_url + "order_items_dataset.csv")
    order_review_df = pd.read_csv(base_url + "order_reviews_dataset.csv")
    orders_df = pd.read_csv(base_url + "orders_dataset.csv")
    products_df = pd.read_csv(base_url + "products_dataset.csv")
    order_payments = pd.read_csv(base_url + "order_payments_dataset.csv")
    
    return customers_df, order_items_df, order_review_df, orders_df, products_df, order_payments

# Load data
customers_df, order_items_df, order_review_df, orders_df, products_df, order_payments = load_data()

# Data cleaning
order_review_df['review_comment_title'].fillna('No Comment', inplace=True)
order_review_df['review_comment_message'].fillna('No Comment', inplace=True)

orders_df_cleaned = orders_df.dropna(subset=['order_approved_at'])
orders_df_cleaned['order_delivered_customer_date'] = pd.to_datetime(orders_df_cleaned['order_delivered_customer_date'], errors='coerce')
orders_df_cleaned['order_purchase_timestamp'] = pd.to_datetime(orders_df_cleaned['order_purchase_timestamp'], errors='coerce')
orders_df_cleaned['order_delivered_carrier_date'].fillna('Unknown', inplace=True)
orders_df_cleaned['order_delivered_customer_date'].fillna('Unknown', inplace=True)

numerical_columns = ['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
products_df[numerical_columns] = products_df[numerical_columns].fillna(products_df[numerical_columns].mean())

products_df = products_df.dropna(subset=['product_category_name'])

# Sidebar filters
st.sidebar.header('Filter Data')
payment_type_filter = st.sidebar.multiselect('Metode Pembayaran', order_payments['payment_type'].unique())
category_filter = st.sidebar.multiselect('Kategori Produk', products_df['product_category_name'].unique())

# Filtered data based on user input
if payment_type_filter:
    order_payments_filtered = order_payments[order_payments['payment_type'].isin(payment_type_filter)]
else:
    order_payments_filtered = order_payments

if category_filter:
    products_filtered = products_df[products_df['product_category_name'].isin(category_filter)]
else:
    products_filtered = products_df

# Show basic stats
st.header('Statistik Dasar')
st.write('Jumlah total pelanggan:', customers_df.shape[0])
st.write('Jumlah total produk:', products_df.shape[0])

# Plot 1: Jumlah Pesanan per Metode Pembayaran
st.subheader('Jumlah Pesanan per Metode Pembayaran')
payments_per_method_month_full = order_payments_filtered.groupby(['payment_type']).agg({
    'order_id': 'count'
}).reset_index()

st.bar_chart(payments_per_method_month_full.set_index('payment_type'))

# Plot 2: Korelasi antara Jumlah Ulasan dan Skor Rata-rata
st.subheader('Korelasi antara Jumlah Ulasan dan Skor Rata-rata per Kategori')
reviews_per_category = order_review_df.groupby('product_category_name').agg({
    'review_id': 'count',
    'review_score': 'mean'
}).reset_index()

reviews_data = reviews_per_category[['review_id', 'review_score']].set_index('review_id')
st.line_chart(reviews_data)

# Plot 3: Waktu Pengiriman Rata-rata
st.subheader('Waktu Pengiriman Rata-rata per Kategori')
items_orders_products_df = pd.merge(order_items_df, orders_df_cleaned, on='order_id', how='left')
items_orders_products_df = pd.merge(items_orders_products_df, products_df, on='product_id', how='left')
items_orders_products_df['shipping_time_days'] = (pd.to_datetime(items_orders_products_df['order_delivered_customer_date']) - pd.to_datetime(items_orders_products_df['order_purchase_timestamp'])).dt.days
shipping_time_per_category = items_orders_products_df.groupby('product_category_name')['shipping_time_days'].mean().reset_index()

st.bar_chart(shipping_time_per_category.set_index('product_category_name'))

st.write("Analisis lanjutan dan insights lebih detail bisa ditambahkan di sini sesuai kebutuhan Anda.")
