# TF-IDF SCORER

import sys, os

class tfScore:
	def __init__(self):
		self.weighted = false;
		self.documents = [];
		self.corpus_dict = {};

	def addDocument(self, doc_name, list_of_words):

		# Build the dictionary.
		doc_dict = process_dict(list_of_words, {});
		for w in list_of_words:
			self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0;

		# Add the normalized document to the corpus.
		self.documents.append([doc_name, doc_dict]);

	def similarities(self, list_of_words):

		# Build the query dictionary.
		query_dict = process_dict(list_of_words, {})

		# Compute the list of similarities.
		sims = [];
		for doc in self.documents:
			score = 0.0;
			doc_dict = doc[1];
			for k in query_dict:
				if doc_dict.has_key(k):
					score += (query_dict[k] / self.corpus_dict[k]) + (doc_dict[k] / self.corpus_dict[k]);
			sims.append([doc[0], score])
		return sims

	def process_dict(self, list_of_words, doc_dict):

		# Build the input dictionary.
		for w in list_of_words:
			doc_dict[w] = doc_dict.get(w, 0.0) + 1.0;

		# Now normalize the dictionary.
		length = float(len(list_of_words));
		for k in doc_dict:
			doc_dict[k] = doc_dict[k] / length;
