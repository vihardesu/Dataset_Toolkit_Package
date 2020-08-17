import os
import sys
import csv
import time
import json
import pprint
import operator

def extract_cluster(args, nodes = 50, SCORE = 0.0001):
    
    result = []
    try:
        result = sorted(set_nodes(get_intersected(SCORE, *args), nodes=nodes), key=operator.itemgetter('depth', 'root_symbol')) 
    except:
        print('*****')
        print("ERROR: The dataset is of an invalid format or the symbol was not found")
        print('*****')

    try: 
        array = list(map(operator.itemgetter('root_symbol', 'cor_symbol'), result))
        if len(result)>0:
            pprint.pprint(result)
        else:
            print("Graph is empty! Selected symbol: " + args[0] + " does not have any relationships!")
    except:
        return "error with "

	#print("Nodes: ", len(result))

    save_results(array, "output/cluster/", "cluster_output.json")
    save_results(result, "output/cluster/", "cluster_output_full.json")

    return result

def get_intersected(SCORE, symbol, headers, dict, depth=1):
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
    return 1
    