import streamlit as st
from multiapp import MultiApp
from apps import summary, skill

app = MultiApp()
st.markdown("""
### test test test""")

app.add_app("Bird's eye view", summary.app)
app.add_app("Skills", skill.py)