#!/usr/bin/env python
# coding: utf-8

# In[1]:


### Creating dataframe from pdfs

import pdf_reader as pdfr
import numpy as np
import pandas as pd
import sys
import pickle, pickleshare
from scipy import sparse
import pickle
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import os
from global_params import path_to_training_data, path_to_papers_train, path_to_trained_models

def pypdf2_parser(path_to_pdf):
    import PyPDF2
    pdf_contents = {}
    pdf_reader = PyPDF2.PdfFileReader(path_to_pdf)
    pdf_contents['total_pages'] = pdf_reader.numPages
    pdf_info = pdf_reader.getDocumentInfo()
    pdf_contents['author'] = pdf_info.author
    pdf_contents['title'] = str(pdf_info.title).lower()
    pdf_contents['creator'] = pdf_info.creator
    try:
        pdf_contents['subject'] = pdf_info['/Subject'].split(' ')[0:-1]
    except:
        pdf_contents['subject'] = 'Unknown'
    try:
        pdf_contents['complete_pdf'] = pdf_contents['title'] + ' '.join([pdf_reader.getPage(i).extractText() for i in range(pdf_contents['total_pages'])])
    except:
        print(f"Error: While trying to combine title and text there is issue at this file: {path_to_pdf}")
    return pdf_contents

def make_training_dataframe(path_to_training_papers):
    import os
    import pandas as pd

    train_data = {}
    list_papers_train = os.listdir(path_to_training_papers)
    list_papers_train.remove('.DS_Store')

    if list_papers_train == [] :
        print(f"No parsable PDF found at the directory of local papers located at {path_to_training_papers}")
        print("Please add more PDF files to let Bardvja ponder.")
        sys.exit()

    for idx, filename in enumerate(os.listdir(path_to_training_papers)):
        if filename != '.DS_Store':
            path_to_pdf = path_to_training_papers+filename
            print(f"Parsing this paper now: {path_to_pdf}")
            train_data[idx] = pypdf2_parser(path_to_pdf)

    df = pd.DataFrame(train_data.values())
    df.dropna(subset=['complete_pdf','title'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def pre_processing_pdf_text(df):
    import pandas as pd
    import wordninja
    from nltk.stem.porter import PorterStemmer
    import regex as re

    porter = PorterStemmer()

    try:
        df['complete_pdf'] = df['complete_pdf'].map(lambda x: re.sub('\d+',"",x))
        print("Finished Regex body")
        df['title'] = df['title'].map(lambda x: re.sub('\d+',"",x))
        print("Finished Regex title")
        df['complete_pdf'] = df['complete_pdf']*2 + ' ' + (df['title']+' ')*10
        print("Finished adding title and body")
        df['complete_pdf'] = df['complete_pdf'].map(lambda x: wordninja.split(x.lower()))
        print("Finished turning into lowercase and wordninja")
        df['complete_pdf'] = df['complete_pdf'].map(lambda x: ' '.join(list(map(porter.stem, x))))
        print("Finished stemming using porter")
    except:
        print("Error: Unable to pre-process this file: ")
    return df

def transform_abstracts_to_vectors(df, custom_stop_words=['a']):
    from sklearn.model_selection import GridSearchCV, train_test_split
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, ENGLISH_STOP_WORDS
    from sklearn.preprocessing import StandardScaler, normalize
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from scipy import sparse
    from nltk.stem.porter import PorterStemmer
    import string
    import pickle
    import joblib

    X = df['complete_pdf']
    porter = PorterStemmer()
    stop_words_english = list(map(porter.stem, ENGLISH_STOP_WORDS))
    custom_stop_words = list(map(porter.stem, custom_stop_words))
    stop_words_english += custom_stop_words

    chars = [c for c in string.ascii_lowercase]
    stop_words_english += chars
    for i in chars:
        for j in chars:
            stop_words_english.append(i+j)

    try:
        joblib.dump(stop_words_english, f'{path_to_trained_models}stop_words_english')
    except:
        print("Raised error trying to write stop_words_english!")

    min_df = min(5, X.shape[0])
    print("minimum df",min_df)
    cvec = CountVectorizer(max_features=500, stop_words=stop_words_english, min_df=5, max_df=0.9)
    tvec = TfidfVectorizer(max_features=500, stop_words=stop_words_english, min_df=5, max_df=0.9)

    try:
        X_vec = cvec.fit_transform(X)
        X_vec2 = tvec.fit_transform(X)
    except:
        cvec = CountVectorizer(stop_words=stop_words_english)
        tvec = TfidfVectorizer(stop_words=stop_words_english)
        X_vec = cvec.fit_transform(X)
        X_vec2 = tvec.fit_transform(X)

    joblib.dump(cvec.vocabulary_, f'{path_to_trained_models}cvec_vocabulary')
    # Save the Vectorizer models for later
    joblib.dump(cvec, f'{path_to_trained_models}count_vectorizer.sav')
    joblib.dump(tvec, f'{path_to_trained_models}tfidf_vectorizer.sav')

    ss = StandardScaler()
    X_vec_ss = ss.fit_transform(X_vec.toarray())
    # Save the StandardScaler for later
    joblib.dump(ss, f'{path_to_trained_models}standard_scaler.sav')

#****** Clustering to get more accurate parameters *********
    n_clusters=min(3, X_vec_ss.shape[0])
    print('clusters in KMeans : ',n_clusters)
    k_cluster = KMeans(n_clusters, random_state=42, n_jobs=-1)
    k_cluster.fit(X_vec_ss)
    # Save the KMeans cluster for later
    joblib.dump(k_cluster, f'{path_to_trained_models}kmeans_cluster.sav')
    df['cluster_label'] = k_cluster.predict(X_vec_ss)
    X_vec = np.append(X_vec.toarray(),df['cluster_label'].values.reshape(-1,1), axis=1)

    X_normal = normalize(sparse.csr_matrix(X_vec)).toarray()
    if (X_normal.shape[0]==0 or X_normal.shape[1]==0):
        print("Add more papers to train the recommendation model and try again!")
        sys.exit()

    return X_normal

# The code body starts here. All defined functions above this line.

if not os.path.isdir(f'{path_to_papers_train}'):
    print(f"Please ensure the directory with pdfs to be trained on is at {path_to_papers_train}")
    os.mkdir(f'{path_to_papers_train}')
    print(f"\nA new directory to store the local papers to base the recommendations on, is created at {path_to_papers_train}")
    print(f"\nAdd the papers of interest to this directory. More papers better the results!")
    sys.exit()

if not os.path.isdir(f'{path_to_training_data}'):
    print(f"Creating folder to keep training data at {path_to_training_data}")
    os.mkdir(f'{path_to_training_data}')

if not os.path.isdir(f'{path_to_trained_models}'):
    print(f"Creating folder to keep trained models at {path_to_trained_models}")
    os.mkdir(f'{path_to_trained_models}/')

df = make_training_dataframe(f'{path_to_papers_train}')

df = pre_processing_pdf_text(df)

df.to_csv(f'{path_to_training_data}local_papers.csv', index=False)

df = pd.read_csv(f'{path_to_training_data}local_papers.csv')

### Developing model

# Added these using some subject-matter expertise being in research
# People may modify it to their needs if required
custom_stop_words = ['fig','figure','table','abstract','summary','method','research','publication','published','test',
                    'effect','different','mean','sum','variance','variety','analysis','given','provided','lead'
                    'large','small','low','pro','pre','similar','report','length','width','high','section','include',
                    'close','approximation','new','old','non','etc','occur','represent','characeristic','characterization'
                    'character','problem','presence','suggestion','enhance']

Z = transform_abstracts_to_vectors(df)
Z_sparse = sparse.csr_matrix(Z)
sparse.save_npz(f'{path_to_training_data}normalized_train_vectors.npz', matrix=Z_sparse)

print('\n Completed processing and training on the local papers! \n')


# In[ ]:
