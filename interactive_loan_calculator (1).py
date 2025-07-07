# 📱 Polished & Mobile-Responsive Investment Loan Calculator

import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Investment Loan Calculator", layout="centered")

st.title("📊 Property Investment Loan Calculator")

with st.expander("📌 Owner-Occupied Property", expanded=True):
    owner_value = st.number_input("Owner Property Value ($)", value=550000)
    owner_price = st.number_input("Owner Purchase Price ($)", value=450000)
    owner_loan = st.number_input("Owner Loan Amount ($)", value=300000)
    equity_used = st.number_input("Equity Accessed for Investment ($)", value=140000)
    owner_rate = st.number_input("Owner Loan Interest Rate (%)", value=5.84, step=0.01) / 100

with st.expander("🏠 Investment Property", expanded=True):
    invest_value = st.number_input("Investment Property Value ($)", value=600000)
    invest_price = st.number_input("Investment Purchase Price ($)", value=450000)
    invest_loan = st.number_input("Direct Investment Loan ($)", value=340000)
    equity_rate = st.number_input("Equity Loan Interest Rate (%)", value=5.84, step=0.01) / 100
    invest_rate = st.number_input("Investment Loan Interest Rate (%)", value=6.19, step=0.01) / 100

with st.expander("💸 Rental Income & Costs", expanded=True):
    rent_weekly = st.number_input("Weekly Rent ($)", value=450)
    expenses_annual = st.number_input("Annual Expenses ($)", value=3500)
    tax_rate = st.number_input("Marginal Tax Rate (%)", value=37, step=1) / 100

with st.expander("📈 Capital Growth & Sale", expanded=True):
    loan_term = st.number_input("Loan Term (Years)", value=30)
    growth_rate = st.number_input("Annual Capital Growth Rate (%)", value=4.0, step=0.1) / 100
    sale_costs_percent = st.number_input("Sale Costs (% of Sale Price)", value=3.0, step=0.1) / 100
    cgt_discount = st.number_input("Capital Gains Discount (%)", value=50.0, step=0.1) / 100

# --- Calculations ---
n = loan_term * 12

def monthly_payment(P, r, n):
    r_monthly = r / 12
    return P * r_monthly * (1 + r_monthly)**n / ((1 + r_monthly)**n - 1) if r > 0 else P / n

owner_repay = monthly_payment(owner_loan, owner_rate, n)
equity_repay = monthly_payment(equity_used, equity_rate, n)
invest_repay = monthly_payment(invest_loan, invest_rate, n)

total_repay_annual = (equity_repay + invest_repay) * 12
rent_annual = rent_weekly * 52

interest_equity = equity_used * equity_rate
interest_invest = invest_loan * invest_rate
tax_savings = (interest_equity + interest_invest) * tax_rate

net_cost = total_repay_annual - rent_annual - tax_savings + expenses_annual

# Sale Projection
future_value = invest_value * ((1 + growth_rate) ** loan_term)
capital_gain = future_value - invest_price
sale_costs = future_value * sale_costs_percent
cgt = (capital_gain * cgt_discount) * tax_rate
net_sale_profit = future_value - (equity_used + invest_loan) - sale_costs - cgt

# --- Display Results ---
st.subheader("📋 Summary")
col1, col2 = st.columns(2)
with col1:
    st.metric("Owner Monthly Repayment", f"${owner_repay:,.2f}")
    st.metric("Equity Loan Monthly", f"${equity_repay:,.2f}")
    st.metric("Investment Monthly", f"${invest_repay:,.2f}")

with col2:
    st.metric("Annual Rent", f"${rent_annual:,.0f}")
    st.metric("Tax Savings", f"${tax_savings:,.0f}")
    st.metric("Net Annual Cost", f"${net_cost:,.0f}")

st.subheader("🏁 30-Year Sale Projection")
st.metric("Future Property Value", f"${future_value:,.0f}")
st.metric("Net Profit After Sale", f"${net_sale_profit:,.0f}")

# --- Downloadable Results ---
results_df = pd.DataFrame({
    "Metric": [
        "Owner Monthly Repayment",
        "Equity Loan Monthly Repayment",
        "Investment Loan Monthly Repayment",
        "Annual Rental Income",
        "Tax Savings from Interest",
        "Final Net Annual Cost",
        "Future Property Value",
        "Net Profit After Sale"
    ],
    "Amount": [
        owner_repay,
        equity_repay,
        invest_repay,
        rent_annual,
        tax_savings,
        net_cost,
        future_value,
        net_sale_profit
    ]
})

st.download_button(
    label="📥 Download Results as CSV",
    data=results_df.to_csv(index=False),
    file_name="investment_calculator_results.csv",
    mime="text/csv"
)

st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Designed for mobile and desktop – adjust values above to explore scenarios.")
