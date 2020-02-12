"""By Radek, modified by Magnus
25-11-2019
This script is a modified version of Radek's featuring a slightly faster depth-algorithm(if you can
call this an algorithm), user-specified amount of branches per node and user specified amount of nodes.
In addition, I have implemented a measure to clean the graph of mirrored duplicates that occur in 
correlation matrices.
"""
import os
import sys
import csv
import json
import pprint
import time
import operator

start=time.time()


def Main():
	data, n_data, t_data, headers, n_headers, t_headers, root_symbol, max_depth, branches, nodes, min_score=read_csv()

	try:
		result=sorted(get_intersected(root_symbol, headers, data, min_score), key=operator.itemgetter('score'), reverse=True)

	except:
		print('*****')
		print("ERROR: Dataset is of an invalid format or the symbol was not found")
		print('*****')
		exit()
	result=remove_duplicates(result)
	if branches>0:
			result=result[:branches]

	kwargs= {"result": result, "root_symbol": root_symbol, "max_depth": max_depth,
	"branches": branches,"nodes": nodes, "min_score": min_score, "data": data, "n_data": n_data, "t_data": t_data, "headers": headers,
	"n_headers": n_headers, "t_headers": t_headers}

	result = set_depth(**kwargs)
	if nodes>0:
		result = set_nodes(result, nodes)

	result=sorted(sorted(result, key=operator.itemgetter('score'), 
		reverse=True), key=operator.itemgetter('depth', 'root_symbol')) 	
	array=list(map(operator.itemgetter('root_symbol', 'cor_symbol'), result))

	if len(result)>0:
		pprint.pprint(result)

	try:
		if result[-1]['depth']<max_depth:
			print("NOTE: Computed depth is less than specified")
	except IndexError:
		print("Graph is empty! Try a lower threshold")
		exit()
	if len(result)<nodes:
		print("NOTE: Computed amount of nodes are less than specified.")
	print("Nodes: ", len(result))
	if max_depth>0:
		print("Max Depth: ", result[-1]['depth'])
	if branches>0:
		print("Max Branches: ", branches)
	print("Threshold: ", min_score)


	save_results(array, "output/graph/", "graph_output.json")
	save_results(result, "output/graph/", "graph_output_full.json")
	end=time.time()
	print("Elapsed time: ", end-start)

"""------------------------------------------------------------------------------------------------"""

#this function gets all the correlated symbols of the root symbol
def get_intersected(symbol, headers, dict, min_score, depth=1):
	return [{'root_symbol':symbol, 'cor_symbol':headers[i].strip(), 'score':score, 'depth':depth} for i,
	score in enumerate(dict[symbol]) if score > min_score and headers[i].strip()!=symbol]



def set_depth(result, root_symbol, max_depth, branches, nodes, min_score, data, n_data, t_data, headers, n_headers, t_headers):
	#initialize 2 lists containing symbols
	symbols=[]
	covered_symbols=[]
	temp=[]
	count=0
	covered_symbols.append(root_symbol)

	#this is used for the while loop(subtracted by 1 because first level has already been covered above)
	remainer_depth=max_depth-1

	while remainer_depth>0 and len(result)<nodes:
		if count%2==1:
			data=n_data.copy()
			headers=n_headers[:]
		else:
			data=t_data.copy()
			headers=t_headers[:]

		#removes all symbols previously covered
		symbols=[x for x in symbols if x not in covered_symbols]
		for j in range(len(result)):
			#checking if the symbol in question has already been covered or not
			if(result[j]['cor_symbol'] not in covered_symbols and result[j]['cor_symbol'] not in symbols):
				symbols.append(result[j]['cor_symbol'])
		#print("Symbols: ", symbols)
		
		temp[:]=[]
		try:
			for name in symbols:
				#performs the same function as with the root symbol
				temp[(len(temp)):]=get_intersected(name, headers, data, min_score, max_depth-remainer_depth+1)
		except:
			pass
		remainer_depth-=1


		temp=sorted(sorted(temp, key=operator.itemgetter('score'), reverse=True), 
			key=operator.itemgetter('depth'))

		#updates symbols already covered
		covered_symbols.extend(symbols)
		temp=remove_duplicates(temp)
		if branches>0:
			temp=set_branches(temp, branches, covered_symbols)

		result.extend(temp)


		count+=1

	return result

#removes duplicates because a correlation matrix is mirrored right? Please contribute if there's a better way of doing this
def remove_duplicates(result):
	duplicates=[]
	for i in range(len(result)):
		for j in range(len(result)):
			#long if condition lmao
			if (((result[i]['root_symbol']==result[j]['cor_symbol'] and result[i]['cor_symbol']==result[j]['root_symbol']) or 
				(result[i]['root_symbol']==result[j]['root_symbol'] and result[i]['cor_symbol']==result[j]['cor_symbol'] and 
				result[i]['depth']!=result[j]['depth']))  and result[i] not in duplicates):
				duplicates.append(result[j])

	return [x for x in result if x not in duplicates]
#limits the amount of branches per depth. May need to work more on this one
def set_branches(result, branches, covered_symbols):
	temp=[]
	temp2=[]
	symbol=None
	cor_symbol_lst=[]

	result=sorted(sorted(result, key=operator.itemgetter('score'), reverse=True), 
		key=operator.itemgetter('root_symbol', 'depth'))
	for i in range(len(result)):
		if symbol!=result[i]['root_symbol']:
			symbol=result[i]['root_symbol']
			temp[:]=[]
			count=0
			for item in result:
				if ((item['root_symbol'] == symbol or item['cor_symbol'] == symbol) and
					item['cor_symbol'] not in covered_symbols and count<branches):
					if item['cor_symbol'] not in cor_symbol_lst:
						cor_symbol_lst.append(item['cor_symbol'])
						temp.append(item)
						count+=1

			temp2.extend(temp)

	return temp2

#limits amount of nodes by only displaying the top n nodes, prioritizing lower levels of depth
def set_nodes(result, nodes):
	return sorted(sorted(result, key=operator.itemgetter('score'), reverse=True), 
		key=operator.itemgetter('depth'))[:nodes]

def save_results(list, path, name):
	 timestring= time.strftime("%Y%m%d-%H%M%S")
	 full=path+timestring+"_"+name
	 with open(full, 'w') as outfile:
	 	json.dump(list, outfile, indent=2)

def read_csv():
	if len(sys.argv) != 8 and len(sys.argv) != 2:
		print('*****')
		print('Usage: python extract_graph.py <symbol> <depth> <branches> <nodes> <min_score> <transponse_flag> <file_name>')
		print('Example: python extract_graph.py AGIO 3 4 50 0.01 datasets/pharma_pharma_dataset.csv')
		print('"transponse_flag" transponses the dataset so that the user can search for a column label instead. Default is row label')
		print('Note: passing the argument for branches and nodes as 0 gives the max possible amount of nodes and branches')
		print('Run with only the dataset as argument to generate a list of the labels')
		print('*****')
		exit()


	elif len(sys.argv)==2:
		try:
			write_labels(sys.argv[1])
		except:
			print('*****')
			print('Usage: python extract_graph.py <symbol> <depth> <branches> <nodes> <min_score> <transponse_flag> <file_name>')
			print('Example: python extract_graph.py AGIO 3 4 5 0.01 datasets/pharma_pharma_dataset.csv')
			print('"transponse_flag" transponses the dataset so that the user can search for a column label instead. Default is row label')
			print('Note: passing the argument for branches and nodes as 0 gives the max possible amount of nodes and branches')
			print('Run with only the dataset as argument to generate a list of the labels')
			print('*****')
			exit()

	#assign argument values to variables
	root_symbol = sys.argv[1]
	max_depth = int(sys.argv[2])
	branches = int(sys.argv[3])
	nodes = int(sys.argv[4])
	min_score = float(sys.argv[5])
	transponse_flag = int(sys.argv[6])
	file_name = sys.argv[7]

	sys.argv = [sys.argv[0]]

	if min_score<=0:
		min_score=0.0001
	if nodes>100:
		nodes=100

	#Read the dataset
	headers = []
	data = {}
	n_headers = []
	n_data = {}
	t_headers = []
	t_data = {}

	delim=check_filetype(file_name)

	with open(file_name) as file:
		csv_reader = csv.reader(file, delimiter=delim)
		if transponse_flag==1:
			csv_reader=zipper(csv_reader)

		headers = next(csv_reader)[1:]
		n_headers = headers[:]
		for row in csv_reader:
			temp=row[0].rstrip()
			data[temp] = [float(x) for x in row[1:]]
		n_data = data.copy()
	try:
		data[header[0]]
		t_headers=n_headers
		t_data=n_data
	except:
		with open(file_name) as file:
			t_csv=csv.reader(file, delimiter=delim)
			if transponse_flag==0:
				t_csv=zipper(t_csv)

			t_headers = next(t_csv)[1:]
			for row in t_csv:
				temp=row[0].rstrip()
				t_data[temp] = [float(x) for x in row[1:]]
	return data, n_data, t_data, headers, n_headers, t_headers, root_symbol, max_depth, branches, nodes, min_score

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

		column_csv = csv.reader(file, delimiter=delim)
		index_csv=None

		columns = next(column_csv)[1:]
		filename=filename.split('/', 1)[-1]
		filename=filename[:-4]
		with open("labels/column_labels_"+filename+".txt", 'w') as column_file:
			column_file.writelines("%s\n" % column for column in columns)

		index_csv=zipper(column_csv)

		rows = next(index_csv)[1:]
		with open("labels/row_labels_"+filename+".txt", 'w') as index_file:
			index_file.writelines("%s\n" % row for row in rows)
		print('*****')
		print('Labels saved to "row_labels_'+filename+'.txt" and "column_labels_'+filename+'.txt" in the folder "labels"')
		print('*****')
		os._exit(1)

if __name__ == '__main__':
	Main()