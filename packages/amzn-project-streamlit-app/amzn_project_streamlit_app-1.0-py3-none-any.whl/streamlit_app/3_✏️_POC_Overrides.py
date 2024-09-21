import streamlit as st
import pandas as pd
from alarms_utils import write_data, get_data

# global variables
alias = 'mhannes'
BUCKET_NAME = 'proto-alarms'
KEY_POC_OVR = 'poc/test_poc_ovr_alarms.csv'


@st.cache_data
def initialize():

    # call function to get data from s3
    poc_ovr = get_data(BUCKET_NAME, KEY_POC_OVR)

    # for debugging
    # poc_ovr = pd.read_csv('test_poc_ovr.csv')

    # filter overrides to just the user that is accessing the tool
    poc_ovr_alias = poc_ovr[poc_ovr.poc == alias].reset_index(drop=True)

    return poc_ovr, poc_ovr_alias


def main():
    st.set_page_config(
        page_title="POC Overrides",
        page_icon="✏️",
        layout="wide",
    )

    st.markdown("# ✏️ POC Overrides")

    with st.spinner('loading POCs and applying overrides'):
        poc_ovr, poc_ovr_alias = initialize()

    # left, right = st.columns([3, 2])

    show = st.toggle('Show How-to', value=False)
    if show:
        st.markdown(
            """
            ### How to use
            When opening the page, the existing overrides for your alias are displayed.  
    
            If you want to **add an entry**, hover over the last, greyed out row and a + will appear. Click on it and a 
            new row is created.  
    
            If you want to **delete an entry**, hover over the first, greyed out column and a checkbox will appear. 
            Select the row and in the small popup bubble on the top right, a trash icon will appear. Click it and 
            the row will be deleted.
    
            You can also make **changes** to existing overrides by clicking into an existing field and edit the values.  
    
            #### What do I need to do if...
            
            If you **want to be notified for an additional POG**, create an entry for that vendor and POG with the 
            action "add".
            
            If you **want to be notified for an additional vendor**, create an entry for that vendor with the 
            action "add".
            
            If you **don't want to be notified for a certain POG**, create an entry for that vendor and POG with 
            the action "ignore".
    
            If you **don't want to be notified for a certain vendor**, create an entry for that vendor with 
            an empty POG Name and the action "ignore".
    
            If you **don't want to be notified at all**, create an entry with an empty vendor and the action "ignore"
    
            """)

    with st.form("input_poc"):
        edited = st.data_editor(
            poc_ovr_alias,
            column_config={
                "marketplace_id": st.column_config.SelectboxColumn(
                    "Marketplace Id",
                    options=[3,4,6,35691,44551],
                    required=True
                    # width='medium',
                    # validate='[A-Z0-9]'
                ),
                "vendor_code": st.column_config.TextColumn(
                    "Vendor Code",
                    # width='medium',
                    # validate='[A-Z0-9]'
                ),
                "pog_name": st.column_config.TextColumn(
                    "POG Name",
                    width='medium'
                ),
                "function": st.column_config.SelectboxColumn(
                    "Function",
                    # width='medium'
                    options=['ISM', 'VM', 'AVS'],
                    required=True
                ),
                "poc": st.column_config.TextColumn(
                    "POC",
                    disabled=True,
                    width='small',
                    default=alias
                ),
                "action": st.column_config.SelectboxColumn(
                    "Action",
                    # width='medium',
                    required=True,
                    options=['add', 'ignore']
                )
                ,
            },
            num_rows='dynamic',
            hide_index=True)
        submit = st.form_submit_button("Submit")

        status = st.info("Not yet uploaded. Click Submit to upload")

    if submit:
        # filter overrides all other users, except the one making changes
        poc_ovr = poc_ovr[poc_ovr.poc != alias]
        # append unchanged data from other users and changed data from user
        poc_ovr = pd.concat([poc_ovr, edited])

        write_data(poc_ovr, BUCKET_NAME, KEY_POC_OVR)

        status.success("Uploaded! Please refresh the page to see changes")


if __name__ == '__main__':
    main()
