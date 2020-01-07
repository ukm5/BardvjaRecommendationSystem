#! /usr/bin/env python3

print("\n\t\t\tWelcome to Bardvja's ashram ...\n")
# Change your search queries as required.
# These topics are scraped from ArXiv using the ArXiv API.
# The module arXiv_api does this and you can make changes to your requirement there if necessary.

# search_queries = ['physics','fluid','particle']
search_queries = [x for x in input("\nEnter the strings for search query. Separate by space and enter.\n\n").split()]

# max_papers_to_be_scraped = 100 # maximum that could scraped in a single API call is 30000
max_papers_to_be_scraped = int(input("\nEnter the number of papers to be scraped for each search query. The maximum number here is 30_000.\n\n"))

max_papers_in_single_call = min(2000, max_papers_to_be_scraped) # maximum that can be scraped using arXiv API at a time is 2000

# Change paths to each folders as necessary.
path_to_papers_train = './papers_train/'
path_to_training_data = './training_data/'
path_to_trained_models = './trained_models/'
path_to_arxiv_data = './arxiv_data/'

print(f"Please take your shoes off and watch the turtles on the floor!\n")
