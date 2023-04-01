from dash import Dash, html, dcc, callback, Output, Input, ctx, State
import plotly.express as px
import pandas as pd
from plot_genre_tree import genre_fig
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
from albums_data import albums

app = Dash(__name__)


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
    html.Button('Get Recommendation', id='rec_button'),
    html.Button('Explore Genre Tree', id='genre_tree_button'),
    html.Div(id='rec_output'),
    dcc.Graph(id='tree_plot', figure=blank_fig())
])


@app.callback(
    Output('rec_output', 'children'),
    Input('rec_button', 'n_clicks'),
    Input('genre_tree_button', 'n_clicks')
)
def update_page(rec_button, genre_tree_button):
    """
    This function updates the page based on the button pressed.
    If the recommendation button is pressed, the page will be changed to display a combobox with every album.
    If the genre tree button is pressed, the page will be changed to display the genre tree from plot_genre_tree.
    """
    if "rec_button" == ctx.triggered_id:
        return html.Div([
            html.H3('Please select an album that you enjoy listening to from the dropdown below:',
                    style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='album_dropdown',
                options=[album.name + ' - ' + album.artist for album in albums],
            ),
            html.Div(id='album_output')
        ])

    elif "genre_tree_button" == ctx.triggered_id:
        return html.Div([
            html.H1('Genre Tree Free Exploration', style={'textAlign': 'center'}),
            html.H3('This is an interactive visualization of music genres displayed in a hierachical tree structure.',
                    style={'textAlign': 'center'}),
            html.H3("You can freely explore the tree and view a genre's subgenres by clicking on it's node",
                    style={'textAlign': 'center'}),
            dcc.Graph(figure=genre_fig)
        ])
    else:
        return html.Div([
            html.H3('Please press a button to get started', style={'textAlign': 'center'}),
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
