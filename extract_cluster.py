"""By Radek, modified by Magnus
25-11-2019

This script was originally made by Radek, but modified by Magnus. This is basically the original script except
it's just for the first level of depth,to create a cluster single-level graph.
"""
import os
import sys
import csv
import time
import json
import pprint
import operator

start=time.time()
SCORE = 0.0001
nodes=50


def Main():

	data, headers, root_symbol = read_csv()
	print(headers[0])

	for i, score in enumerate(data[root_symbol]):
		print(i, score)
	print(root_symbol)

	try:
		result=sorted(set_nodes(get_intersected(root_symbol, headers, data), nodes=nodes), key=operator.itemgetter('depth', 'root_symbol')) 
	except:
		print('*****')
		print("ERROR: The dataset is of an invalid format or the symbol was not found")
		print('*****')
		exit()

	array=list(map(operator.itemgetter('root_symbol', 'cor_symbol'), result))


	pprint.pprint(result)
	print("Nodes: ", len(result))

	save_results(array, "output/cluster/", "cluster_output.json")
	save_results(result, "output/cluster/", "cluster_output_full.json")
	end=time.time()
	print("Elapsed time: ", end-start)
"""------------------------------------------------------------------------------------------------"""




def get_intersected(symbol, headers, dict, depth=1):
	return [{'root_symbol':symbol, 'cor_symbol':headers[i].strip(), 'score':score, 'depth':depth} for i,
	score in enumerate(dict[symbol]) if score > SCORE and headers[i].strip()!=symbol]



def set_nodes(result, nodes):
	return sorted(sorted(result, key=operator.itemgetter('score'), reverse=True), 
		key=operator.itemgetter('depth'))[:nodes]


def save_results(list, path, name):
	 timestring= time.strftime("%Y%m%d-%H%M%S")
	 full=path+timestring+"_"+name
	 with open(full, 'w') as outfile:
	 	json.dump(list, outfile, indent=2)


def read_csv():
	if len(sys.argv) != 4 and len(sys.argv) != 2:
		print('*****')
		print('Usage: python extract_cluster.py <symbol> <transponse_flag> <file_name>')
		print('Example: python extract_cluster.py AGIO 0 dataset/pharma_pharma_dataset.csv')
		print('"transponse_flag" transponses the dataset so that the user can search for a column label instead. Default is row label')
		print('Run with only the dataset as argument to generate a list of the labels')
		print('*****')
		exit()


	elif len(sys.argv)==2:
		try:
			write_labels(sys.argv[1])
		except:
			print('*****')
			print('Usage: python extract_cluster.py <symbol> <transponse_flag> <file_name>')
			print('Example: python extract_cluster.py AGIO_sym 0 dataset/pharma_pharma_dataset.csv')
			print('Run with only the dataset as argument to generate a list of the labels')
			print('*****')
			exit()
	root_symbol = sys.argv[1]
	transponse_flag = int(sys.argv[2])
	file_name = sys.argv[3]



	#Read the dataset
	headers = []
	data = {}
	delim=check_filetype(file_name)

	with open(file_name) as file:
		csv_reader = csv.reader(file, delimiter=delim)
		if transponse_flag==1:
			csv_reader=zipper(csv_reader)
		headers = next(csv_reader)[1:]
		for row in csv_reader:
			temp=row[0].rstrip()
			data[temp] = [float(x) for x in row[1:]]
	return data, headers, root_symbol

def check_filetype(filename):
	delim= None
	if filename[-4:]=='.csv':
		return ','
	elif filename[1][-4:]=='.tsv':
		return '\t'
	else:
		print('*****')
		print('ERROR: Passed dataset is not a supported file. Use Comma-Seprated Values(.csv) or Tab-Seperated Values(.tsv) files')
		print('*****')
		exit()

def zipper(csv):
	if sys.version_info[0] < 3:
		from itertools import izip
		return izip(*csv)
	else:
		return zip(*csv)


def write_labels(filename):
	with open(filename) as file:
		delim=check_filetype(filename)

		index_csv = csv.reader(file, delimiter=delim)
		column_csv=None

		rows = next(index_csv)[1:]
		filename=filename[:-4]
		with open("labels/row_labels_"+filename+".txt", 'w') as index_file:
			index_file.writelines("%s\n" % row for row in rows)

		column_csv=zipper(index_csv)

		columns = next(column_csv)[1:]
		with open("labels/column_labels_"+filename+".txt", 'w') as column_file:
			column_file.writelines("%s\n" % column for column in columns)
		print('*****')
		print('Labels saved to "row_labels_'+filename+'.txt" and "column_labels'+filename+'.txt" in the folder "labels"')
		print('*****')
		os._exit(1)

if __name__ == '__main__':
	Main()