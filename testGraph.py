import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_node("lol")
G.add_node("lel")
#G.remove_node("lol")



nx.draw(G, with_labels=True)

plt.draw()
plt.show()

