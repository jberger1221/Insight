# Import dependencies
import pandas as pd
import numpy as np
import io, time, json
import re
import os
import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# -----------------------------------
# Navigate to web pages using Selenium
# -----------------------------------
def scrape_fertility_iq(url):
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options) #options=options

    browser.get(url)
    time.sleep(1)

    elem = browser.find_element_by_css_selector("body")


    # Infinite Scroll - Scroll down to the end of the page
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
    
    # Collect all the data from the page
    page = browser.page_source

    # Call function to parse data into dataframe
    df = parse_web_reviews(page)
    return df

# ------------------------------------
# Function to parse data
def parse_web_data(html):

    soup = BeautifulSoup(html,'html.parser')    
    reviews=soup.find_all(class_='review-detail')
    
    avg_doc_score=soup.find(class_="nps-badge nps-badge--doctor nps-badge--large").get_text()
    avg_clinic_score =  soup.find(class_="nps-chart__title").get_text()
    clinic_name = soup.find(class_ = "search-result-detail__name").get_text()
    clinic_address_st = soup.find(class_ = "branch-address__street").get_text()
    clinic_address_city = soup.find(class_ = "branch-address__city-zip").get_text()
    #n=0
    rows = []
    
    for i, r in enumerate (reviews):
    
        clinic_score = r.find(class_='nps-badge nps-badge--clinic review-card__show_for_clinic').get_text()
        doc_score = r.find(class_='nps-badge nps-badge--doctor review-card__show_for_doctor').get_text()
        age = r.find(class_='reviewer-detail reviewer-detail--age').get_text()[3:]
        year = r.find(class_='reviewer-detail reviewer-detail--treated').get_text()[7:]
        success = r.find(class_="reviewer-detail reviewer-detail--success-with-this-doc").get_text()[21:]
        procedure = r.find(class_='reviewer-detail reviewer-detail--treatment').get_text()[9:]
        diagnosis = r.find(class_="reviewer-detail reviewer-detail--diagnosis").get_text()[9:]
            
        if r.find(class_='reviewer-detail reviewer-detail--income'):
            income = r.find(class_='reviewer-detail reviewer-detail--income').get_text()[6:]
            #print(i,income)
        if r.find(class_='reviewer-detail reviewer-detail--order-number-of-docs-seen'):
            num_docs = r.find(class_='reviewer-detail reviewer-detail--order-number-of-docs-seen').get_text()[27:]
            #print(i,num_docs)
        
        response = r.find_all(class_ = 'review-question__response')
        
        rows.append([clinic_name,clinic_address_st,clinic_address_city,avg_doc_score,avg_clinic_score,clinic_score,doc_score,age,year,success,procedure,
                    diagnosis,income,num_docs,response])
        
        df_reviews=pd.DataFrame(rows, columns=(['clinic_name','clinic_address_st','clinic_address_city','avg_doc_score','avg_clinic_score','clinic_score','doc_score',
                                                'age','year','success','procedure','diagnosis','income','num_docs',
                                                'response']))
    return df_reviews


# Function loop through list of urls
def scrape_urls(list_of_urls):
    df = pd.DataFrame()
    for u in list_of_urls:
        df_temp = scrape_fertility_iq(u)
        df = pd.concat([df,df_temp],ignore_index=True)
    return df

# --------------------------------------------------
# Function to split text into questions and answers
# --------------------------------------------------
def parse_web_reviews(html):

    soup = BeautifulSoup(html,'html.parser')    
    reviews=soup.find_all(class_='review-detail')

    avg_clinic_score =  soup.find(class_="nps-chart__title").get_text()
    avg_doc_score=soup.find(class_="nps-badge nps-badge--doctor nps-badge--large").get_text()
    clinic_name = soup.find(class_ = "search-result-detail__name").get_text()
    clinic_address_st = soup.find(class_ = "branch-address__street").get_text()
    clinic_address_city = soup.find(class_ = "branch-address__city-zip").get_text()
    #n=0
    rows = []

    # Loop through each review on page
    for r in reviews:
    
        clinic_score = r.find(class_='nps-badge nps-badge--clinic review-card__show_for_clinic').get_text()
        doc_score = r.find(class_='nps-badge nps-badge--doctor review-card__show_for_doctor').get_text()
        age = r.find(class_='reviewer-detail reviewer-detail--age').get_text()[3:]
        year = r.find(class_='reviewer-detail reviewer-detail--treated').get_text()[7:]
        success = r.find(class_="reviewer-detail reviewer-detail--success-with-this-doc").get_text()[21:]
        procedure = r.find(class_='reviewer-detail reviewer-detail--treatment').get_text()[9:]
        diagnosis = r.find(class_="reviewer-detail reviewer-detail--diagnosis").get_text()[9:]
            
        if r.find(class_='reviewer-detail reviewer-detail--income'):
            income = r.find(class_='reviewer-detail reviewer-detail--income').get_text()[6:]
            
        if r.find(class_='reviewer-detail reviewer-detail--order-number-of-docs-seen'):
            num_docs = r.find(class_='reviewer-detail reviewer-detail--order-number-of-docs-seen').get_text()[27:]
            
        # list of rows    
        row_first = [clinic_name,clinic_address_st,clinic_address_city,avg_doc_score,avg_clinic_score,clinic_score,doc_score,age,year,success,procedure,diagnosis,income,num_docs]
        
        # Some clinics have a list of things that went wrong
        if not r.find('div', attrs={'class':'review-question review-question--clinic-fails'}):
          
            question = r.find_all(class_='review-question__question')
            response = r.find_all(class_ = 'review-question__response')
        
            row_text = []
            for i in range(len(question)):
                row_text.append(question[i].get_text())
                row_text.append(response[i].get_text())
            
            if len(question)<10:
                add = [np.nan, np.nan]
                rows.append(row_first+row_text+add)
            else:
                rows.append(row_first+row_text)  
                
        # If review has a clinic fails list:        
        else :

            question = r.find_all(class_='review-question__question')
            response = r.find_all(class_ = 'review-question__response')
            # list of clinic failures
            clinic_fail_list = [r.find_all(class_ = 'reviewer-clinic-fails__list')]#.get_text()
        
            row_text = []
            for i in range(len(question)-1):
                row_text.append(question[i].get_text())
                row_text.append(response[i].get_text())
        
            # Create list for question    
            clinic_fail_question = [question[len(question)-1].get_text()]                      

            if len(question)<10:
                add = [np.nan, np.nan]
                rows.append(row_first+row_text+ clinic_fail_question + clinic_fail_list+add)
            else:
                # Create one row in list
                rows.append(row_first+row_text+ clinic_fail_question + clinic_fail_list)
        
    #Create list of column names
            # List of column Names without adding questions and responses 
    cols = ['clinic_name','clinic_address_st','clinic_address_city','avg_doc_score',
            'avg_clinic_score','clinic_score','doc_score','age','year','success','procedure',
            'diagnosis','income','num_docs']
    col_qa = []
    for i in range(1,11):
        col_qa.append('Question '+str(i))
        col_qa.append('Answer '+str(i))

    all_cols = cols+col_qa
    
    df_reviews = pd.DataFrame(rows, columns=all_cols)

    return df_reviews