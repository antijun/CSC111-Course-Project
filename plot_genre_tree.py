"""CSC111 Project Phase 2: Interactive Music Genre and Album Recommendation Tree (Genre Data)

Description
===============================

This Python module contains the functions used to generate a visualization of the genre tree using ploty and igraph. The
genres are taken from functions in genres_data.py

This file is Copyright (c) 2023 David Wu and Kevin Hu.
"""
import plotly.graph_objects as go
from igraph import Graph, EdgeSeq
from genres_data import create_genres, Genre


def plot_default_genre_tree() -> go.Figure:
    """Obtained from the plotly library for tree-plots, this function plots the genre tree with the root being 'Genres',
    each subgenre is has a parent genre of None. In other words, this function plots the root node of the entire genre
    tree, as well as its direct subtrees.
    """
    genres = create_genres()
    G = Graph(directed=True)
    G.add_vertex('Genres')
    for genre in genres:
        if genre.parent_genre is None:
            G.add_vertex(genre.name)
            G.add_edge('Genres', genre.name)
    lay = G.layout('rt')
    v_label = G.vs['name']
    position = {k: lay[k] for k in range(len(lay))}
    Y = [lay[k][1] for k in range(len(lay))]
    M = max(Y)
    es = EdgeSeq(G)
    E = [e.tuple for e in G.es]

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]
    Xe = []
    Ye = []
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
                             name='Genre',
                             marker=dict(symbol='circle-dot',
                                         size=30,
                                         color='hotpink',
                                         line=dict(color='rgb(50,50,50)', width=1),
                                         ),
                             hoverinfo='text',
                             opacity=0.8
                             ))

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.for_each_trace(lambda t: t.update(textfont_color='white', opacity=1))
    fig.update_traces(textposition=improve_text_position(Xn))
    fig.update_layout(showlegend=False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    return fig


def plot_genre_tree(root_genre: Genre) -> go.Figure:
    """Obtained from the plotly library for tree-plots, this function plots the genre tree of the given root genre. The
    root genre is a valid genre in genres_dataset.csv, with its subtrees being subgenres of the root genre.

    Preconditions:
            - root_genre.name in [genre.name for genre in create_genres()]
    """
    genres = create_genres()
    G = Graph(directed=True)
    G.add_vertex(root_genre.name)
    for genre in genres:
        if genre.parent_genre == root_genre.name:
            G.add_vertex(genre.name)
            G.add_edge(root_genre.name, genre.name)
    lay = G.layout('rt')
    v_label = G.vs['name']
    position = {k: lay[k] for k in range(len(lay))}
    Y = [lay[k][1] for k in range(len(lay))]
    M = max(Y)
    es = EdgeSeq(G)
    E = [e.tuple for e in G.es]
    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]
    Xe = []
    Ye = []
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
                             name='Genre',
                             marker=dict(symbol='circle-dot',
                                         size=30,
                                         color='hotpink',
                                         line=dict(color='rgb(50,50,50)', width=1),
                                         ),
                             hoverinfo='text',
                             opacity=0.8
                             ))

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.for_each_trace(lambda t: t.update(textfont_color='white', opacity=1))
    fig.update_traces(textposition=improve_text_position(Xn))
    fig.update_layout(showlegend=False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    return fig


def improve_text_position(Xn: list) -> list[str]:
    """This function fixes text overlap issues by alternating between top and bottom text positions (Note: still overlap
    for some cases).
    """
    positions = ['top center', 'bottom center']
    return ['middle center' if Xn[i] == 0 else positions[i % 2] for i in range(len(Xn))]


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['plotly.graph_objects', 'igraph', 'genres_data'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'disable': ['too-many-locals', 'unnecessary-indexing', 'invalid-name'],
        'max-line-length': 120
    })
