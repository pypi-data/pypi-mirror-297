import streamlit as st
import boto3

st.set_page_config(
    page_title="COMET - Onboard POC",
    page_icon="🚢",
)

alias = 'mhannes'

st.markdown("# 🚢 Onboard POC")
left, right = st.columns([3, 2])

ses = boto3.client(
    'ses',
    aws_access_key_id='AKIAQKXQNKZFQ7OHMNN4',
    aws_secret_access_key='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',
    region_name="us-east-1"
)

with left:
    clicked = st.button("Verify my E-Mail-Address")

    if clicked:
        ses.verify_email_identity(EmailAddress=alias+'@amazon.com')

with right:
    st.markdown(
        """
        Please click the button on the left to verify your E-Mail-Address and be notified about alarms.
        
        You will receie an E-Mail in your inbox to confirm your identity. Click on the link in the E-Mail to confirm.
        
        **You only have to do this step once**
        """
    )