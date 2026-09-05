"""All SQL queries used by the Cart2Insights dashboard."""

import pandas as pd
import streamlit as st
from sqlalchemy import text


# ============================================================
# 1. BUSINESS OVERVIEW
# ============================================================

@st.cache_data(ttl=600)
def get_kpis(_engine):
    """Top-level numbers: revenue, orders, customers, sellers, AOV."""
    query = text("""
        SELECT
            (SELECT SUM(total_order_value) FROM order_features) AS total_revenue,
            (SELECT COUNT(*) FROM orders) AS total_orders,
            (SELECT COUNT(*) FROM customers) AS total_customers,
            (SELECT COUNT(*) FROM sellers) AS total_sellers,
            (SELECT AVG(total_order_value) FROM order_features) AS avg_order_value
    """)

    return pd.read_sql(query, _engine).iloc[0]


@st.cache_data(ttl=600)
def avg_review(_engine):
    """Overall average customer review score."""
    query = text("""
        SELECT AVG(review_score) AS score
        FROM reviews
    """)

    return pd.read_sql(query, _engine).iloc[0]["score"]


# ============================================================
# 2. SALES ANALYSIS
# ============================================================

@st.cache_data(ttl=600)
def get_revenue_trend(_engine):
    """Total revenue per month."""
    query = text("""
        SELECT
            DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
            SUM(f.total_order_value) AS revenue
        FROM order_features f
        JOIN orders o
            ON f.order_id = o.order_id
        GROUP BY month
        ORDER BY month
    """)

    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def get_revenue_by_category(_engine):
    """Top 10 product categories by revenue."""
    query = text("""
        SELECT
            p.product_category_name AS category,
            SUM(oi.price + oi.freight_value) AS revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY category
        ORDER BY revenue DESC
        LIMIT 10
    """)

    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def top_products(_engine):
    """Top 10 products by number of items sold."""
    query = text("""
        SELECT
            product_id AS product,
            COUNT(*) AS items_sold
        FROM order_items
        GROUP BY product_id
        ORDER BY items_sold DESC
        LIMIT 10
    """)

    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def sales_by_state(_engine):
    """Revenue by customer state."""
    query = text("""
        SELECT
            c.customer_state AS state,
            SUM(f.total_order_value) AS revenue
        FROM order_features f
        JOIN customers c
            ON f.customer_id = c.customer_id
        GROUP BY c.customer_state
        ORDER BY revenue DESC
    """)

    return pd.read_sql(query, _engine)


# ============================================================
# 3. CUSTOMER ANALYSIS
# ============================================================

@st.cache_data(ttl=600)
def get_customers_by_state(_engine):
    """Number of customers per state (demographics)."""
    query = text("""
        SELECT
            customer_state AS state,
            COUNT(*) AS customers
        FROM customers
        GROUP BY state
        ORDER BY customers DESC
    """)

    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def get_repeat_vs_new(_engine):
    """Compare repeat customers vs one-time customers."""
    query = text("""
        SELECT
            is_repeat_customer,
            COUNT(*) AS customers,
            AVG(customer_total_spending) AS avg_spending
        FROM customer_features
        GROUP BY is_repeat_customer
    """)

    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def top_customers(_engine):
    """Top 10 customers by total spending."""
    query = text("""
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

    return pd.read_sql(query, _engine)


# ============================================================
# 4. SELLER & PRODUCT ANALYSIS
# ============================================================

@st.cache_data(ttl=600)
def get_top_sellers(_engine):
    """Top 10 sellers by revenue."""
    query = text("""
        SELECT
            seller_id,
            seller_state,
            seller_order_count,
            seller_revenue
        FROM seller_features
        ORDER BY seller_revenue DESC
        LIMIT 10
    """)

    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def get_category_metrics(_engine):
    """Top 10 categories by number of items sold, with average price."""
    query = text("""
        SELECT
            p.product_category_name AS category,
            COUNT(*) AS items_sold,
            AVG(oi.price) AS avg_price
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY category
        ORDER BY items_sold DESC
        LIMIT 10
    """)

    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def seller_ratings(_engine):
    """Top 10 sellers by average review rating."""
    query = text("""
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

    return pd.read_sql(query, _engine)


# ============================================================
# 5. DELIVERY ANALYSIS
# ============================================================

@st.cache_data(ttl=600)
def get_delivery_summary(_engine):
    """On-time delivery rate and average delivery time."""
    query = text("""
        SELECT
            AVG(delivery_days) AS avg_delivery_days,
            SUM(
                CASE
                    WHEN delivery_delay_days <= 0 THEN 1
                    ELSE 0
                END
            ) AS on_time_orders,
            COUNT(delivery_days) AS delivered_orders
        FROM order_features
        WHERE delivery_days IS NOT NULL
    """)

    return pd.read_sql(query, _engine).iloc[0]


@st.cache_data(ttl=600)
def delivery_status(_engine):
    """Compare on-time and delayed orders."""
    query = text("""
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

    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def get_delivery_by_state(_engine):
    """Average delivery time and delay per customer state."""
    query = text("""
        SELECT
            c.customer_state AS state,
            AVG(f.delivery_delay_days) AS avg_delay,
            AVG(f.delivery_days) AS avg_delivery_days
        FROM order_features f
        JOIN customers c
            ON f.customer_id = c.customer_id
        WHERE f.delivery_days IS NOT NULL
        GROUP BY state
        ORDER BY avg_delay DESC
    """)

    return pd.read_sql(query, _engine)


# ============================================================
# 6. CUSTOMER EXPERIENCE
# ============================================================

@st.cache_data(ttl=600)
def get_review_distribution(_engine):
    """Number of reviews at each star rating."""
    query = text("""
        SELECT
            review_score,
            COUNT(*) AS reviews
        FROM reviews
        GROUP BY review_score
        ORDER BY review_score
    """)

    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def reviews_by_category(_engine):
    """Top 10 product categories by average review rating."""
    query = text("""
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

    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def get_review_vs_delivery(_engine):
    """Average delivery delay for each review score."""
    query = text("""
        SELECT
            r.review_score,
            AVG(f.delivery_delay_days) AS avg_delay
        FROM reviews r
        JOIN order_features f
            ON r.order_id = f.order_id
        WHERE f.delivery_days IS NOT NULL
        GROUP BY r.review_score
        ORDER BY r.review_score
    """)

    return pd.read_sql(query, _engine)
