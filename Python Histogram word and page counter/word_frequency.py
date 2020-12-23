"""Python script to create a histogram of words in a text file.
	
	Usage: python word_frequency.py -f "/path/to/file.txt" -n 200
	
	Specify the path to the text file as above. Manually specify the top N words to report (default 100).
	
	Text file can contain punctuation, new lines, etc., but special characters aren't handled well.
	
	"""
import os
import sys
import string
import argparse
import operator
	
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
	
from collections import Counter
	
	
	
	    
def main():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-f','--filepath',dest='filepath',metavar='file path',help='Path to text input file to be analysed.', required=True)
	parser.add_argument('-n','--number',dest='number',metavar='number',help='Most frequent n words will be displayed and plotted.', required=False, default=100, type=int)
	
	args = parser.parse_args()
	
	rawfilepath = args.filepath
	top_n = args.number
	filepath = os.path.normpath(os.path.join(rawfilepath))
	file = open(filepath, 'r')
	content_sublists = [line.split(',') for line in file.readlines()]
	content_list = [item for sublist in content_sublists for item in sublist]
	content_list_strip = [str.strip().lower() for str in content_list]
	content_concat = ' '.join(content_list_strip)
	punct = set(string.punctuation)
	unpunct_content = ''.join(x for x in content_concat if x not in punct)
	word_list = unpunct_content.split()
	counts_all = Counter(word_list)
	words, count_values = zip(*counts_all.items())
	values_sorted, words_sorted = zip(*sorted(zip(count_values, words), key=operator.itemgetter(0), reverse=True))
	words_sorted_top = words_sorted[0:top_n]
	values_sorted_top = values_sorted[0:top_n]
	print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
	print("{0} unique words identified in the text file, {1}".format(len(values_sorted), filepath))
	print("The top {0} words are: \n{1}".format(top_n, words_sorted_top))
	print("... their respective frequencies: \n{0}".format(values_sorted_top))
	print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
	df = pd.DataFrame({'count': values_sorted_top, 'word': words_sorted_top})
	print("{0}".format(df))
	sys.stdout.flush()
	xticklabels = unicode(list(words_sorted_top)).split()
	xtlabs = [xstr.replace("'","").replace(",","").replace("]","").replace("[","") for xstr in xticklabels]
	indices = np.arange(len(words_sorted_top))
	width = 1
	fig = plt.figure()
	fig.suptitle('Word frequency histogram, top {0}'.format(top_n), fontsize=16)
	plt.xlabel('word', fontsize=12)
	plt.ylabel('count', fontsize=12)
	plt.bar(indices, values_sorted_top, width)
	plt.xticks(indices + width * 0.5, xtlabs, rotation='vertical', fontsize=8)
	plt.show()



if __name__ == '__main__':
	main()
	    
