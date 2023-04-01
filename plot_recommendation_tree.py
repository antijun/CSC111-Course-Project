import plotly.graph_objects as go
from igraph import Graph, EdgeSeq
from genres_data import genres, Genre
from albums_data import albums, Album
from tree_classes import AlbumTree


def plot_genre_recommendation_tree(selected_genre: Genre):
    """
    This function plots the genre tree of the given root genre.
    """
    # Create a graph object
    G = Graph(directed=True)

    # Add the root node
    G.add_vertex(selected_genre.name)

    # Add the children of the root node
    top_albums_by_genre = get_albums_by_genre_and_popularity(selected_genre.name, albums)

    for i in range(0, 10):
        G.add_vertex(top_albums_by_genre[i].name)
        G.add_edge(selected_genre.name, top_albums_by_genre[i].name)

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


# genre_fig = plot_genre_recommendation_tree(genres[436])


def get_albums_by_genre_and_popularity(genre: str, albums_list: list[Album]) -> list[Album]:
    """Given a list of albums sorted from most popular to leat popular and a genre, return a list containing albums with
    the specified genre(Note that albums from albums data are already sorted by popularity)
    """

    filtered_ablums_list = []

    for album in albums_list:
        if genre in album.genres:
            filtered_ablums_list.append(album)

    return filtered_ablums_list


def plot_album_recommendation_tree(selected_album: Album, visited: set[str]):
    """
    This function plots the genre tree of the given root genre.
    """
    # Create a graph object
    G = Graph(directed=True)

    # Add the root node
    G.add_vertex(selected_album.name)

    # Add the children of the root node
    album_tree = generate_album_recommendation_tree(selected_album, albums, 3, 2, visited)
    edges = get_all_branches(album_tree)

    for edge in edges:
        G.add_vertex(edge[0])
        G.add_vertex(edge[1])
        G.add_edge(edge[0], edge[1])

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


def get_albums_by_matches(album: Album, albums_list: list[Album], num_recommendations,
                          visited: set[str]) -> list[Album]:
    """Given an album and a list of albums, return a list sorted based on the number of matching descriptors between
    ablum and the ablums in albums_list. The returned list is sorted from most to least number of matches
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
            edges.append((album_tree.root.name, subtree.root.name))

        return edges
