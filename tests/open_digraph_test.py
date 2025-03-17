import sys
import os
root = os.path.expanduser('~/L2/ProjetInfo/Project-LDD2-S4')
sys.path.append(root) # allows us to fetch files from the project root
import unittest
from modules.open_digraph import * 


class InitTest(unittest.TestCase):

    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)
        self.assertIsNot(n0.copy(),n0)


    def test_open_digraph(self):
        n0 = node(0, 'i1', {}, {1:1})
        n1 = node(1, 'i2', {0:1}, {})
        G = open_digraph([0], [1], [n0, n1])

        # Input and outputs tests
        self.assertEqual(G.inputs, [0])
        self.assertEqual(G.outputs, [1])

        # Instances tests
        self.assertIsInstance(G.nodes, dict)
        self.assertIsInstance(G.nodes[0], node)
        self.assertIsInstance(G.nodes[1], node)

        # Nodes tests
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i1')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})

        self.assertEqual(n1.id, 1)
        self.assertEqual(n1.label, 'i2')
        self.assertEqual(n1.parents, {0:1})
        self.assertEqual(n1.children, {})

        self.assertIsNot(G.copy(),G)

    def test_node_setters(self):
        n = node(1, 'test', {}, {})
        n.set_id(2)
        n.set_label('new label')
        n.set_children({3: 1})
        n.add_parent_id(4)
        n.add_child_id(5)

        self.assertEqual(n.id, 2)
        self.assertEqual(n.label, 'new label')
        self.assertEqual(n.children, {3: 1, 5: 1})
        self.assertEqual(n.parents, {4: 1})
        self.assertEqual(n.children[5], 1)

    def test_open_digraph_setters(self):
        graph = open_digraph([], [], [])
        graph.set_inputs([1, 2])
        graph.set_outputs([3, 4])
        graph.add_input_id(5)
        graph.add_output_id(6)
        graph.add_output_id(6)

        self.assertEqual(graph.inputs, [1, 2, 5])
        self.assertEqual(graph.outputs, [3, 4, 6])

    def test_add_edge(self):
        graph = open_digraph([], [], [node(0, '', {}, {}), node(1, '', {}, {})])
        graph.add_edge(0, 1)
        graph.assert_is_well_formed()

        self.assertEqual(graph.nodes[0].children, {1: 1})
        self.assertEqual(graph.nodes[1].parents, {0: 1})

    def test_add_edges(self):
        graph = open_digraph([], [], [node(0, '', {}, {}), node(1, '', {}, {}), node(2, '', {}, {})])
        graph.add_edges([(0, 1), (0, 2)])

        self.assertEqual(graph.nodes[0].children, {1: 1, 2: 1})
        self.assertEqual(graph.nodes[1].parents, {0: 1})
        self.assertEqual(graph.nodes[2].parents, {0: 1})
        graph.assert_is_well_formed()


    def test_add_node_no_parents_children(self):
        graph = open_digraph([], [], [])
        # Test adding a node without parents and children
        node_id = graph.add_node(label='Test Node')
        self.assertEqual(len(graph.nodes), 1)
        self.assertIn(node_id, graph.nodes)
        self.assertEqual(graph.nodes[node_id].label, 'Test Node')
        self.assertEqual(graph.nodes[node_id].parents, {})
        self.assertEqual(graph.nodes[node_id].children, {})
        graph.assert_is_well_formed()

    def test_add_node_with_parents_children(self):
        graph = open_digraph([], [], [])
        # Adding initial nodes
        parent_id = graph.add_node(label='Parent')
        child_id = graph.add_node(label='Child')

        # Test adding a node with parents and children
        new_node_id = graph.add_node(label='New Node', parents={parent_id: 1}, children={child_id: 2})
        self.assertIn(new_node_id, graph.nodes)
        self.assertEqual(graph.nodes[new_node_id].parents, {parent_id: 1})
        self.assertEqual(graph.nodes[new_node_id].children, {child_id: 2})

        # Check if parent and child nodes were updated
        self.assertEqual(graph.nodes[parent_id].children, {new_node_id: 1})
        self.assertEqual(graph.nodes[child_id].parents, {new_node_id: 2})
        graph.assert_is_well_formed()

    def test_remove_nodes(self):
        n0 = node(0, 'i1', {}, {1:3})
        n1 = node(1, 'i2', {0:4}, {})
        n2 = node(2, 'i1', {}, {3:1})
        n3 = node(3, 'i2', {2:1}, {})
        graph = open_digraph([], [], [n0, n1])
        n0.remove_child_once(1)
        n1.remove_parent_once(0)
        n2.remove_child_once(3)
        n3.remove_parent_once(2)

        #Remove_once fonctions tests
        self.assertEqual(n0.children[1], 2)
        self.assertEqual(n1.parents[0], 3)
        self.assertEqual(n2.children, {})
        self.assertEqual(n3.parents, {})

        n0.remove_child_id(1)
        n1.remove_parent_id(0)

        #remove_all fonctions tests
        self.assertEqual(n0.children, {})
        self.assertEqual(n1.parents, {})


    def test_remove_edge(self):
        graph = open_digraph([], [], [node(0, '', {1:3, 2:2}, {}), node(1, '', {}, {0:3, 2:4}), node(2, '', {1:4}, {0:2})])
        graph.remove_edge(1,0)

        self.assertEqual(graph.nodes[0].parents[1], 2)
        self.assertEqual(graph.nodes[1].children[0], 2)

        graph.remove_parallel_edges(1,0)
        self.assertEqual(graph.nodes[0].parents, {2:2})
        self.assertEqual(graph.nodes[1].children, {2:4})

        graph.remove_node_by_id(2)

        self.assertEqual(graph.nodes, {0: node(0, '', {}, {}), 1: node(1, '', {}, {})})
        graph.assert_is_well_formed()

    def test_is_well_formed(self):
        well_formed_graph = open_digraph(
            inputs=[0], outputs=[2],
            nodes=[
                node(0, 'Input', {}, {1: 1}), 
                node(1, 'Middle', {0: 1}, {2: 1}),
                node(2, 'Output', {1: 1}, {})
            ]
        )
        #Graph with an output node having more than one parent
        malformed_graph_1 = open_digraph(
            inputs=[0], outputs=[2],
            nodes=[
                node(0, 'Input', {}, {2: 1}),
                node(2, 'Output', {0: 1, 1: 1}, {})
            ]
        )


        # Graph with mismatched parent-child multiplicity
        malformed_graph_2 = open_digraph(
            inputs=[0], outputs=[2],
            nodes=[
                node(0, 'Input', {}, {1: 1}),
                node(1, 'Middle', {0: 2}, {2: 1}),  # Mismatch here
                node(2, 'Output', {1: 1}, {})
            ]
        )
        # Graph with an input node having more than one child
        malformed_graph_3 = open_digraph(
            inputs=[0], outputs=[2],
            nodes=[
                node(0, 'Input', {}, {1: 1, 0:1}), 
                node(1, 'Middle1', {0: 1}, {2: 1}),
                node(3, 'Middle2', {0: 1}, {}),
                node(2, 'Output', {1: 1}, {})
            ]
        )
        self.assertTrue(well_formed_graph.is_well_formed())
        self.assertFalse(malformed_graph_1.is_well_formed())
        self.assertFalse(malformed_graph_2.is_well_formed())
        self.assertFalse(malformed_graph_3.is_well_formed())

    def test_add_input_node(self):
        graph = open_digraph([], [], [node(0, 'Existing', {}, {})])
        graph.add_input_node(0)
        self.assertEqual(len(graph.inputs), 1)  # Corrected this line
        self.assertIn(0, graph.nodes[graph.inputs[0]].children)
        self.assertIn(graph.inputs[0], graph.nodes[0].parents)

        graph2 = open_digraph([], [], [node(0, 'Existing', {}, {})])
        with self.assertRaises(ValueError):
            graph2.add_input_node(1)  # Node with id 1 does not exist

        graph.assert_is_well_formed()

    def test_add_output_node(self):
        # Create a graph with one existing node
        graph = open_digraph([], [], [node(0, 'Existing', {}, {})])
        # Add an output node pointed to by the existing node
        output_node_id = graph.add_output_node(0)

        # Check if the output node is added correctly
        self.assertIn(output_node_id, graph.outputs)
        self.assertIn(output_node_id, graph.nodes)
        self.assertIn(0, graph.nodes[output_node_id].parents)
        self.assertEqual(graph.nodes[output_node_id].parents[0], 1)
        # Check if the existing node now has the new node as a child
        self.assertIn(output_node_id, graph.nodes[0].children)
        self.assertEqual(graph.nodes[0].children[output_node_id], 1)
        graph.assert_is_well_formed()

    def test_create_graph(self): 
        # Faire ces tests
        free_graph = open_digraph.random(n=4, bound=3, form="free")
        ...

    def test_adjacency_matrix(self):
        # Faire ces tests
        graph1 = open_digraph([], [], [node(0, '', {1:3, 2:2}, {}), node(1, '', {}, {0:3, 2:4}), node(2, '', {1:4}, {0:2})])
        m = graph1.adjacency_matrix()
        ...

    def test_to_dot_file(self):
        # Create an instance of the open_digraph class
        graph = open_digraph.random(n=5, bound=3, form="DAG")
        
        graph2 = open_digraph(
            inputs=[0], outputs=[2],
            nodes=[
                node(0, 'Input', {}, {1: 1}), 
                node(1, 'Middle', {0: 1}, {2: 1}),
                node(2, 'Output', {1: 1}, {})
            ])

        path1 = os.path.expanduser('~/L2/ProjetInfo/Project-LDD2-S4/tests/test1.dot')
        path2 = os.path.expanduser('~/L2/ProjetInfo/Project-LDD2-S4/tests/test2.dot')

        graph.save_as_dot_file(path1, verbose=False)
        graph2.save_as_dot_file(path2, verbose=True)
        
    def test_from_dot_file(self):
        # Assume os module is imported for path handling
        path1 = os.path.expanduser('~/L2/ProjetInfo/Project-LDD2-S4/tests/test1.dot')
        path2 = os.path.expanduser('~/L2/ProjetInfo/Project-LDD2-S4/tests/test2.dot')
        
        path3 = os.path.expanduser('~/L2/ProjetInfo/Project-LDD2-S4/tests/test3.dot')

        # Load graphs from .dot files
        graph1 = open_digraph.from_dot_file(path1)
        graph2 = open_digraph.from_dot_file(path2)
        graph2.save_as_dot_file(path3, verbose=False)

        print(graph1)
        print("\n\n")
        print(graph2)
        
    def test_display_graph(self):
        # Create an instance of the open_digraph class
        graph = open_digraph.random(n=10, bound=3, form="DAG")

        # Display the graph, adjust verbose as needed
        graph.display()


if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run