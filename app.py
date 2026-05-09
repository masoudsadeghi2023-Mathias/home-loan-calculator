import streamlit as st

# -----------------------------
# Beräkning av månadskostnad för bolån
# -----------------------------
def monthly_payment(loan, annual_interest_percent, years):
    r = annual_interest_percent / 100 / 12
    n = years * 12

    if r == 0:
        return loan / n

    payment = loan * (r * (1 + r)**n) / ((1 + r)**n - 1)
    return payment


# -----------------------------
# Beräkning av Lagfart och Pantbrev
# -----------------------------
def extra_costs(price, loan, existing_pantbrev):
    lagfart = price * 0.015 + 825

    if loan > existing_pantbrev:
        pantbrev = (loan - existing_pantbrev) * 0.02 + 375
    else:
        pantbrev = 375

    return lagfart, pantbrev, lagfart + pantbrev


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Bolånekalkyl – Sverige", layout="centered")

st.title("🏡 Bolånekalkyl för husköp i Sverige")
st.write("Mobilanpassad kalkylator för bolån, lagfart och pantbrev.")

# Inmatningar
price = st.number_input("Köpeskilling (kr)", min_value=0, value=850000)
cash = st.number_input("Kontantinsats (kr)", min_value=0, value=150000)

# Automatisk beräkning av bolån
loan = max(price - cash, 0)
st.info(f"💰 Bolån (automatiskt beräknat): **{loan:,.0f} kr**")

interest = st.number_input("Ränta (%)", min_value=0.0, value=3.0)
years = st.number_input("Återbetalningstid (år)", min_value=1, value=30)
monthly_cost = st.number_input("Månadsavgift / Driftkostnad (kr)", min_value=0, value=2500)
existing_pantbrev = st.number_input("Befintliga pantbrev (kr)", min_value=0, value=200000)

# Beräkning
if st.button("Beräkna"):
    monthly = monthly_payment(loan, interest, years)
    total_monthly = monthly + monthly_cost
    lagfart, pantbrev, extra_total = extra_costs(price, loan, existing_pantbrev)

    st.subheader("Resultat")

    st.metric("Månadskostnad för lånet", f"{monthly:,.0f} kr")
    st.metric("Total månadskostnad", f"{total_monthly:,.0f} kr")

    st.write("---")
    st.subheader("Köpkostnader")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Lagfartskostnad", f"{lagfart:,.0f} kr")
    with col2:
        st.metric("Pantbrevskostnad", f"{pantbrev:,.0f} kr")

    st.success(f"Totala köpkostnader: **{extra_total:,.0f} kr**")
