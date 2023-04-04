# Importing libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.figure_factory as ff
from google.oauth2 import service_account
from google.cloud import bigquery

st.set_page_config(
    page_title="Twitter_EDA",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title('Twitter_EDA')
st.write('idk what im doing with my life')

cat_input = []
num_input = []
# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query("SELECT * FROM `branding-nlp-project.twitter_data.tweets_merged`")
st.write((type(rows)))
st.write((len(rows)))
st.write(rows[0])
st.write(rows[1])
st.write((type(rows[1])))
