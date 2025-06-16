# =============================================================================
# PLOTTING COMPONENTS PAGE
# =============================================================================
"""
Plotting Components Dashboard Page

This module contains reusable plotting functions and demonstrations
for the main dashboard application.
"""

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
import polars as pl
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import inspect
from datetime import date
from typing import Optional

# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================

# Chart styling constants
CHART_COLORS = {
    "orange": "#FF6200",
    "blue": "#0131FF", 
    "gray": "#C7D2FF",
    "success": "#00AA44",
    "warning": "#FFB800",
    "danger": "#FF4B4B"
}

FORMAT_TEMPLATES = {
    "number": "{text:,.0f}",
    "percentage": "{text:.1%}",
    "currency": "${text:,.0f}M",
    "decimal": "{text:,.2f}"
}

CHART_DEFAULTS = {
    "n_points": 12,
    "tick_angle": 45,
    "date_format": "%B %y",
    "text_position": "top center",
    "line_shape": "linear",
    "mode": "lines+markers+text"
}

# =============================================================================
# CORE PLOTTING FUNCTIONS
# =============================================================================

def plot_line_chart(
    df: pl.DataFrame,
    date_col: str,
    y_values: str,
    y_format: str = FORMAT_TEMPLATES["number"],
    title: str = "Line Chart",
    color: str = CHART_COLORS["orange"],
    n_points: int = CHART_DEFAULTS["n_points"],
    tick_angle: int = CHART_DEFAULTS["tick_angle"],
    date_format: str = CHART_DEFAULTS["date_format"],
) -> go.Figure:
    """
    Create a single line chart with customizable styling.
    
    Args:
        df: Polars DataFrame containing the data
        date_col: Name of the date column
        y_values: Name of the y-axis values column
        y_format: Format string for y-axis labels
        title: Chart title
        color: Line color
        n_points: Number of data points to display
        tick_angle: Angle for x-axis tick labels
        date_format: Date format for x-axis labels
    
    Returns:
        Plotly Figure object
    """
    plot_data = df.sort(pl.col(date_col)).tail(n_points)

    fig = px.line(plot_data, x=date_col, y=y_values, text=y_values)

    fig.update_traces(
        textposition=CHART_DEFAULTS["text_position"],
        texttemplate=f'<b style="color:white;">%{y_format}</b>',
        line=dict(color=color),
    )

    fig.update_layout(
        title=title,
        xaxis=dict(
            tickvals=plot_data[date_col],
            ticktext=[d.strftime(date_format) for d in plot_data[date_col]],
            tickangle=tick_angle,
        ),
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig


def plot_dual_line_chart(
    df: pl.DataFrame,
    date_col: str,
    y1_col: str,
    y2_col: str,
    title: str,
    y1_name: str,
    y2_name: str,
    y1_color: str = CHART_COLORS["blue"],
    y2_color: str = CHART_COLORS["gray"],
    y1_format: str = FORMAT_TEMPLATES["number"],
    y2_format: str = FORMAT_TEMPLATES["percentage"],
    date_format: str = CHART_DEFAULTS["date_format"],
    tick_angle: int = CHART_DEFAULTS["tick_angle"],
    n_points: int = CHART_DEFAULTS["n_points"],
) -> go.Figure:
    """
    Create a dual-axis line chart with two different metrics.
    
    Args:
        df: Polars DataFrame containing the data
        date_col: Name of the date column
        y1_col: Name of the first y-axis column
        y2_col: Name of the second y-axis column
        title: Chart title
        y1_name: Display name for first metric
        y2_name: Display name for second metric
        y1_color: Color for first line
        y2_color: Color for second line
        y1_format: Format string for first metric
        y2_format: Format string for second metric
        date_format: Date format for x-axis labels
        tick_angle: Angle for x-axis tick labels
        n_points: Number of data points to display
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    plot_data = df.sort(date_col).tail(n_points)

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=plot_data[date_col],
            y=plot_data[y1_col],
            name=y1_name,
            line=dict(color=y1_color),
            line_shape=CHART_DEFAULTS["line_shape"],
            mode=CHART_DEFAULTS["mode"],
            text=plot_data[y1_col],
            textposition=CHART_DEFAULTS["text_position"],
            texttemplate=f"%{y1_format}",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=plot_data[date_col],
            y=plot_data[y2_col],
            name=y2_name,
            line=dict(color=y2_color),
            line_shape=CHART_DEFAULTS["line_shape"],
            mode=CHART_DEFAULTS["mode"],
            text=plot_data[y2_col],
            textposition=CHART_DEFAULTS["text_position"],
            texttemplate=f"%{y2_format}",
        )
    )

    fig.update_layout(
        title=title,
        xaxis=dict(
            tickvals=plot_data[date_col],
            ticktext=[d.strftime(date_format) for d in plot_data[date_col]],
            tickangle=tick_angle,
        ),
        margin=dict(t=50, b=50, l=50, r=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def plot_bar_chart(
    df: pl.DataFrame,
    x_axis: str,
    y_values: str,
    title: str = "Bar Chart",
    color: str = CHART_COLORS["orange"],
    value_column: str = "Monto_Efectivo",
    scale_factor: int = 1_000_000,
    n_points: int = CHART_DEFAULTS["n_points"],
) -> go.Figure:
    """
    Create a bar chart with customizable styling.
    
    Args:
        df: Polars DataFrame containing the data
        x_axis: Name of the x-axis column
        y_values: Name of the y-axis values column
        title: Chart title
        color: Bar color
        value_column: Column to scale (for monetary values)
        scale_factor: Factor to scale values by
        n_points: Number of data points to display
    
    Returns:
        Plotly Figure object
    """
    plot_data = df.with_columns(pl.col(value_column) / scale_factor).tail(n_points)

    fig = px.bar(plot_data, x=x_axis, y=y_values)

    fig.update_traces(
        textposition="outside",
        texttemplate=f'<b style="color:white;">{FORMAT_TEMPLATES["currency"]}</b>',
        marker=dict(color=color),
    )

    fig.update_layout(
        title=title,
        xaxis=dict(
            tickvals=plot_data[x_axis],
            ticktext=[d.strftime("%B %Y") for d in plot_data[x_axis]],
            tickangle=CHART_DEFAULTS["tick_angle"],
        ),
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def show_function_code(func, label: Optional[str] = None):
    """Display function source code in an expandable section."""
    display_label = label or f"📝 {func.__name__}"
    
    with st.expander(display_label):
        st.code(inspect.getsource(func), language='python')


def create_demo_data() -> pl.DataFrame:
    """Generate sample data for chart demonstrations."""
    np.random.seed(42)  # For reproducible demo data
    
    date_df = pl.DataFrame({
        "date": pl.date_range(
            start=date(2022, 1, 1), 
            end=date(2024, 1, 1), 
            eager=True, 
            interval="1mo"
        ),
    })
    
    return date_df.with_columns([
        pl.lit(np.random.randint(500, 2000, size=date_df.height)).alias("Value1"),
        pl.lit(np.random.randint(800, 1500, size=date_df.height)).alias("Value2"),
        pl.lit(np.random.randint(1000000, 5000000, size=date_df.height)).alias("Monto_Efectivo"),
    ])


def render_chart_section(
    chart_fig: go.Figure, 
    chart_function, 
    column, 
    chart_key: str,
    show_code: bool = True
):
    """Render a chart with optional source code display."""
    # Render the chart
    column.plotly_chart(chart_fig, use_container_width=True, key=chart_key)
    
    # Show source code if requested
    if show_code:
        with column:
            show_function_code(chart_function)

# =============================================================================
# PAGE CONTENT FUNCTIONS
# =============================================================================

def render_page_header():
    """Render the page header and description."""
    st.title("📊 Plotting Components")
    st.markdown("""
    This page demonstrates the reusable plotting components available in the dashboard.
    Each chart type includes customizable parameters and displays its source code for reference.
    """)


def render_data_preview(data: pl.DataFrame):
    """Render the data preview section."""
    with st.expander("📋 View Sample Data", expanded=False):
        st.dataframe(data.head(10), use_container_width=True)
        st.caption(f"Dataset contains {data.height:,} rows and {data.width} columns")


def render_chart_gallery(data: pl.DataFrame):
    """Render the main chart gallery."""
    st.subheader("📈 Chart Gallery")
    
    # Primary charts
    col1, col2 = st.columns(2)
    
    # Single line chart
    line_chart = plot_line_chart(
        df=data,
        date_col="date",
        y_values="Value1",
        title="Monthly Trend - Value 1",
        color=CHART_COLORS["orange"],
    )
    
    # Dual line chart
    dual_chart = plot_dual_line_chart(
        df=data,
        date_col="date",
        y1_col="Value1",
        y2_col="Value2",
        title="Comparative Analysis",
        y1_name="Primary Metric",
        y2_name="Secondary Metric",
        y2_format=FORMAT_TEMPLATES["number"],  # Override default
    )
    
    render_chart_section(line_chart, plot_line_chart, col1, "demo_line_chart")
    render_chart_section(dual_chart, plot_dual_line_chart, col2, "demo_dual_chart")





# =============================================================================
# MAIN PAGE FUNCTION
# =============================================================================

def show_plotting_page():
    """
    Main function to render the plotting components page.
    Call this function from your main dashboard app.
    """
    # Page header
    render_page_header()
    
    # Generate demo data
    demo_data = create_demo_data()
    
    # Data preview
    render_data_preview(demo_data)
    
    st.divider()
    
    # Chart gallery
    render_chart_gallery(demo_data)
     
    # Footer info
    st.markdown("---")
    st.caption("💡 **Tip**: All charts are responsive and will adapt to container width. Source code is available for each chart type.")


# =============================================================================
# STANDALONE EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    # Configure page only when running standalone
    st.set_page_config(
        page_title="Plotting Components", 
        page_icon="📊", 
        layout="wide"
    )
    
    # Run the page
    show_plotting_page()