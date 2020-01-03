#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from scipy import sparse
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from global_params import search_queries, path_to_arxiv_data, path_to_training_data, path_to_trained_models, max_papers_to_be_scraped
import sys

print(" Bardvja is thinking ...")
print(" Please sit down, have some tea!")

# closer the function to 1 better match the paper is
def cosine_similarity_maximizer(array1, array2):
    # array1 is the local vectors
    # array2 is the vectors in arxiv
    # calculates the cosine with every vector in the arxiv
    # returns the minimum of cosine with all vectors in array1
    import numpy as np
    dot_prod = np.dot(array2, array1.T)
    cos_maximizer = []
    cos_maximizer = [np.mean(row) for row in dot_prod]
    return np.array(cos_maximizer)

pd.options.display.max_columns = 1000
pd.options.display.max_rows = 1000

# Read in the data files for arxiv and the local papers
df_local = pd.read_csv(f'{path_to_training_data}local_papers.csv')
df_to_concat = [pd.read_csv(f'{path_to_arxiv_data}arxiv_{query}_{max_papers_to_be_scraped}.csv') for query in search_queries]
df_arxiv = pd.concat(df_to_concat, join='outer')

# Load the normalized vectors
local_array = sparse.load_npz(f'{path_to_training_data}normalized_train_vectors.npz')

arrays_to_concat = [
    sparse.load_npz(f'{path_to_arxiv_data}normalized_arxiv_paper_vectors_{query}.npz').todense() for query in search_queries
]
arxiv_array = np.concatenate(arrays_to_concat, axis = 0)
arxiv_array = sparse.csr_matrix(arxiv_array)
sparse.save_npz(f'{path_to_arxiv_data}normalized_arxiv_paper_vectors.npz', matrix=arxiv_array)

# Comment these if you are not creating a new recommender
cos_maximizer = cosine_similarity_maximizer(local_array, arxiv_array)

joblib.dump(cos_maximizer,f'{path_to_arxiv_data}cosine_similarity_maximizer')

cos_maximizer = joblib.load(f'{path_to_arxiv_data}cosine_similarity_maximizer')

df_arxiv['cosine_similarity_maximizer'] = cos_maximizer

df_arxiv_arranged = df_arxiv.sort_values(by='cosine_similarity_maximizer', ascending=False).drop_duplicates()
df_arxiv_arranged.reset_index(drop=True, inplace=True)
df_arxiv_arranged.to_csv(f'{path_to_arxiv_data}df_arxiv_arranged.csv', index=False)

vocab = joblib.load(f'{path_to_trained_models}cvec_vocabulary')

print("\n Thank you for waiting ... ")
print(f"\n The papers in order of relevance are at {path_to_arxiv_data}")
print("\n Here are ten papers and their links for you")
print(df_arxiv_arranged.loc[:10, ['title','id']])


# In[ ]:




