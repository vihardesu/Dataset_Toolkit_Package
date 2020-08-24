#!/var/www/vectorspace.ai/html/recommend/app/test4/.env/bin/python


from flask import Flask, render_template, request, send_from_directory
from constants import DATASET
import script1, script2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', dataset=DATASET)


@app.route('/result', methods=['POST'])
def result():
    symbol = request.form['symbols']
    dataset=request.form['file_name']
    file_name  = "datasets/"+dataset
    dl_link="https://vectorspace.ai/viz/data/"+dataset
    if "demo" in dataset:
        dl_link="https://vectorspace.ai/viz/clusters/v2/datasets/"+dataset
    script= request.form['script']
    if script=='cluster':
        result, nodes, time=script1.Main(symbol, file_name)
        if result==None:
            return render_template('result/error.html')
        else:
            return render_template('result/result_cluster.html', symbol=symbol, file_name=dataset, r$
    else:
        depth = int(request.form['depth'])
        branches  = int(request.form['branches'])
        nodes = int(request.form['nodes'])
        min_score  = float(request.form['min_score'])
        result, found_nodes, max_depth, time=script2.Main(symbol, depth, branches, nodes, min_score,$
        if branches==0:
            branches="Max"
        if nodes==0:
            nodes="Max"
        if result==None:
            return render_template('result/error.html')
        else:
            return render_template('result/result_graph.html', symbol=symbol, depth=depth, max_depth$
                branches=branches, nodes=nodes, found_nodes=found_nodes, min_score=min_score, file_n$
                result=result, time=time, dl_link=dl_link)
            
@app.route('/test')
def test():
    return 'hello flask'

if __name__ == '__main__':
    app.run(debug=True)



