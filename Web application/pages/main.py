import streamlit as st
from PIL import Image

def app():
    st.title('Find Homes in Seattle')
    page_bg_img = '''
        <style>
        .reportview-container {
            background: url("https://images.unsplash.com/photo-1567016376408-0226e4d0c1ea?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=634&q=80")
        }
        </style>
        '''
    st.markdown(page_bg_img, unsafe_allow_html=True)