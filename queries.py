"""All SQL queries used by the dashboard.

"""
import pandas as pd
import streamlit as st
from sqlalchemy import text


# ---------- 1. Business Overview ----------

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


# ---------- 2. Sales Analysis ----------

@st.cache_data(ttl=600)
def get_revenue_trend(_engine):
    """Total revenue per month."""
    query = text("""
        SELECT DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
               SUM(f.total_order_value) AS revenue
        FROM order_features f
        JOIN orders o ON f.order_id = o.order_id
        GROUP BY month
        ORDER BY month
    """)
    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def get_revenue_by_category(_engine):
    """Top 10 product categories by revenue."""
    query = text("""
        SELECT p.product_category_name AS category,
               SUM(oi.price + oi.freight_value) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY category
        ORDER BY revenue DESC
        LIMIT 10
    """)
    return pd.read_sql(query, _engine)


# ---------- 3. Customer Analysis ----------

@st.cache_data(ttl=600)
def get_customers_by_state(_engine):
    """Number of customers per state (demographics)."""
    query = text("""
        SELECT customer_state AS state, COUNT(*) AS customers
        FROM customers
        GROUP BY state
        ORDER BY customers DESC
    """)
    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def get_repeat_vs_new(_engine):
    """Compare repeat customers vs one-time (new) customers."""
    query = text("""
        SELECT is_repeat_customer,
               COUNT(*) AS customers,
               AVG(customer_total_spending) AS avg_spending
        FROM customer_features
        GROUP BY is_repeat_customer
    """)
    return pd.read_sql(query, _engine)


# ---------- 4. Seller & Product Analysis ----------

@st.cache_data(ttl=600)
def get_top_sellers(_engine):
    """Top 10 sellers by revenue."""
    query = text("""
        SELECT seller_id, seller_state, seller_order_count, seller_revenue
        FROM seller_features
        ORDER BY seller_revenue DESC
        LIMIT 10
    """)
    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def get_category_metrics(_engine):
    """Top 10 categories by number of items sold, with average price."""
    query = text("""
        SELECT p.product_category_name AS category,
               COUNT(*) AS items_sold,
               AVG(oi.price) AS avg_price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY category
        ORDER BY items_sold DESC
        LIMIT 10
    """)
    return pd.read_sql(query, _engine)


# ---------- 5. Delivery Analysis ----------

@st.cache_data(ttl=600)
def get_delivery_summary(_engine):
    """On-time delivery rate and average delivery time."""
    query = text("""
        SELECT
            AVG(delivery_days) AS avg_delivery_days,
            SUM(CASE WHEN delivery_delay_days <= 0 THEN 1 ELSE 0 END) AS on_time_orders,
            COUNT(delivery_days) AS delivered_orders
        FROM order_features
        WHERE delivery_days IS NOT NULL
    """)
    return pd.read_sql(query, _engine).iloc[0]


@st.cache_data(ttl=600)
def get_delivery_by_state(_engine):
    """Average delivery time and delay per customer state (bottlenecks)."""
    query = text("""
        SELECT c.customer_state AS state,
               AVG(f.delivery_delay_days) AS avg_delay,
               AVG(f.delivery_days) AS avg_delivery_days
        FROM order_features f
        JOIN customers c ON f.customer_id = c.customer_id
        WHERE f.delivery_days IS NOT NULL
        GROUP BY state
        ORDER BY avg_delay DESC
    """)
    return pd.read_sql(query, _engine)


# ---------- 6. Customer Experience ----------

@st.cache_data(ttl=600)
def get_review_distribution(_engine):
    """How many reviews were given at each star rating (1-5)."""
    query = text("""
        SELECT review_score, COUNT(*) AS reviews
        FROM reviews
        GROUP BY review_score
        ORDER BY review_score
    """)
    return pd.read_sql(query, _engine)


@st.cache_data(ttl=600)
def get_review_vs_delivery(_engine):
    """Average delivery delay for each review score."""
    query = text("""
        SELECT r.review_score,
               AVG(f.delivery_delay_days) AS avg_delay
        FROM reviews r
        JOIN order_features f ON r.order_id = f.order_id
        WHERE f.delivery_days IS NOT NULL
        GROUP BY r.review_score
        ORDER BY r.review_score
    """)
    return pd.read_sql(query, _engine)
