# standard python library for creating, analyzing, and visualzing graph / networks
# It is used everywhere:
#   - social network analysis
#   - recommendation systems
#   - biology networks
#   - transportation networks
#   - research & education

# to make a network / graph
import networkx as nx
# to get the working directory, aboslute path, and relative path
import os
# visualization of graph
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# random usage
import random
# community detection
import community as community_louvain
# default dict generation
from collections import defaultdict
# generating 2D matrix
import numpy as np

# 1. load edges
def load_edges(path):
    '''
    loads the edge list from the .edges file
    each row looks like:
    236 186
    122 285
    meaning user 236 is friend with user 186

    create an undirected graph becuz friendships have no direction
    '''
    G = nx.Graph()

    with open(path, 'r') as f:

        for line in f:
            u, v = line.strip().split()

            # convert string -> integer
            u = int(u)
            v = int(v)

            # add an undirected edge to the graph
            G.add_edge(u, v)
    
    # ego node is not connected to any other node
    # manually add edges to ego node
    ego_node_id = "ego_0"
    for node in list(G.nodes):
        if node != ego_node_id:
            G.add_edge(ego_node_id, node)
    
    return G

# 2. load feature names
def load_featnames(path):
    '''
    loads the feature names from the .featname file
    each row looks like:
    0 Birthday: Born in January
    1 Birthday: Born in February
    followed by a column index

    return a dictionary mapping:
    index -> feature_name
    '''
    featnames = {}
    feature_order = []

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # split on first whitespace ONLY
            parts = line.split(None, 1)

            # must have: [index, feature name]
            if len(parts) != 2:
                print("Skipping malformed line:", line)
                continue

            idx_str, name_str = parts

            try:
                idx = int(idx_str)
            except ValueError:
                print("Skipping line with non-integer index:", line)
                continue

            featnames[idx] = name_str.strip()
            feature_order.append(idx)

    return featnames, feature_order

# 3. load features for each node
def load_features(path):
    '''
    loads the node features from the .feat file
    each row looks like:
    1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    while the first integer is the user ID and the other integers 
    are feature vector

    return a dictionary: node_id -> feature_vector(list of integers)
    '''
    feature = {}

    with open(path, 'r') as f:
        for line in f:
            # split only one time and leave the rest to the list
            temp = line.strip().split()
            idx = int(temp[0])
            vectors = list(map(int, temp[1:]))
            feature[int(idx)] = vectors
    
    return feature

# 4. load the ego's own features
def load_egofeat(path):
    '''
    loads the ego user's feature vector
    ego is the central person of this ego-network
    text file looks like this: (like feat file)
    (no user ID included)
    0 0 0 0 0 0 0 0 0 1 0 0 0 0

    returns a list containing only vectors
    '''
    with open(path, 'r') as f:
        temp = f.readline().strip().split()
        vector = list(map(int, temp))
    
    return vector

# 5. load social circles
def load_circles(path):
    '''
    loads circle (community) friendship from .circles file
    the text file looks like:
    circle0	71	215
    circle1	173

    returns a dictionary with key
    dict: "circle0" -> [71, 215]
    '''
    circle = {}

    with open(path, 'r') as f:
        for line in f:
            temp = line.strip().split()
            key = temp[0]
            value = list(map(int, temp[1:]))
            
            circle[key] = value
    
    return circle

# 6. build the full graph object
def build_graph(ego_id):
    '''
    this function loads all 5 files for a given ego
    then constructs a fully annotated networkx graph
    '''
    # define file paths by changing the ego_id
    edges_fileName = f"{ego_id}.edges"
    featname_fileName = f"{ego_id}.featnames"
    feat_fileName = f"{ego_id}.feat"
    egofeat_fileName = f"{ego_id}.egofeat"
    circle_fileName = f"{ego_id}.circles"

    # get the current working directory
    script_file = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_file)

    # get the files path
    edges_path = os.path.join(script_dir, "data", edges_fileName)
    featname_path = os.path.join(script_dir, "data", featname_fileName)
    feat_path = os.path.join(script_dir, "data", feat_fileName)
    egofeat_path = os.path.join(script_dir, "data", egofeat_fileName)
    circle_path = os.path.join(script_dir, "data", circle_fileName) 

    # load data
    print("Loading edges...")
    G = load_edges(edges_path)

    print("Loading feature names...")
    featnames, feature_order = load_featnames(featname_path)

    print("Loading node features...")
    features = load_features(feat_path)

    print("Loading ego features...")
    ego_features = load_egofeat(egofeat_path)

    print("Loading circles...")
    circles = load_circles(circle_path)

    print("Attaching features to nodes")
    for node, feat_vector in features.items():
        if node not in G:
            G.add_node(node)
        G.nodes[node]["feature"] = feat_vector

    print("Attaching circle labels")
    for circle_name, members in circles.items():
        for node in members:
            # if member node in circle in current graph
            if node in G.nodes:
                # the node in the graph would get a circles key and its value would
                # be a list that get the circle name
                G.nodes[node].setdefault("circles", []).append(circle_name)
    
    # create an explicit ego node
    ego_node_id = f"ego_{ego_id}"
    G.add_node(ego_node_id)
    G.nodes[ego_node_id]["feature"] = ego_features
    G.nodes[ego_node_id]["is_ego"] = True

    print("Graph loaded completely")
    return G, featnames, feature_order, features, ego_features, circles, ego_node_id

def visualization(G, circles, ego_node_id):
    '''
    visualization using networkx plotting and matplotlib
    with true circles
    '''
    # delete nodes with no edges (isolated nodes) for better visualization
    # networkx built-in function isolates can identify the isolated nodes
    isolated_nodes = list(nx.isolates(G))
    G.remove_nodes_from(isolated_nodes)

    # assign a color to each circle in the graph
    number_circle = len(circles)
    color_map = cm.get_cmap("tab20", number_circle)
    
    circle_name = list(circles.keys())
    circle_color = {}
    for i in range(number_circle):
        circle_color[circle_name[i]] = color_map(i)
    
    # assign color to each node
    def get_node_color(node):
        node_circles = G.nodes[node].get("circles", [])
        if not node_circles:
            # node not in any circle
            return "yellow"
        # get the first circle in in multiple circles
        return circle_color[node_circles[0]]

    # spring layout is best for social graphs
    plt.figure(figsize = (12, 10))

    pos = nx.spring_layout(G, seed = 42)

    node_colors = [get_node_color(n) for n in G.nodes()]

    # draw edges
    nx.draw_networkx_edges(G, pos, alpha = 0.3)

    # draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_color = node_colors,
        node_size = [250 if n == ego_node_id else 80 for n in G.nodes()],
        edgecolors = "black"
    )

    # draw labels
    nx.draw_networkx_labels(G, pos, font_size = 6)

    plt.title("Visualization of Ego Network 0")
    plt.axis("off")
    plt.show()

def visualization_louvain(G, ego_node_id):
    '''
    visualization using networkx plotting and matplotlib
    with louvain community
    '''
    plt.figure(figsize = (12, 10))

    pos = nx.spring_layout(G, seed = 42)

    comm_colors = []

    partition = circle_detection(G)

    for n in G.nodes():
        comm_colors.append(partition[n])

    # draw edges
    nx.draw_networkx_edges(G, pos, alpha = 0.3)

    # draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_color = comm_colors,
        node_size = [250 if n == ego_node_id else 80 for n in G.nodes()],
        edgecolors = "black"
    )

    # draw labels
    nx.draw_networkx_labels(G, pos, font_size = 6)

    plt.title("Visualization of Ego Network 0 with Louvain Community")
    plt.axis("off")
    plt.show()

# relationship analysis
def summarize_community_features(
    G, 
    community_id, 
    method="louvain", 
    partition=None,
    circles=None,
    features=None,
    featnames=None,
    feature_order=None,
    top_k=10
):
    '''
    get the feature name and percentage of each community
    '''
    if feature_order is None:
        raise ValueError("feature_order must be provided")

    # Get members
    if method == "louvain":
        members = [n for n in G.nodes() if partition[n] == community_id]
    else:
        circle_names = sorted(circles.keys())
        cname = circle_names[community_id]
        members = circles[cname]

    valid_members = [n for n in members if n in features]
    if not valid_members:
        return []

    # Feature matrix
    feat_matrix = np.array([features[n] for n in valid_members])
    feature_percent = feat_matrix.mean(axis=0) * 100

    # Build correct feature ID list
    num_cols = feat_matrix.shape[1]
    feature_id_order = []

    for j in range(num_cols):
        if j < len(feature_order):
            fid = feature_order[j]
        else:
            fid = j   # fallback: unknown feature → use index
        feature_id_order.append(fid)

    # Sort features
    idx_sorted = np.argsort(feature_percent)[::-1]

    # Build results
    results = []
    for idx in idx_sorted[:top_k]:
        fid = feature_id_order[idx]
        name = featnames.get(fid, f"Unknown feature {fid}")
        pct = feature_percent[idx]
        results.append((name, f"{pct:.1f}%"))

    return results

# relation analysis (using louvain community detection)
def circle_detection(G):

    # run louvain
    partition = community_louvain.best_partition(G)

    return partition

# node information
def show_node(G, number_node):

    return list(G.nodes())[:number_node]

def node_information(G, node, featnames = None, feature_order = None):

    print("Node: ", node)
    print("Degree: ", G.degree(node))
    print("True Community: ", G.nodes[node].get("circles", []))
    partition = circle_detection(G)
    print("Louvain Community: ", partition[node])
    
    if featnames is not None and feature_order is not None:
        vector = G.nodes[node].get("feature", None)

        if vector is None:
            print("Feature: None")
        else:
            active_features = []
            for col_index, value in enumerate(vector):
                if value == 1:
                    fid = feature_order[col_index]
                    name = featnames.get(fid, f"Unknown feature {fid}")
                    active_features.append(name)
            print("\nActive Features: ")
            for f in active_features:
                print(" -", f)
    else:
        print("Attributes: ", G.nodes[node])

# search if such node is in the graph
def search_node(G, node):

    if node in G.nodes():
        print("Node is in the Graph")
    else:
        print("No such node in the Graph")

if __name__ == "__main__": 

    # load ego-network 0
    G, featnames, feature_order, features, ego_features, circles, ego_node_id = build_graph(0)

    # visualize the graph (social network)
    visualization(G, circles, ego_node_id)

    # louvain community
    partition = circle_detection(G)

    # get the node of the Graph
    print(show_node(G, 5))

    # get the node information
    node_information(G, 171)

    # get the feature name of certain community id
    top_feats = summarize_community_features(G, 
        community_id = 0, 
        method = "true", 
        partition = partition, 
        circles = circles,
        features = features,
        featnames = featnames,
        feature_order = feature_order,
        top_k = 10)
    
    print(top_feats)

    node_information(G, 236)