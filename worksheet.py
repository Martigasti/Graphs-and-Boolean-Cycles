from modules.open_digraph import *
import random
import inspect

# print("node methods:")
# print([method for method in dir(node)])
# print("")

# print("open_digraph methods:")
# print([method for method in dir(open_digraph)])
# print("")

# print("add_child_id source:")
# print(inspect.getsource(node.add_child_id))
# print("")

# print("add_child_id doc:")
# print(inspect.getdoc(node.add_child_id))
# print("")

# print("add_child_id file:")
# print(inspect.getfile(node.add_child_id))
# print("")

# n0 = node(0, 'a', {}, {1:1, 2:1})
# n1 = node(1, 'b', {0:1}, {3:1, 4:1})
# n2 = node(2, 'c', {0:1}, {4:1})
# n3 = node(3, 'd', {1:1}, {})
# n4 = node(4, 'e', {2:1}, {})
# G = open_digraph([0],[3,4],[n0,n1,n2,n3,n4])
            
# print(G)

# empty_graph = open_digraph.empty()
                
#Tests
print("l1:")
l1 = random_int_list(10, 9)

print("\n")
m1 = random_int_matrix(5, 9, null_diag = True)
print("m1:")
print(m1)
print_matrix(m1)


print("\n")
m2 = random_symmetric_int_matrix(5, 9, null_diag=False)
print("m2:")
print_matrix(m2)

print("\n")
m3 = random_int_matrix(5, 9, symmetric=True, null_diag=True)
print("m3:")
print_matrix(m3)

print("\n")
m4 = random_int_matrix(5, 2, null_diag = True, oriented = True)
print("m4:")
print_matrix(m4)

print("\n")
m5 = random_dag_int_matrix(5, 2)
print("m5:")
print_matrix(m5)


g2 = graph_from_adjacency_matrix(m5)
print(g2)