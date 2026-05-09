import streamlit as st

# ============================
#       TRANSLATIONS
# ============================

translations = {
    "fa": {
        "lang_name": "فارسی 🇮🇷",
        "title": "🏡 محاسبه‌گر خرید خانه در سوئد",
        "subtitle": "نسخه موبایل‌پسند — ساخته شده با Streamlit",

        "price": "قیمت خانه (kr)",
        "cash": "پرداخت نقدی (kr)",
        "loan_auto": "💰 مبلغ وام (محاسبه خودکار):",

        "interest": "درصد بهره وام (%)",
        "years": "مدت بازپرداخت (سال)",
        "monthly_cost": "هزینه ماهانه خانه (kr)",
        "pantbrev_exist": "Pantbrev موجود (kr)",

        "calculate": "محاسبه",
        "results": "نتایج محاسبه",
        "monthly_payment": "قسط ماهانه",
        "total_monthly": "قسط + هزینه ماهانه",

        "extra_costs": "هزینه‌های جانبی خرید",
        "lagfart": "Lagfart",
        "pantbrev": "Pantbrev",
        "extra_total": "جمع هزینه‌های جانبی:",

        "footer": "ساخته شده توسط مسعود ❤️"
    },

    "sv": {
        "lang_name": "Svenska 🇸🇪",
        "title": "🏡 Bolånekalkyl för bostadsköp i Sverige",
        "subtitle": "Mobilvänlig version — byggd med Streamlit",

        "price": "Bostadspris (kr)",
        "cash": "Kontantinsats (kr)",
        "loan_auto": "💰 Lånebelopp (automatiskt beräknat):",

        "interest": "Bolåneränta (%)",
        "years": "Återbetalningstid (år)",
        "monthly_cost": "Månadskostnad för boende (kr)",
        "pantbrev_exist": "Befintliga pantbrev (kr)",

        "calculate": "Beräkna",
        "results": "Beräkningsresultat",
        "monthly_payment": "Månadskostnad lån",
        "total_monthly": "Lån + månadskostnad",

        "extra_costs": "Kostnader vid köp",
        "lagfart": "Lagfart",
        "pantbrev": "Pantbrev",
        "extra_total": "Totala extrakostnader:",

        "footer": "Skapad av Masoud ❤️"
    }
}

# ============================
#       FUNCTIONS
# ============================

def monthly_payment(loan, annual_interest_percent, years):
    r = annual_interest_percent / 100 / 12
    n = years * 12
    if r == 0:
        return loan / n
    return loan * (r * (1 + r)**n) / ((1 + r)**n - 1)


def extra_costs(price, loan, existing_pantbrev):
    lagfart = price * 0.015 + 825
    pantbrev = (loan - existing_pantbrev) * 0.02 + 375 if loan > existing_pantbrev else 375
    return lagfart, pantbrev, lagfart + pantbrev


# ============================
#       STREAMLIT UI
# ============================

st.set_page_config(page_title="Home Loan Calculator", layout="centered")

# Language selector
st.sidebar.title("Language / زبان")
lang = st.sidebar.selectbox(
    "",
    ("fa", "sv"),
    format_func=lambda x: translations[x]["lang_name"]
)
t = translations[lang]

# Title
st.title(t["title"])
st.write(t["subtitle"])

# Inputs
price = st.number_input(t["price"], min_value=0, value=850000)
cash = st.number_input(t["cash"], min_value=0, value=150000)

loan = max(price - cash, 0)
st.info(f"{t['loan_auto']} **{loan:,.0f} kr**")

interest = st.number_input(t["interest"], min_value=0.0, value=3.0)
years = st.number_input(t["years"], min_value=1, value=30)
monthly_cost = st.number_input(t["monthly_cost"], min_value=0, value=2500)
existing_pantbrev = st.number_input(t["pantbrev_exist"], min_value=0, value=200000)

# Button
if st.button(t["calculate"]):
    monthly = monthly_payment(loan, interest, years)
    total_monthly = monthly + monthly_cost
    lagfart, pantbrev, extra_total = extra_costs(price, loan, existing_pantbrev)

    st.subheader(t["results"])
    st.metric(t["monthly_payment"], f"{monthly:,.0f} kr")
    st.metric(t["total_monthly"], f"{total_monthly:,.0f} kr")

    st.write("---")
    st.subheader(t["extra_costs"])

    col1, col2 = st.columns(2)
    with col1:
        st.metric(t["lagfart"], f"{lagfart:,.0f} kr")
    with col2:
        st.metric(t["pantbrev"], f"{pantbrev:,.0f} kr")

    st.success(f"{t['extra_total']} **{extra_total:,.0f} kr**")

# Footer
st.markdown(f"<br><center>{t['footer']}</center>", unsafe_allow_html=True)
