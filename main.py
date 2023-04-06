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
    def __init__(self, data, group_by, y_var, stat, color_var, plot_type):
        self.data = data
        self.group_by = group_by
        self.stat = stat
        self.y_var = y_var
        self.color_var = color_var
        if (plot_type == "Hist"):
            self.prepare_data()
        else: 
            self.data_plot = data
    def show_plot(self):
        self.get_fig()
        st.plotly_chart(self.fig)
    def scatter_plot(self):
        self.scatter_fig = px.scatter(self.data_plot, x = self.group_by, y = self.y_var, color = self.color_var)
        st.plotly_chart(self.scatter_fig)
    def prepare_data(self):
        if (self.color_var == 'None'): 
            if (self.stat == "Count"):
                self.data_plot = self.data.groupby(self.group_by).count()[self.y_var]
            if (self.stat == "Sum"):
                self.data_plot = self.data.groupby(self.group_by).sum()[self.y_var]
            if (self.stat == "Mean"):
                self.data_plot = self.data.groupby(self.group_by).mean()[self.y_var]
            self.data_plot = self.data_plot.to_frame()
        else: 
            if (self.stat == "Count"):
                self.data_plot = self.data.groupby(self.group_by).count()[[self.y_var,self.color_var]]
            if (self.stat == "Sum"):
                self.data_plot = self.data.groupby(self.group_by).sum()[[self.y_var,self.color_var]]
            if (self.stat == "Mean"):
                self.data_plot = self.data.groupby(self.group_by).mean()[[self.y_var,self.color_var]]
        self.data_plot = self.data_plot.reset_index()
        st.write(self.data_plot)
    def get_fig(self):
        if (self.color_var == 'None'): 
            if (self.stat == "Count"):
                self.fig = px.bar(self.data_plot, x = self.group_by, y = self.y_var, title=f"# Tweets distribution over {self.group_by}s")
            else:
                self.fig = px.bar(self.data_plot, x = self.group_by, y = self.y_var, title=f"{self.y_var} {self.stat} distribution over {self.group_by}s")
        else: 
            if (self.stat == "Count"):
                self.fig = px.bar(self.data_plot, x = self.group_by, y = self.y_var, title=f"# Tweets distribution over {self.group_by}s color {self.color_var}", color=self.color_var)
            else:
                self.fig = px.bar(self.data_plot, x = self.group_by, y = self.y_var, title=f"{self.y_var} {self.stat} distribution over {self.group_by}s  color {self.color_var}", color=self.color_var)
            
        
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
    df = pd.DataFrame(rows)
    return df

df = run_query("SELECT * FROM `branding-nlp-project.twitter_data.twitter_data_merged_clean`")

st.write("Data head")
st.write(df.head())
st.write("Data shape")
st.write(df.shape)
st.write("Data columns/vars")
st.write(df.columns)
st.write("Numerical variables stats")

@st.cache_data()
def get_stats(data):
    df_stats  = data.describe().apply(lambda s: s.apply(lambda x: format(x, 'f')))
    return df_stats

df_stats  = get_stats(df)
df_num_stats = df_stats[["Retweet_Count", "Quote_Count", "Like_Count", "Word_count", "Emoji_count"]]
st.dataframe(df_num_stats)
st.write("Graphsssssssss")

def get_plot_time(var_time_plot): 
    var_time_plot.show_plot()
    
histg = st.checkbox("Distribution histogram with x axis as a cualitative var")

if histg:
    histx_option = st.selectbox(
            "Select x time var",
            ("Hour", "Day", "Month", "Day_Month", "Day_of_the_week")
    )
    stat =  st.radio(
        "Select stat for y axis var",
        options=["Count","Mean","Sum"]
    )
    if (stat == "Count"): 
        y_poss_options = ("#_Tweets")
        histy_option = "Retweet_Count"
    else: 
        y_poss_options = ("Retweet_Count", "Quote_Count", "Like_Count", "Emoji_count", "Word_count")  
        histy_option = st.selectbox(
                "Select y var",
                y_poss_options
            )
    if st.button('Create histogram'):
        var_time_plot = plotting(df, histx_option, histy_option, stat, "None", "Hist")

        get_plot_time(var_time_plot)

histg_color = st.checkbox("Distribution histogram with x axis as a cualitative var with co=lo=ur")

if histg_color:
    histx_option_2 = st.selectbox(
            "Select x time var for color histogram",
            ("Hour", "Day", "Month", "Day_Month", "Day_of_the_week")
    )
    stat_2 =  st.radio(
        "Select stat for y axis var color histogram",
        options=["Count","Mean","Sum"]
    )
    if (stat_2 == "Count"): 
        y_poss_options_2 = ("#_Tweets")
        histy_option_2 = "Retweet_Count"
    else: 
        y_poss_options_2 = ("Retweet_Count", "Quote_Count", "Like_Count", "Emoji_count", "Word_count")  
        histy_option_2 = st.selectbox(
                "Select y var for color histogram",
                y_poss_options_2
            )  
        
    color_op = st.selectbox(
                "Select var for color",
                y_color_poss_options_2
            )  
    if (histy_option_2 == color_op): 
        st.write("same var")
    else:
        if st.button('Create color histogram'):
            var_time_plot_2 = plotting(df, histx_option_2, histy_option_2, stat_2, color_op, "Hist")

            get_plot_time(var_time_plot_2)
        
    
scatter = st.checkbox("scatter plot") 
if scatter:
    poss_options = ("Retweet_Count", "Quote_Count", "Like_Count", "Emoji_count", "Word_count")

    x_var = st.selectbox(
                "Select x var",
                poss_options
        )

    y_var = st.selectbox(
                "Select y var",
                poss_options
        )

    color_var = st.selectbox(
                "Select color var",
                poss_options
        )
    
    if st.button('Create scatter'):
        scatter_plot = plotting(df, x_var, y_var, 'None', color_var, "Scatter")
        scatter_plot.scatter_plot()
