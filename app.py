#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image


# In[2]:


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.subheader('Solution by Borivoj Grujičić')


# In[3]:


image = Image.open('bizanaliza.JPG')
st.image(image,
        use_column_width=False)


# In[4]:


df = pd.read_excel('Sales.xlsx')


# In[5]:


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
wh = st.sidebar.multiselect(
    "Select the Warehouse:",
    options=df["WH"].unique(),
    default=df["WH"].unique()
)

year = st.sidebar.multiselect(
    "Select the Year:",
    options=df["YEAR"].unique(),
    default=df["YEAR"].unique(),
)

month = st.sidebar.multiselect(
    "Select the Month:",
    options=df["MONTH"].unique(),
    default=df["MONTH"].unique(),
)


colour = st.sidebar.multiselect(
    "Select the Colour:",
    options=df["COLOUR"].unique(),
    default=df["COLOUR"].unique()
)

df_selection = df.query(
    "WH == @wh & YEAR ==@year & MONTH ==@month & COLOUR == @colour"
)


# In[6]:


# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


# In[7]:


# TOP KPI's
total_sales = int(df_selection["REVENUE"].sum())
average_sale_by_transaction = round(df_selection["REVENUE"].mean(), 2)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")


# In[8]:


# SALES BY THE COLOUR LINE [BAR CHART]
sales_by_colour_line = (
    df_selection.groupby(by=["COLOUR"]).sum()[["REVENUE"]].sort_values(by="REVENUE")
)


# In[9]:


fig_colour_sales = px.bar(
    sales_by_colour_line,
    x="REVENUE",
    y=sales_by_colour_line.index,
    orientation="h",
    title="<b>Sales by Colour Line</b>",
    color_discrete_sequence=["#E694FF"] * len(sales_by_colour_line),
    template="plotly_white",
)
fig_colour_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# In[10]:


# SALES BY DAY [BAR CHART]
sales_by_day = df_selection.groupby(by=["DAY"]).sum()[["REVENUE"]]
fig_daily_sales = px.bar(
    sales_by_day,
    x=sales_by_day.index,
    y="REVENUE",
    title="<b>Sales by Day</b>",
    color_discrete_sequence=["#E694FF"] * len(sales_by_day),
    template="plotly_white",
)
fig_daily_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


# In[11]:


#left_column, right_column = st.columns(2)
#left_column.plotly_chart(fig_daily_sales, use_container_width=True)
#right_column.plotly_chart(fig_colour_sales, use_container_width=True)


# In[12]:


st.plotly_chart(fig_daily_sales)
st.plotly_chart(fig_colour_sales)


# In[13]:


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
