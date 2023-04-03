"""This is the main file that runs our app.

Note: even though some function parameters seem unused, they are actually required for the app to run properly.
"""

# import os
# from dotenv import load_dotenv
from dash import Dash, html, dcc, Output, Input, ctx
import plotly.graph_objects as go
import spotipy
from spotipy import SpotifyOAuth

from plot_genre_tree import plot_genre_tree, plot_default_genre_tree
from plot_recommendation_tree import plot_album_recommendation_tree, plot_genre_recommendation_tree, \
    get_albums_by_genre_and_popularity
from albums_data import Album, create_albums
from genres_data import Genre, create_genres


def main() -> None:
    """
    This function is the main block of code that runs our app
    """
    external_stylesheets = [
        'https://raw.githubusercontent.com/antijun/CSC111-Course-Project/main/assets/stylesheet.css']

    app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

    root_genre_stack, visited = [], set()
    albums, genres = create_data()

    sp = spotify_auth()

    app.layout = html.Div([
        html.H1(children='Music Recommendation System',
                style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
        html.Div(children='''This is a web application that can recommend music based on a user's input.''',
                 style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
        html.Button('Get Recommendation', id='rec_button', style={'textAlign': 'center'}),
        html.Button('Explore Genre Tree', id='genre_tree_button', style={'textAlign': 'center'}),
        html.Div(id='rec_output'),
        dcc.Graph(id='tree_plot', figure=blank_fig()),

    ])

    @app.callback(
        Output('rec_output', 'children'),
        Output('tree_plot', 'figure', allow_duplicate=True),
        Input('rec_button', 'n_clicks'),
        Input('genre_tree_button', 'n_clicks'),
        prevent_initial_call='initial_duplicate',
        suppress_callback_exceptions=True
    )
    def update_page(rec_button: html.Button, genre_tree_button: html.Button) -> tuple[html.Div, go.Figure]:
        """
        This function updates the page based on the button pressed.
        If the recommendation button is pressed, the page will be changed to display a combobox with every album.
        If the genre tree button is pressed, the page will be changed to display the genre tree from plot_genre_tree.
        """
        if "rec_button" == ctx.triggered_id:
            main.visited = set()
            return (html.Div([
                html.H3('Choose either an album you like or a genre you like from one of the dropdowns below and press'
                        ' the respective submit button:',
                        style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
                html.H4('Clicking on an album node will give you a new set of recommendations based on the new album'
                        ' you clicked!',
                        style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
                dcc.Dropdown(
                    id='album_dropdown',
                    options=[album.name + ' - ' + album.artist for album in albums],
                    style={'backgroundColor': 'white', 'color': 'black'},
                    placeholder='Select an album...'
                ),
                dcc.Dropdown(
                    id='genre_dropdown',
                    options=[genre.name for genre in genres],
                    style={'backgroundColor': 'white', 'color': 'black'},
                    placeholder='Select a genre...'
                ),
                html.Div(id='album_output'),
                html.Button('Submit Album', id='album_submit', style={'textAlign': 'center'}),
                html.Button('Submit Genre', id='genre_submit', style={'textAlign': 'center'}),
                html.Div(id='spotify_output', style={'textAlign': 'center'}),
                dcc.Graph(id='rec_tree_plot', figure=blank_fig()),
            ]), blank_fig())

        elif "genre_tree_button" == ctx.triggered_id:
            main.root_genre_stack = []
            return (html.Div([
                html.H2('Genre Tree Free Exploration',
                        style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
                html.H3(
                    'This is an interactive visualization of music genres displayed in a hierachical tree structure.',
                    style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
                html.H3("You can freely explore the tree and view a genre's subgenres by clicking on it's node",
                        style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
                html.Button('Go Back', id='back_button', style={'textAlign': 'center'}),
            ]), plot_default_genre_tree())

        else:
            return (html.Div([
                html.H3('Please press a button to get started',
                        style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
            ]), blank_fig())

    @app.callback(
        Output('tree_plot', 'figure', allow_duplicate=True),
        Input('tree_plot', 'clickData'),
        prevent_initial_call=True
    )
    def plot_new_tree(clickData: dict) -> go.Figure or None:
        """
        This function plots a new genre tree based on the node clicked on the old genre tree.
        """
        if clickData is not None:
            if clickData['points'][0]['text'] == 'Genres':
                return plot_default_genre_tree()
            else:
                genre_name = clickData['points'][0]['text']
                new_root = Genre(genre_name, None)
                root_genre_stack.append(new_root)
                new_fig = plot_genre_tree(new_root)
                return new_fig
        else:
            return None

    @app.callback(
        Output('tree_plot', 'figure', allow_duplicate=True),
        Input('back_button', 'n_clicks'),
        prevent_initial_call=True,
    )
    def plot_previous_tree(back_button: html.Button) -> go.Figure:
        """
        This function plots the previous genre tree, does nothing if it is currently the default tree.
        """
        if "back_button" == ctx.triggered_id and len(root_genre_stack) > 0:
            return plot_genre_tree(root_genre_stack.pop())
        else:
            return plot_default_genre_tree()

    @app.callback(
        Output('rec_tree_plot', 'figure', allow_duplicate=True),
        Output('spotify_output', 'children', allow_duplicate=True),
        Input('album_dropdown', 'value'),
        Input('album_submit', 'n_clicks'),
        prevent_initial_call=True,
    )
    def get_album_dropdown_value(value: str, album_submit: html.Button) -> tuple[go.Figure, html.Iframe]:
        """
        This function returns the value of the album dropdown when the recommend button is pressed and plots the
        recommendation tree.

        Preconditions:
            - value != ''

        """
        main.visited = set()
        if "album_submit" == ctx.triggered_id:
            album_name = value.split(' - ')[0]
            album_artist = value.split(' - ')[1]
            album = [alb for alb in albums if alb.name == album_name and alb.artist == album_artist][0]
            return (plot_album_recommendation_tree(album, visited), html.Iframe(src='', id='spotify_embed',
                                                                                style={'display': 'none'}))
        else:
            return (blank_fig(), html.Iframe(src='', id='spotify_embed', style={'display': 'none'}))

    @app.callback(
        Output('rec_tree_plot', 'figure', allow_duplicate=True),
        Output('spotify_output', 'children', allow_duplicate=True),
        Input('genre_dropdown', 'value'),
        Input('genre_submit', 'n_clicks'),
        prevent_initial_call=True,
    )
    def get_genre_dropdown_value(value: str, genre_submit: html.Button) -> tuple[go.Figure, html.Iframe]:
        """
        This function returns the value of the genre dropdown when the recommend button is pressed and plots the
        recommendation tree.

        Preconditions:
            - value != ''

        """
        if "genre_submit" == ctx.triggered_id:
            genre = [gen for gen in genres if gen.name == value][0]
            return (plot_genre_recommendation_tree(genre), html.Iframe(src='', id='spotify_embed',
                                                                       style={'display': 'none'}))
        else:
            return (blank_fig(), html.Iframe(src='', id='spotify_embed', style={'display': 'none'}))

    @app.callback(
        Output('spotify_output', 'children', allow_duplicate=True),
        Input('rec_tree_plot', 'clickData'),
        prevent_initial_call=True
    )
    def SpotifyEmbed(clickData: dict) -> html.Div:
        """
        Embeds a spotify player of the album clicked on the recommendation tree.
        """
        album_name = clickData['points'][0]['text'].split(' - ')[0]
        album_artist = clickData['points'][0]['text'].split(' - ')[1]
        results = sp.search(q='album:' + album_name + ' artist:' + album_artist, type='album')

        if not results['albums']['items']:
            results = sp.search(q='album:' + album_name, type='album')
        if not results['albums']['items']:
            results = sp.search(q='album:' + album_name.split(' (')[0] + ' artist:' + album_artist, type='album')
        if not results['albums']['items']:
            results = sp.search(q='album:' + album_name.split('(')[1].split(')')[0] + ' artist:' + album_artist,
                                type='album')
        if not results['albums']['items']:
            return html.Div('No Spotify results found', style={'textAlign': 'center', 'color': 'hotpink'})

        album_id = results['albums']['items'][0]['id']
        return html.Div([
            html.Iframe(src='https://open.spotify.com/embed/album/' + album_id, width='700', height='380'),
        ])

    @app.callback(
        Output('rec_tree_plot', 'figure', allow_duplicate=True),
        Input('rec_tree_plot', 'clickData'),
        prevent_initial_call=True
    )
    def plot_new_recommendation_tree(clickData: dict) -> go.Figure or None:
        """
        This function plots a new recommendation tree based on the node clicked on the old recommendation tree.
        When a leaf node is clicked on the genre recommendation tree, it will plot the album recommendation tree.
        """
        if clickData is not None:
            print(clickData['points'][0]['text'])
            album_name = clickData['points'][0]['text'].split(' - ')[0]
            album_artist = clickData['points'][0]['text'].split(' - ')[1]
            album = [alb for alb in albums if alb.name == album_name and alb.artist == album_artist][0]
            visited.add(album_name)
            return plot_album_recommendation_tree(album, visited)
        else:
            return None

    app.run_server(debug=False)


def create_data() -> tuple[list[Album], list[Genre]]:
    """
    This function creates the data needed for our app.
    """
    albums = create_albums()
    genres = create_genres()
    genres = [genre for genre in genres if get_albums_by_genre_and_popularity(genre.name, albums) != []]
    return albums, genres


def spotify_auth() -> spotipy.Spotify:
    """
    This function authenticates for the spotify API.
    """
    # load_dotenv()
    # SPOTIPY_CLIENT_ID = load_dotenv('SPOTIPY_CLIENT_ID')
    # SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    # SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

    SPOTIPY_CLIENT_ID = 'cccd08f05aea4eb4b794ba8c4606f057'
    SPOTIPY_CLIENT_SECRET = '0fa3ff51327c4118b26813dd916570a9'
    SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback/'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                   client_secret=SPOTIPY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIPY_REDIRECT_URI,
                                                   ))
    return sp


def blank_fig() -> go.Figure:
    """
    This function creates a blank figure.
    """
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['os', 'spotipy', ' plotly.graph_objects', 'dotenv', 'plot_genre_tree',
                          'plot_recommendation_tree',
                          'dash', 'albums_data', 'genres_data'],
        'allowed-io': ['main'],
    })

    main()
