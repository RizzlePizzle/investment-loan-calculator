# Enhanced Investment Loan Calculator – Phase 1 Build

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(page_title="Advanced Loan Calculator", layout="centered")
st.title("📊 Investment Loan Calculator – Enhanced Edition")

# --- Inputs ---
with st.sidebar:
    st.header("🏠 Property Details")
    owner_loan = st.number_input("Owner Loan ($)", value=300000)
    equity_used = st.number_input("Equity Used for Investment ($)", value=140000)
    invest_loan = st.number_input("Investment Loan ($)", value=340000)
    loan_term = st.number_input("Loan Term (Years)", value=30)
    interest_only_years = st.slider("Interest-Only Period (Years)", 0, 10, 1)

    st.header("📈 Rates & Rent")
    owner_rate = st.number_input("Owner Rate (%)", value=5.84) / 100
    invest_rate = st.number_input("Investment Rate (%)", value=6.19) / 100
    rent_weekly = st.number_input("Weekly Rent ($)", value=450)
    expenses_annual = st.number_input("Annual Expenses ($)", value=3500)
    tax_rate = st.number_input("Marginal Tax Rate (%)", value=37) / 100
    growth_rate = st.number_input("Capital Growth Rate (%)", value=4.0) / 100
    invest_price = st.number_input("Purchase Price ($)", value=450000)

# --- Functions ---
def loan_schedule(principal, rate, years, interest_only):
    balance = principal
    values = []
    r_monthly = rate / 12
    n_total = years * 12
    n_io = interest_only * 12
    n_pi = n_total - n_io

    io_payment = balance * r_monthly
    pi_payment = balance * r_monthly * (1 + r_monthly) ** n_pi / ((1 + r_monthly) ** n_pi - 1) if r_monthly > 0 else balance / n_pi

    for month in range(1, n_total + 1):
        year = (month - 1) // 12 + 1
        if month <= n_io:
            interest = balance * r_monthly
            principal_paid = 0
            payment = io_payment
        else:
            interest = balance * r_monthly
            principal_paid = pi_payment - interest
            payment = pi_payment
        balance -= principal_paid
        values.append((year, balance, payment, interest, principal_paid))

    df = pd.DataFrame(values, columns=["Year", "Balance", "Payment", "Interest", "Principal"])
    summary = df.groupby("Year").sum().reset_index()
    return summary

# --- Calculations ---
rent_annual = rent_weekly * 52

schedule = loan_schedule(equity_used + invest_loan, invest_rate, loan_term, interest_only_years)
schedule["Net Cash Flow"] = rent_annual - schedule["Payment"] - expenses_annual + schedule["Interest"] * tax_rate
schedule["Equity"] = invest_price * ((1 + growth_rate) ** schedule["Year"]) - schedule["Balance"]

# --- Charts ---
st.subheader("📈 Forecast Charts")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=schedule["Year"], y=schedule["Balance"], mode="lines+markers", name="Loan Balance"))
fig1.add_trace(go.Scatter(x=schedule["Year"], y=schedule["Equity"], mode="lines+markers", name="Equity Built"))
fig1.update_layout(title="Loan Balance vs Equity Over Time", xaxis_title="Year", yaxis_title="Amount ($)")
st.plotly_chart(fig1, use_container_width=True)

fig2 = go.Figure()
fig2.add_trace(go.Bar(x=schedule["Year"], y=schedule["Net Cash Flow"], name="Net Cash Flow"))
fig2.update_layout(title="Annual Net Cash Flow", xaxis_title="Year", yaxis_title="Amount ($)")
st.plotly_chart(fig2, use_container_width=True)

# --- Table + Export ---
st.subheader("📊 30-Year Forecast Table")
st.dataframe(schedule.style.format({"Balance": "$ {:,.0f}", "Payment": "$ {:,.0f}", "Interest": "$ {:,.0f}", "Principal": "$ {:,.0f}", "Net Cash Flow": "$ {:,.0f}", "Equity": "$ {:,.0f}"}))
st.download_button("📥 Download Forecast CSV", schedule.to_csv(index=False), file_name="loan_forecast.csv", mime="text/csv")

# --- Stub: Recommendations ---
st.subheader("🧠 Recommendations")
if interest_only_years > 0:
    st.info("You're using an interest-only period. Ensure you transition to P&I early enough to build equity.")
if invest_rate > owner_rate:
    st.info("Investment loan has a higher rate. Consider negotiating fixed/variable options to lower cost.")

st.caption("Phase 1 complete: Charts, Interest-Only toggle, Forecast Table, Download. Next: scenario save, API, PDF.")
