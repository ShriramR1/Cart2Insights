"""Connects to the MySQL database used by the Olist analysis."""

import streamlit as st
from sqlalchemy import create_engine

DB_USER = "olist_user"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_NAME = "olist_ecommerce"


@st.cache_resource
def get_engine():
    """Create one shared database connection for the whole app."""
    url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    return create_engine(url)