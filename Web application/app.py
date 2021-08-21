import streamlit as st

from multipage import MultiPage
from pages import visual, zillow, ml, main, About

app = MultiPage()



app.add_page('Main', main.app)
app.add_page('About', About.app)
app.add_page('Real Estate Market Visualization', visual.app)
app.add_page('Searching on Zillow', zillow.app)
app.add_page('House Price Estimation', ml.app)

app.run()