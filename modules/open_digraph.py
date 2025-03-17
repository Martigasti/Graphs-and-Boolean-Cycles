import random
import re
from urllib.parse import quote
import webbrowser

class node:

    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent nodes id to its multiplicity
        children: int->int dict; maps a child nodes id to its multiplicity
        '''

        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children 

    def __str__(self):
        return f"Node(ID: {self.id}, Label: '{self.label}', Parents: {self.parents}, Children: {self.children})"

    def __repr__(self):
        return f"node({self.id}, '{self.label}', {self.parents}, {self.children})"

    def __eq__(self, other):
        return (self.id == other.id and self.label == other.label and self.parents == other.parents and self.children == other.children)

    def copy(self):
        return node(self.id, self.label, self.parents.copy(), self.children.copy())

    #getters
    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_parents(self):
        return self.parents.copy()

    def get_children(self):
        return self.children.copy()

    #setters
    def set_id(self, identity: int):
        self.id = identity

    def set_label(self, lab: str):
        self.label = lab

    def set_children(self, child: dict):
        self.children = child

    def add_parent_id(self, parent_id: int):
        if parent_id in self.parents:
            self.parents[parent_id] += 1
        else:
            self.parents[parent_id] = 1

    def add_child_id(self, child_id: int):
        '''
        Adds a children if it's a new id, augments the counter by one if it isn't
        '''
        if child_id in self.children:
            self.children[child_id] += 1
        else:
            self.children[child_id] = 1

    def remove_parent_once(self, parent: int):
        if not (parent in self.parents.keys()):
            raise ValueError(f"{parent} not in parents")
        else:
            if self.parents[parent] > 1:
                self.parents[parent] -= 1
            else:
                del self.parents[parent]


    def remove_child_once(self, child: int):
        if not (child in self.children.keys()):
            raise ValueError(f"{child} not in children")
        else:
            if self.children[child] > 1:
                self.children[child] -= 1
            else:
                del self.children[child]

    def remove_parent_id(self, parent: int):
        if parent in self.parents.keys():
            del self.parents[parent]
        else:
            raise ValueError(f"{parent} not in parents")

    def remove_child_id(self, child: int):
        if child in self.children.keys():
            del self.children[child]
        else:
            raise ValueError(f"{parent} not in parents")


class open_digraph: # for open directed graph

    def __init__(self, inputs=[], outputs=[], nodes=[]):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict 

    def __str__(self):
        nodes_str = ', '.join(str(self.nodes[nid]) for nid in self.nodes)
        return f"Graph({self.inputs},{self.outputs}, [{nodes_str}])"

    def __repr__(self):
        nodes_repr = ', '.join(repr(self.nodes[nid]) for nid in self.nodes)
        return f"Graph({self.inputs}, {self.outputs}, [{nodes_repr}])"

    def copy(self):
        copied_nodes = [node.copy() for node in self.nodes.values()]
        return open_digraph(self.inputs, self.outputs, copied_nodes)

    @classmethod
    def empty(cls):
        return cls(inputs=[], outputs=[], nodes=[])

    #getters
    def get_input_ids(self):
        return self.inputs

    def get_output_ids(self):
        return self.outputs

    def get_id_node_map(self):
        return self.nodes.copy()

    def get_nodes(self):
        return list(self.nodes.values())

    def get_node_ids(self):
        return list(self.nodes.keys())

    def get_node_by_id(self, identity):
        return self.nodes.get(identity, None)

    def get_nodes_by_ids(self, ids):
        return [self.nodes[identity] for identity in ids if identity in self.nodes]

    #setters
    def set_inputs(self, new_inputs):
        self.inputs = new_inputs

    def set_outputs(self, new_outputs):
        self.outputs = new_outputs

    def add_input_id(self, input_id):
        if input_id not in self.inputs:
            self.inputs.append(input_id)

    def add_output_id(self, output_id):
        if output_id not in self.outputs:
            self.outputs.append(output_id)

    def new_id(self):
        existing_ids = set(self.nodes.keys())
        new_id = 0
        while new_id in existing_ids:
            new_id += 1
        return new_id

    def add_edge(self, src: int, tgt: int):
        if src in self.nodes and tgt in self.nodes:
            # .get: if key not found, then returns seconds parameter (0 in this case)
            # +1 to edge count in the children of the src node
            self.nodes[src].children[tgt] = self.nodes[src].children.get(tgt, 0) + 1
            # +1 to edge count in the parents of the tgt node
            self.nodes[tgt].parents[src] = self.nodes[tgt].parents.get(src, 0) + 1

    def add_edges(self, edges: list):
        for src, tgt in edges:
            self.add_edge(src, tgt)

    def add_node(self, label='', parents=None, children=None):
        if parents is None:
            parents = {}
        if children is None:
            children = {}
        # New id generated
        newid = self.new_id()

        # Create a new node that will later be added to the graph
        new_node = node(newid, label, parents.copy(), children.copy())
        self.nodes[newid] = new_node

        # Link the new node with its parents
        for parent_id, multiplicity in parents.items():
            if parent_id in self.nodes:
                self.nodes[parent_id].children[newid] = multiplicity

        # Link the new node with its children
        for child_id, multiplicity in children.items():
            if child_id in self.nodes:
                self.nodes[child_id].parents[newid] = multiplicity
        # Return the id of the new node
        return newid

    def remove_edge(self, src: int, tgt: int):
        if src in self.nodes and tgt in self.nodes: 
            self.nodes[src].remove_child_once(tgt)
            self.nodes[tgt].remove_parent_once(src)
        else:
            raise ValueError(f"{src} or {tgt} not in the graph")

    def remove_parallel_edges(self, src: int, tgt: int):
        if src in self.nodes and tgt in self.nodes: 
            self.nodes[src].remove_child_id(tgt)
            self.nodes[tgt].remove_parent_id(src)
        else:
            raise ValueError(f"{src} or {tgt} not in the graph")

    def remove_node_by_id(self, node_id: int):
        # List of node parents
        pn = list(self.nodes[node_id].parents.keys())
        # List of node children
        cn = list(self.nodes[node_id].children.keys())

        # Eliminate all the parents of node from both sides
        for parent_id in pn:
            self.remove_parallel_edges(parent_id, node_id)

        # Elimate all the children of node from both sides
        for child_id in cn:
            self.remove_parallel_edges(node_id, child_id)
        # Eliminate the node from the list
        del self.nodes[node_id]

    def remove_edges(self, *edges: tuple):
        for src, tgt in edges:
            self.remove_edge(src, tgt)

    def remove_several_parallel_edges(self, *edges):
        for src, tgt in edges:
            self.remove_parallel_edges(src, tgt)

    def remove_nodes_by_id(self, *node_ids: tuple):
        for node_id in node_ids:
            self.remove_node_by_id(node_id)

    def is_well_formed(self):

        for output_id in self.outputs:
            # Check if outputs are in the graph
            if not output_id in self.nodes:
                return False
            # Check if outputs have a single parent 
            if len(self.nodes[output_id].parents) != 1:  
                    return False
            # Check if its multiplicity is 1
            parent_list = list(self.nodes[output_id].parents.values())
            if parent_list[0] != 1:
                return False
            # Check if outputs have no children
            if self.nodes[output_id].children != {}:
                return False

        for input_id in self.inputs:
            # Check if inputs are in the graph
            if not input_id in self.nodes:
                return False
            # Check if inputs have a single child
            if len(self.nodes[input_id].children) != 1:  
                    return False
            # Check if its multiplicity is 1
            child_list = list(self.nodes[input_id].children.values())
            if child_list[0] != 1:
                return False

            # Check if inputs has no parents
            if self.nodes[input_id].parents != {}:
                return False

        for node_id, node in self.nodes.items():
            # Check if each key in nodes corresponds to a node with the same id
            node_id2 = self.nodes[node_id].get_id()
            if node_id != node_id2:
                return False

            # Check condition 5
            for child_id, child_multiplicity in node.children.items():

                child_node = self.nodes[child_id]
                if node_id not in child_node.parents or child_node.parents[node_id] != child_multiplicity:
                    return False  
        return True

    def assert_is_well_formed(self):
        """
        Asserts if the graph is well formed, if not sends a ValueError
        """
        if not self.is_well_formed():
            raise ValueError("The graph is not well_formed")


    def add_input_node(self, child_id):
        """
        Creates a new node, defines it as an input, points it to the node with the given child_id and returns its id
        """
        # Check if child_id is not in graph
        if not child_id in self.nodes:
            raise ValueError(f"{child_id} doesn't exist in graph")
        new_id = self.add_node(children = {child_id : 1})
        self.inputs.append(new_id)
        return new_id


    def add_output_node(self, parent_id):
        """
        Creates a new node, defines it as an output, points it to the node with the given parent_id and returns its id
        If the source node already has children, raises an error.
        """
        # Check if the child_id node exists and does not have other children
        if parent_id not in self.nodes:
            raise ValueError(f"{parent_id} doesn't exist in graph")
        new_id = self.add_node(parents={parent_id: 1}) 
        self.outputs.append(new_id)
        return new_id

    @classmethod
    def random(cls, n, bound, inputs=0, outputs=0, form="free"):
        # Generate a matrix based on the form argument
        if form == "free":
            m = random_int_matrix(n, bound)
        elif form == "DAG":
            m = random_int_matrix(n, bound, dag=True)
        elif form == "oriented":
            m = random_int_matrix(n, bound)
        elif form == "loop-free":
            m = random_int_matrix(n, bound)
            m = non_cyclic_int_matrix(n, m)
        elif form == "undirected":
            m = random_int_matrix(n, bound, symmetric=True)
        elif form == "loop-free undirected":
            m = random_int_matrix(n, bound, symmetric=True, null_diag=True)
        else:
            raise ValueError("Unknown form")

        # Transform the matrix into a graph
        graph = graph_from_adjacency_matrix(m)

        # Add inputs and outputs
        for i in range(inputs):
            n_id = graph.new_id()
            graph.add_input_id(n_id)
        for i in range(outputs):
            n_id = graph.new_id()
            graph.add_output(n_id)
        return graph

    def dic_nodes(self):
        """
        Method to assign a unique integer (0 to n-1) to each node ID in the graph.
        Returns:
            dict: A dictionary mapping each node ID to a unique integer.
        """
        return {node_id: i for i, node_id in enumerate(self.nodes)}


    def adjacency_matrix(self):
        """
        Generates the adjacency matrix of a graph
        """
        id_dic = self.dic_nodes()

        size = len(self.nodes)
        m = [[0 for _ in range(size)] for _ in range(size)] # Matrix filled with 0s

        # Fill the matrix based on the graph
        for node_id, node in self.nodes.items():
            for child_id, multiplicity in node.children.items():
                if child_id in self.nodes:
                    m[id_dic[node_id]][id_dic[child_id]] = multiplicity
        return m
    
    #CAMBIAR 
    def save_as_dot_file(self, path: str, verbose=False):
        """
        Creates a file .dot, which has the graph
        """
        with open(path, 'w') as f: 
            f.write('digraph G {\n')
            # Write nodes with labels. If verbose is True, include the ID in the label.
            for node_id, node in self.nodes.items():
                if verbose:
                    f.write(f'{node_id} [label="{node_id}: {node.label}"];\n')
                else:
                    f.write(f'{node_id} [label="{node.id}"];\n')

            # Write edges
            for node_id, node in self.nodes.items():
                for child_id, multiplicity in node.children.items():
                    for _ in range(multiplicity):
                        f.write(f'    {node_id} -> {child_id};\n')
            f.write('}\n')
    
    @classmethod
    def from_dot_file(cls, path):
        # Create an empty graph instance
        graph = cls.empty()

        # Regular expressions to match nodes and edges
        node_pattern = re.compile(r'\s*(\S+)\s*\[label="([^"]+)"\];')
        edge_pattern = re.compile(r'\s*(\S+)\s*->\s*(\S+);')

        with open(path, 'r') as f:
            for line in f:
                # Check for a node definition
                node_match = node_pattern.match(line)
                if node_match:
                    node_id, label = node_match.groups()
                    # Convert node_id to int if possible
                    try:
                        node_id = int(node_id)
                    except ValueError:
                        pass  # Keep node_id as string if it cannot be converted
                    graph.add_node(label=label)
                    continue
                
                # Check for an edge definition
                edge_match = edge_pattern.match(line)
                if edge_match:
                    src, tgt = edge_match.groups()
                    # Convert src and tgt to int if possible
                    try:
                        src = int(src)
                        tgt = int(tgt)
                    except ValueError:
                        pass  # Keep src and tgt as string if they cannot be converted
                    graph.add_edge(src, tgt)

        return graph
    
    def display(self, verbose=False):
        # Generate the .dot representation as a string
        dot_str = 'digraph G {\n'
        for node_id, node in self.nodes.items():
            if verbose:
                dot_str += f'    {node_id} [label="{node_id}: {node.label}"];\n'
            else:
                dot_str += f'    {node_id} [label="{node.label}"];\n'
        for node_id, node in self.nodes.items():
            for child_id, multiplicity in node.children.items():
                for _ in range(multiplicity):
                    dot_str += f'    {node_id} -> {child_id};\n'
        dot_str += '}'

        # Encode the .dot string for URL use
        encoded_dot = quote(dot_str)  # Use the imported quote function

        # Construct the URL for the online Graphviz viewer
        url = f'https://dreampuf.github.io/GraphvizOnline/#{encoded_dot}'

        # Open the URL in the default web browser
        webbrowser.open(url)
        #print(url)
            

################# END CLASS ##########################

def random_int_list(n, bound):
    return [random.randint(0, bound) for _ in range(n)]


def random_null_diag_int_matrix(n : int, l: list):
    """
    Modifie la matrice en parametre, rendant sa diagonalle nulle
    """
    for i in range(n):
        l[i][i] = 0
    return l


def random_symmetric_int_matrix(n, bound, null_diag=True):
    """
    Renvoie une matrice symetrique avec option de diagonale nulle
    """
    m = random_int_matrix(n, bound)
    for i in range(n):
        for j in range(n):
            if i > j:
                m[i][j] = m[j][i]
    if null_diag:
        return random_null_diag_int_matrix(n, m)
    return m

def non_cyclic_int_matrix(n: int, null_diag=True):
    for i in range(n):
        for j in range(n):
            if j > i and m[i][j] != 0:
                m[j][i] = 0
    return m

def random_oriented_int_matrix(n: int, bound: int, null_diag=True):
    m = random_int_matrix(n, bound, null_diag)
    for i in range(n):
        for j in range(n):
            if j > i and m[i][j] != 0:
                m[j][i] = 0
    return m

def random_dag_int_matrix(n, bound, null_diag=True):
    m = []
    for i in range(n):
        l = []
        for j in range(n):
            if j >= i: # Up right (diagonal included) 
                l.append(random.randint(0, bound))
            else:
                l.append(0)
        m.append(l)
    if null_diag:
        return random_null_diag_int_matrix(n, m)
    return m

def random_int_matrix(n, bound, null_diag=False, symmetric=False, oriented=False, dag=False):
    m = []
    if symmetric:
        return random_symmetric_int_matrix(n, null_diag)
    elif oriented:
        return random_oriented_int_matrix(n, bound, null_diag)
    elif dag:
        return random_dag_int_matrix(n, bound, null_diag)
    else:
        for i in range(n):
            m.append(random_int_list(n, bound))
        if null_diag:
            return random_null_diag_int_matrix(n, m)
        return m

def graph_from_adjacency_matrix(m: list[list[int]]):
    graph = open_digraph() # Initialise an empty graph graph

    nodes_list = [] # List with all nodes ids
    for i in range(len(m)): 
        node_id = graph.add_node() # Add each node to the graph
        nodes_list.append(node_id)

    for i in range(len(m)):
        for j in range(len(m)):
            edges = m[i][j]
            for _ in range(edges):
                graph.add_edge(nodes_list[i], nodes_list[j])

    return graph

def print_matrix(m: list):
    for i in range (len(m)):
        if i == 0:
            print("[" + str(m[i]) + ",")
        elif i == len(m)-1:
            print(" " + str(m[i]) + "]")
        else: print(" " + str(m[i]) + ",")


