import streamlit as st
from fydjob.multiapp import MultiApp
from fydjob.apps import summary, skill, jd


app = MultiApp()
st.markdown("""
# Find Your Dream Job""")

app.add_app("Bird's Eye View", summary.app)
app.add_app("Skill Search", skill.app)
app.add_app("Similar Job Offer Search", jd.app)

app.run()