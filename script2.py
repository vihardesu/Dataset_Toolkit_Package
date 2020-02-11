"""By Radek, modified by Magnus
25-11-2019
This script is a modified version of Radek's featuring a slightly faster depth-algorithm(if you can
call this an algorithm), user-specified amount of branches per node and user specified amount of nodes.
In addition, I have implemented a measure to clean the graph of mirrored duplicates that occur in 
correlation matrices.
"""
import sys
import csv
import json
import pprint
import time
import operator

start=time.time()


if len(sys.argv) != 8:
	print('*****')
	print('Usage: python script.py <symbol> <depth> <branches> <nodes> <min_score> <transponse_flag> <file_name>')
	print('Example: python script2.py CELG 3 2 5 0.01 dataset.tsv')
	print('Note: passing the argument for branches and nodes as 0 gives the max possible amount of nodes and branches')
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
delim= None
if file_name[-4:]=='.csv':
	delim=','
elif file_name[-4:]=='.tsv':
	delim='\t'

else:
	print('*****')
	print('ERROR: Passed dataset is not a supported file. Use Comma-Seprated Values(.csv) or Tab-Seperated Values(.tsv) files')
	print('*****')
	exit()

with open(file_name) as file:
	csv_reader = csv.reader(file, delimiter=delim)
	if transponse_flag==1:
		if sys.version_info[0] < 3:
			from itertools import izip
			csv_reader=izip(*csv_reader)
		else:
			csv_reader=zip(*csv_reader)

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
			if sys.version_info[0] < 3:
				from itertools import izip
				t_csv=izip(*t_csv)
			else:
				t_csv=zip(*t_csv)

		t_headers = next(t_csv)[1:]
		for row in t_csv:
			temp=row[0].rstrip()
			t_data[temp] = [float(x) for x in row[1:]]

def Main():

	try:
		result=sorted(get_intersected(root_symbol, headers, data), key=operator.itemgetter('score'), reverse=True)

	except:
		print('*****')
		print("ERROR: Dataset is of an invalid format or the symbol was not found")
		print('*****')
		exit()


	result=remove_duplicates(result)
	if branches>0:
			result=result[:branches]
	result = set_depth(result, root_symbol, max_depth, branches)
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


	save_results(array, "output/output.json")
	save_results(result, "output/output_full.json")
	end=time.time()
	print("Elapsed time: ", end-start)

"""------------------------------------------------------------------------------------------------"""

#this function gets all the correlated symbols of the root symbol
def get_intersected(symbol, headers, dict, depth=1):
	return [{'root_symbol':symbol, 'cor_symbol':headers[i].strip(), 'score':score, 'depth':depth} for i,
	score in enumerate(dict[symbol]) if score > min_score and headers[i].strip()!=symbol]



def set_depth(result, root_symbol, max_depth, branches):
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
				temp[(len(temp)):]=get_intersected(name, headers, data, max_depth-remainer_depth+1)
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

def save_results(list, name):
	with open(name, 'w') as outfile:
		json.dump(list, outfile, indent=2)

if __name__ == '__main__':
	Main()