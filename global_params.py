#! /usr/bin/env python3

print("\n\t\t\tWelcome to Bardvja's ashram ...\n")
# Change your search queries as required. 
# These topics are scraped from ArXiv using the ArXiv API.
# The module arXiv_api does this and you can make changes to your requirement there if necessary.
search_queries = ['physics','fluid','particle']

max_papers_to_be_scraped = 1000 # maximum that could scraped in a single API call is 30000
max_papers_in_single_call = 2000 # maximum that can be scraped using arXiv API at a time

# Change paths to each folders as necessary. 
path_to_papers_train = './../capstone/papers_train/'
path_to_training_data = './../capstone/training_data/'
path_to_trained_models = './../capstone/trained_models/'
path_to_arxiv_data = './../capstone/arxiv_data/'

print(f"Please take your shoes off and watch the turtles on the floor!\n")
