"""Cart2Insights - Olist E-Commerce Dashboard

Run with: streamlit run app.py
"""

import streamlit as st

import queries as q
import utils as u
from database import get_engine


# ============================================================
# PAGE CONFIGURATION
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
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🛒 Cart2Insights")

page = st.sidebar.radio(
    "Go to",
    [
        "Business Overview",
        "Sales Analysis",
        "Customer Analysis",
        "Seller & Product Analysis",
        "Delivery Analysis",
        "Customer Experience",
    ],
)


# ============================================================
# 1. BUSINESS OVERVIEW
# ============================================================

if page == "Business Overview":

    st.title("📊 Business Overview")

    kpis = q.get_kpis(engine)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Revenue",
        u.format_currency(kpis["total_revenue"])
    )

    col2.metric(
        "Total Orders",
        u.format_number(kpis["total_orders"])
    )

    col3.metric(
        "Total Customers",
        u.format_number(kpis["total_customers"])
    )

    col4.metric(
        "Total Sellers",
        u.format_number(kpis["total_sellers"])
    )

    col5.metric(
        "Avg Order Value",
        u.format_currency(kpis["avg_order_value"])
    )


# ============================================================
# 2. SALES ANALYSIS
# ============================================================

elif page == "Sales Analysis":

    st.title("💰 Sales Analysis")

    st.subheader("Revenue Over Time")

    trend = q.get_revenue_trend(engine)

    st.line_chart(
        trend.set_index("month")["revenue"]
    )

    st.subheader("Top 10 Categories by Revenue")

    category_revenue = q.get_revenue_by_category(engine)

    st.bar_chart(
        category_revenue.set_index("category")["revenue"]
    )

    st.subheader("Top 10 Products by Items Sold")

    products = q.top_products(engine)

    st.bar_chart(
        products.set_index("product")["items_sold"]
    )

    st.dataframe(
        products,
        use_container_width=True
    )

    st.subheader("Revenue by Customer State")

    location = q.sales_by_state(engine)

    st.bar_chart(
        location.set_index("state")["revenue"]
    )


# ============================================================
# 3. CUSTOMER ANALYSIS
# ============================================================

elif page == "Customer Analysis":

    st.title("👥 Customer Analysis")

    st.subheader("Customers by State")

    states = q.get_customers_by_state(engine)

    st.bar_chart(
        states.set_index("state")["customers"]
    )

    st.subheader("Repeat vs New Customers")

    repeat = q.get_repeat_vs_new(engine)

    repeat["label"] = repeat["is_repeat_customer"].map({
        0: "New",
        1: "Repeat"
    })

    col1, col2 = st.columns(2)

    with col1:

        st.caption("Number of Customers")

        st.bar_chart(
            repeat.set_index("label")["customers"]
        )

    with col2:

        st.caption("Average Spending (R$)")

        st.bar_chart(
            repeat.set_index("label")["avg_spending"]
        )

    st.subheader("Top 10 Customers by Spending")

    customers = q.top_customers(engine)

    st.dataframe(
        customers,
        use_container_width=True
    )


# ============================================================
# 4. SELLER & PRODUCT ANALYSIS
# ============================================================

elif page == "Seller & Product Analysis":

    st.title("🏪 Seller & Product Analysis")

    st.subheader("Top 10 Sellers by Revenue")

    top_sellers = q.get_top_sellers(engine)

    st.dataframe(
        top_sellers,
        use_container_width=True
    )

    st.subheader("Top 10 Categories by Items Sold")

    category_metrics = q.get_category_metrics(engine)

    st.bar_chart(
        category_metrics.set_index("category")["items_sold"]
    )

    st.dataframe(
        category_metrics,
        use_container_width=True
    )

    st.subheader("Top 10 Sellers by Average Rating")

    ratings = q.seller_ratings(engine)

    st.bar_chart(
        ratings.set_index("seller_id")["rating"]
    )

    st.dataframe(
        ratings,
        use_container_width=True
    )


# ============================================================
# 5. DELIVERY ANALYSIS
# ============================================================

elif page == "Delivery Analysis":

    st.title("🚚 Delivery Analysis")

    summary = q.get_delivery_summary(engine)

    on_time_rate = (
        summary["on_time_orders"]
        / summary["delivered_orders"]
        * 100
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "On-Time Delivery Rate",
        u.format_percent(on_time_rate)
    )

    col2.metric(
        "Avg Delivery Time",
        f"{summary['avg_delivery_days']:.1f} days"
    )

    st.subheader("Delivery Status")

    status = q.delivery_status(engine)

    st.bar_chart(
        status.set_index("status")["orders"]
    )

    st.subheader("Average Delivery Delay by State")

    st.caption("Positive = late, negative = early")

    by_state = q.get_delivery_by_state(engine)

    st.bar_chart(
        by_state.set_index("state")["avg_delay"]
    )


# ============================================================
# 6. CUSTOMER EXPERIENCE
# ============================================================

elif page == "Customer Experience":

    st.title("⭐ Customer Experience")

    score = q.avg_review(engine)

    st.metric(
        "Average Review Score",
        f"{score:.2f} / 5"
    )

    st.subheader("Review Score Distribution")

    reviews = q.get_review_distribution(engine)

    st.bar_chart(
        reviews.set_index("review_score")["reviews"]
    )

    st.subheader("Top 10 Categories by Average Rating")

    category = q.reviews_by_category(engine)

    st.bar_chart(
        category.set_index("category")["rating"]
    )

    st.subheader("Average Delivery Delay by Review Score")

    st.caption(
        "Lower review scores tend to come with longer delays"
    )

    review_delay = q.get_review_vs_delivery(engine)

    st.bar_chart(
        review_delay.set_index("review_score")["avg_delay"]
    )
