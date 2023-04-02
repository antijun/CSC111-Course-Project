import plotly.graph_objects as go
from igraph import EdgeSeq, Graph

from albums_data import Album, create_albums
from genres_data import Genre
from tree_classes import AlbumTree


def get_albums_by_genre_and_popularity(genre: str, albums_list: list[Album]) -> list[Album]:
    """Given a list of albums sorted from most popular to leat popular and a genre, return a list containing albums with
    the specified genre(Note that albums from albums data are already sorted by popularity)
    """
    filtered_ablums_list = []

    for album in albums_list:
        if genre in album.genres:
            filtered_ablums_list.append(album)

    return filtered_ablums_list


def improve_text_position(Xn) -> list[str]:
    """
    Fixes text overlap issues by alternating between top and bottom text positions (still overlap for some cases).
    """
    positions = ['top center', 'bottom center']
    return ['middle center' if Xn[i] == 0 else positions[i % 2] for i in range(len(Xn))]


def plot_genre_recommendation_tree(selected_genre: Genre) -> go.Figure:
    """
    This function plots the genre recommendation tree with the root being the selected genre,
    each subgenre is has a parent
    """
    albums = create_albums()
    G = Graph(directed=True)
    G.add_vertex(selected_genre.name)
    top_albums_by_genre = get_albums_by_genre_and_popularity(selected_genre.name, albums)
    if len(top_albums_by_genre) > 10:
        for i in range(0, 10):
            album_name_and_artist = top_albums_by_genre[i].name + ' - ' + top_albums_by_genre[i].artist
            G.add_vertex(album_name_and_artist)
            G.add_edge(selected_genre.name, album_name_and_artist)
    else:
        for album in top_albums_by_genre:
            album_name_and_artist = album.name + ' - ' + album.artist
            G.add_vertex(album_name_and_artist)
            G.add_edge(selected_genre.name, album_name_and_artist)
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
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=30,
                                         color='hotpink',
                                         line=dict(color='rgb(50,50,50)', width=1)
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


def plot_album_recommendation_tree(selected_album: Album, visited: set[str]) -> go.Figure:
    """
    This function plots the genre tree of the given root genre.
    """
    albums = create_albums()
    G = Graph(directed=True)
    # G.add_vertex(selected_album.name)
    album_tree = generate_album_recommendation_tree(selected_album, albums, 3, 2, visited)
    edges = get_all_branches(album_tree)
    vertices = get_all_vertices(album_tree)
    for vertex in vertices:
        G.add_vertex(vertex)
    for edge in edges:
        G.add_edge(edge[0], edge[1])
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
                             name='bla',
                             marker=dict(symbol='circle-dot',
                                         size=30,
                                         color='hotpink',
                                         line=dict(color='rgb(50,50,50)', width=1)
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


def get_albums_by_matches(album: Album, albums_list: list[Album], num_recommendations,
                          visited: set[str]) -> list[Album]:
    """Given an album and a list of albums, return a list sorted based on the number of matching descriptors between
    ablum and the ablums in albums_list. The returned list is sorted from most to least number of matches

    Preconditions:
        - num_recommendations > 0
        - album is in albums_list

    """

    sorted_matches_list = []
    album_to_matches = {}
    max_matches = 0

    for current_album in albums_list:
        if current_album.name != album.name and current_album.name not in visited:
            matching_descriptors = set(album.descriptors).intersection(current_album.descriptors)
            num_matches = len(matching_descriptors)

            album_to_matches[current_album.name] = (current_album, num_matches)

            if num_matches > max_matches:
                max_matches = num_matches

    for i in range(max_matches, -1, -1):
        for album in album_to_matches:
            if album_to_matches[album][1] == i:
                sorted_matches_list.append(album_to_matches[album][0])

            if len(sorted_matches_list) == num_recommendations:
                return sorted_matches_list

    return sorted_matches_list


def generate_album_recommendation_tree(root_album: Album, albums_list: list[Album], num_recommendations: int,
                                       depth: int, visited: set) -> AlbumTree:
    """Given a root album and a list of albums, create a tree starting at root_album with each subtree having
    num_recommendations number of subtrees. The return tree should be up to the depth specified.

    Preconditions:
        - depth >= 0
        - num_recommendations >= 0
        - root_album is in albums_list
    """
    album_tree = AlbumTree(root_album, [])

    if depth == 0:
        return album_tree
    else:
        visited.add(root_album.name)
        recommeneded_albums = get_albums_by_matches(root_album, albums_list, num_recommendations, visited)
        for album in recommeneded_albums:
            visited.add(album.name)

        for album in recommeneded_albums:
            album_tree.add_subtree(generate_album_recommendation_tree(album, albums_list, num_recommendations,
                                                                      depth - 1, visited))

        return album_tree


def get_all_branches(album_tree: AlbumTree) -> list[tuple[str, str]]:
    """Given an album tree, return a list of all the branches in the tree
    """
    edges = []
    if album_tree.is_empty() or album_tree.get_subtrees() == []:
        return []
    else:
        subtrees = album_tree.get_subtrees()
        for subtree in subtrees:
            root_album_and_artist = album_tree.root().name + ' - ' + album_tree.root().artist
            subtree_album_and_artist = subtree.root().name + ' - ' + subtree.root().artist
            edges.append((root_album_and_artist, subtree_album_and_artist))
            edges.extend(get_all_branches(subtree))

        return edges


def get_all_vertices(album_tree: AlbumTree) -> list[str]:
    """Given an album tree, return a list of all the branches in the tree
    """
    vertices = []
    if album_tree.is_empty():
        return []
    elif not album_tree.get_subtrees():
        album_and_artist = album_tree.root().name + ' - ' + album_tree.root().artist
        return [album_and_artist]
    else:
        album_and_artist = album_tree.root().name + ' - ' + album_tree.root().artist
        vertices.append(album_and_artist)
        subtrees = album_tree.get_subtrees()
        for subtree in subtrees:
            vertices.extend(get_all_vertices(subtree))

        return vertices
