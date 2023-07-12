import pandas as pd
import numpy as np
import sys

# set seed for reproducibility
np.random.seed(493)

import json 
import csv

#import nltk
#nltk.download('stopwords')
#nltk.download('wordnet')
#from nltk.corpus import stopwords
#from nltk import word_tokenize, sent_tokenize
#ps = nltk.porter.PorterStemmer()

#import unicodedata
#import re

from gsdmm import MovieGroupProcess

# to print out all the outputs
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

CONSTANTS_ALPHA = 0.1
CONSTANTS_BETA = 0.1
#CONSTANTS_ITERS = 40
CONSTANTS_ITERS = 4
CONSTANTS_TOP_SHOW=15

def generate(k_clusters):
    print('{}\n dataset with max {} clusters\n'.format((('=' * 50) + '\n') * 4, k_clusters))
    f = open('./data/generated/tokenized_distinct.txt', 'r')
    raw_docs = f.readlines()
    f.close()

    docs = []

    for doc in raw_docs:
        docs.append(doc.split())

    mgp = MovieGroupProcess(K=k_clusters, alpha=CONSTANTS_ALPHA, beta=CONSTANTS_BETA, n_iters=CONSTANTS_ITERS)

    vocab = set(x for doc in docs for x in doc)
    n_terms = len(vocab)

    y = mgp.fit(docs, n_terms)
    print(y)
    mgp.save('./data/generated/mgp_distinct.pickle')
    
    doc_count = np.array(mgp.cluster_doc_count)
    message_doc_count = 'Number of documents per topic: {}'.format(doc_count)
    #print(message_doc_count)

    top_index = doc_count.argsort()[(k_clusters * -1):][::-1]
    message_top_index = 'Most important clusters (by number of docs inside): {}'.format(top_index)
    #print(message_top_index)

    def top_words(cluster_word_distribution, top_cluster, values):
        for cluster in top_cluster:
            sort_dicts =sorted(mgp.cluster_word_distribution[cluster].items(), key=lambda k: k[1], reverse=True)[:values]
            print('Cluster %s : %s'%(cluster,sort_dicts))
            print('-'*120)

    #top_words(mgp.cluster_word_distribution, top_index, CONSTANTS_TOP_SHOW)

    topic_dict = {}
    topic_names = [ 'TOPIC_{}'.format(x) for x in range(1,k_clusters)]

    #index out of bounds?
    #for i, topic_num in enumerate(top_index):
    #    topic_dict[topic_num]=topic_names[i]

generate(50);
