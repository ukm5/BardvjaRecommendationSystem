import pickle
import joblib
import pandas as pd
from scipy import sparse

def pre_processing_pdf_text(df):
    import pandas as pd
    import wordninja
    from nltk.stem.porter import PorterStemmer
    import regex as re

    df['title'] = df['title'].map(lambda x: re.sub('\d+',"",x))
    print("completed RegEx on title!")
    df['abstract'] = df['abstract'].map(lambda x: re.sub('\d+',"",x))
    print("completed RegEx on abstract!")
    df['title'] = df['title'].map(lambda x: wordninja.split(x.lower()))
    print("completed WordNinja on title!")
    df['abstract'] = df['abstract'].map(lambda x: wordninja.split(x.lower()))
    print("completed WordNinja on abstract!")

    porter = PorterStemmer()
    df['title'] = df['title'].map(lambda x: ' '.join(list(map(porter.stem, x))))
    print("completed Porter Stemming title!")
    df['abstract'] = df['abstract'].map(lambda x: ' '.join(list(map(porter.stem, x))))
    print("completed Porter Stemming title!")
    
    df['complete_pdf'] = df['abstract']*2 + ' ' + (df['title']+' ')*10
    print("completed adding title and abstract!")
    
    return df

# abstract here refer to the complete_pdf column we have made

def transform_abstracts_to_vectors(df):
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    from sklearn.preprocessing import normalize
    from scipy import sparse
    from nltk.stem.porter import PorterStemmer
    import string
    import pickle
    import joblib
    import numpy as np
    
    X = df['complete_pdf']
    porter = PorterStemmer()
    stop_words_english = joblib.load('./../trained_models/stop_words_english')

    chars = [c for c in string.ascii_lowercase]
    stop_words_english += chars
    for i in chars:
        for j in chars:
            stop_words_english.append(i+j)
            
    # Load the vectorizer models
    cvec = joblib.load('./../trained_models/count_vectorizer.sav')
    tvec = joblib.load('./../trained_models/tfidf_vectorizer.sav')
    X_vec = cvec.transform(X)
    X_vec2 = tvec.transform(X)   

    # Load the Standard Scaler model
    ss = joblib.load('./../trained_models/standard_scaler.sav')
    X_vec_ss = ss.transform(X_vec.toarray())

    # Load the KMeans cluster model
    k_cluster = joblib.load('./../trained_models/kmeans_cluster.sav')    

    df['cluster_label'] = k_cluster.predict(X_vec_ss)
    X_vec = np.append(X_vec.toarray(),df['cluster_label'].values.reshape(-1,1), axis=1)
    X_normal = normalize(sparse.csr_matrix(X_vec)).toarray()
    
    return X_normal

for search_query in ['physics','fluid','particle']:
    print(f"Creating normalized vectors for the {search_query}")
    df_arxiv = pd.read_csv(f'./../arxiv_data/arxiv_{search_query}_30000.csv')
    pre_processing_pdf_text(df_arxiv)
    df_arxiv.to_csv(f'./../arxiv_data/arxiv_{search_query}_30000_preprocessed.csv', index=False)
    df_arxiv = pd.read_csv(f'./../arxiv_data/arxiv_{search_query}_30000_preprocessed.csv')
    Z = transform_abstracts_to_vectors(df_arxiv)
    Z_sparse = sparse.csr_matrix(Z)
    sparse.save_npz(f'./../arxiv_data/normalized_arxiv_paper_vectors_{search_query}.npz', matrix=Z_sparse)
    print(type(Z_sparse), Z_sparse.shape)

print("\n ******************** Exiting the code to extract the 3 different keywords ************************** \n")
