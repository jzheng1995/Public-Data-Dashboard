import pandas as pd
import streamlit as st
from helper import *


df = load_data()


province_count = df['PROV'].value_counts().reset_index()


st.write("# Canada Labour Characteristics")


st.write("The following dashboard is based on the Monthly Labour Characteristics data collected by Statistics Canada (Statcan). More information on this dataset and study can be found at [Statcan](https://www150.statcan.gc.ca/n1/pub/71m0001x/71m0001x2021001-eng.htm).")

"## Number of study participants across nation"
st_map = fmap()

