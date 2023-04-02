import os
from dotenv import load_dotenv
from dash import Dash, html, dcc, Output, Input, ctx
import spotipy
from spotipy import SpotifyOAuth
from plot_genre_tree import plot_genre_tree, plot_default_genre_tree
from plot_recommendation_tree import *
import plotly.graph_objects as go
from albums_data import create_albums
from genres_data import Genre


def main() -> None:
    """
    This function is the main block of code that runs our app
    """
    load_dotenv()
    SPOTIPY_CLIENT_ID = load_dotenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                   client_secret=SPOTIPY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIPY_REDIRECT_URI,
                                                   ))

    external_stylesheets = [
        'https://raw.githubusercontent.com/antijun/CSC111-Course-Project/main/assets/stylesheet.css']

    app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

    root_genre_stack = []
    visited = set()
    albums = create_albums()

    def blank_fig():
        """
        This function creates a blank figure.
        """
        fig = go.Figure(go.Scatter(x=[], y=[]))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.update_layout(template=None)
        fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
        return fig

    app.layout = html.Div([
        html.H1(children='Music Recommendation System',
                style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
        html.Div(children='''This is a web application that recommends music based on the user's preferences.''',
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
    def update_page(self, rec_button, genre_tree_button):
        """
        This function updates the page based on the button pressed.
        If the recommendation button is pressed, the page will be changed to display a combobox with every album.
        If the genre tree button is pressed, the page will be changed to display the genre tree from plot_genre_tree.
        """
        if "rec_button" == ctx.triggered_id:
            self.visited = set()
            return html.Div([
                html.H3('Please select an album that you enjoy listening to from the dropdown below:',
                        style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
                dcc.Dropdown(
                    id='album_dropdown',
                    options=[album.name + ' - ' + album.artist for album in albums],
                    style={'backgroundColor': 'white', 'color': 'black'}
                ),
                html.Div(id='album_output'),
                html.Button('Recommend Me!', id='album_submit', style={'textAlign': 'center'}),
                html.Div(id='spotify_output', style={'textAlign': 'center'}),
                dcc.Graph(id='rec_tree_plot', figure=blank_fig()),
            ]), blank_fig()

        elif "genre_tree_button" == ctx.triggered_id:
            self.root_genre_stack = []
            return html.Div([
                html.H2('Genre Tree Free Exploration',
                        style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
                html.H3(
                    'This is an interactive visualization of music genres displayed in a hierachical tree structure.',
                    style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
                html.H3("You can freely explore the tree and view a genre's subgenres by clicking on it's node",
                        style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
                html.Button('Go Back', id='back_button', style={'textAlign': 'center'}),
            ]), plot_default_genre_tree()

        else:
            return html.Div([
                html.H3('Please press a button to get started',
                        style={'textAlign': 'center', 'backgroundColor': '#383838', 'color': 'hotpink'}),
            ]), blank_fig()

    @app.callback(
        Output('tree_plot', 'figure', allow_duplicate=True),
        Input('tree_plot', 'clickData'),
        prevent_initial_call=True
    )
    def plot_new_tree(clickData):
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

    @app.callback(
        Output('tree_plot', 'figure', allow_duplicate=True),
        Input('back_button', 'n_clicks'),
        prevent_initial_call=True,
    )
    def plot_previous_tree(back_button):
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
    def get_album_dropdown_value(self, value, album_submit):
        """
        This function returns the value of the album dropdown when the recommend button is pressed and plots the
        recommendation tree.

        Also adds an empty Iframe
        """
        self.visited = set()
        if "album_submit" == ctx.triggered_id:
            album_name = value.split(' - ')[0]
            album_artist = value.split(' - ')[1]
            album = [album for album in albums if album.name == album_name and album.artist == album_artist][0]
            return plot_album_recommendation_tree(album, visited), html.Iframe(src='', id='spotify_embed',
                                                                               style={'display': 'none'})
        else:
            return blank_fig()

    @app.callback(
        Output('spotify_output', 'children', allow_duplicate=True),
        Input('rec_tree_plot', 'clickData'),
        prevent_initial_call=True
    )
    def SpotifyEmbed(clickData):
        """
        Embeds the Spotify player of the album at the root
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
        return html.Iframe(src='https://open.spotify.com/embed/album/' + album_id, width='700', height='380', )

    @app.callback(
        Output('rec_tree_plot', 'figure', allow_duplicate=True),
        Input('rec_tree_plot', 'clickData'),
        prevent_initial_call=True
    )
    def plot_new_recommendation_tree(clickData):
        """
        This function plots a new recommendation tree based on the node clicked on the old recommendation tree.
        """
        if clickData is not None:
            album_name = clickData['points'][0]['text'].split(' - ')[0]
            album_artist = clickData['points'][0]['text'].split(' - ')[1]
            album = [album for album in albums if album.name == album_name and album.artist == album_artist][0]
            visited.add(album_name)
            return plot_album_recommendation_tree(album, visited)

    app.run_server(debug=False)


if __name__ == '__main__':
    main()
