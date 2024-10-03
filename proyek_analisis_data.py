import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
reviews_per_category = pd.read_csv("Data/reviews_per_category.csv")
payments_per_method_month_full = pd.read_csv("Data/payments_per_method_month_full.csv")
top_10_fastest_shipping = pd.read_csv("Data/result.csv")
rfm_df = pd.read_csv("Data/rfm_df.csv")

st.title("E-commerce Analytics Dashboard")

# Plot 1: Correlation between Review Count and Customer Satisfaction
st.header("Korelasi antara Jumlah Ulasan dan Tingkat Kepuasan Pelanggan per Kategori Produk")
reviews_per_category = reviews_per_category.sort_values(by='review_id', ascending=False)
plt.figure(figsize=(12, 6))
sns.scatterplot(data=reviews_per_category, x='review_id', y='review_score', size='review_id', sizes=(40, 200), hue='review_score', palette='viridis', legend=False)
plt.title('Korelasi antara Jumlah Ulasan dan Tingkat Kepuasan Pelanggan per Kategori Produk')
plt.xlabel('Jumlah Ulasan')
plt.ylabel('Rata-rata Skor Ulasan')
plt.tight_layout()
st.pyplot(plt)
correlation_value = reviews_per_category['review_id'].corr(reviews_per_category['review_score'])
st.write(f"Korelasi antara jumlah ulasan dan skor kepuasan: {correlation_value:.3f}")

# Plot 2: Orders by Payment Method
st.header("Jumlah Pesanan per Metode Pembayaran (Per Bulan)")
payments_per_method_month_full['order_month'] = payments_per_method_month_full['order_month'].astype(str)
filtered_payments_per_method_month = payments_per_method_month_full[
    ~payments_per_method_month_full['order_month'].isin(['2018-09', '2018-10']) &
    (payments_per_method_month_full['payment_type'] != 'not_defined')
]
plt.figure(figsize=(14, 7))
sns.lineplot(data=filtered_payments_per_method_month, x='order_month', y='order_id', hue='payment_type', marker='o')
plt.title('Jumlah Pesanan per Metode Pembayaran (Per Bulan)')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Pesanan')
plt.xticks(rotation=45)
plt.legend(title='Metode Pembayaran')
plt.tight_layout()
st.pyplot(plt)

# Plot 3: Top 10 Fastest Shipping Categories
st.header("Top 10 Kategori Produk dengan Waktu Pengiriman Tercepat (6 bulan terakhir)")
top_10_fastest_shipping = result.sort_values(by='average_shipping_time_days').head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x='product_category_name', y='average_shipping_time_days', data=top_10_fastest_shipping, palette='Blues_d')
plt.xlabel('Kategori Produk')
plt.ylabel('Waktu Pengiriman Rata-rata (Hari)')
plt.title('Top 10 Kategori Produk dengan Waktu Pengiriman Tercepat')
plt.xticks(rotation=90)
ax2 = plt.twinx()
sns.lineplot(x='product_category_name', y='total_sales', data=top_10_fastest_shipping, color='orange', marker="o", label='Total Penjualan')
ax2.set_ylabel('Total Penjualan')
ax2.legend(loc='upper left')
plt.tight_layout()
st.pyplot(plt)

# Plot 4: RFM Analysis
st.header("Analisis RFM Pelanggan")
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(18, 10))

sns.barplot(x="recency", y="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette="Blues_d", ax=ax[0])
ax[0].set_title("Top 10 Customers by Recency (Days)")
ax[0].set_xlabel("Recency (Days)")
ax[0].set_ylabel("Customer ID")

sns.barplot(x="frequency", y="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette="Greens_d", ax=ax[1])
ax[1].set_title("Top 10 Customers by Frequency")
ax[1].set_xlabel("Frequency")
ax[1].set_ylabel("Customer ID")

sns.barplot(x="monetary", y="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette="Reds_d", ax=ax[2])
ax[2].set_title("Top 10 Customers by Monetary Value")
ax[2].set_xlabel("Monetary Value")
ax[2].set_ylabel("Customer ID")

plt.tight_layout()
st.pyplot(fig)
