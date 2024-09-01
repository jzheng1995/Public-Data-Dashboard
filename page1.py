import pandas as pd
import streamlit as st
from helper import *


df = load_data()


province_count = df['PROV'].value_counts().reset_index()



st_map = fmap()
