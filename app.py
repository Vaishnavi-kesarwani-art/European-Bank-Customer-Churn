import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="European Bank Customer Churn",
    page_icon="🏦",
    layout="wide"
)

# Load dataset
df = pd.read_csv("European_Bank.csv")

st.title("🏦 European Bank Customer Churn Analysis")
st.write("Dashboard to analyze customer churn and banking patterns.")

# Sidebar filters
st.sidebar.header("Filters")

geography = st.sidebar.multiselect(
    "Select Country",
    options=df["Geography"].unique(),
    default=df["Geography"].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered_df = df[
    (df["Geography"].isin(geography)) &
    (df["Gender"].isin(gender))
]

# Key metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", len(filtered_df))
col2.metric("Exited Customers", int(filtered_df["Exited"].sum()))
col3.metric(
    "Churn Rate",
    f"{filtered_df['Exited'].mean() * 100:.2f}%"
)
col4.metric(
    "Average Balance",
    f"€{filtered_df['Balance'].mean():,.0f}"
)

st.divider()

# Churn by Geography
st.subheader("🌍 Customers by Country")

country_data = filtered_df.groupby("Geography")["Exited"].agg(
    Customers="count",
    Exited="sum"
).reset_index()

st.dataframe(country_data, use_container_width=True)

# Churn chart
st.subheader("📊 Churn Distribution")

churn_data = filtered_df["Exited"].value_counts()

fig, ax = plt.subplots()
ax.bar(
    ["Stayed", "Exited"],
    [
        churn_data.get(0, 0),
        churn_data.get(1, 0)
    ]
)
ax.set_ylabel("Number of Customers")
ax.set_title("Customer Churn Distribution")

st.pyplot(fig)

# Age analysis
st.subheader("👥 Age vs Churn")

age_data = filtered_df.groupby("Age")["Exited"].mean() * 100

fig2, ax2 = plt.subplots()
ax2.plot(age_data.index, age_data.values)
ax2.set_xlabel("Age")
ax2.set_ylabel("Churn Rate (%)")
ax2.set_title("Churn Rate by Age")

st.pyplot(fig2)

# Active members
st.subheader("💳 Active Member Analysis")

active_data = filtered_df.groupby("IsActiveMember")["Exited"].mean() * 100

st.write(
    "Churn rate among active and inactive members:"
)

st.dataframe(
    active_data.rename("Churn Rate (%)").reset_index(),
    use_container_width=True
)

st.success("Dashboard loaded successfully!")
