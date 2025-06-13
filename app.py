import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("superstore.csv", encoding="ISO-8859-1")
df["Order Date"] = pd.to_datetime(df["Order Date"])

kategori = st.sidebar.multiselect(
    "Pilih Kategori Produk", df["Category"].unique(), default=df["Category"].unique()
)

df_filtered = df[df["Category"].isin(kategori)]

st.title("Dashboard Penjualan Superstore")

total_profit = df_filtered["Profit"].sum()
st.metric("Total Profit", f"${total_profit:,.2f}")

# EDA 1: Trend penjualan tahunan
df_filtered["Year"] = df_filtered["Order Date"].dt.year
annual_sales = df_filtered.groupby("Year")["Sales"].sum().reset_index()

st.subheader("📈 Trend Penjualan Tahunan")
fig1, ax1 = plt.subplots(facecolor='black')

# Plot garis dengan efek glow
ax1.plot(
    annual_sales["Year"],
    annual_sales["Sales"],
    marker='o',
    color='deepskyblue',
    linewidth=2.5,
    markersize=8,
    markerfacecolor='cyan'
)

# Tema dark
ax1.set_facecolor("black")
fig1.patch.set_facecolor('black')

# Label dan tampilan
ax1.set_title("Total Penjualan per Tahun", color='white', fontsize=14)
ax1.set_xlabel("Tahun", color='white')
ax1.set_ylabel("Total Penjualan", color='white')
ax1.tick_params(colors='white')

# Grid dengan warna samar
ax1.grid(True, linestyle='--', alpha=0.3, color='gray')

st.pyplot(fig1)

# EDA 2: Profitabilitas per kategori
profit_by_category = df_filtered.groupby("Category")["Profit"].sum().reset_index()

st.subheader("💰 Profitabilitas per Kategori Produk")
fig2, ax2 = plt.subplots(facecolor='black')

# Warna gradasi untuk bar
colors = ['#FF6F61', '#6B5B95', '#88B04B']
bars = ax2.bar(
    profit_by_category["Category"],
    profit_by_category["Profit"],
    color=colors,
    edgecolor='white',
    linewidth=1
)

# Tema dark
ax2.set_facecolor("black")
fig2.patch.set_facecolor('black')

# Label dan tampilan
ax2.set_title("Total Profit per Kategori", color='white', fontsize=14)
ax2.set_ylabel("Total Profit", color='white')
ax2.set_xlabel("Kategori", color='white')
ax2.tick_params(colors='white')

# Tambahkan nilai di atas batang
for bar in bars:
    height = bar.get_height()
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"${height:,.0f}",
        ha='center',
        va='bottom',
        color='white',
        fontsize=10
    )

# Grid horizontal
ax2.yaxis.grid(True, linestyle='--', alpha=0.3, color='gray')

st.pyplot(fig2)