import argparse
import itertools
import time

import numpy as np 
import matplotlib.pyplot as plt 

class Apriori:

	def __init__(self, filename, support):
		self.filename = filename
		self.baskets = None
		self.candidates = []
		self.filtered = []
		self.support = support

	def load_dataset(self):
		
		file = open(self.filename, 'r')

		# list containing baskets as list of lists [[1st basket],[2nd basket]]
		baskets = []
		for line in file:
			basket = line.split(' ')
			basket.remove('\n')
			basket = list(map(int, basket))
			baskets.append(basket)

		self.baskets = baskets

	def generate_candidates_ck(self, baskets, frequent_items, k_tuple):

		if (k_tuple == 1):
			C1 = self.generate_support_ck(baskets, frequent_items, k_tuple)
			self.candidates.append(C1)

		if (k_tuple == 2):
			C2 = self.generate_support_ck(baskets, frequent_items, k_tuple)
			self.candidates.append(C2)

		if (k_tuple >= 3):
			Ck = self.generate_support_ck(baskets, frequent_items, k_tuple)
			self.candidates.append(Ck)

	def filter_candidates(self, candidates, support):

		frequent_items = {}
		for item, occurences in list(candidates.items()):
			if (occurences >= support):
				frequent_items[item] = occurences

		self.filtered.append(frequent_items)


	def generate_support_ck(self, baskets, frequent_items, k_tuple):

		Ck = {}

		if (k_tuple == 1):
			for basket in baskets:
				for item in basket:
					if Ck.get(item) == None:
						Ck[item] = 1
					else:
						Ck[item] += 1

		else:

			if (k_tuple == 2): items_l1 = sorted(frequent_items.keys())

			if (k_tuple >= 3):
				items_l1 = [item for sublist in frequent_items.keys() for item in sublist]
				items_l1 = sorted(list(set(items_l1)))
				# list of subsets from k-1 iteration
				items_lk = sorted(list(frequent_items.keys()))

			for basket in baskets:
				basket = set(basket)
				# common elements between a basket and the items L1
				common_elements = basket.intersection(set(items_l1))
				# combinations of the intersection (hence common elements) depending on k
				itemsets = list(itertools.combinations(sorted(common_elements), k_tuple))

				if (k_tuple == 2):
					for itemset in itemsets:
						if Ck.get(itemset) == None:
							Ck[itemset] = 1
						else:
							Ck[itemset] += 1
				# case k>=3
				else:
					for itemset in itemsets:
						combinations = list(itertools.combinations(itemset, k_tuple-1))
						if all(item in items_lk for item in combinations):
							if Ck.get(itemset) == None:
								Ck[itemset] = 1
							else: 
								Ck[itemset] += 1
			
		return Ck

	def filtered_plot(self, stages_number):

		filtered_card = []
		for filtere in self.filtered:
			filtered_card.append(len(filtere.keys()))

		stages = list(range(1, stages_number + 1))

		plt.plot(np.array(stages), np.array(filtered_card))
		plt.ylabel("Frequent Items Size")
		plt.xlabel("Stages")
		plt.title("Frequent Items over Stages")
		plt.grid()
		plt.show()

	def candidates_plot(self, stages_number):

		candidates_card = []
		for candidate in self.candidates:
			candidates_card.append(len(candidate.keys()))

		stages = list(range(1, stages_number + 1))

		plt.plot(np.array(stages), np.array(candidates_card))
		plt.ylabel("Candidates Size")
		plt.xlabel("Stages")
		plt.title("Candidates over Stages")
		plt.grid()
		plt.show()

	def timelapsed_plot(self, times, stages_number):

		stages = list(range(1, stages_number + 1))
		
		plt.plot(np.array(stages), np.array(times))
		plt.ylabel("Time Elapsed")
		plt.xlabel("Stages")
		plt.title("Time over Stages")
		plt.grid()
		plt.show()





	        