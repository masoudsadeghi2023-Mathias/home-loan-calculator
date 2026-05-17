import streamlit as st

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
        "title": "محاسبه هزینه‌های خرید خانه در سوئد",
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
        "error": "لطفاً مقدار وام و مدت بازپرداخت را به‌درستی وارد کنید."
    },
    "sv": {
        "title": "Beräkna bostadskostnader i Sverige",
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
        "error": "Vänligen ange korrekta värden."
    },
    "en": {
        "title": "Home Purchase Cost Calculator (Sweden)",
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
        "error": "Please enter valid values."
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
    except:
        return "en"


# -----------------------------
# رابط Streamlit
# -----------------------------
st.set_page_config(page_title="Home Loan Calculator", page_icon="🏠", layout="centered")

# انتخاب زبان
lang_choice = st.selectbox("Language / زبان / Språk", ["fa", "sv", "en"])
T = LANG[lang_choice]

st.title(T["title"])
st.markdown(T["desc"])

# ورودی‌ها
price = st.number_input(T["price"], min_value=0, value=1_000_000, step=50_000)
cash = st.number_input(T["cash"], min_value=0, value=100_000, step=10_000)
interest = st.number_input(T["interest"], min_value=0.0, value=3.0, step=0.1, format="%.2f")
years = st.number_input(T["years"], min_value=1, value=30, step=1)
monthly_cost = st.number_input(T["monthly_cost"], min_value=0, value=3_000, step=500)
existing_pantbrev = st.number_input(T["pantbrev"], min_value=0, value=0, step=10_000)

# محاسبه خودکار وام
loan = max(price - cash, 0)
st.markdown(f"**{T['loan']}** {fmt(loan)} kr")

# دکمه
if st.button(T["btn"]):
    if loan == 0 or years == 0:
        st.error(T["error"])
    else:
        monthly = monthly_payment(loan, interest, years)
        total = monthly + monthly_cost
        lagfart, pantbrev, extra_total = extra_costs(price, loan, existing_pantbrev)
        total_initial_cash = cash + lagfart + pantbrev

        st.subheader("Resultat / نتایج / Results")

        st.write(f"**{T['monthly']}** {fmt(monthly)} kr")
        st.write(f"**{T['total_monthly']}** {fmt(total)} kr")
        st.write(f"**{T['lagfart']}** {fmt(lagfart)} kr")
        st.write(f"**{T['pantbrev_cost']}** {fmt(pantbrev)} kr")
        st.write(f"**{T['extra_total']}** {fmt(extra_total)} kr")

        st.markdown("---")
        st.write(f"💰 **{T['initial_cash']}** {fmt(total_initial_cash)} kr")
