import time

import streamlit as st
import pandas as pd
from alarms_utils import filter_dataframe, get_data

alias = 'mhannes'

@st.cache_data
def initialize():

    BUCKET_NAME = 'proto-alarms'

    KEY_POC = 'poc/data'
    KEY_POC_OVR = 'poc/test_poc_ovr_alarms.csv'

    poc = get_data(BUCKET_NAME, KEY_POC)
    poc_ovr = get_data(BUCKET_NAME, KEY_POC_OVR)

    # poc = pd.read_csv('test_poc.csv')
    # poc_ovr = pd.read_csv('test_poc_ovr.csv')

    # poc.to_csv('test_poc.csv', index=False)
    # poc_ovr.to_csv('test_poc_ovr.csv', index=False)

    poc_ovr_ignore = poc_ovr[
        (poc_ovr.action == 'ignore') & (poc_ovr.vendor_code.isna())
    ]
    poc_ovr_vendor_add = poc_ovr[
        (poc_ovr.action == 'add') & (poc_ovr.vendor_code.notnull())
    ].drop(columns='action')
    poc_ovr_vendor_ignore = poc_ovr[
        (poc_ovr.action == 'ignore') & (poc_ovr.vendor_code.notnull()) & (poc_ovr.pog_name.isna())
    ]
    poc_ovr_pog_ignore = poc_ovr[
        (poc_ovr.action == 'ignore') & (poc_ovr.vendor_code.notnull()) & (poc_ovr.pog_name.notnull())
    ]

    poc = pd.concat([poc, poc_ovr_vendor_add])

    poc = pd.merge(poc, poc_ovr_pog_ignore, on=['marketplace_id', 'poc', 'function', 'vendor_code', 'pog_name'], how='left')
    poc = poc[poc.action.isna()]
    poc = poc.drop(columns=['action'])

    poc = pd.merge(poc, poc_ovr_vendor_ignore.drop(columns='pog_name'), on=['marketplace_id', 'function', 'poc', 'vendor_code'], how='left')
    poc = poc[poc.action.isna()]
    poc = poc.drop(columns=['action'])

    poc = pd.merge(poc, poc_ovr_ignore.drop(columns=['vendor_code','pog_name']), on=['marketplace_id', 'function', 'poc'], how='left')
    poc = poc[poc.action.isna()]
    poc = poc.drop(columns=['action'])

    poc['pt'] = 'https://badgephotos.corp.amazon.com/?fullsizeimage=1&give404ifmissing=1&uid=' + poc['poc']

    poc = poc[['marketplace_id', 'vendor_code', 'pog_name', 'function', 'poc', 'pt']]

    return poc


def main():
    st.set_page_config(
        page_title="POC Overview",
        page_icon="🕵️‍♀️",
        layout="wide",
    )

    st.markdown("# 🕵️‍♀️ POC Overview")

    with st.spinner('loading POCs and applying overrides'):
        time.sleep(1)
        poc = initialize()

    st.dataframe(
        filter_dataframe(poc, alias),
        column_config={
            "marketplace_id": st.column_config.TextColumn(
                "Marketplace ID",
                width='medium'
            ),
            "vendor_code": st.column_config.TextColumn(
                "Vendor Code",
                width='medium'
            ),
            "pog_name": st.column_config.TextColumn(
                "POG Name",
                width='medium'
            ),
            "function": st.column_config.TextColumn(
                "Function",
                # width='small',
            ),
            "poc": st.column_config.TextColumn(
                "POC",
                # width='medium',
            ),
            "pt": st.column_config.ImageColumn(
                "",
            )
        },
        hide_index=True,
    )


if __name__ == '__main__':
    main()
