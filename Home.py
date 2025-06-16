# %%
# Libs
# ==============================================================================
import streamlit as st
import polars as pl


# page settings
# ==============================================================================
st.set_page_config(
    page_title="Home",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
# %%
st.write("Hello from graficos-herramientas!")
st.sidebar.success("Select a demo above.")
