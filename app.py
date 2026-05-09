import streamlit as st

# ============================
#       TRANSLATIONS
# ============================

translations = {
    "fa": {
        "lang_name": "فارسی 🇮🇷",
        "title": "محاسبه‌گر وام مسکن",
        "loan_amount": "مبلغ وام (کرون)",
        "interest_rate": "نرخ بهره سالانه (%)",
        "years": "مدت وام (سال)",
        "calculate": "محاسبه",
        "monthly_payment": "قسط ماهانه",
        "footer": "ساخته شده توسط مسعود ❤️"
    },
    "sv": {
        "lang_name": "Svenska 🇸🇪",
        "title": "Bolånekalkylator",
        "loan_amount": "Lånebelopp (SEK)",
        "interest_rate": "Årsränta (%)",
        "years": "Lånetid (år)",
        "calculate": "Beräkna",
        "monthly_payment": "Månadskostnad",
        "footer": "Skapad av Masoud ❤️"
    }
}

# ============================
#       LANGUAGE SELECTOR
# ============================

st.sidebar.title("Language / زبان")
lang = st.sidebar.selectbox(
    "",
    ("fa", "sv"),
    format_func=lambda x: translations[x]["lang_name"]
)

t = translations[lang]

# ============================
#       PAGE TITLE
# ============================

st.title(t["title"])

# ============================
#       USER INPUTS
# ============================

loan = st.number_input(t["loan_amount"], min_value=0, step=10000)
rate = st.number_input(t["interest_rate"], min_value=0.0, step=0.1)
years = st.number_input(t["years"], min_value=1, step=1)

# ============================
#       CALCULATION
# ============================

if st.button(t["calculate"]):
    if rate == 0:
        payment = loan / (years * 12)
    else:
        monthly_rate = rate / 100 / 12
        months = years * 12
        payment = loan * monthly_rate / (1 - (1 + monthly_rate) ** -months)

    st.success(f"{t['monthly_payment']}: {payment:,.0f} SEK")

# ============================
#       FOOTER
# ============================

st.markdown(f"<br><center>{t['footer']}</center>", unsafe_allow_html=True)
