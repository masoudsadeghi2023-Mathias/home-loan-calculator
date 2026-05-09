import streamlit as st

# -----------------------------
# محاسبه قسط ماهانه وام
# -----------------------------
def monthly_payment(loan, annual_interest_percent, years):
    r = annual_interest_percent / 100 / 12
    n = years * 12

    if r == 0:
        return loan / n

    payment = loan * (r * (1 + r)**n) / ((1 + r)**n - 1)
    return payment


# -----------------------------
# محاسبه Lagfart و Pantbrev
# -----------------------------
def extra_costs(price, loan, existing_pantbrev):
    lagfart = price * 0.015 + 825

    if loan > existing_pantbrev:
        pantbrev = (loan - existing_pantbrev) * 0.02 + 375
    else:
        pantbrev = 375

    return lagfart, pantbrev, lagfart + pantbrev


# -----------------------------
# رابط Streamlit
# -----------------------------
st.set_page_config(page_title="محاسبه‌گر خرید خانه در سوئد", layout="centered")

st.title("🏡 محاسبه‌گر خرید خانه در سوئد")
st.write("نسخه موبایل‌پسند — ساخته شده با Streamlit")

# ورودی‌ها
price = st.number_input("قیمت خانه (kr)", min_value=0, value=850000)
cash = st.number_input("پرداخت نقدی (kr)", min_value=0, value=150000)

# محاسبه خودکار وام
loan = max(price - cash, 0)
st.info(f"💰 مبلغ وام (محاسبه خودکار): **{loan:,.0f} kr**")

interest = st.number_input("درصد بهره وام (%)", min_value=0.0, value=3.0)
years = st.number_input("مدت بازپرداخت (سال)", min_value=1, value=30)
monthly_cost = st.number_input("هزینه ماهانه خانه (kr)", min_value=0, value=2500)
existing_pantbrev = st.number_input("Pantbrev موجود (kr)", min_value=0, value=200000)

# دکمه محاسبه
if st.button("محاسبه"):
    monthly = monthly_payment(loan, interest, years)
    total_monthly = monthly + monthly_cost
    lagfart, pantbrev, extra_total = extra_costs(price, loan, existing_pantbrev)

    st.subheader("نتایج محاسبه")

    st.metric("قسط ماهانه", f"{monthly:,.0f} kr")
    st.metric("قسط + هزینه ماهانه", f"{total_monthly:,.0f} kr")

    st.write("---")
    st.subheader("هزینه‌های جانبی خرید")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Lagfart", f"{lagfart:,.0f} kr")
    with col2:
        st.metric("Pantbrev", f"{pantbrev:,.0f} kr")

    st.success(f"جمع هزینه‌های جانبی: **{extra_total:,.0f} kr**")
