import json

from dash import Dash, html, dcc, callback, Output, Input, ctx, State
import plotly.express as px
import pandas as pd
from plot_genre_tree import plot_genre_tree, plot_default_genre_tree
from plot_recommendation_tree import *
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
from albums_data import albums
from genres_data import Genre

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

root_genre_stack = []
visited = set()


def blank_fig():
    """
    This function creates a blank figure.
    """
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


app.layout = html.Div([
    html.H1(children='Music Recommendation System', style={'textAlign': 'center'}),
    html.Div(children='''This is a web application that recommends music based on the user's preferences.'''),
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
def update_page(rec_button, genre_tree_button):
    """
    This function updates the page based on the button pressed.
    If the recommendation button is pressed, the page will be changed to display a combobox with every album.
    If the genre tree button is pressed, the page will be changed to display the genre tree from plot_genre_tree.
    """
    if "rec_button" == ctx.triggered_id:
        global visited
        visited = set()
        return html.Div([
            html.H3('Please select an album that you enjoy listening to from the dropdown below:',
                    style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='album_dropdown',
                options=[album.name + ' - ' + album.artist for album in albums],
            ),
            html.Div(id='album_output'),
            html.Button('Recommend Me!', id='album_submit', style={'textAlign': 'center'}),
            dcc.Graph(id='rec_tree_plot', figure=blank_fig()),
        ]), blank_fig()

    elif "genre_tree_button" == ctx.triggered_id:
        global root_genre_stack
        root_genre_stack = []
        return html.Div([
            html.H2('Genre Tree Free Exploration', style={'textAlign': 'center'}),
            html.H3('This is an interactive visualization of music genres displayed in a hierachical tree structure.',
                    style={'textAlign': 'center'}),
            html.H3("You can freely explore the tree and view a genre's subgenres by clicking on it's node",
                    style={'textAlign': 'center'}),
            html.Button('Go Back', id='back_button', style={'textAlign': 'center'}),
        ]), plot_default_genre_tree()

    else:
        return html.Div([
            html.H3('Please press a button to get started', style={'textAlign': 'center'}),
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
    global root_genre_stack
    if "back_button" == ctx.triggered_id and len(root_genre_stack) > 0:
        return plot_genre_tree(root_genre_stack.pop())
    else:
        return plot_default_genre_tree()


@app.callback(
    Output('rec_tree_plot', 'figure', allow_duplicate=True),
    Input('album_dropdown', 'value'),
    Input('album_submit', 'n_clicks'),
    prevent_initial_call=True,
)
def get_album_dropdown_value(value, album_submit):
    """
    This function returns the value of the album dropdown when the recommend button is pressed and plots the
    recommendation tree.
    """
    if "album_submit" == ctx.triggered_id:
        album_name = value.split(' - ')[0]
        album_artist = value.split(' - ')[1]
        album = [album for album in albums if album.name == album_name and album.artist == album_artist][0]
        return plot_album_recommendation_tree(album, visited)
    else:
        return blank_fig()


if __name__ == '__main__':
    app.run_server(debug=True)
