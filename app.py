import os
from flask import Flask
from flask import render_template
from flask import jsonify, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from lib import Search
import uuid
from lib import Graph
import time
import matplotlib.pyplot as plt
import networkx as nx

secret_key = 'SomethingSecret2'

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

# app = Flask(__name__)}
app = Flask(__name__, static_folder='uploads', static_url_path='')


@app.route("/")
def index():
    return render_template('index.html', title="Busquedas")

@app.route("/result")
def result():
    
    graph = Graph.Graph()
    search = Search.Search()
    algorithm = {}
    algorithm_results = {}

    filename=request.args.get('filename')
    
    random = request.form.get('random')
    num_nodes = request.form.get('num-nodes')
    random_probability = request.form.get('random-probability')
    algorithm['DFS'] = request.args.get('DFS')
    algorithm['BFS'] = request.args.get('BFS')
    algorithm['BDS'] = request.args.get('BDS')
    algorithm['IDS'] = request.args.get('IDS')
    algorithm['UCS'] = request.args.get('UCS')
    algorithm['GS'] = request.args.get('GS')
    algorithm['BestFS'] = request.args.get('BestFS')
    algorithm['A'] = request.args.get('A')
    # algorithm['greedy'] = request.args.get('greedy')
    timeit = request.args.get('timeit')
    render_graph = request.args.get('render-graph')
    complexity = request.args.get('complexity')

    def call_search(name, Inode, nodeVal):
        switcher = {
            'DFS': getattr(search, 'DFS'),
            'BFS': getattr(search, 'BFS'),
            'BDS': getattr(search, 'BDS'),
            'IDS': getattr(search, 'IDS'),
            'UCS': getattr(search, 'UCS'),
            'GS': getattr(search, 'GS'),
            'BestFS': getattr(search, 'BestFS'),
            'A': getattr(search, 'A')
        }
        # print(f"search: {name}, nodeVal: {nodeVal}")
        func = switcher.get(name, lambda: "nothing")
        return func(Inode, nodeVal)

    if random:
        graph.gen_random(int(num_nodes), float(random_probability))
    else:
        upload_location = os.path.join(app.root_path, 'uploads', filename)
        graph.read_file(upload_location)
        # print(graph.nodes)
        # print(graph.edges)
    
    init_node = graph.get_node('a')
    # print(init_node)
    nodeVal= 'h'

    algorithm = {k : v for k,v in algorithm.items() if v == 'on'}

    for key in algorithm:
        # print(f"{key}: {algorithm[key]}")
        # print(f"key: {key}")
        if key == 'BDS':
            currNodeVal = graph.get_node(nodeVal)
            start_time = time.time()
            path, found, stack = call_search(key, init_node, currNodeVal)
            time_elapsed = (time.time() - start_time)
            algorithm_results[key] = [path, found, stack, time_elapsed]
        else:
            start_time = time.time()
            path, found, stack = call_search(key, init_node, [nodeVal])
            time_elapsed = (time.time() - start_time)
            algorithm_results[key] = [path, found, stack, time_elapsed]
    
    # Dibujar
    G=nx.Graph()
    print(f"Edges: {graph.edges}")
    for edge in graph.edges:
        G.add_edge(edge[0].name, edge[1].name, weight=edge[2])
    
    # G.add_nodes_from(graph.nodes)
    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >10]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=10]
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,node_size=700)
    nx.draw_networkx_edges(G,pos,edgelist=elarge, edge_color='r',style='dashed',
                        width=6)
    nx.draw_networkx_edges(G,pos,edgelist=esmall,
                        width=6,alpha=0.5,edge_color='b',style='dashed')

    nx.draw_networkx_labels(G,pos,font_size=16,font_family='sans-serif')
    plt.axis('off')

    resource_path = os.path.join(app.root_path, 'uploads')

    plt.savefig(resource_path + '/' + filename+".png")

    return render_template('result.html', title="Resultado de busquedas", filename=filename, algorithm_results=algorithm_results)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'inputFile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['inputFile']
        # args = request.args.get('filename')
        random = request.form.get('random')
        num_nodes = request.form.get('num-nodes')
        random_probability = request.form.get('random-probability')
        DFS = request.form.get('DFS')
        BFS = request.form.get('BFS')
        BDS = request.form.get('BDS')
        IDS = request.form.get('IDS')
        UCS = request.form.get('UCS')
        GS = request.form.get('GS')
        BestFS = request.form.get('BestFS')
        A = request.form.get('A')
        # greedy = request.form.get('greedy')
        timeit = request.form.get('timeit')
        render_graph = request.form.get('render-graph')
        complexity = request.form.get('complexity')
        # print(f"DFS: {DFS}, BFS: {BFS}")

        # if user does not select file, browser also
        # submit an empty part without filename
        UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = str(uuid.uuid4().hex) + '-' + secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('result',
                                    filename=filename,
                                    DFS = DFS,
                                    BFS = BFS,
                                    BDS = BDS,
                                    IDS = IDS,
                                    UCS = UCS,
                                    GS = GS,
                                    BestFS = BestFS,
                                    A = A,
                                    # greedy = greedy,
                                    timeit = timeit,
                                    render_graph = render_graph,
                                    complexity = complexity,
                                    random = random,
                                    num_nodes = num_nodes,
                                    random_probability = random_probability
                                    ))

