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

class plotting():
    def __init__(self, data, group_by, y_var, stat):
        self.data = data
        self.group_by = group_by
        self.stat = stat
        self.y_var = y_var
        self.prepare_data()
    def show_plot(self):
        self.get_fig()
        st.plotly_chart(self.fig)
    def prepare_data(self):
        if (stat == "Count"):
            self.data_plot = data.groupby(histx_option).count()[self.y_var]
        if (stat == "Sum"):
            self.data_plot = data.groupby(histx_option).sum()[self.y_var]
        if (stat == "Mean"):
            self.data_plot = data.groupby(histx_option).mean()[self.y_var]
        self.data_plot = self.data_plot.to_frame()
        self.data_plot = self.data_plot.reset_index()
    def get_fig(self):
        self.fig = px.histogram(self.data_plot, x = self.group_by, y = self.y_var,
                   marginal="box",
                   hover_data=self.data_plot)
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
@st.cache_data()
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query("SELECT * FROM `branding-nlp-project.twitter_data.twitter_data_merged`")
df = pd.DataFrame(rows)
st.write("Data head")
st.write(df.head())
st.write("Data shape")
st.write(df.shape)
st.write("Data columns/vars")
st.write(df.columns)
st.write("Numerical variables stats")
df_stats  = df.describe().apply(lambda s: s.apply(lambda x: format(x, 'f')))
df_num_stats = df_stats[["Retweet_Count", "Quote_Count", "Like_Count", "Word_count", "Emoji_count"]]
st.dataframe(df_num_stats)
st.write("Graphsssssssss")
histg = st.checkbox("Distribution histogram with x axis as a cualitative var")
if histg:
    st.write("Distribution histogram with x axis as a cualitative var")
    histx_option = st.selectbox(
            "Select x time var",
            ("Day", "Month", "Year", "Day_Month", "Month_Year")
    )
    stat =  st.radio(
        "Select stat for y axis var",
        options=["Count","Mean","Sum"]
    )
    if (stat == "Count"): 
        y_poss_options = ("#_Tweets")
    else: 
        y_poss_options = ("Retweet_Count", "Quote_Count", "Like_Count", "Emoji_count", "Word_count")
        
    histy_option = st.selectbox(
            "Select y var",
            y_poss_options
        )
    var_time_plot = plotting(df, histx_option, histy_option, stat)
    var_time_plot.show_plot()
