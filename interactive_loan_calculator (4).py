# 📱 Investment Loan Calculator with Live Comparison + Pros & Cons

import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Investment Loan Calculator", layout="centered")

st.title("📊 Property Investment Loan Strategy Comparison")

with st.expander("📌 Owner-Occupied Property (Custom Strategy)", expanded=True):
    owner_value = st.number_input("Owner Property Value ($)", value=550000)
    owner_price = st.number_input("Owner Purchase Price ($)", value=450000)
    owner_loan = st.number_input("Owner Loan Amount ($)", value=300000)
    equity_used = st.number_input("Equity Accessed for Investment ($)", value=140000)
    owner_rate = st.number_input("Owner Loan Interest Rate (%)", value=5.84, step=0.01) / 100

with st.expander("🏠 Investment Property (Custom Strategy)", expanded=True):
    invest_value = st.number_input("Investment Property Value ($)", value=600000)
    invest_price = st.number_input("Investment Purchase Price ($)", value=450000)
    invest_loan = st.number_input("Direct Investment Loan ($)", value=340000)
    equity_rate = st.number_input("Equity Loan Interest Rate (%)", value=5.84, step=0.01) / 100
    invest_rate = st.number_input("Investment Loan Interest Rate (%)", value=6.19, step=0.01) / 100

with st.expander("🏦 Bank Proposal Inputs (Editable)", expanded=False):
    bank_home_loan = st.number_input("Bank: Owner Loan Amount ($)", value=270000)
    bank_home_rate = st.number_input("Bank: Owner Loan Rate (%)", value=5.84, step=0.01) / 100
    bank_invest_loan = st.number_input("Bank: Investment Loan Amount ($)", value=480000)
    bank_invest_rate = st.number_input("Bank: Investment Loan Rate (%)", value=6.19, step=0.01) / 100

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

# Custom Strategy
owner_repay = monthly_payment(owner_loan, owner_rate, n)
equity_repay = monthly_payment(equity_used, equity_rate, n)
invest_repay = monthly_payment(invest_loan, invest_rate, n)
total_repay_annual = (equity_repay + invest_repay) * 12
rent_annual = rent_weekly * 52
interest_equity = equity_used * equity_rate
interest_invest = invest_loan * invest_rate
tax_savings = (interest_equity + interest_invest) * tax_rate
net_cost = total_repay_annual - rent_annual - tax_savings + expenses_annual
future_value = invest_value * ((1 + growth_rate) ** loan_term)
capital_gain = future_value - invest_price
sale_costs = future_value * sale_costs_percent
cgt = (capital_gain * cgt_discount) * tax_rate
net_sale_profit = future_value - (equity_used + invest_loan) - sale_costs - cgt

# Bank Proposal Calculation
bank_owner_repay = monthly_payment(bank_home_loan, bank_home_rate, n)
bank_invest_repay = monthly_payment(bank_invest_loan, bank_invest_rate, n)
bank_total_repay_annual = bank_invest_repay * 12
bank_interest = bank_invest_loan * bank_invest_rate
bank_tax_savings = bank_interest * tax_rate
bank_net_cost = bank_total_repay_annual - rent_annual - bank_tax_savings + expenses_annual
bank_net_sale_profit = future_value - bank_invest_loan - sale_costs - ((future_value - invest_price) * cgt_discount * tax_rate)

# --- Display Results ---
st.subheader("📋 Repayment Summary")
col1, col2 = st.columns(2)
with col1:
    st.metric("Custom: Owner Repayment", f"${owner_repay:,.2f}")
    st.metric("Custom: Equity Loan", f"${equity_repay:,.2f}")
    st.metric("Custom: Investment Loan", f"${invest_repay:,.2f}")
    st.metric("Custom: Net Annual Cost", f"${net_cost:,.0f}")
with col2:
    st.metric("Bank: Owner Repayment", f"${bank_owner_repay:,.2f}")
    st.metric("Bank: Investment Loan", f"${bank_invest_repay:,.2f}")
    st.metric("Bank: No Equity Used", "N/A")
    st.metric("Bank: Net Annual Cost", f"${bank_net_cost:,.0f}")

st.subheader("🏁 30-Year Sale Projection")
col3, col4 = st.columns(2)
with col3:
    st.metric("Custom: Future Value", f"${future_value:,.0f}")
    st.metric("Custom: Net Profit After Sale", f"${net_sale_profit:,.0f}")
with col4:
    st.metric("Bank: Future Value", f"${future_value:,.0f}")
    st.metric("Bank: Net Profit After Sale", f"${bank_net_sale_profit:,.0f}")

# --- Pros & Cons ---
st.subheader("📊 Strategy Pros & Cons")

custom_pros = ["Maximises tax-deductible debt", "Uses equity effectively", "Greater flexibility with splits"]
custom_cons = ["Higher upfront repayments", "More complex structure"]

bank_pros = ["Simple loan structure", "Lower repayments short-term"]
bank_cons = ["Less efficient use of equity", "Less flexibility"]

if net_sale_profit > bank_net_sale_profit:
    custom_pros.append("Higher projected long-term profit")
else:
    bank_pros.append("Higher projected long-term profit")

st.markdown("### ✅ Custom Strategy")
st.markdown("**Pros:**\n- " + "\n- ".join(custom_pros))
st.markdown("**Cons:**\n- " + "\n- ".join(custom_cons))

st.markdown("### 🏦 Bank Proposal")
st.markdown("**Pros:**\n- " + "\n- ".join(bank_pros))
st.markdown("**Cons:**\n- " + "\n- ".join(bank_cons))

# --- Downloadable Results ---
comparison_df = pd.DataFrame({
    "Metric": [
        "Owner Monthly Repayment (Custom)",
        "Investment Monthly Repayment (Custom)",
        "Net Annual Cost (Custom)",
        "Net Profit After Sale (Custom)",
        "Owner Monthly Repayment (Bank)",
        "Investment Monthly Repayment (Bank)",
        "Net Annual Cost (Bank)",
        "Net Profit After Sale (Bank)"
    ],
    "Amount": [
        owner_repay,
        invest_repay,
        net_cost,
        net_sale_profit,
        bank_owner_repay,
        bank_invest_repay,
        bank_net_cost,
        bank_net_sale_profit
    ]
})

st.download_button(
    label="📥 Download Comparison CSV",
    data=comparison_df.to_csv(index=False),
    file_name="loan_strategy_comparison.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Live comparison of your custom strategy vs. bank proposal, including pros & cons.")
