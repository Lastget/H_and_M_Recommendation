import pickle
import streamlit as st
import requests
import pandas as pd
import numpy as np
import time 

# func
import ast
# Define function to convert string to list
def str_to_list(s):
    return ast.literal_eval(s)

# Set page setting
st.set_page_config(page_title='Recommend Clothes', layout="wide", page_icon = "🛍️")

# Import preprocessed data
most_buy_df = pd.read_csv("./output/customer_most_bought.csv" , dtype={'article_id': str})
with open('./output/pairs.pkl', 'rb') as file:
    paris_dict = pickle.load(file)
top12_arr = np.load('./output/top12.npy', allow_pickle=True)
last_purchase_df =  pd.read_csv("./output/last_purchase.csv", dtype={'last_purchase': str})
col_f_df = pd.read_csv("./output/cofilter.csv", dtype={'customer_id': str}, converters={'prediction': str_to_list})


# Title
st.write("# H&M E-Commerce Recommendation System 🛍️")
st.write("Please select your user ID. And system will recommend you items.")

user_tp = ('0001b0127d3e5ff8dadcfc6e5043682dba2070f2667081623faeb31c996242a6', '0020a3067dd6f6f14cbbb291061142a2b717beb629d62af74872ae5ed76266d8','01627a134fc6a832142b16e08dde78e7707a0a24075866e02c160f86cd8b4bf0')

userId = st.selectbox( 'What is your user ID?', user_tp)

button_recon = st.button('Recommend', type='secondary', help="Click to generate recommendation") 

if button_recon:
    if not userId:
        st.warning('Please provide user ID.', icon="⚠️")
        st.stop()

    # Check userID  
    if userId not in most_buy_df['customer_id'].unique():
        st.warning('You are not a previous buyer. Please insert another user id.', icon="⚠️")
        st.stop()

    # Find most purchase 
    most_item = most_buy_df.loc[most_buy_df['customer_id'] == userId, 'article_id'].values[0]
    # Find the last purchase 
    last_item = last_purchase_df.loc[last_purchase_df['customer_id'] == userId, 'last_purchase'].values[0]
    
    col1, col2, _ = st.columns(3)
    with col1:
        st.subheader(f'What you bought the most:')
        st.image(f'./input/images/{most_item}.jpg')
    with col2:
        st.subheader(f'What you bought last time:')
        st.image(f'./input/images/{last_item}.jpg')


    # Get Paired items with last purchase 
    item1, item2, item3  = paris_dict[last_item]
    st.subheader(f'People often bought these together with your last purchase:')
    col3, col4, col5 = st.columns(3)
    with col3:
        st.image(f'./input/images/{item1}.jpg')
    with col4:
        st.image(f'./input/images/{item2}.jpg')
    with col5:
        st.image(f'./input/images/{item3}.jpg')

    # Show last week top item 
    top3list = top12_arr[:3]
    top1, top2, top3 = top3list
    st.subheader(f'Last week top 3 item:')
    col6, col7, col8 = st.columns(3)
    with col6:
        st.image(f'./input/images/{top1}.jpg')
    with col7:
        st.image(f'./input/images/{top2}.jpg')
    with col8:
        st.image(f'./input/images/{top3}.jpg')

    
    # get colab filtering 
    fitem1, fitem2, fitem3 = col_f_df.loc[col_f_df['customer_id'] == userId, 'prediction'].values[0][:3]
    st.subheader(f'Recommend items by collaberate filtering:')
    col9, col10, col11 = st.columns(3)
    with col9:
        st.image(f'./input/images/{fitem1}.jpg')
    with col10:
        st.image(f'./input/images/{fitem2}.jpg')
    with col11:
        st.image(f'./input/images/{fitem3}.jpg')

    

    

    
    
    
    
    
    


        
    
        

