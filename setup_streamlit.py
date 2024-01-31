import warnings
warnings.filterwarnings('ignore')
import streamlit as st
st.set_option('server.headless', True)
st.set_option('server.address', '0.0.0.0')
import app
