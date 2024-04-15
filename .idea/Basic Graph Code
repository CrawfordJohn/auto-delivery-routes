import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_node(1)
G.add_node(2)
G.add_edge(1, 2, weight=5)
nx.draw(G, with_labels=True, node_size=1000, font_size=12, node_color='skyblue', font_color='black')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G), edge_labels=labels)
plt.show()
