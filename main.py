# Importing libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.figure_factory as ff
from google.oauth2 import service_account
from google.cloud import bigquery
import plotly.express as px

class user_input():
    def __init__(self, var, type, data, type_data, input_list):
        self.var = var
        self.type = type
        self.data = data
        self.type_data = type_data
        self.input_list = input_list
        self.get_input()
    def get_input(self):
        self.user_input = 'placeholder'
        if (self.type == 'radio'):
            self.get_radio()
        elif (self.type == 'slider'):
            self.get_slider()
        self.input_list.append(self.user_input)
    def get_radio(self):
        if (self.type_data == 'dataframe'):
            self.user_input = st.radio(
                self.var,
                np.unique(self.data.data_source[self.var]))
        elif (self.type_data == 'list'):
            self.user_input = st.radio(
                self.var,
                self.data)
        st.write(self.var,": ",self.user_input)
    def get_slider(self):
        if (self.type_data == 'dataframe'):
            self.user_input = st.slider(self.var, 0, max(self.data.data_source[self.var]), 1)
        elif (self.type_data == 'list'):
            self.user_input = st.slider(self.var, 0, max(self.data), 1)
        st.write(self.var,": ",self.user_input)
        
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

rows = run_query("SELECT * FROM `branding-nlp-project.twitter_data.tweets_merged_all`")
df = pd.DataFrame(rows)
st.write("Data head")
st.write(df.head())
st.write("Data shape")
st.write(df.shape)
st.write("Data columns/vars")
st.write(df.columns())
st.write("Numerical variables stats")
df_stats  = df.describe().apply(lambda s: s.apply(lambda x: format(x, 'f')))
df_num_stats = df_stats[["Retweet Count",	"Quote Count",	"Like Count", "Word_count", "Emoji_count"]]
st.dataframe(df_num_stats)
st.write("Graphsssssssss")
