import streamlit as st

page_1 = st.Page("page1.py", title = "Main page", icon=":material/add_circle:", default = True)
page_2 = st.Page("page2.py", title = "Second page", icon=":material/delete:")
pg = st.navigation([page_1, page_2])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()