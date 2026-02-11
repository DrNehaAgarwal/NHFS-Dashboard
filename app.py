# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="NFHS India Dashboard", layout="wide")

st.title("📊 NFHS 4 vs NFHS 5 Dashboard - India")
st.markdown("Comparison of health indicators across States and Districts")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("India_Change.csv", low_memory=False)
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

state = st.sidebar.selectbox(
    "Select State",
    options=sorted(df["State"].unique())
)

filtered_state = df[df["State"] == state]

district = st.sidebar.selectbox(
    "Select District",
    options=sorted(filtered_state["District Name"].unique())
)

filtered_district = filtered_state[filtered_state["District Name"] == district]

category = st.sidebar.selectbox(
    "Select Category",
    options=sorted(filtered_district["Category"].unique())
)

filtered_category = filtered_district[filtered_district["Category"] == category]

indicator = st.sidebar.selectbox(
    "Select Indicator",
    options=sorted(filtered_category["Indicator"].unique())
)

final_df = filtered_category[filtered_category["Indicator"] == indicator]

# -----------------------------
# KPI Metrics
# -----------------------------
if not final_df.empty:
    nfhs5 = float(final_df["NFHS 5"].values[0])
    nfhs4 = float(final_df["NFHS 4"].values[0])
    change = float(final_df["Change"].values[0])

    col1, col2, col3 = st.columns(3)

    col1.metric("NFHS 5", f"{nfhs5}%")
    col2.metric("NFHS 4", f"{nfhs4}%")
    col3.metric("Change", f"{change}%", delta=change)

    st.markdown("---")

    # -----------------------------
    # Bar Chart Comparison
    # -----------------------------
    chart_df = pd.DataFrame({
        "Survey": ["NFHS 4", "NFHS 5"],
        "Value": [nfhs4, nfhs5]
    })

    fig = px.bar(
        chart_df,
        x="Survey",
        y="Value",
        text="Value",
        title="NFHS 4 vs NFHS 5 Comparison"
    )

    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # District Level Comparison (All Indicators)
    # -----------------------------
    st.markdown("### 📌 All Indicators for Selected District")

    district_all = filtered_district[filtered_district["Category"] == category]

    fig2 = px.bar(
        district_all,
        x="Indicator",
        y="Change",
        title="Change Across Indicators",
    )

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("No data available for selected filters.")
