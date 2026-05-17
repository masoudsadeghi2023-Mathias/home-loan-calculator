import streamlit as st

def inject_pwa():
    st.markdown("""
    <link rel="manifest" href="/.streamlit/public/manifest.json">
    <script>
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/.streamlit/public/service-worker.js');
      }
    </script>
    """, unsafe_allow_html=True)

inject_pwa()

# -----------------------------
# توابع محاسباتی
# -----------------------------
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


def fmt(x):
    return f"{x:,.0f}".replace(",", ".")


# -----------------------------
# متن‌ها برای سه زبان
# -----------------------------
LANG = {
    "fa": {
        "title": "محاسبه هزینه‌های خرید خانه در سوئد🏠",
        "desc": "این ابزار برای محاسبه قسط، هزینه‌های جانبی و کل نقدینگی لازم در ابتدای خرید است.",
        "price": "قیمت خانه (kr)",
        "cash": "پرداخت نقدی (kr)",
        "loan": "مبلغ وام (محاسبه خودکار):",
        "interest": "درصد بهره (%)",
        "years": "مدت بازپرداخت (سال)",
        "monthly_cost": "هزینه ماهانه خانه (kr)",
        "pantbrev": "Pantbrev موجود (kr)",
        "btn": "محاسبه",
        "monthly": "قسط ماهانه:",
        "total_monthly": "قسط + هزینه ماهانه خانه:",
        "lagfart": "هزینه Lagfart:",
        "pantbrev_cost": "هزینه Pantbrev:",
        "extra_total": "جمع هزینه‌های جانبی:",
        "initial_cash": "کل مبلغ نقدی لازم در ابتدای خرید:",
        "error": "لطفاً مقدار وام و مدت بازپرداخت را به‌درستی وارد کنید.",
        "results_header": "نتایج محاسبه"
    },
    "sv": {
        "title": "Beräkna bostadskostnader i Sverige🏠",
        "desc": "Detta verktyg beräknar månadskostnad, lagfart, pantbrev och kontantinsats.",
        "price": "Köpeskilling (kr)",
        "cash": "Kontantinsats (kr)",
        "loan": "Bolån (automatisk beräkning):",
        "interest": "Ränta (%)",
        "years": "Återbetalningstid (år)",
        "monthly_cost": "Månadsavgift / Driftkostnad (kr)",
        "pantbrev": "Befintliga pantbrev (kr)",
        "btn": "Beräkna",
        "monthly": "Månadskostnad för lånet:",
        "total_monthly": "Total månadskostnad:",
        "lagfart": "Lagfartskostnad:",
        "pantbrev_cost": "Pantbrevskostnad:",
        "extra_total": "Totala köpkostnader:",
        "initial_cash": "Total kontantinsats vid köp:",
        "error": "Vänligen ange korrekta värden.",
        "results_header": "Resultat"
    },
    "en": {
        "title": "Home Purchase Cost Calculator (Sweden)🏠",
        "desc": "This tool calculates mortgage payments, fees, and total upfront cash needed.",
        "price": "Home price (kr)",
        "cash": "Down payment (kr)",
        "loan": "Loan amount (auto-calculated):",
        "interest": "Interest rate (%)",
        "years": "Repayment period (years)",
        "monthly_cost": "Monthly housing cost (kr)",
        "pantbrev": "Existing pantbrev (kr)",
        "btn": "Calculate",
        "monthly": "Monthly mortgage payment:",
        "total_monthly": "Total monthly cost:",
        "lagfart": "Lagfart fee:",
        "pantbrev_cost": "Pantbrev fee:",
        "extra_total": "Total extra fees:",
        "initial_cash": "Total upfront cash required:",
        "error": "Please enter valid values.",
        "results_header": "Results"
    }
}


# -----------------------------
# تشخیص زبان مرورگر
# -----------------------------
def detect_browser_language():
    try:
        lang_header = st.context.headers.get("Accept-Language", "")
        lang_header = lang_header.lower()
        if "fa" in lang_header:
            return "fa"
        if "sv" in lang_header:
            return "sv"
        return "en"
    except Exception:
        return "en"


# -----------------------------
# تنظیم صفحه
# -----------------------------
st.set_page_config(
    page_title="Home Loan Calculator",
    page_icon="🏠",
    layout="centered"
)

# -----------------------------
# انتخاب زبان (با پیش‌فرض مرورگر)
# -----------------------------
default_lang = detect_browser_language()
lang_order = ["fa", "sv", "en"]

lang_choice = st.selectbox(
    "Language / زبان / Språk",
    lang_order,
    index=lang_order.index(default_lang) if default_lang in lang_order else 0
)

T = LANG[lang_choice]

st.title(T["title"])
st.markdown(T["desc"])

# -----------------------------
# CSS برای UI فشرده و لیبل کنار باکس
# -----------------------------
st.markdown("""
<style>
.row-container {
    display: flex;
    align-items: center;
    margin-bottom: 8px;
}
.row-label {
    width: 45%;
    font-size: 15px;
    padding-right: 10px;
}
.row-input {
    width: 55%;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# ورودی‌ها (فشرده واقعی با columns)
# -----------------------------

# قیمت خانه
c1, c2 = st.columns([1, 2])
with c1:
    st.write(T["price"])
with c2:
    price = st.number_input(
        T["price"],
        min_value=0,
        value=1_000_000,
        step=50_000,
        label_visibility="collapsed"
    )

# پرداخت نقدی
c1, c2 = st.columns([1, 2])
with c1:
    st.write(T["cash"])
with c2:
    cash = st.number_input(
        T["cash"],
        min_value=0,
        value=100_000,
        step=10_000,
        label_visibility="collapsed"
    )

# مبلغ وام (خودکار)
loan = max(price - cash, 0)
st.markdown(f"**{T['loan']}** {fmt(loan)} kr")

# درصد بهره
c1, c2 = st.columns([1, 2])
with c1:
    st.write(T["interest"])
with c2:
    interest = st.number_input(
        T["interest"],
        min_value=0.0,
        value=3.0,
        step=0.1,
        format="%.2f",
        label_visibility="collapsed"
    )

# مدت بازپرداخت
c1, c2 = st.columns([1, 2])
with c1:
    st.write(T["years"])
with c2:
    years = st.number_input(
        T["years"],
        min_value=1,
        value=30,
        step=1,
        label_visibility="collapsed"
    )

# هزینه ماهانه
c1, c2 = st.columns([1, 2])
with c1:
    st.write(T["monthly_cost"])
with c2:
    monthly_cost = st.number_input(
        T["monthly_cost"],
        min_value=0,
        value=2500,
        step=500,
        label_visibility="collapsed"
    )

# Pantbrev
c1, c2 = st.columns([1, 2])
with c1:
    st.write(T["pantbrev"])
with c2:
    existing_pantbrev = st.number_input(
        T["pantbrev"],
        min_value=0,
        value=0,
        step=10_000,
        label_visibility="collapsed"
    )

# -----------------------------
# دکمه و محاسبه
# -----------------------------
if st.button(T["btn"]):
    if loan == 0 or years == 0:
        st.error(T["error"])
    else:
        monthly = monthly_payment(loan, interest, years)
        total = monthly + monthly_cost
        lagfart, pantbrev_fee, extra_total = extra_costs(price, loan, existing_pantbrev)
        total_initial_cash = cash + lagfart + pantbrev_fee

        st.subheader(T["results_header"])
        st.write(f"**{T['monthly']}** {fmt(monthly)} kr")
        st.write(f"**{T['total_monthly']}** {fmt(total)} kr")
        st.write(f"**{T['lagfart']}** {fmt(lagfart)} kr")
        st.write(f"**{T['pantbrev_cost']}** {fmt(pantbrev_fee)} kr")
        st.write(f"**{T['extra_total']}** {fmt(extra_total)} kr")

        st.markdown("---")
        st.write(f"💰 **{T['initial_cash']}** {fmt(total_initial_cash)} kr")
        st.write("Created by Masoud❤️")
