import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


#setting page configurations
st.set_page_config(
    page_title='Adidas Sales Dashboard',
    page_icon=':bar_chart:',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.title('Adidas US Sales Dashboard')
st.write('This dashboard is based on the Adidas US Sales dataset. The data for the dashbaord can be found here: https://www.kaggle.com/datasets/heemalichaudhari/adidas-sales-dataset.')

#importing css stylesheet
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

#custom css code
st_style = """
<style>
footer {visibility:hidden;}
</style>
"""
st.markdown(st_style,unsafe_allow_html=True)

# ==========
# Data Pre-Processing Section
# ==========

#reading in dataset
@st.cache_data
def get_data():
    sales = pd.read_csv('Adidas US Sales Datasets.csv')
    return sales
sales = get_data()

#data pre-processing
#converting column names to lowercase
sales.columns = [s.strip().lower().replace(' ','_') for s in sales.columns]
#converting invoice date to date/time format
sales['invoice_date'] = sales['invoice_date'].astype('datetime64[ns]')


#2020 total sales
sales_2020 = sales[(sales['invoice_date'].dt.year == 2020)]

#creating a new column for category
def define_category(product):
    if 'Street Footwear' in product:
        return 'Street Footwear'
    elif 'Apparel' in product:
        return 'Apparel'
    elif 'Athletic Footwear' in product:
        return 'Athletic Footwear'
    else:
        return 'Unknown'
#applying the function to the sales dataframe
sales['category'] = sales['product'].apply(define_category)

#creating a gender column

def define_gender(product):
    if "Men's" in product:
        return 'Men'
    elif "Women's" in product:
        return 'Women'
    
sales['gender'] = sales['product'].apply(define_gender)

#2020 total sales
sales_2020['total_sales'].sum()
#2021 total sales
sales_2021 = sales[(sales['invoice_date'].dt.year == 2021)]
sales_2021['total_sales'].sum()


# ==========
# Sidebar Section
# ==========

#sidebar section
##have a multi-select option for city
#have a multi-select or slider for year
with st.sidebar:
    st.header('Select Filters')

    #select region
    region = st.multiselect(
        label = 'Select a region to filter',
        options = sales['region'].unique(),
        default= sales['region'].unique()
    )
    #select product category
    category = st.multiselect(
          label = 'Select a product category',
          options = sales['category'].unique(),
          default = sales['category'].unique()
    )
    #filtering the dataframe based on selected filters
    sales = sales.query(
        'region == @region & category  == @category'
    )

# ==========
# Dashboard Section
# ==========


#displaying dataframe with a button
counter = 1
if st.button('Display data'):
        counter = counter + 1
        st.dataframe(sales)
        if st.button('Hide'):
              st.rerun()



#displaying KPI metrics in boxes
with st.container():
    col1, col2, col3, col4 = st.columns(spec=4,gap = 'medium')
    with col1:
        st.subheader('Total Sales in 2021')
        sales_2021 = sales[(sales['invoice_date'].dt.year == 2021)]
        st.markdown(f"${sales_2021['total_sales'].sum()}")
    with col2:
        st.subheader('Total Sales in 2020')
        st.markdown(f"${sales_2020['total_sales'].sum()}")
    with col3:
        st.subheader('Most Valuable Category')
        st.markdown("Men's Street Footwear")
    with col4:
        st.subheader('Most Valuable Market')
        st.markdown('New York')


st.markdown('---')

with st.container():
    st.subheader('Total Sales Over Time')
    st.plotly_chart(px.line(sales.groupby('invoice_date')['total_sales'].sum().reset_index(),x='invoice_date',y='total_sales'),use_container_width=True)

with st.container():
    col1,col2 = st.columns(spec=2,gap='medium')
    with col1:
        st.subheader('Sales by Product Category')
        st.plotly_chart(px.histogram(sales,x=sales['product'],y=sales['total_sales']),use_container_width=True)
    with col2:
        st.subheader('Sales by City')
        st.plotly_chart(px.histogram(sales,x=sales['city'],y=sales['total_sales'],color=sales['region']),use_container_width=True)

with st.container():
    col1,col2 = st.columns(spec=2,gap='medium')
    with col1:
        st.subheader('Sales by Retailer')
        st.plotly_chart(px.histogram(sales,x=sales['retailer'],y=sales['total_sales'],color=sales['category'],labels={'sum of total_sales':'Total Sales'}),use_container_width=True)
    with col2:
        st.subheader('Monthly Trend in Sales')
        st.plotly_chart(px.bar(sales.groupby(sales['invoice_date'].dt.month)['total_sales'].sum(),labels={'invoice_date':'Month','value':'Total Sales'},title='Total Sales by Month'),use_container_width=True)

with st.container():
    col1,col2 = st.columns(spec=2,gap='medium')
    with col1:
        st.subheader('Sales by Category')
        st.plotly_chart(px.pie(sales,sales['category'],values=sales['total_sales'],labels=sales['category']),use_container_width=True)
    with col2:
        st.subheader('Sales by Channel')
        st.plotly_chart(px.pie(sales,sales['sales_method'],values=sales['total_sales'],hole=.5,title='Sales by Channels'),use_container_width=True)

with st.container():
    col1,col2 = st.columns(spec=2,gap='medium')
    with col1:
        st.subheader('Sales by Gender')
        st.plotly_chart(px.pie(sales,sales['gender']),use_container_width=True)
    with col2:
        st.subheader('Sales by Retailer')
        sales.groupby(sales['retailer'])['total_sales'].sum()
        st.plotly_chart(px.histogram(sales,x=sales['retailer'],y=sales['total_sales'],color=sales['category'],labels={'sum of total_sales':'Total Sales'}),use_container_width=True)

