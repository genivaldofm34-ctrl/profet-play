import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Teste Google Sheets")

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

st.write(df)
