# Clean review text data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import nltk


#def clean_text(col):
    # Convert type from b4 to str
#    df[col] = df.col.apply(str)

# Remove html text
#def remove_html(val):
#    return val.replace('<div class="review-question__response">','')
#df[col] = df.col.apply(remove_html)


# -------------------
# Clean text from failure lists.
# -------------------
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

# -------------------
# Remove punctuation
# -------------------
def remove_punc(text):
    punc_list = ['.',',',"!",'*','?','-']
    text = ''.join(char for char in text if char not in punc_list)
    return text


# --------------------
# Remove stop words
# --------------------
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

# ----------------------
# Remove Punctuation
# ----------------------
def preprocessor(text):
    if type(text) == str:
        text = re.sub('<[^>]*>', '', text)
        text = re.sub('[\W]+', '', text.lower())
    return text

# ----------------------------
# tokenize text after removing stop words, punc and lemmetization
# ----------------------------
def spacy_clean_text(review):
                 
    nlp = English()
    tokenizer = nlp.Defaults.create_tokenizer(nlp)
    tokens = tokenizer(review)
    lemma_list = []
    for token in tokens:
        if token.is_stop is False:
            token_preprocessed = preprocessor(token.lemma_)
            if token_preprocessed != '':
                lemma_list.append(token_preprocessed)
    return (lemma_list)


# -------------------------------------
# Create one Question and answer column
# -------------------------------------
def concat_q_and_a(df):
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

    df = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10], ignore_index=True)
    df = df.drop(['Question 1','Answer 1','Question 2','Answer 2','Question 3','Answer 3','Question 4','Answer 4',
                   'Question 5','Answer 5','Question 6','Answer 6','Question 7','Answer 7','Question 8','Answer 8',
                   'Question 9','Answer 9','Question 10','Answer 10'], axis=1)
    return (df)

# -------------------------------
# Convert questions to labels
# -------------------------------

def replace_q (val):
    if val[:28]=='How was your experience with':
        val = 'experience with doctor'   # classify under doctor
    elif val[:16] =='During treatment':  # Treated like num or human
        val = "experience with doctor"   # classify under doctor
    elif val[:16] == "What's one piece":
        val = 'advice give prospective patient'
    elif val[:40] == "Describe your experience with your nurse":
        val = "experience with nurse"
    elif val[:42] == "Describe your experience with your nursing":
        val = "experience with nurse"
    elif val[:29]=="Describe your experience with":
        val = "experience with clinic"
    elif val[:22] == "Describe the protocols":
        val = "protocols and success"
    elif val[:18]== "Describe the costs":
        val = "cost"
    elif val[:31] == "What specific things went wrong":
        val = "specific things went wrong"
    else:
        if "eSET" in val:
            val = "eSET vs. multiple embryo transfer"
        else:
            val=val
    return val