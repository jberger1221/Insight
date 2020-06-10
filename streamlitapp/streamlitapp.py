"""
Build Streamlit app to predict ART clinic performance. 

"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

#import model 

# import dataframe
df = pd.read_csv("df_final.csv") 

#use 2018 Clinics for search criteria
#df_2018


#
# Heading of webapp
#
st.text_input("Fertile Crescent") 


#
#
#
age = st.sidebar.text_input('Enter Age')
#st.write('The Entered Age is', age)

#
# Dropdown menu for clinics.
#
option = st.sidebar.selectbox(
    'List of all Current Clinics',
     df[df["Year"]==2018]["ClinicNames"].unique())
'You selected: ', option

#
# Checkbox to display selected clinic from dropdown menu
#
if st.sidebar.checkbox('Show historical results from ', option):
    new_df = df[(df['ClinicNames']==option)]
st.write(new_df)


# ------------------
# Search for clinics
# ------------------
clinics = st.sidebar.multiselect(
 'Select a Clinic', df[df["Year"]==2018]["ClinicNames"].unique())

# -----------------
# Search for cities
# -----------------
city = st.sidebar.multiselect(
 'Select a city', df[df["Year"]==2018]["CurrentClinicCity"].unique()) 
# 
#
#
new_df = df[(df['ClinicNames'].isin(clinics)) | (df['CurrentClinicCity'].isin(city))]
st.write(new_df.reset_index())
