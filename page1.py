import pandas as pd
import streamlit as st
from helper import *

def main():
    df = load_data()


    province_count = df['PROV'].value_counts().reset_index()


    st.write("# Canada Labour Characteristics")


    st.write("This dashboard app is made from data extracted from the Monthly Labour Characteristics July 2024 survey by Statistics Canada (StatCan). More information on this dataset and study can be found on the [StatCan website](https://www150.statcan.gc.ca/n1/pub/71m0001x/71m0001x2021001-eng.htm). The full app is hosted on [streamlit cloud](https://public-data-dashboard-zaexazhwocap2sucygqzre.streamlit.app/).")

    "## Number of study participants in July 2024"
    st_map = fmap(width = 1000)


col1, col2, col3 = st.columns([1,9,1])

with col2:
    main()

