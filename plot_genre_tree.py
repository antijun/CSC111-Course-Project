import plotly.graph_objects as go
from igraph import Graph, EdgeSeq
from genres_data import create_genres


def plot_default_genre_tree() -> go.Figure:
    """
    This function plots the genre tree with the root being 'Genres', each subgenre is has a parent genre of None.
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


def plot_genre_tree(root_genre) -> go.Figure:
    """
    This function plots the genre tree of the given root genre.
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


def improve_text_position(Xn) -> list[str]:
    """
    Fixes text overlap issues by alternating between top and bottom text positions (still overlap for some cases).
    """
    positions = ['top center', 'bottom center']
    return ['middle center' if Xn[i] == 0 else positions[i % 2] for i in range(len(Xn))]
