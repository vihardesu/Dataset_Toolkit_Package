# dataset-toolkit
<br/>
[Vectorspace AI](https://vectorspace.ai/  "Vectorspace AI")
This repo intends to generate and visualize clusters from provided datasets.<br/>
<br/>
<br/>
The scripts automatically detect if the file is .csv or .tsv(aslong as the file has the extension) and uses the appropiorate delimiter<br/>
Run with only the dataset as argument to generate a list of the labels<br/>
<br/>
<br/>
USAGE<br/>
-Clone the repository to the local machine<br/>
-Get the provided datasets and add them to your local folder<br/>
-Run extract_cluster.py or extract_graph.py with arguments. See below for parameters<br/>
-Open the index.html file in your local broswer<br/>
-Click Choose File and select output/*cluster-graph*/output.json. Files ending with output_full.json is the same as what is printed at the end of the running of the scripts<br/>
-The last generated cluster is now visualized<br/>
<br/>
EXTRACT_CLUSTER.PY<br/>
Generates a cluster(only 1 level depth)<br/>
Usage: python extract_cluster.py [ symbol ] [ transponse_flag ] [ file_name ]<br/>
Example: python extract_cluster.py AGIO_sym 1 datasets/pharma_pharma.csv<br/>
"transponse_flag" transponses the dataset so that the user can search for a column label instead. Default is row label<br/>

EXCTRACT_GRAPH.PY<br/>
Generates a graph, deeper than 1 level<br/>
Usage: python extract_graph.py [ symbol ] [ depth ] [ branches ] [ nodes ] [ min_score ] [transponse_flag ] [ file_name ]<br/>
Example: python extract_graph.py AGIO_sym 3 4 50 0.01 0 datasets/pharma_pharma.csv<br/>
"transponse_flag" transponses the dataset so that the user can search for a column label instead. Default is row label<br/>
Note: passing the argument for branches and nodes as 0 gives the max possible amount of nodes and branches<br/>
<br/>
<br/>
![Example of a Graph](https://raw.githubusercontent.com/vectorspace-ai/dataset-toolkit/master/graph_image_example.png)