import altair as alt
import streamlit as st
from helper import *


df = load_data()
alt.data_transformers.enable("vegafusion")

bar = alt.Chart(df).mark_bar().encode(
    alt.X('PROV', title = 'Province',axis=alt.Axis(labels = False)).sort('-y'),
    alt.Y(aggregate='count', type='quantitative', title = 'Count'),
    color = 'PROV'
).properties(
    width=800,
    height=300
)

st.altair_chart(bar)