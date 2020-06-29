"""
Build Streamlit app to predict ART clinic performance. 

"""
#pip install matplotlib

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#import operator
#import plotly.figure_factory as ff
#import geopandas as gpd
#import geopy
#from geopy.geocoders import Nominatim
#import plotly.express as px

#from sklearn.preprocessing import PolynomialFeatures
#from sklearn.linear_model import LinearRegression
#from sklearn.pipeline import Pipeline

#import model 
#st.cache

# -------------------------
# import dataframes
# -------------------------
# CDC
cdc = pd.read_csv("cdc_data.csv")

# fertilityiq
f_iq_reviews = pd.read_csv('reviews.csv')
# columns = 'clinic_name', 'avg_clinic_score', 'avg_doc_score','success', 'income', 'Question', 'Answer', 'clean_answers','Topics]
f_iq_summary = pd.read_csv('fiq_summary.csv')
# columns = ['Clinic_name', 'Topics', 'Reviews', 'Avg_clinic_score', 'Avg_doc_score','summary']

# yelp
# Yelp Summary
yelp_summary = pd.read_csv('yelp_summary.csv')
#Yelp Reviews
yelp_r = pd.read_csv('yelp_reviews.csv')
#Yelp Model
yelp_m = pd.read_csv('yelp_model_results.csv')


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
#st.subheader("About")
st.subheader('Fertile Crescent helps you decide the right assisted reproductive clinic, by combining data from Fertility IQ and Yelp, and success data from the CDC, to help quickly research fertility clinic.')
#st.header("")

#about_text = st.subheader("Fertile Crescent combines data from the review sites Fertility IQ and Yelp, and success data from the CDC to help you quickly research fertility care.")



# how_to_use
st.write("User reviews have been cleaned and categorized by topics using NLP to label each sentence in a review according to their predicted topic. A summary of all the reviews for a given topic and a given clinic is generated using a BERT extractive summarizer.")
st.write("")
st.subheader("How to Use")
st.write("1. Select a Review site.")
st.write("2. Select a Clinic to view Clinic Topics and CDC Success Rates.")
st.write("3. Select a Topic to view a summary of the reviews for that topic.")
st.write(" ")
############################################################################################
##################################        DATA              ################################
############################################################################################

# Fertility IQ
# ------------
# Fertility IQ checkbox
box_fiq = st.checkbox('Fertility IQ Reviews',value=False)
# Yelp checkbox
box_yelp = st.checkbox('Yelp Reviews',value=False)

if box_fiq:
    #display multiselect tool for clinics
    clinic = st.multiselect('Clinic', f_iq_reviews.clinic_name.unique())
    
    #display multiselect tool for topics
    topic = st.multiselect('Topic', f_iq_summary.Topics.unique())
    
    # display summary topics
    if len(clinic)!=0:

        df_temp = f_iq_reviews[f_iq_reviews['clinic_name'] == clinic[-1]]

        st.subheader("Fertility IQ Clinic and Doctor Scores")
        # Avg Clinic Score
        st.write("The Fertility IQ average score for {} is {}.".format(clinic[-1], round(df_temp['avg_clinic_score'].mean(),2)))
        # Avg doc Score
        st.write("The Fertility IQ average score for {} doctors is {}.".format(clinic[-1], round(df_temp['avg_doc_score'].mean(),2)))

        # Plot Success rates for clinic
        st.subheader(" ")
        box_cdc_plot = st.checkbox('Show CDC Success rates of Clinic Topics',value=True)
        if box_cdc_plot:
            age_input = st.text_input('Please enter your age (e.g. "35").',max_chars=2)

            if (len(age_input)!=0):
                #st.write("Please enter a valid age using numerical values.")
                age = int(age_input)
                df_cdc = cdc[cdc['fiq']==clinic[-1]]
                plot_cdc = False
                if age<=35 and age>20:
                    y_axis = "ND_TransLB1"
                    plot_cdc = True
                elif age>35 and age<=37:
                    y_axis = "ND_TransLB2"
                    plot_cdc = True
                elif age>37 and age<=40:
                    y_axis = "ND_TransLB3"
                    plot_cdc = True
                elif age>40 and age<50:
                    y_axis = "ND_TransLB4"
                    plot_cdc = True
                else:
                    st.write("Please enter a valid age.")
                
                if plot_cdc: 
                    p = sns.regplot(data=df_cdc, x="Year",  y = y_axis)
                    p.set_ylim(10,80)
                    plt.xlabel("Year")
                    plt.ylabel("Percent Success")
                    plt.title("CDC Success Rate by Year for {}".format(clinic[-1]))
                    st.pyplot() 
        

        if (len(topic) != 0) and (len(clinic) !=0):
            s = f_iq_summary[f_iq_summary['Topics']==topic[-1]]
            summary = s[s['Clinic_name']==clinic[-1]]['summary'].values[0]
            st.subheader("Summary of Reviews for {}, for Topic: {}".format(clinic[-1],topic[-1]))
            st.write(summary)

            #
            # Read individual reviews
            #
            st.subheader("Individual Reviews for {}, for Topic: {}".format(clinic[-1],topic[-1]))
            box_fiq_r = st.checkbox('Select for Fertility IQ Individual Reviews',value=False)
            #st.slider

            if box_fiq_r:
                r_clinic = f_iq_reviews[f_iq_reviews['clinic_name'] == clinic[-1]]
                rev = r_clinic[r_clinic['Topics']==topic[-1]]
                for idx, r in enumerate (rev.Answer):
                    st.write(idx,r)
        
        st.subheader(" ")
        box_fiq_plot = st.checkbox('Show Plot of Clinic Topics',value=True)
        if box_fiq_plot:
            sns.countplot(y = df_temp['Topics'])
            plt.xlabel("Count")
            plt.ylabel("Topics")
            plt.title("Fertility IQ Topic Count {}".format(clinic[-1]))
            st.pyplot()


    else:
        sns.countplot(y = f_iq_reviews.Topics)
        plt.xlabel("Count")
        plt.ylabel("Topics")
        plt.title("Fertility IQ Topic Count - All Clinics")
    #plt.figure(figsize=(2,2))
    #p.show()
        st.pyplot()


##################################################################
########################### YELP #################################
##################################################################
# Yelp data
if box_yelp:
    #display multiselect tool for clinics
    clinic_y = st.multiselect('Clinic', yelp_m.Clinic.unique())
    
    #display multiselect tool for topics
    topic_y = st.multiselect('Topic', yelp_m.Topics.unique())

    # display summary topics
    if len(clinic_y)!=0:

        df_temp_r = yelp_r[yelp_r['Clinic_name'] == clinic_y[-1]]
        df_temp = yelp_m[yelp_m['Clinic'] == clinic_y[-1]]

        st.subheader("Yelp Clinic Rating")
        # Avg Clinic Score
        st.write("The Yelp average rating for {} is {}.".format(clinic_y[-1], round(df_temp_r['Num_Rating'].mean(),1)))

        # Plot Success rates for clinic
        st.subheader(" ")
        box_cdc_y_plot = st.checkbox('Show CDC Success rates of Clinic Topics',value=True)
        if box_cdc_y_plot:
            age_input = st.text_input('Please enter your age (e.g. "35").',max_chars=2)

            if (len(age_input)!=0):
                #st.write("Please enter a valid age using numerical values.")
                age = int(age_input)
                df_cdc = cdc[cdc['Yelp']==clinic_y[-1]]
                plot_cdc = False
                if age<=35 and age>20:
                    y_axis = "ND_TransLB1"
                    plot_cdc = True
                elif age>35 and age<=37:
                    y_axis = "ND_TransLB2"
                    plot_cdc = True
                elif age>37 and age<=40:
                    y_axis = "ND_TransLB3"
                    plot_cdc = True
                elif age>40 and age<50:
                    y_axis = "ND_TransLB4"
                    plot_cdc = True
                else:
                    st.write("Please enter a valid age.")
                
                if plot_cdc: 
                    p = sns.regplot(data=df_cdc, x="Year",  y = y_axis)
                    p.set_ylim(10,80)
                    plt.xlabel("Year")
                    plt.ylabel("Percent Success")
                    plt.title("CDC Success Rate by Year for {}".format(clinic_y[-1]))
                    st.pyplot() 
        

        if (len(topic_y) != 0) and (len(clinic_y) !=0):
            s = yelp_summary[yelp_summary['Topics']==topic_y[-1]]
            summary = s[s['Clinic_name']==clinic_y[-1]]['summary'].values[0]
            st.subheader("Summary of Reviews for {}, for Topic: {}".format(clinic_y[-1],topic_y[-1]))
            st.write(summary)

            #
            # Read individual reviews
            #
            st.subheader("Individual Reviews for {}, for Topic: {}".format(clinic_y[-1],topic_y[-1]))
            box_fiq_r = st.checkbox('Select for Yelp Individual Reviews',value=False)
            #st.slider

            if box_fiq_r:
                r_clinic = yelp_m[yelp_m['Clinic'] == clinic_y[-1]]
                rev = r_clinic[r_clinic['Topics']==topic_y[-1]]
                for idx, r in enumerate (rev.Reviews_by_sentence):
                    st.write(idx,r)
        
        st.subheader(" ")
        box_yelp_plot = st.checkbox('Show Plot of Clinic Topics',value=True)
        if box_yelp_plot:
            sns.countplot(y = df_temp['Topics'])
            plt.xlabel("Count")
            plt.ylabel("Topics")
            plt.title("Fertility IQ Topic Count {}".format(clinic_y[-1]))
            st.pyplot()


    else:
        sns.countplot(y = yelp_m.Topics)
        plt.xlabel("Count")
        plt.ylabel("Topics")
        plt.title("Yelp Topic Count - All Clinics")
        st.pyplot()




# ###########################
# ---------------------------
# Side Bar code
# ---------------------------
# ###########################

# ----------------
# About me
# ----------------
about = st.sidebar.title("About Me")
#st.write(about)

name = st.sidebar.subheader("Jacob Berger Ph.D.")
#st.write(name)

proj = st.sidebar.subheader("Insight Project 2020")
#st.write(proj)

#email = st.sidebar.text("jacobsberger@gmail.com")
#st.write(email)

# --------------------
# OLD
# --------------------

#
#age_reason = st.text('Age is an important factor for estimating the propability of fertility success.')
#age_reason1 = st.text('Use the slider to see how success rates change as a function of age.')
#age = st.number_input('Enter Age', min_value = 1, max_value = 50)
#st.write('The Entered Age is', age)
#age_value = st.slider('Age',min_value = 20, max_value = 50, step = 1)
#st.write('You entered ', age_value)

#if age_value < 35:
    #plt.hist(df_join.ND_TransLB1,bins=50,edgecolor='w') 
#    df.ND_TransLB1.hist(bins=50)
    #st.plotly_chart(f)
#    st.pyplot()
#elif (age_value >= 35 ) & (age_value < 38):
#    df.ND_TransLB1.hist(bins=50,alpha=0.5)
#    df.ND_TransLB2.hist(bins=50)
    #st.plotly_chart(f)
#    st.pyplot()
#elif (age_value >= 38 ) & (age_value < 40):
#    df.ND_TransLB1.hist(bins=50,alpha=0.5)
#    df.ND_TransLB2.hist(bins=50,alpha=0.5)
#    df.ND_TransLB3.hist(bins=50)
#    st.pyplot()
    #st.plotly_chart(f)
#else:
#    df.ND_TransLB1.hist(bins=50,alpha=0.5)
#    df.ND_TransLB2.hist(bins=50,alpha=0.5)
#    df.ND_TransLB3.hist(bins=50,alpha=0.5)
#    df.ND_TransLB4.hist(bins=50)
    #st.plotly_chart(f)
#    st.pyplot()


#address = st.text_input('Enter Your Addess to find Assisted Reproductive clinics near your location')
#st.write('The Entered Age is', age)

#if len(address) !=0:
    #data_load_state = st.text('Loading data...')
#    locator = Nominatim(user_agent="myGeocoder")
#    location = locator.geocode(address)
#    m = {'lon':[location.longitude],'lat':[location.latitude]}
#    map_df = pd.DataFrame(m)
#    st.map(data=map_df, zoom=0.001)

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

# ------------------
# Search for clinics
# ------------------
#clinics = st.sidebar.multiselect(#
# 'Select a Clinic', f_iq_summary["Clinic_name"].unique())
#st.write(clinics['ClinicNames'])

