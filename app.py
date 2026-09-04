"""Cart2Insights - Olist E-Commerce Dashboard"""

import streamlit as st
import pandas as pd
from sqlalchemy import text

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
# ADDITIONAL QUERIES
# ============================================================

@st.cache_data(ttl=600)
def run_query(_engine, sql):
    return pd.read_sql(text(sql), _engine)


def avg_review():
    return run_query(
        engine,
        "SELECT AVG(review_score) AS score FROM reviews"
    ).iloc[0]["score"]


def top_products():
    return run_query(engine, """
        SELECT
            product_id AS product,
            COUNT(*) AS items_sold
        FROM order_items
        GROUP BY product_id
        ORDER BY items_sold DESC
        LIMIT 10
    """)


def sales_by_state():
    return run_query(engine, """
        SELECT
            c.customer_state AS state,
            SUM(f.total_order_value) AS revenue
        FROM order_features f
        JOIN customers c
            ON f.customer_id = c.customer_id
        GROUP BY c.customer_state
        ORDER BY revenue DESC
    """)


def top_customers():
    return run_query(engine, """
        SELECT
            o.customer_id,
            SUM(f.total_order_value) AS spending
        FROM orders o
        JOIN order_features f
            ON o.order_id = f.order_id
        GROUP BY o.customer_id
        ORDER BY spending DESC
        LIMIT 10
    """)


def seller_ratings():
    return run_query(engine, """
        SELECT
            oi.seller_id,
            AVG(r.review_score) AS rating
        FROM order_items oi
        JOIN reviews r
            ON oi.order_id = r.order_id
        GROUP BY oi.seller_id
        ORDER BY rating DESC
        LIMIT 10
    """)


def delivery_status():
    return run_query(engine, """
        SELECT
            CASE
                WHEN delivery_delay_days <= 0 THEN 'On-Time'
                ELSE 'Delayed'
            END AS status,
            COUNT(*) AS orders
        FROM order_features
        WHERE delivery_days IS NOT NULL
        GROUP BY status
    """)


def reviews_by_category():
    return run_query(engine, """
        SELECT
            p.product_category_name AS category,
            AVG(r.review_score) AS rating
        FROM reviews r
        JOIN order_items oi
            ON r.order_id = oi.order_id
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY p.product_category_name
        ORDER BY rating DESC
        LIMIT 10
    """)


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
    score = avg_review()

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

    products = top_products()

    st.subheader("Top-Selling Products")
    st.bar_chart(
        products.set_index("product")["items_sold"]
    )

    location = sales_by_state()

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

    customers = top_customers()

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

    ratings = seller_ratings()

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

    status = delivery_status()

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

    category = reviews_by_category()

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
