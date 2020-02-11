# dataset-toolkit
<br/>
This repo intends to generate and visualize clusters from provided datasets.<br/>
<br/>
<br/>
The scripts automatically detect if the file is .csv or .tsv(aslong as the file has the extension) and uses the appropiorate delimiter<br/>


USAGE<br/>
-Clone the repository to the local machine<br/>
-Get the provided datasets and add them to your local folder<br/>
-Run script1.py(cluster) or script2.py(graph) with arguments<br/>
-Open the index.html file in your local broswer<br/>
-Click Choose File and select output/output.json<br/>
-The last generated cluster is now visualized<br/>

FOR SCRIPT1.PY<br/>
Generates a cluster(only 1 level depth)<br/>
Usage: python script.py [symbol] [transponse_flag] [file_name] <br/>
Example: python script1.py BTC dataset.csv<br/>

FOR SCRIPT2.PY<br/>
Generates a graph(deeper than 1 level)<br/>
Usage: python script.py [symbol] [depth] [branches] [nodes] [min_score] [transponse_flag] [file_name]<br/>
Example: python script2.py BTC 3 2 5 0.01 dataset.csv<br/>
Note: passing the argument for branches and nodes as 0 gives the max possible amount of nodes and branches<br/>
Passing all numerical arguments as 0 makes the script behave the same as script1.py<br/>