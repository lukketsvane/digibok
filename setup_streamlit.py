import warnings
warnings.filterwarnings('ignore')
import streamlit as st
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('global.developmentMode', False)
st.script_run_ctx.add_script_run_ctx()
st._is_running_with_streamlit = True
import app
