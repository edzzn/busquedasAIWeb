import os
from flask import Flask
from flask import render_template
from flask import jsonify, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import Search
import uuid
import Graph
import time
import matplotlib.pyplot as plt
import networkx as nx

secret_key = 'SomethingSecret2'

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

# app = Flask(__name__)}
app = Flask(__name__, static_folder='uploads', static_url_path='')

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

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
    
    data_origin = request.args.get('data_origin')
    print(data_origin + '\n\n')
    num_nodes = request.args.get('num_nodes')
    random_probability = request.args.get('random_probability')
    identificador=request.args.get('identificador')
    
    algorithm['DFS'] = request.args.get('DFS')
    algorithm['BFS'] = request.args.get('BFS')
    algorithm['BDS'] = request.args.get('BDS')
    algorithm['IDS'] = request.args.get('IDS')
    algorithm['UCS'] = request.args.get('UCS')
    algorithm['GS'] = request.args.get('GS')
    algorithm['BestFS'] = request.args.get('BestFS')
    algorithm['A'] = request.args.get('A')
    
    algorithm['greedy'] = request.args.get('greedy')
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
            'A': getattr(search, 'A'),
            'greedy': getattr(search, 'Greedy')
            
        }
        # print(f"search: {name}, nodeVal: {nodeVal}")
        func = switcher.get(name, lambda: "nothing")
        return func(Inode, nodeVal)

    def get_complexity(name, b, d, m):
        d = int(d)
        b = int(b)
        b = int(m)
        switcher = {
            'DFS': (b^d, b^d),
            'BFS': (b*m, b^d),
            'BDS': (b^int(d/2), b^int(d/2)),
            'IDS': (b*d, b^d),
            'UCS': (b^d, b^d),
            'GS': (1, b*d),
            'BestFS': (b^d, b^d),
            'A': (b^d, b^d),
            'greedy': (b^d, b^d)
        }
        # print(f"search: {name}, nodeVal: {nodeVal}")
        complexi = switcher.get(name, lambda: "nothing")
        return complexi

    if data_origin == 'random':
        graph.gen_random(int(num_nodes), float(random_probability))
    elif data_origin == 'db':
        graph.load_graph()
    else:
        upload_location = os.path.join(app.root_path, 'uploads', filename)
        graph.read_file(upload_location)
        
        # for node in graph.nodes:
        #     graph.conn.insert_node(node)
        # for node in graph.nodes:
        #     for child in node.children:
        #         graph.conn.insert_edge(node, child)
                
        # graph.load_graph()
    # print(graph.nodes)
    # print(graph.edges)
    # print(f"Hijos Promedio: {graph.average_children()}")
    
    
    init_node = graph.get_node('N1')
    print('init_node')
    print(init_node)
    print(init_node.children)
    nodeVal= 'N8'

    # print(f"maxDepth: {graph.maxDepth(init_node)}")
    algorithm = {k : v for k,v in algorithm.items() if v == 'on'}

    average_children = graph.average_children()
    max_depth = init_node.maxDepth()

    for key in algorithm:
        # print(f"{key}: {algorithm[key]}")
        # print(f"key: {key}")
        if key == 'BDS':
            currNodeVal = graph.get_node(nodeVal)
            start_time = time.time()
            path, found, stack = call_search(key, init_node, currNodeVal)
            time_elapsed = (time.time() - start_time)
            algorithm_results[key] = [path, found, stack, time_elapsed, get_complexity(key, len(path), average_children, max_depth)]
        else:
            start_time = time.time()
            path, found, stack = call_search(key, init_node, [nodeVal])
            time_elapsed = (time.time() - start_time)
            algorithm_results[key] = [path, found, stack, time_elapsed, get_complexity(key, len(path), average_children, max_depth)]
    
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

    plt.savefig(resource_path + '/' + identificador+".png")

    return render_template('result.html', title="Resultado de busquedas", filename=filename, algorithm_results=algorithm_results, identificador=identificador)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part

        data_origin = request.form.get('data_origin')
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
        greedy = request.form.get('greedy')

        identificador = str(uuid.uuid4().hex)

        if 'inputFile' not in request.files:
            
            if data_origin != 'file':
                return redirect(url_for('result',
                                                filename='',
                                                DFS = DFS,
                                                BFS = BFS,
                                                BDS = BDS,
                                                IDS = IDS,
                                                UCS = UCS,
                                                GS = GS,
                                                BestFS = BestFS,
                                                A = A,
                                                greedy = greedy,
                                                data_origin = data_origin,
                                                num_nodes = num_nodes,
                                                random_probability = random_probability,
                                                identificador = identificador
                ))
            else:
                return redirect(url_for('index'))
        file = request.files['inputFile']

        # if user does not select file, browser also
        # submit an empty part without filename
        UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = identificador
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
                                    greedy = greedy,
                                    data_origin = data_origin,
                                    num_nodes = num_nodes,
                                    random_probability = random_probability,
                                    identificador= identificador
                                    ))


app.debug = True
app.run()