import altair as alt
import streamlit as st
from helper import *


df = load_data()
alt.data_transformers.enable("vegafusion")
selection = alt.selection_single(fields=['PROV'], empty = 'none')

df_light =  df.groupby(['PROV', 'LFSSTAT']).size().reset_index(name = 'count')

# base chart
base = alt.Chart(df_light).mark_bar().encode(
    alt.X('PROV', title = 'Province',axis=alt.Axis(labels = False)).sort('-y'),
    alt.Y('sum(count)', type='quantitative', title = 'Number of Records'),
    # Set the color encoding for the bars and customize the legend title
    color=alt.Color('PROV:N', legend=alt.Legend(title="Province"), scale = alt.Scale(scheme='tableau10')),
    # Conditional stroke to highlight the selected province
    stroke=alt.condition(selection, alt.value('white'), alt.value(None)),
    # Conditional stroke width for the selected province
    strokeWidth=alt.condition(selection, alt.value(3), alt.value(0)),
    tooltip=[
        alt.Tooltip('PROV:N', title='Province: '),
        alt.Tooltip('sum(count)', title='Count: ')
    ]
).properties(
    width=500,
    height=300,
)

# provincial employment
employment = alt.Chart(df_light).mark_bar().encode(
    x = alt.X('LFSSTAT:N', title = 'Employment Status', axis = alt.Axis(labels = False)),
    y = alt.Y('sum(count)',type = 'quantitative', title = 'Number of Records'),
    color=alt.Color('LFSSTAT:N',scale = alt.Scale(scheme='oranges'), legend=alt.Legend(title="Employment Status")),
    tooltip=[
        alt.Tooltip('PROV:N', title='Province: '),
        alt.Tooltip('LFSSTAT:N', title = 'Status: '),
        alt.Tooltip('sum(count)', title='Count: ')
    ]
).transform_filter(
    selection
).properties(
    width = 500,
    height = 300
)

texts = alt.Chart(df_light).mark_text(
    align='center',
    baseline='middle',
    dy=-200,  # Adjust the y position of the text
    fontSize=30,
    color = 'white',
    font = 'serif',
    fontWeight = 'bold'
).encode(
    text=alt.condition(selection, 'PROV:N', alt.value(''))  # Only show text when a province is selected
).transform_filter(
    selection
).properties(
    width = 500,
    height = 300
)

base_text = base.add_selection(selection)
employment_text = employment + texts
chart = alt.vconcat(
    base_text,
    employment_text
).resolve_scale(
    color='independent')

# organize page

st.markdown("<h1 style='text-align: center; color: white;'>Labour Characteristics for July 2024</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Click on a bar to examine by Province!</h3>", unsafe_allow_html=True)

st.altair_chart(chart)

