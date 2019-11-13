"""Created on Thu Oct  2 16:49:12 2014.

Author: Joseph Salmon <joseph.salmon@umontpellier.fr>
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
from os import mkdir, path
import igraph
import matplotlib.image as img


# Uncomment the following 2 lines for Mac OS X / Spyder for using Tex display
# import os as macosx
# macosx.environ['PATH'] = macosx.environ['PATH'] + ':/usr/texbin'

###############################################################################
# Plot initialization

imageformat = '.pdf'
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Computer Modern Roman']})
params = {'axes.labelsize': 16,
          'font.size': 23,
          'legend.fontsize': 12,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'text.usetex': True
          }
plt.rcParams.update(params)


###############################################################################
# display function:

saving = True


print(igraph.__version__)
color_blind_list = sns.color_palette("colorblind", 8)


# adj_matrix = np.array([[0.448, 0.054, 0.011],
#                        [0.484, 0.699, 0.503],
#                        [0.068, 0.247, 0.486]])

eAB = 0.8
eAC = 0.01

eBA = 0.8
eBC = 0.05

eCA = 0.1
eCB = 0.01

adj_matrix = np.array([[1 - eAB - eAC, eBA          , eCA],
                       [eAB          , 1 - eBA - eBC, eCB],
                       [eAC          , eBC          , 1 - eCA - eCB]])
nodes_values = np.array([10, 20, 70])


# n_vertices = 8
# threshold = 0.5
# adj_matrix = np.random.rand(n_vertices, n_vertices)
# adj_matrix[adj_matrix < threshold] = 0
# adj_matrix = adj_matrix / np.sum(adj_matrix, axis=0)
# nodes_values = np.random.rand(n_vertices)
# nodes_values = nodes_values / np.sum(nodes_values) * 100

n_vertices = adj_matrix.shape[0]
n_images = 48
print("Spectrum:", (np.linalg.eig(adj_matrix)[0]))
print("Eigen vectors:")
print(np.linalg.eig(adj_matrix)[1])
print(adj_matrix)

adj_matrix_to_display = adj_matrix.copy()
np.fill_diagonal(adj_matrix_to_display, 0)


pop_cum_time = np.zeros((n_images + 3, n_vertices + 1))
pop_cum_time[0, 1:] = nodes_values.cumsum()
# pop_cum_time[1, 1:] = nodes_values.cumsum()

files = ''
# Main loop to create png images
for i in range(0, n_images + 1):
    print(i)
    # print(np.linalg.matrix_power(adj_matrix, i))
    # print(np.linalg.matrix_power(adj_matrix, i) @ nodes_values)

    # get the row, col indices of the non-zero elements in your adjacency matrix
    conn_indices = np.where(adj_matrix_to_display)
    # get the weights corresponding to these indices
    weights = adj_matrix_to_display.T[conn_indices]

    # a sequence of (i, j) tuples, each corresponding to an edge from i -> j
    edges = list(zip(*conn_indices))

    G = igraph.Graph(edges=edges, directed=True)
    G.es['width'] = 26 * weights / np.sum(weights)
    G.es['arrow_size'] = 2.3
    G.vs['size'] = 3 * np.linalg.matrix_power(adj_matrix, i) @ nodes_values
    G.vs['color'] = color_blind_list[:(n_vertices)]
    # plot the graph, just for fun
    # G.es['layout'] = "rt"
    # G.es['labels'] = "True"
    G.es['margin'] = 150

#     G=G.simplify(loops=True)
#     G.es['label'] = weights
#     G.vs['name'] = ["A", "B", "C"]
#     G.vs['label'] = ["A", "B", "C"]

    graph_name_png = "pngs/test_" + str(i) + ".png"
    out = igraph.plot(G, layout="rt", labels=True, margin=150, edge_curved=0.3)
    out.save(graph_name_png)

    fig = plt.figure(figsize=(16, 8))

    ax1 = fig.add_subplot(1, 2, 1, xticklabels=[], yticklabels=[],
                          xticks=[], yticks=[])
    # reading png image file
    plt.imshow(img.imread(graph_name_png))
    ax1.axis('off')
    ax2 = fig.add_subplot(1, 2, 2, xticklabels=[], yticklabels=[],
                          xticks=[], yticks=[])
    # cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    plt.ylim(0, 100)     # set the xlim to left, right
    plt.xlim(0, n_images - 1)     # set the xlim to left, right

    plt.ylabel('Population')
    plt.xlabel('Time')
    ax2.set_xticks([])
    ax2.set_yticks([])
    popu = np.zeros(n_vertices + 1)
    popu[1:] = np.linalg.matrix_power(adj_matrix, i) @ nodes_values
    pop_cum_time[i + 1, :] = np.cumsum(popu)
    for vertex in range(n_vertices):
        ax2.fill_between(np.arange(i + 2), pop_cum_time[:i + 2, vertex],
                         pop_cum_time[:i + 2, vertex + 1],
                         color=color_blind_list[vertex])
    fig_name_png = "gifs/test_cum{}.png".format(str(i).zfill(3))
    fig.savefig(fig_name_png, dpi=150)
    files = files + ' ' + fig_name_png

    print(files)

job = 'convert -layers optimize -resize 1000 -delay 12 {} -loop 3 gifs/dynamic_pop.gif'.format(files)
os.system(job)