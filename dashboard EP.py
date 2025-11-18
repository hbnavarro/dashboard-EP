import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt


st.set_page_config(
    page_title="Física no ENEM",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.theme.enable("dark")

df = pd.read_csv("Base de dados - ENEM EPUFABC.csv", sep=",")
