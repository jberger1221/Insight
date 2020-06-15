"""
Build Streamlit app to predict ART clinic performance. 

"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import operator
import plotly.figure_factory as ff
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

#import model 
#st.cache

# import dataframe
#df = pd.read_csv("df_final.csv")
df = pd.read_csv("df_concat.csv")  

#use 2018 Clinics for search criteria
#df_2018




#
# Add Image to app
#
from PIL import Image
image = Image.open('Logo.png')
st.image(image, width =150)

#
# Heading of webapp
#
st.title("Fertile Crescent") 
st.header("Creating life with informed descisions")

#
#
#
eplanation_txt = st.subheader('Fertile Crescent is a webapp to help you decide the right assisted reproductive clinic for you.')
st.header("")

#
age_reason = st.text('Age is an important factor for estimating the propability of fertility success.')
age_reason1 = st.text('Use the slider to see how success rates change as a function of age.')
#age = st.number_input('Enter Age', min_value = 1, max_value = 50)
#st.write('The Entered Age is', age)
age_value = st.slider('Age',min_value = 20, max_value = 50, step = 1)
st.write('You entered ', age_value)

if age_value < 35:
    #plt.hist(df_join.ND_TransLB1,bins=50,edgecolor='w') 
    df.ND_TransLB1.hist(bins=50)
    #st.plotly_chart(f)
    st.pyplot()
elif (age_value >= 35 ) & (age_value < 38):
    df.ND_TransLB1.hist(bins=50,alpha=0.5)
    df.ND_TransLB2.hist(bins=50)
    #st.plotly_chart(f)
    st.pyplot()
elif (age_value >= 38 ) & (age_value < 40):
    df.ND_TransLB1.hist(bins=50,alpha=0.5)
    df.ND_TransLB2.hist(bins=50,alpha=0.5)
    df.ND_TransLB3.hist(bins=50)
    st.pyplot()
    #st.plotly_chart(f)
else:
    df.ND_TransLB1.hist(bins=50,alpha=0.5)
    df.ND_TransLB2.hist(bins=50,alpha=0.5)
    df.ND_TransLB3.hist(bins=50,alpha=0.5)
    df.ND_TransLB4.hist(bins=50)
    #st.plotly_chart(f)
    st.pyplot()

address = st.text_input('Enter Your Addess to find Assisted Reproductive clinics near your location')
#st.write('The Entered Age is', age)

if len(address) !=0:
    #data_load_state = st.text('Loading data...')
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(address)
    m = {'lon':[location.longitude],'lat':[location.latitude]}
    map_df = pd.DataFrame(m)
    st.map(data=map_df, zoom=0.001)



st.sidebar.title('Clinic Selector')
#
#
#
# Dropdown menu for clinics.
#
#option = st.sidebar.selectbox(
#    'List of all Current Clinics',
#     df[df["Year"]==2018]["ClinicNames"].unique())
#'You selected: ', option

#
# Checkbox to display selected clinic from dropdown menu
#
#if st.sidebar.checkbox('Show historical results from ', option):
#    new_df = df[(df['ClinicNames']==option)]
#st.write(new_df)

def model_success_rate(df):
    
    model = Pipeline([('poly', PolynomialFeatures(degree=3)), 
                  ('linear', LinearRegression(fit_intercept=False))])
    
    #x = df[df.ClinicNames == clinic]['Year'].values.reshape(-1,1)
    #y = df[df.ClinicNames == clinic]['ND_TransLB1'].values.reshape(-1,1)
    x = df['Year'].values.reshape(-1,1)
    y = df['ND_TransLB1'].values.reshape(-1,1)
    
    polynomial_features= PolynomialFeatures(degree=3)
    x_poly = polynomial_features.fit_transform(x)
    
    model = LinearRegression()
    model.fit(x_poly, y)
    y_poly_pred = model.predict(x_poly) 
    
    x_predict = np.array([[2019],[2020]])
    x_test = polynomial_features.fit_transform(x_predict)
    y_pre = model.predict(x_test)
    
    plt.scatter(x, y, s=10)
    sort_axis = operator.itemgetter(0)
    sorted_zip = sorted(zip(x,y_poly_pred), key=sort_axis)
    x, y_poly_pred = zip(*sorted_zip)
    plt.plot(x, y_poly_pred, color='m')

    plt.scatter(x_predict, y_pre, s=10)
    plt.plot(x_predict, y_pre, color='b')
    plt.xlabel('Year')
    plt.ylabel('Success Rate')
    plt.show()
    st.pyplot()


# ------------------
# Search for clinics
# ------------------
clinics = st.sidebar.multiselect(
 'Select a Clinic', df[df["Year"]==2018]["ClinicNames"].unique())
#st.write(clinics['ClinicNames'])



# -----------------
# Search for cities
# -----------------
city = st.sidebar.multiselect(
 'Select a city', df[df["Year"]==2018]["PrevClinName1"].unique()) 
# 
#
#
new_df = df[(df['ClinicNames'].isin(clinics)) | (df['ClinCityCode'].isin(city))]
st.write(new_df.reset_index())


if len(clinics)!=0:
    model_success_rate(new_df)



