# Advanced Property Investment Loan Calculator with Enhancements

import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Property Investment Calculator", layout="wide")

st.title("📊 Advanced Property Investment Loan Calculator")

st.sidebar.header("Owner-Occupied Property")
owner_value = st.sidebar.number_input("Owner Property Value ($)", value=550000)
owner_price = st.sidebar.number_input("Owner Purchase Price ($)", value=450000)
owner_loan = st.sidebar.number_input("Owner Loan Amount ($)", value=300000)
equity_used = st.sidebar.number_input("Equity Accessed for Investment ($)", value=140000)
owner_rate = st.sidebar.number_input("Owner Loan Interest Rate (%)", value=5.84) / 100

st.sidebar.header("Investment Property")
invest_value = st.sidebar.number_input("Investment Property Value ($)", value=600000)
invest_price = st.sidebar.number_input("Investment Purchase Price ($)", value=450000)
invest_loan = st.sidebar.number_input("Direct Investment Loan ($)", value=340000)
equity_rate = st.sidebar.number_input("Equity Loan Interest Rate (%)", value=5.84) / 100
invest_rate = st.sidebar.number_input("Investment Loan Interest Rate (%)", value=6.19) / 100

st.sidebar.header("Rental and Expenses")
rent_weekly = st.sidebar.number_input("Weekly Rent ($)", value=450)
expenses_annual = st.sidebar.number_input("Annual Expenses ($)", value=3500)
tax_rate = st.sidebar.number_input("Marginal Tax Rate (%)", value=37) / 100
loan_term = st.sidebar.number_input("Loan Term (Years)", value=30)
growth_rate = st.sidebar.number_input("Annual Capital Growth Rate (%)", value=4.0) / 100
sale_costs_percent = st.sidebar.number_input("Sale Costs (% of Sale Price)", value=3.0) / 100
cgt_discount = st.sidebar.number_input("Capital Gains Discount (%)", value=50.0) / 100

# Calculations
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

# Sale projection
total_loan = equity_used + invest_loan
future_value = invest_value * ((1 + growth_rate) ** loan_term)
capital_gain = future_value - invest_price
sale_costs = future_value * sale_costs_percent
cgt = (capital_gain * cgt_discount) * tax_rate
net_sale_profit = future_value - total_loan - sale_costs - cgt

# Output Summary
st.header("📌 Repayment Summary")
st.metric("Owner Loan Monthly Repayment", f"${owner_repay:,.2f}")
st.metric("Equity Loan Monthly Repayment", f"${equity_repay:,.2f}")
st.metric("Investment Loan Monthly Repayment", f"${invest_repay:,.2f}")

st.header("📈 Annual Performance")
st.metric("Annual Rental Income", f"${rent_annual:,.2f}")
st.metric("Tax Savings from Interest", f"${tax_savings:,.2f}")
st.metric("Final Net Annual Cost", f"${net_cost:,.2f}")

st.header("🏁 30-Year Sale Projection")
st.metric("Future Property Value", f"${future_value:,.2f}")
st.metric("Estimated Sale Costs", f"${sale_costs:,.2f}")
st.metric("Capital Gains Tax", f"${cgt:,.2f}")
st.metric("Net Profit After Sale", f"${net_sale_profit:,.2f}")

# Downloadable CSV
results_df = pd.DataFrame({
    "Metric": [
        "Owner Loan Monthly Repayment",
        "Equity Loan Monthly Repayment",
        "Investment Loan Monthly Repayment",
        "Annual Rental Income",
        "Tax Savings from Interest",
        "Final Net Annual Cost",
        "Future Property Value",
        "Estimated Sale Costs",
        "Capital Gains Tax",
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
        sale_costs,
        cgt,
        net_sale_profit
    ]
})

st.download_button(
    label="📥 Download Results as CSV",
    data=results_df.to_csv(index=False),
    file_name="investment_results.csv",
    mime="text/csv"
)
