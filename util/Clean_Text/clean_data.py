"""
Clean scraped data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

def concat_columns(df):
    df1 = df[['clinic_name','clinic_score','doc_score','success','income','Question 1','Answer 1']]
    df1['Question'] = df1['Question 1']
    df1['Answer']   = df1['Answer 1']
    df2 = df[['clinic_name','clinic_score','doc_score','success','income','Question 2','Answer 2']]
    df2['Question'] = df2['Question 2']
    df2['Answer']   = df2['Answer 2']
    df3 = df[['clinic_name','clinic_score','doc_score','success','income','Question 3','Answer 3']]
    df3['Question'] = df3['Question 3']
    df3['Answer']   = df3['Answer 3']
    df4 = df[['clinic_name','clinic_score','doc_score','success','income','Question 4','Answer 4']]
    df4['Question'] = df4['Question 4']
    df4['Answer']   = df4['Answer 4']
    df5 = df[['clinic_name','clinic_score','doc_score','success','income','Question 5','Answer 5']]
    df5['Question'] = df5['Question 5']
    df5['Answer']   = df5['Answer 5']
    df6 = df[['clinic_name','clinic_score','doc_score','success','income','Question 6','Answer 6']]
    df6['Question'] = df6['Question 6']
    df6['Answer']   = df6['Answer 6']
    df7 = df[['clinic_name','clinic_score','doc_score','success','income','Question 7','Answer 7']]
    df7['Question'] = df7['Question 7']
    df7['Answer']   = df7['Answer 7']
    df8 = df[['clinic_name','clinic_score','doc_score','success','income','Question 8','Answer 8']]
    df8['Question'] = df8['Question 8']
    df8['Answer']   = df8['Answer 8']
    df9 = df[['clinic_name','clinic_score','doc_score','success','income','Question 9','Answer 9']]
    df9['Question'] = df9['Question 9']
    df9['Answer']   = df9['Answer 9']
    df10 = df[['clinic_name','clinic_score','doc_score','success','income','Question 10','Answer 10']]
    df10['Question'] = df10['Question 10']
    df10['Answer']   = df10['Answer 10']

    df_new = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10], ignore_index=True)

    df_new = df_new.drop(['Question 1','Answer 1','Question 2','Answer 2','Question 3','Answer 3','Question 4','Answer 4',
                   'Question 5','Answer 5','Question 6','Answer 6','Question 7','Answer 7','Question 8','Answer 8',
                   'Question 9','Answer 9','Question 10','Answer 10'], axis=1)
    
    df_new = df_new.dropna().reset_index(drop=True)

    return df_new

#
# Replace questions into categories
#
def replace_q (val):
    if val[:28]=='How was your experience with':
        val = 'Doctor'   # classify under doctor
    elif val[:16] =='During treatment':  # Treated like num or human
        val = "Doctor"   # classify under doctor
    elif val[:16] == "What's one piece":
        val = 'Advice
    elif val[:40] == "Describe your experience with your nurse":
        val = "Nurse"
    elif val[:42] == "Describe your experience with your nursing":
        val = "Nurse"
    elif val[:29]=="Describe your experience with":
        val = "Clinic"
    elif val[:22] == "Describe the protocols":
        val = "Protocols"
    elif val[:18]== "Describe the costs":
        val = "Cost"
    elif val[:31] == "What specific things went wrong":
        val = "Problems"
    else:
        if "eSET" in val:
            val = "Protocols"
        else:
            val=val
       
    return val

#
# The List of things that went wrong scraped data needs to be cleaned further. 
#
def failed_list(text):
    if "<ul" in text:
        text_list = text.split(">")
        fail_list =[]
        for i in text_list:
            if "</li" in i:
                fail_list.append(i.split('<')[0])
        doc = ', '.join(fail_list)
        return doc
    
    else:
        return text

#
# Function to implement categoies on DataFrame
#
def clean_qa(df):
    df.Question = df.Question.apply(replace_q)
    df.Answer = df.Answer.apply(failed_list)
    return df

#
# Save data to CSV
#
def save_date(df,save_name):
    df.to_csv(save_name)
    return

# Clean text, word embeddings, stop words removal and punctuation removal.
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))
wpt = nltk.WordPunctTokenizer()
#wt = nltk.word_tokenizer()
#list of words to not remove
remove_form_stop_words = ['no','not',"aren't","couldn't","didn't","doesn't",
                          "wasn't","wouldn't","won't","don't","isn't","shouldn't"]
for w in remove_form_stop_words:
    en_stop.remove(w)
contractions = { 
"aren't": "are not,
"can't": "cannot",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"isn't": "is not",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"wasn't": "was not",
"weren't": "were not",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not"
}
def simple_clean_document(doc):
    # lower case and remove special characters\whitespaces
    #doc = re.sub(r'[^a-zA-Z\s]', '', doc, re.I|re.A)
    punc_list = ['.',',',"!",'*','?','-']
    
    doc = doc.lower()
    doc = doc.strip()
    
    doc = doc.split(" ")
    # Contractions in text 
    new_doc=[]
    for token in doc:
        if token in contractions:
            new_doc.append(contractions[token])
        else:
            new_doc.append(token)
    doc = ' '.join(new_doc)
    
    # tokenize document
    tokens = wpt.tokenize(doc)
    
    tokens = [token for token in tokens]
    # Contractions in text    
    for token in tokens:
        if token in contractions:
            token = contractions[token]
            
    # Remove Punctuation
    tokens = [token for token in tokens if token not in punc_list]
    
    # filter stopwords out of document
    filtered_tokens = [token for token in tokens if token not in en_stop]
    
    #Lemmatize tokens
    lemm_tokens = [get_lemma(token) for token in filtered_tokens]
    
    # re-create document from filtered tokens
    doc = ' '.join(lemm_tokens)
    return doc


#
# Split of yelp review into sentences
#
def split_up_review(df):
    df_final = pd.DataFrame()
    for c in df.Clinic_name.unique():
        
        df_temp = df[df.Clinic_name == c]
        
        
        sentences = []
        #id = c + "_" + str(0)
        for i, r in enumerate (df_temp.Reviews):
            list_of_sentences = r.replace("Dr.","Dr").split(".")
        
            sentences = sentences + list_of_sentences
            #print(i,c)
            
        df_new = pd.DataFrame(sentences,columns=['Reviews_by_sentence'])
        df_new['Clinic'] = c
        df_final = pd.concat([df_final,df_new],ignore_index=True)
        
    return df_final

#
# Check for non-english characters
#
def check_char(df):
    for i, rev in enumerate (df.Reviews):
        for n in re.findall(r'[\u4e00-\u9fff]+', rev):
            print(i,n)
        df = df.drop(i,axis=0)
    return df
        

