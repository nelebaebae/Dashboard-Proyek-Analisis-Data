import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title and description
st.title("Dashboard Proyek Analisis Data")
st.write("""
Ini adalah dashboard yang menampilkan analisis data terkait korelasi ulasan produk, metode pembayaran, 
dan waktu pengiriman produk, serta analisis pelanggan berdasarkan Recency, Frequency, dan Monetary.
""")

# Load data from CSV files
customers_df = pd.read_csv("customers_dataset.csv")
order_items_df = pd.read_csv("order_items_dataset.csv")
order_review_df = pd.read_csv("order_reviews_dataset.csv")
orders_df = pd.read_csv("orders_dataset.csv")
products_df = pd.read_csv("products_dataset.csv")
order_payments = pd.read_csv("order_payments_dataset.csv")

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

# Merge order_reviews with products to get product_category_name
order_reviews_with_category = pd.merge(order_review_df, products_df[['product_id', 'product_category_name']], on='product_id', how='left')

# Pertanyaan 1: Korelasi antara Jumlah Ulasan dan Tingkat Kepuasan Pelanggan
st.header('Korelasi antara Jumlah Ulasan dan Tingkat Kepuasan Pelanggan')
reviews_per_category = order_reviews_with_category.groupby('product_category_name').agg({
    'review_id': 'count',
    'review_score': 'mean'
}).reset_index()

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.scatterplot(data=reviews_per_category, x='review_id', y='review_score', size='review_id', hue='review_score', palette='viridis', ax=ax1)
plt.title('Korelasi antara Jumlah Ulasan dan Tingkat Kepuasan Pelanggan per Kategori')
plt.xlabel('Jumlah Ulasan')
plt.ylabel('Rata-rata Skor Ulasan')
st.pyplot(fig1)

# Pertanyaan 2: Jumlah Pesanan per Metode Pembayaran (Per Bulan)
st.header('Jumlah Pesanan per Metode Pembayaran (Per Bulan)')
payments_per_method_month_full = order_payments.groupby(['payment_type']).agg({
    'order_id': 'count'
}).reset_index()

fig2, ax2 = plt.subplots(figsize=(14, 7))
sns.barplot(x='payment_type', y='order_id', data=payments_per_method_month_full, ax=ax2)
plt.title('Jumlah Pesanan per Metode Pembayaran')
plt.xlabel('Metode Pembayaran')
plt.ylabel('Jumlah Pesanan')
st.pyplot(fig2)

# Pertanyaan 3: Waktu Pengiriman Rata-rata per Kategori
st.header('Waktu Pengiriman Rata-rata per Kategori')
items_orders_products_df = pd.merge(order_items_df, orders_df_cleaned, on='order_id', how='left')
items_orders_products_df = pd.merge(items_orders_products_df, products_df, on='product_id', how='left')
items_orders_products_df['shipping_time_days'] = (pd.to_datetime(items_orders_products_df['order_delivered_customer_date']) - pd.to_datetime(items_orders_products_df['order_purchase_timestamp'])).dt.days
shipping_time_per_category = items_orders_products_df.groupby('product_category_name')['shipping_time_days'].mean().reset_index()

fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.barplot(x='product_category_name', y='shipping_time_days', data=shipping_time_per_category, palette='Blues_d', ax=ax3)
plt.title('Waktu Pengiriman Rata-rata per Kategori')
plt.xticks(rotation=90)
st.pyplot(fig3)

# Analisis Pelanggan: RFM Analysis
st.header('Analisis Pelanggan: RFM (Recency, Frequency, Monetary)')
orders_items_merged = pd.merge(order_items_df, orders_df_cleaned, on='order_id', how='left')

# Step 2: Aggregate the data to compute Recency, Frequency, and Monetary
rfm_df = orders_items_merged.groupby(by='customer_id', as_index=False).agg({
    'order_purchase_timestamp': 'max',  # recency
    'order_id': 'nunique',  # frequency
    'price': 'sum'  # monetary value
})

rfm_df.columns = ['customer_id', 'last_order_date', 'frequency', 'monetary']

latest_date = orders_items_merged['order_purchase_timestamp'].max()
rfm_df['recency'] = (latest_date - rfm_df['last_order_date']).dt.days

rfm_df.drop('last_order_date', axis=1, inplace=True)

# Visualize RFM Analysis
fig4, ax4 = plt.subplots(nrows=1, ncols=3, figsize=(18, 10))

sns.barplot(x="recency", y="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette="Blues_d", ax=ax4[0])
ax4[0].set_title("Top 5 Customers by Recency (Days)")

sns.barplot(x="frequency", y="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette="Greens_d", ax=ax4[1])
ax4[1].set_title("Top 5 Customers by Frequency")

sns.barplot(x="monetary", y="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette="Reds_d", ax=ax4[2])
ax4[2].set_title("Top 5 Customers by Monetary Value")

plt.tight_layout()
st.pyplot(fig4)
