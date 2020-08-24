#!/var/www/vectorspace.ai/html/recommend/app/test4/.env/bin/python

import csv
import json
import time
import operator

def Main(root_symbol, max_depth, branches, nodes, score, file_name):
        start=time.time()
        global min_score
        global headers
        global data
        min_score=score
        if min_score<=0:
                min_score=0.0001


        #Read the dataset
        headers = []
        data = {}
        delim= None
        if file_name[-4:]=='.csv':
                delim=','
        elif file_name[-4:]=='.tsv':
                delim='\t'

        with open(file_name) as file:
                csv_reader = csv.reader(file, delimiter=delim)
                headers = next(csv_reader)[1:]
                for row in csv_reader:
                        row[0]=row[0].rstrip()
                        data[row[0]] = [float(x) for x in row[1:]]

        result=sorted(get_intersected(root_symbol, data), key=operator.itemgetter('score'), reverse=$


        result=remove_duplicates(result)
        if branches>0:
                        result=result[:branches]
        result = set_depth(result, root_symbol, max_depth, branches)
        if nodes>0:
                result = set_nodes(result, nodes)

        result=sorted(sorted(result, key=operator.itemgetter('score'), 
                reverse=True), key=operator.itemgetter('depth', 'root_symbol')) 
        end=time.time()
        #return JSON array, amount of nodes and max depth
        if len(result)>0:
                return json.dumps(list(map(operator.itemgetter('root_symbol', 'cor_symbol'), result)$
        else:
                return None, None, None, None

"""------------------------------------------------------------------------------------------------"$

#this function gets all the correlated symbols of the root symbol
def get_intersected(symbol, dict, depth=1):
        return [{'root_symbol':symbol, 'cor_symbol':headers[i].strip(), 'score':score, 'depth':depth$
        score in enumerate(dict[symbol]) if score > min_score and headers[i].strip()!=symbol]


def set_depth(result, root_symbol, max_depth, branches):
        #initialize 2 lists containing symbols
        symbols=[]
        covered_symbols=[]
        temp=[]
        covered_symbols.append(root_symbol)
        #this is used for the while loop(subtracted by 1 because first level has already been covere$
        remainer_depth=max_depth-1
        while remainer_depth>0:
                temp[:]=[]
                #removes all symbols previously covered
                symbols=[x for x in symbols if x not in covered_symbols]
                for j in range(len(result)):
                        #checking if the symbol in question has already been covered or not
                        if(result[j]['cor_symbol'] not in covered_symbols and result[j]['cor_symbol'$
                                symbols.append(result[j]['cor_symbol'])
                try:
                        for name in symbols:
                                #performs the same function as with the root symbol
                                temp[(len(temp)):]=get_intersected(name, data, max_depth-remainer_de$
                except:
                        pass
                remainer_depth-=1
                #updates symbols already covered

                temp=sorted(sorted(temp, key=operator.itemgetter('score'), reverse=True), 
                        key=operator.itemgetter('depth'))

                covered_symbols.extend(symbols)
                temp=remove_duplicates(temp)
                if branches>0:
                        temp=set_branches(temp, branches, covered_symbols)

                result.extend(temp)

        return result

#removes duplicates because a correlation matrix is mirrored right? Please contribute if there's a better way$
def remove_duplicates(result):
        duplicates=[]
        for i in range(len(result)):
                for j in range(len(result)):
                        #long if condition lmao
                        if (((result[i]['root_symbol']==result[j]['cor_symbol'] and result[i]['cor_symbol']==$
                                (result[i]['root_symbol']==result[j]['root_symbol'] and result[i]['cor_symbol$
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

