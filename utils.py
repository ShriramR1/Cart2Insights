"""Small formatting helpers used across the dashboard."""


def format_currency(value):
    """Show a number as Brazilian Real currency, e.g. R$ 1,234.56"""
    return f"R$ {value:,.2f}"


def format_number(value):
    """Show a number with thousands separators, e.g. 12,345"""
    return f"{value:,.0f}"


def format_percent(value):
    """Show a number as a percentage, e.g. 87.3%"""
    return f"{value:.1f}%"
