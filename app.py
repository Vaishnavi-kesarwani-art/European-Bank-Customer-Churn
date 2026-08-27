
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="European Banking Churn Analysis",
    page_icon="🏦",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("European_Bank.csv")

# -----------------------------
# Create Segments
# -----------------------------
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 29, 45, 60, 100],
    labels=["<30", "30-45", "46-60", "60+"]
)

df["Credit_Score_Band"] = pd.cut(
    df["CreditScore"],
    bins=[0, 579, 669, 850],
    labels=["Low", "Medium", "High"]
)

df["Tenure_Group"] = pd.cut(
    df["Tenure"],
    bins=[-1, 2, 7, 20],
    labels=["New", "Mid-term", "Long-term"]
)

df["Balance_Segment"] = pd.cut(
    df["Balance"],
    bins=[-1, 50000, 150000, float("inf")],
    labels=["Low-balance", "Medium-balance", "High-balance"]
)

# -----------------------------
# Title
# -----------------------------
st.title("🏦 Customer Segmentation & Churn Pattern Analytics")
st.write(
    "Analysis of customer churn across geography, demographics and financial profiles."
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Segment Filters")

countries = st.sidebar.multiselect(
    "Geography",
    df["Geography"].unique(),
    default=list(df["Geography"].unique())
)

genders = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=list(df["Gender"].unique())
)

age_groups = st.sidebar.multiselect(
    "Age Group",
    df["Age_Group"].dropna().unique(),
    default=list(df["Age_Group"].dropna().unique())
)

credit_bands = st.sidebar.multiselect(
    "Credit Score",
    df["Credit_Score_Band"].dropna().unique(),
    default=list(df["Credit_Score_Band"].dropna().unique())
)

# Apply filters
filtered_df = df[
    (df["Geography"].isin(countries)) &
    (df["Gender"].isin(genders)) &
    (df["Age_Group"].isin(age_groups)) &
    (df["Credit_Score_Band"].isin(credit_bands))
]

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_customers = len(filtered_df)
churned = int(filtered_df["Exited"].sum())
churn_rate = (churned / total_customers * 100) if total_customers else 0
avg_balance = filtered_df["Balance"].mean() if total_customers else 0

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned:,}")
col3.metric("Overall Churn Rate", f"{churn_rate:.2f}%")
col4.metric("Average Balance", f"€{avg_balance:,.0f}")

st.divider()

# -----------------------------
# Overall Churn
# -----------------------------
st.subheader("📊 Overall Churn Distribution")

churn_counts = filtered_df["Exited"].value_counts().reindex([0, 1], fill_value=0)

fig, ax = plt.subplots()
ax.bar(["Retained", "Churned"], churn_counts.values)
ax.set_ylabel("Customers")
ax.set_title("Retained vs Churned Customers")
st.pyplot(fig)

# -----------------------------
# Geography Analysis
# -----------------------------
st.subheader("🌍 Geography-wise Churn Analysis")

geo = filtered_df.groupby("Geography").agg(
    Customers=("Exited", "count"),
    Churned=("Exited", "sum")
).reset_index()

geo["Churn Rate (%)"] = geo["Churned"] / geo["Customers"] * 100

st.dataframe(geo, use_container_width=True)

fig, ax = plt.subplots()
ax.bar(geo["Geography"], geo["Churn Rate (%)"])
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Country")
st.pyplot(fig)

# -----------------------------
# Age Analysis
# -----------------------------
st.subheader("👥 Age Group Churn Analysis")

age_data = filtered_df.groupby("Age_Group", observed=False)["Exited"].agg(
    Customers="count",
    Churned="sum"
).reset_index()

age_data["Churn Rate (%)"] = (
    age_data["Churned"] / age_data["Customers"] * 100
)

st.dataframe(age_data, use_container_width=True)

# -----------------------------
# Tenure Analysis
# -----------------------------
st.subheader("⏳ Tenure-wise Churn Analysis")

tenure_data = filtered_df.groupby("Tenure_Group", observed=False)["Exited"].agg(
    Customers="count",
    Churned="sum"
).reset_index()

tenure_data["Churn Rate (%)"] = (
    tenure_data["Churned"] / tenure_data["Customers"] * 100
)

st.dataframe(tenure_data, use_container_width=True)

# -----------------------------
# Credit Score Analysis
# -----------------------------
st.subheader("💳 Credit Score Churn Analysis")

credit_data = filtered_df.groupby(
    "Credit_Score_Band", observed=False
)["Exited"].agg(
    Customers="count",
    Churned="sum"
).reset_index()

credit_data["Churn Rate (%)"] = (
    credit_data["Churned"] / credit_data["Customers"] * 100
)

st.dataframe(credit_data, use_container_width=True)

# -----------------------------
# Balance Analysis
# -----------------------------
st.subheader("💰 Balance Segment Analysis")

balance_data = filtered_df.groupby(
    "Balance_Segment", observed=False
)["Exited"].agg(
    Customers="count",
    Churned="sum"
).reset_index()

balance_data["Churn Rate (%)"] = (
    balance_data["Churned"] / balance_data["Customers"] * 100
)

st.dataframe(balance_data, use_container_width=True)

# -----------------------------
# High Value Customer Churn
# -----------------------------
st.subheader("⭐ High-Value Customer Churn Explorer")

high_value = filtered_df[
    filtered_df["Balance"] >= filtered_df["Balance"].quantile(0.75)
]

hv_customers = len(high_value)
hv_churned = int(high_value["Exited"].sum())

hv_churn_rate = (
    hv_churned / hv_customers * 100
    if hv_customers else 0
)

c1, c2, c3 = st.columns(3)

c1.metric("High-Value Customers", f"{hv_customers:,}")
c2.metric("High-Value Churners", f"{hv_churned:,}")
c3.metric("High-Value Churn Rate", f"{hv_churn_rate:.2f}%")

# -----------------------------
# Active Member Analysis
# -----------------------------
st.subheader("📱 Engagement vs Churn")

active_data = filtered_df.groupby("IsActiveMember")["Exited"].agg(
    Customers="count",
    Churned="sum"
).reset_index()

active_data["Churn Rate (%)"] = (
    active_data["Churned"] / active_data["Customers"] * 100
)

active_data["Member Status"] = active_data["IsActiveMember"].map({
    0: "Inactive",
    1: "Active"
})

st.dataframe(
    active_data[
        ["Member Status", "Customers", "Churned", "Churn Rate (%)"]
    ],
    use_container_width=True
)

# -----------------------------
# Churned vs Retained Financial Profile
# -----------------------------
st.subheader("📈 Churned vs Retained Financial Profile")

profile = filtered_df.groupby("Exited").agg(
    Average_Balance=("Balance", "mean"),
    Average_Salary=("EstimatedSalary", "mean"),
    Average_CreditScore=("CreditScore", "mean"),
    Average_Age=("Age", "mean")
).reset_index()

profile["Customer Status"] = profile["Exited"].map({
    0: "Retained",
    1: "Churned"
})

st.dataframe(
    profile[
        [
            "Customer Status",
            "Average_Balance",
            "Average_Salary",
            "Average_CreditScore",
            "Average_Age"
        ]
    ],
    use_container_width=True
)

# -----------------------------
# Drill-down Customer View
# -----------------------------
st.subheader("🔍 Customer Drill-down")

show_customers = st.checkbox("Show filtered customer records")

if show_customers:
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# -----------------------------
# Key Insights
# -----------------------------
st.subheader("💡 Key Insights")

if len(filtered_df) > 0:
    highest_geo = geo.loc[geo["Churn Rate (%)"].idxmax(), "Geography"]
    highest_geo_rate = geo["Churn Rate (%)"].max()

    highest_age = age_data.loc[
        age_data["Churn Rate (%)"].idxmax(),
        "Age_Group"
    ]

    st.write(
        f"• Overall churn rate for the selected customers is "
        f"**{churn_rate:.2f}%**."
    )

    st.write(
        f"• **{highest_geo}** has the highest geographic churn rate "
        f"at approximately **{highest_geo_rate:.2f}%**."
    )

    st.write(
        f"• The age segment with the highest churn rate is "
        f"**{highest_age}**."
    )

    st.write(
        f"• High-value customers have a churn rate of "
        f"**{hv_churn_rate:.2f}%**."
    )

    st.write(
        "• These insights can help banks identify high-risk customer "
        "segments and design targeted retention strategies."
    )

st.success("Analysis completed successfully!")
