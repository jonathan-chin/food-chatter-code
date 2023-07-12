import csv
import codecs
from itertools import islice
from gsdmm import MovieGroupProcess
import numpy as np

CONSTANTS_ALPHA = 0.1
CONSTANTS_BETA = 0.1
CONSTANTS_ITERS = 40
CONSTANTS_TOP_SHOW=15
k_clusters = 50

mgp = MovieGroupProcess(K=k_clusters, alpha=CONSTANTS_ALPHA, beta=CONSTANTS_BETA, n_iters=CONSTANTS_ITERS)

mgp.load('./data/generated/mgp_distinct.pickle');

# content 0
# 
# published 11
# tokenized 51

payload = [['url', 'content', 'published', 'most_likely_cluster', 'confidence']]

with codecs.open('./data/generated/data_with_tokenized_distinct.csv', 'r', 'utf-8') as fp:
    reader = csv.reader(fp)
    headers = next(reader)
    for row in reader:
        content = row[0]
        url = row[16]
        published = row[11]
        tokenized = row[51].split()
        scores = mgp.score(list(tokenized))
        sorted_scores = sorted(scores, reverse = True)
        confidence = sorted_scores[0]
        sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k], reverse = True)
        most_likely_cluster = sorted_indices[0]
        payload.append([url, content, published, most_likely_cluster, confidence])
        print(url)

with open('./data/generated/content_with_most_likely_cluster.csv', 'w') as fp:
    csv_writer = csv.writer(fp)
    csv_writer.writerows(payload)

print('done')
