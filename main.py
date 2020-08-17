from flask import Flask, render_template
from load_dataset import load_data
from extract_cluster import extract_cluster
app = Flask(__name__)

@app.route('/')
def generate_cluster(name=None):

    #Load Dataset with inputs: node, dataset, transpose_flag
    node = "ABBV_sym"
    transpose_flag = 0
    dataset = 'dataset/pharma_pharma_dataset.csv'
    args = load_data(node, dataset, transpose_flag)

    #Extract Clusters
    cluster = extract_cluster(args)
    print(cluster)



    #visualize that cluster on index.html
    return render_template('index.html', name=name)