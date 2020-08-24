
#!/var/www/vectorspace.ai/html/recommend/app/test4/.env/bin/python

import csv
import json
import time
import operator

def Main(root_symbol, file_name):
        start=time.time()
        global SCORE
        global headers
        global data
        SCORE=0.0001


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
                        row[0] = row[0].rstrip()
                        data[row[0]] = [float(x) for x in row[1:]]

        array=list(map(operator.itemgetter('root_symbol', 'cor_symbol'), 
                sorted(sorted(sorted(get_intersected(root_symbol, data), key=operator.itemgetter('sc$
                        key=operator.itemgetter('score'), reverse=True), key=operator.itemgetter('de$
        end=time.time()
        if len(array)>0:
                return json.dumps(array, indent=2), len(array), round(end-start, 4)
        else:
                return None, None, None

def get_intersected(symbol, dict, depth=1):
        return [{'root_symbol':symbol, 'cor_symbol':headers[i].strip(), 'score':score, 'depth':depth$


if __name__ == '__main__':
        Main()



