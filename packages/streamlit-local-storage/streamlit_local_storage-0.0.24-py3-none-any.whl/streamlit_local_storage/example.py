import time 
import streamlit as st
from __init__ import LocalStorage
# from streamlit_local_storage import LocalStorage

st.set_page_config(layout="wide")

localStorage = LocalStorage() 
# 

with st.container(height=1, border=False):
    localStorage.setItem("Jade", "Kyle")
    localStorage.setItem("Jeff", "Jones", key="set_test")
    result = localStorage.getAll() 
    localStorage.refreshItems()

# result = localStorage.getItem("screenStats")
# st.write(result)

result2 = localStorage.getItem("Jade") 
st.write(result2)
# result3 = localStorage.getItem("Mike")
# st.write(result3)

# localStorage.deleteAll()
st.write(result["testing"])
st.write(result["Jeff"])



