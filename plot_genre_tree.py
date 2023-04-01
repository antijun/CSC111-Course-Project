import plotly.graph_objects as go
from igraph import Graph, EdgeSeq
from genres_data import genres


def plot_genre_tree(root_genre):
    """
    This function plots the genre tree of the given root genre.
    """
    # Create a graph object
    G = Graph(directed=True)

    # Add the root node
    G.add_vertex(root_genre.name)

    # Add the children of the root node
    for genre in genres:
        if genre.parent_genre == root_genre.name:
            G.add_vertex(genre.name)
            G.add_edge(root_genre.name, genre.name)

    # Create a layout for the graph
    lay = G.layout('rt')

    # Create the labels for the vertices
    v_label = G.vs['name']

    # Create a list of positions for the vertices
    position = {k: lay[k] for k in range(len(lay))}
    Y = [lay[k][1] for k in range(len(lay))]
    M = max(Y)

    # Create a list of edges
    es = EdgeSeq(G)  # sequence of edges
    E = [e.tuple for e in G.es]  # list of edges

    # Create a list
    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]
    Xe = []
    Ye = []

    # Create a list of edges
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                             y=Ye,
                             mode='lines',
                             line=dict(color='rgb(210,210,210)', width=1),
                             hoverinfo='none'
                             ))
    fig.add_trace(go.Scatter(x=Xn,
                             y=Yn,
                             text=v_label,
                             mode='markers+text',
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=18,
                                         color='#6175c1',  # '#DB4551',
                                         line=dict(color='rgb(50,50,50)', width=1)
                                         ),
                             hoverinfo='text',
                             opacity=0.8
                             ))

    return fig


genre_fig = plot_genre_tree(genres[436])
