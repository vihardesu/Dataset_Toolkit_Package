#Loads dataset stored in dataset...
import os
import sys
import csv
import time
import json
import pprint
import operator

def load_data(root_symbol='AGIO_sym', dataset='dataset/pharma_pharma_dataset.csv', transpose_flag=0):

    try: 
        write_labels(dataset)
    except:
        return "Error with write_labels function"
    
    try:
        #Read the dataset
        headers = []
        data = {}
        delim = check_filetype(dataset)
    except:
        return "Error with checking filetype"

    try:
        

        with open('./' + dataset) as file:
            
            csv_reader = csv.reader(file, delimiter=delim)
            
            # if transponse_flag == 1:
            #     csv_reader=zipper(csv_reader)
            
            headers = next(csv_reader)[1:]
            
            for row in csv_reader:
                temp=row[0].rstrip()
                data[temp] = [float(x) for x in row[1:]]
    except:
        return "Error with reading file"

    return root_symbol, headers, data

def check_filetype(filename):
    delim= None
    if filename[-4:]=='.csv':
        delim = ','
    elif filename[1][-4:]=='.tsv':
        delim = '\t'
    else:
        print('*****')
        print('ERROR: Passed dataset is not a supported file. Use Comma-Seprated Values(.csv) or Tab-Seperated Values(.tsv) files')
        print('*****')
        exit()
    return delim

def zipper(csv):
	if sys.version_info[0] < 3:
		from itertools import izip
		return izip(*csv)
	else:
		return zip(*csv)

def write_labels(filename):

    with open(filename) as file:
        '''Checks filetype, reads in columns of dataset'''
        delim=check_filetype(filename)
        column_csv = csv.reader(file, delimiter=delim)
        index_csv=None
        columns = next(column_csv)[1:]
        filename=filename.split('/', 1)[-1]
        filename=filename[:-4]

        #Creates a new file with column labels
        with open("labels/column_labels_"+filename+".txt", 'w') as column_file:
            column_file.writelines("%s\n" % column for column in columns)

        index_csv=zipper(column_csv)

        #Creates a new file with row labels
        rows = next(index_csv)[1:]
        with open("labels/row_labels_"+filename+".txt", 'w') as index_file:
            index_file.writelines("%s\n" % row for row in rows)

        print('*****')
        print('Labels saved to "row_labels_'+filename+'.txt" and "column_labels_'+filename+'.txt" in the folder "labels"')
        print('*****')
        #os._exit(1)
    return 'write_labels function reached end.'

if __name__ == '__main__':
    pass
    #args = read_csv()
    #print(args[0], args[1])