import pandas as pd
import streamlit as st
from helper import *


df = load_data()


province_count = df['PROV'].value_counts().reset_index()


st.write("# Canada Labour Characteristics")


st.write("This dashboard app is made from data extracted from the Monthly Labour Characteristics July 2024 survey by Statistics Canada (StatCan). More information on this dataset and study can be found on the [StatCan website](https://www150.statcan.gc.ca/n1/pub/71m0001x/71m0001x2021001-eng.htm).")

"## Number of study participants in July 2024"
st_map = fmap()

