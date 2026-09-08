"""Cart2Insights - Olist E-Commerce Dashboard"""

import streamlit as st

import queries as q
import utils as u
from database import get_engine


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Cart2Insights Dashboard",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

engine = get_engine()


# ============================================================
# DESIGN
# ============================================================

st.markdown("""
<style>
.stApp {
    background-color: #EAEDED;
}

[data-testid="stSidebar"] {
    background-color: #131921;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

h1 {
    color: #131921 !important;
}

h2, h3 {
    color: #232F3E !important;
}

div[data-testid="stMetric"] {
    background-color: white;
    border-top: 4px solid #FF9900;
    border-radius: 8px;
    padding: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}

div[data-testid="stMetric"] label {
    color: #5F6B76 !important;
    font-weight: 600;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #131921 !important;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛒 Cart2Insights")
st.sidebar.caption("Olist E-Commerce Analytics")

page = st.sidebar.radio(
    "EXPLORE",
    [
        "Business Overview",
        "Sales Analysis",
        "Customer Analysis",
        "Seller & Product Analysis",
        "Delivery Analysis",
        "Customer Experience"
    ]
)


# ============================================================
# 1. BUSINESS OVERVIEW
# ============================================================

if page == "Business Overview":

    st.title("Business Overview")
    st.caption("Marketplace performance at a glance")

    k = q.get_kpis(engine)
    score = q.avg_review(engine)

    cols = st.columns(3)

    cols[0].metric(
        "Total Revenue",
        u.format_currency(k["total_revenue"])
    )

    cols[1].metric(
        "Total Orders",
        u.format_number(k["total_orders"])
    )

    cols[2].metric(
        "Total Customers",
        u.format_number(k["total_customers"])
    )

    cols = st.columns(3)

    cols[0].metric(
        "Total Sellers",
        u.format_number(k["total_sellers"])
    )

    cols[1].metric(
        "Average Order Value",
        u.format_currency(k["avg_order_value"])
    )

    cols[2].metric(
        "Average Review Score",
        f"{score:.2f} ⭐"
    )


# ============================================================
# 2. SALES ANALYSIS
# ============================================================

elif page == "Sales Analysis":

    st.title("Sales Analysis")
    st.caption("Revenue, product and location performance")

    trend = q.get_revenue_trend(engine)

    st.subheader("Monthly Revenue Trend")

    st.line_chart(
        trend.set_index("month")["revenue"]
    )

    category = q.get_revenue_by_category(engine)

    st.subheader("Revenue by Category")

    st.bar_chart(
        category.set_index("category")["revenue"]
    )

    products = q.top_products(engine)

    st.subheader("Top-Selling Products")

    st.bar_chart(
        products.set_index("product")["items_sold"]
    )

    location = q.sales_by_state(engine)

    st.subheader("Sales by Location")

    st.bar_chart(
        location.set_index("state")["revenue"]
    )


# ============================================================
# 3. CUSTOMER ANALYSIS
# ============================================================

elif page == "Customer Analysis":

    st.title("Customer Analysis")
    st.caption("Customer distribution, spending and retention")

    states = q.get_customers_by_state(engine)

    st.subheader("Customer Distribution by State")

    st.bar_chart(
        states.set_index("state")["customers"]
    )

    repeat = q.get_repeat_vs_new(engine)

    repeat["label"] = repeat["is_repeat_customer"].map({
        0: "New",
        1: "Repeat"
    })

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("Repeat vs New Customers")

        st.bar_chart(
            repeat.set_index("label")["customers"]
        )

    with c2:

        st.subheader("Customer Spending")

        st.bar_chart(
            repeat.set_index("label")["avg_spending"]
        )

    customers = q.top_customers(engine)

    st.subheader("Top Customers by Spending")

    st.bar_chart(
        customers.set_index("customer_id")["spending"]
    )


# ============================================================
# 4. SELLER & PRODUCT ANALYSIS
# ============================================================

elif page == "Seller & Product Analysis":

    st.title("Seller & Product Analysis")
    st.caption("Seller contribution, ratings and product performance")

    sellers = q.get_top_sellers(engine)

    st.subheader("Top Sellers by Revenue")

    st.bar_chart(
        sellers.set_index("seller_id")["seller_revenue"]
    )

    category = q.get_category_metrics(engine)

    st.subheader("Product / Category Performance")

    st.bar_chart(
        category.set_index("category")["items_sold"]
    )

    ratings = q.seller_ratings(engine)

    st.subheader("Seller Ratings")

    st.bar_chart(
        ratings.set_index("seller_id")["rating"]
    )


# ============================================================
# 5. DELIVERY ANALYSIS
# ============================================================

elif page == "Delivery Analysis":

    st.title("Delivery Analysis")
    st.caption("Delivery speed, delays and location performance")

    summary = q.get_delivery_summary(engine)

    rate = (
        summary["on_time_orders"]
        / summary["delivered_orders"]
        * 100
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "On-Time Delivery",
        u.format_percent(rate)
    )

    c2.metric(
        "Average Delivery Time",
        f'{summary["avg_delivery_days"]:.1f} days'
    )

    status = q.delivery_status(engine)

    st.subheader("On-Time vs Delayed Orders")

    st.bar_chart(
        status.set_index("status")["orders"]
    )

    state = q.get_delivery_by_state(engine)

    st.subheader("Delivery Performance by Location")

    st.caption(
        "Positive = late delivery | Negative = early delivery"
    )

    st.bar_chart(
        state.set_index("state")["avg_delay"]
    )


# ============================================================
# 6. CUSTOMER EXPERIENCE
# ============================================================

elif page == "Customer Experience":

    st.title("Customer Experience")
    st.caption("Reviews, ratings and delivery satisfaction")

    reviews = q.get_review_distribution(engine)

    st.subheader("Review Score Distribution")

    st.bar_chart(
        reviews.set_index("review_score")["reviews"]
    )

    category = q.reviews_by_category(engine)

    st.subheader("Reviews by Category")

    st.bar_chart(
        category.set_index("category")["rating"]
    )

    delay = q.get_review_vs_delivery(engine)

    st.subheader("Rating vs Delivery Performance")

    st.caption(
        "Compare delivery delay with customer review score"
    )

    st.bar_chart(
        delay.set_index("review_score")["avg_delay"]
    )
