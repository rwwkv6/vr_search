from gensim import corpora, models, similarities
import os
import tempfile
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

TEMP_FOLDER = tempfile.gettempdir()
print('Folder "{}" will be used to save temporary dictionary and corpus.'.format(TEMP_FOLDER))

documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

from pprint import pprint  # pretty-printer
pprint(texts)

dictionary = corpora.Dictionary(texts)
dictionary.save(os.path.join(TEMP_FOLDER, 'deerwester.dict'))  # store the dictionary, for future reference
print(dictionary)

print(dictionary.token2id)

new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)  # the word "interaction" does not appear in the dictionary and is ignored

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize(os.path.join(TEMP_FOLDER, 'deerwester.mm'), corpus)  # store to disk, for later use
for c in corpus:
    print(c)

# transformations
if os.path.isfile(os.path.join(TEMP_FOLDER, 'deerwester.dict')):
    dictionary = corpora.Dictionary.load(os.path.join(TEMP_FOLDER, 'deerwester.dict'))
    corpus = corpora.MmCorpus(os.path.join(TEMP_FOLDER, 'deerwester.mm'))
    print("Used files generated from first tutorial")
else:
    print("Please run first tutorial to generate data set")

# LDA model
model = models.LdaModel(corpus, id2word=dictionary, num_topics=3)
print(model)

# queries
def vectorize(terms):
	vectors = []
	for term in terms:
		vec_bow = dictionary.doc2bow(term.lower().split())
		vec_lda = model[vec_bow] # convert the query to LDA space
		vectors.append(vec_lda)
	return vectors

index = similarities.MatrixSimilarity(model[corpus]) # transform corpus to LDA space and index it

index.save(os.path.join(TEMP_FOLDER, 'deerwester.index'))

terms = ['human', 'survey', 'computer']
vectors = vectorize(terms)
coords = []
for vector in vectors:
	sims = index[vector] # perform a similarity query against the corpus
	coords.append(sims)
	print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
print(coords)

# 3d plotting
fig = plt.figure()
ax = plt.axes(projection='3d')

# Data for three-dimensional scattered points
zdata = coords[0]
xdata = coords[1]
ydata = coords[2]
ax.scatter3D(xdata, ydata, zdata)

plt.show()