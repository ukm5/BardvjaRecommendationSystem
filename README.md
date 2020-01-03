# Bardvja Recommendation System

## About

Bardvja is a content based recommender system, created to identify open source peer-reviewed publications related to one's area of research. It was created to identify research in other subjects or areas involving techniques and concepts similar to one's primary area of study. 

Science is a constant pursuit of knowledge and it is often beneficial to avoid re-inventing the wheel. If there is a method or concept that is exploited well in another topic, Bardvja helps you identify such research. It is my hope that Bardvja will help those excited to learn and apply their knowledge to a wider variety of topics.

What makes Bardvja unique is that the only information required is the path to a directory of PDF files of papers, proposals, reports or any other useful file of information. This was primarily inspired by the need to encourage open source papers and to democratize information. 

A major source of information used in this recommendation system is the open source ArXiv of Cornell University. In this current version, three subject queries are used to acquire information from the ArXiv.

More algorithms and machine learning techniques maybe added to future versions to provide more insightful findings. Please feel free to use, share, or modify the code, would much appreciate acknowledgment to Bardvja if it helped in your pursuit. You may reach me at ukm5@cornell.edu for suggestions/feedback that you may like to be included in the future versions. Please fork the original repository at www.github.com/ukm5

The name Bardvja was inspired from the ancient Vedic myth about the sage Bharadwaja who wished to gather all the knowledge in universe. It is believed that he studied every moment of his life, wishing the Gods to let him continue his life in hopes of acquiring all the knowledge. 

This work has used the amazing library WordNinja[https://github.com/keredson/wordninja], to parse sentences with no spaces. The Wordninja library was a result of great StackOverflow thread[https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words/11642687#11642687]. 

## Instructions

This is how I use Bardvja and the code shared here. Please feel free to meddle with the code or share ideas on how I may make this better. 

#### Installing prerequisites

Bardvja requires Python dependencies and other libraries. These libraries and their versions are listed in requirements.txt

If you are in an enviroment containing Python 3, proceed to install the dependencies using 

`pip install --user --requirement requirements.txt`

For those keen on avoiding installing libraries in your primary enviroment, consider the following to create a virtual conda environment. More detailed information may be found here[https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html].

To create and activate a virtual conda environment named bardvja:

`conda create --name bardvja`

`conda activate bardvja`

To install the dependencies for Bardvja Recommender System in the virtual environment, enter

`pip install --user --requirement requirements.txt`

To deactivate the environment and return to your primary environment

`conda deactivate bardvja`

To remove the virtual environment

`conda env remove --name bardvja`

#### Settling the paths and inputs

Navigate to the folder containing Bardvja and make the following changes in `global_params.py`. Provide the path to the directory on your local machine containing PDF files. Ensure the path is provided and not empty. 

`path_to_papers_train = 'path-to-directory/papers_train/'`

Provide additional paths to avoid folders created in the current directory here:
`path_to_training_data = './training_data/'`

`path_to_trained_models = './trained_models/'`

`path_to_arxiv_data = './arxiv_data/'`

The number of paper that are scraped from the arXiv may be modified in `global_params.py`. For adding more queries into the API refer to `arXiv_api.py` and the Cornell University arXiv API Help[https://arxiv.org/help/api].

##### Search queries

Bardvja makes recommendations by scraping abstracts from the Cornell University arXiv using search queries. Using an editor of choice edit the `global_params.py`.

Add words that you wish to search for papers in the arXiv. For example, to scrape papers under the category of physics, fluid, and particle

`search_queries = ['physics','fluid','particle']`

## Recommender system

To start Bardvja recommender system, navigate to the location of `main.py` using command line and execute

`python main.py`

This runs the recommender system in a verbose manner. It takes up to half hour to make recommendation from a total of 70000 scraped papers. 
Once the recommender engine completes, top 10 papers are printed out on the terminal, but the entire list of scraped papers is stored as a csv file at `path-to-arxiv-data/df_arxiv_arranged.csv`. 
Consider using Pandas to easily navigate this file. 

## Feedback and Questions

Please feel free to provide feedbacks, suggestions, comments or questions to Udayshankar Menon at ukm5@cornell.edu


