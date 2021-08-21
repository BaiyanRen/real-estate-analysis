import streamlit as st
import webbrowser

def app():
    st.header('About')
    st.markdown('''
    Hi there! Welcome to my app "Find Homes in Seattle"!
    
    This app collects real-estate data in Seattle from [Zillow](https://www.zillow.com/) and [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction).
    
    These data were used to visualize the market, and build the machine learning model to predict house price.
    
    Feel free to explore the app and find your home!''')

    st.markdown('''
    
    *My name is Baiyan. I am a fellow of The Data Incubator. This is my capstone project.*
    
    *I'm willing to hear any comments and answer questions!*''')

    kaggle = 'https://www.kaggle.com/baiyanren'
    linkedin = 'https://www.linkedin.com/in/baiyanren/'
    if st.button('Kaggle'):
        webbrowser.open_new_tab(kaggle)
    if st.button('LinkedIn'):
        webbrowser.open_new_tab(linkedin)
