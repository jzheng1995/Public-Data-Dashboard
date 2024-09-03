import streamlit as st


import altair as alt
from helper import *


df = load_data()

alt.data_transformers.enable("vegafusion")
selection_prov = alt.selection_single(fields=['PROV'], empty = 'none')
selection_employ= alt.selection_single(fields=['LFSSTAT'], empty = 'none')


demo_vars = ['AGE_12','SEX', 'MARSTAT', 'EDUC', 'IMMIG', 'PROV', 'LFSSTAT']

demo_df = df.groupby(demo_vars).size().reset_index(name = 'count')

base = alt.Chart(demo_df).mark_bar().encode(
    alt.X('PROV:N', title = 'Province',axis=alt.Axis(labels = False)).sort('-y'),
    alt.Y('sum(count):Q', title = 'Number of Records'),
    color=alt.Color('PROV:N', legend=alt.Legend(title="Province"), scale = alt.Scale(scheme='tableau10')),
    tooltip=[
        alt.Tooltip('PROV:N', title='Province: '),
        alt.Tooltip('sum(count)', title='Count: ')
    ],
    stroke=alt.condition(selection_prov, alt.value('white'), alt.value(None)),
    # Conditional stroke width for the selected province
    strokeWidth=alt.condition(selection_prov, alt.value(3), alt.value(0)),
).properties(
    width=500,
    height=300,
).add_selection(selection_prov)

employment = alt.Chart(demo_df).mark_bar().encode(
    x = alt.X('LFSSTAT:N', title = 'Employment Status', axis = alt.Axis(labels = False)),
    y = alt.Y('sum(count)',type = 'quantitative', title = 'Number of Records'),
    color=alt.Color('LFSSTAT:N',scale = alt.Scale(scheme='oranges'), legend=alt.Legend(title="Employment Status")),
    tooltip=[
        alt.Tooltip('PROV:N', title='Province: '),
        alt.Tooltip('LFSSTAT:N', title = 'Status: '),
        alt.Tooltip('sum(count)', title='Count: ')
    ],
    stroke=alt.condition(selection_employ, alt.value('white'), alt.value(None)),
    # Conditional stroke width for the selected province
    strokeWidth=alt.condition(selection_employ, alt.value(3), alt.value(0))
).transform_filter(
    selection_prov
).properties(
    width = 250,
    height = 300
).add_selection(selection_employ)




age = alt.Chart(demo_df).mark_bar().encode(
    x = alt.X('AGE_12:O', title = 'Age Groups', axis = alt.Axis(labels = False)),
    y = alt.Y('sum(count)',type = 'quantitative', title = 'Number of Records'),
    color=alt.Color('AGE_12:N',scale = alt.Scale(scheme='oranges'), legend=alt.Legend(title="Age Group")),
    tooltip=[
        alt.Tooltip('PROV:N', title='Province: '),
        alt.Tooltip('AGE_12:O', title = 'Status: '),
        alt.Tooltip('sum(count)', title='Count: ')
    ]
).transform_filter(
    selection_employ
).transform_filter(
    selection_prov
).properties(
    width = 200,
    height = 300
)

sex = alt.Chart(demo_df).mark_bar().encode(
    x = alt.X('SEX:N', title = 'Sex', axis = alt.Axis(labels = False)),
    y = alt.Y('sum(count)',type = 'quantitative', title = 'Number of Records'),
    color=alt.Color('SEX:N',scale = alt.Scale(scheme='redblue'), legend=alt.Legend(title="Sex Group")),
    tooltip=[
        alt.Tooltip('PROV:N', title='Province: '),
        alt.Tooltip('SEX:N', title = 'Status: '),
        alt.Tooltip('sum(count)', title='Count: ')
    ]
).transform_filter(
    selection_employ
).transform_filter(
    selection_prov
).properties(
    width = 100,
    height = 300
)

educ = alt.Chart(demo_df).mark_bar().encode(
    x = alt.X('EDUC:O', title = 'Education', axis = alt.Axis(labels = False), sort = ['0 to 8 years','Some high school','High school graduate','Some postsecondary','Postsecondary certificate or diploma',"Bachelor's degree","Above bachelor's degree"]),
    y = alt.Y('sum(count)',type = 'quantitative', title = 'Number of Records'),
    color=alt.Color('EDUC:O',scale = alt.Scale(scheme='oranges'), legend=alt.Legend(title="Education Group")).sort(['0 to 8 years','Some high school','High school graduate','Some postsecondary','Postsecondary certificate or diploma',"Bachelor's degree","Above bachelor's degree"]),
    tooltip=[
        alt.Tooltip('PROV:N', title='Province: '),
        alt.Tooltip('EDUC:O', title = 'Status: '),
        alt.Tooltip('sum(count)', title='Count: ')
    ]
).transform_filter(
    selection_employ
).transform_filter(
    selection_prov
).properties(
    width = 200,
    height = 300
)

st.markdown("<h1 style='text-align: center; color: white;'>Explore demographics by Province and Employment 2024</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>Click on a bar from Province and Employment to filter!</h3>", unsafe_allow_html=True)

layer_1 =  alt.hconcat(
    base,
    employment
).resolve_scale(
    color='independent')



layer_2 = alt.hconcat(
    age, educ, sex
).resolve_scale(
    color='independent')

layer_3 = alt.hconcat(
    sex
).resolve_scale(
    color='independent')

layout = alt.vconcat(
    layer_1,
    layer_2
).resolve_scale(
    color='independent')

st.altair_chart(layout)