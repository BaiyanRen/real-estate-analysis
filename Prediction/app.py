import streamlit as st

from multipage import MultiPage
from pages import visual, zillow, ml

app = MultiPage()

st.title('Find Homes in Seattle')



app.add_page('Real Estate Market Visualization', visual.app)
app.add_page('Searching on Zillow', zillow.app)
app.add_page('House Price Estimation', ml.app)

app.run()