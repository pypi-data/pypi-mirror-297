import streamlit as st

st.set_page_config(
    page_title="COMET",
    page_icon="☄️",
)

st.write('# COMET ☄️')

st.markdown(
    """
    Welcome to the **C**oordinated **O**perational **M**onitoring and **E**scalation **T**ool

    This tool will automatically execute certain checks and notify the relevant POCs via E-Mail. 

    In this interface you can:

    - see data that is triggering an alarm  
    - inspect the POCs  
    - make overrides to the POCs  
    - verify and onboard POCs

    The functionalities are accessible from the side bar on the left.

    **In order to receive notifications, you need to verify your E-Mail-Address first.**  
    **Please visit "Onboard POC" for this.**
    """)
