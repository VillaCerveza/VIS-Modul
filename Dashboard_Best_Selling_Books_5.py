
# Bibliotheken importieren
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import Output, Input
import pandas as pd
import plotly.express as px
import math
import numpy as np


# Dash-Web App 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])



# GitHub-Dateipfad definieren
github_path = "https://github.com/VillaCerveza/VIS-Modul/raw/main/BEREINIGT_ohne_Autoren_top_100.csv"

# CSV-Datei von GitHub einlesen
df = pd.read_csv(github_path)



# Daten für das erste Diagramm (Balkendiagramm Originalsprache und Verkaufszahlen, Jess)

# nach Originalsprache wird gruppiert und danach der Durchschnitt der Verkaufszahlen berechnet
df_grouped_1 = df.groupby('Original language')['Approximate sales in millions'].mean().reset_index()

fig1 = px.bar(df_grouped_1, x='Original language', y='Approximate sales in millions',
              title='Durchschn. Verkauf nach Sprache',
              color='Original language', color_discrete_sequence=px.colors.qualitative.Light24,
              template='plotly_dark')

# Farblegende verbergen
fig1.update_traces(showlegend=False)



# Daten für das zweite Diagramm (Histogramm Veröffentlichungsjahr 1915-2015 und Verkaufszahlen, Feli)

filtered_df = df[(df['First published'] >= 1915) & (df['First published'] <= 2015)]

fig2 = px.bar(filtered_df, x='First published', y='Approximate sales in millions', 
             title='Verkaufszahlen von Büchern (1915-2015)',
             color='Book',
             color_discrete_sequence=px.colors.qualitative.Antique,
             template='plotly_dark')

fig2.update_xaxes(tickmode='array', 
                  tickvals=list(range(1915, 2015, 15)), 
                  ticktext=[str(year) for year in range(1915, 2015, 15)],
                  showgrid=True)

# Rangeslider für Diagramm 2
fig2.update_layout(
    xaxis=dict(
        rangeslider=dict(
            visible=True,
            thickness=0.01,
            bgcolor='lightblue',  
        ),
        type='linear',
    )
)

# Farblegende verbergen
fig2.update_traces(showlegend=False)

           

# Daten für das dritte Diagramm (Liniendiagramm Veröffentlichungsjahr und Verkaufszahlen, Sarina)

# Abfolge der verknüpften Datenpunkte nach Datum
df_sorted = df.sort_values(by=['Original language', 'First published'])

fig3 = px.line(df_sorted, x='First published', y='Approximate sales in millions',
               title='Verkaufszahlen nach Originalsprache im Zeitverlauf',
               color='Original language', hover_data=['Book'], markers=True, 
               color_discrete_sequence=px.colors.qualitative.Light24,
               template='plotly_dark')



# Daten für das vierte Diagramm (Tortendiagramm Top 5 Genres, Jess)

#Genres zählen
top_fünf_genres = df['Genre'].value_counts().nlargest(5)

# Tortendiagramm erstellen
fig4 = px.pie(top_fünf_genres, values=top_fünf_genres.values, names=top_fünf_genres.index, 
              title='Top 5 Genres', template='plotly_dark') 

# Farblegende verbergen
fig4.update_traces(textinfo='label+percent', showlegend=False, textposition='outside')
   
    
   
# Layoutgestaltung
app.layout = dbc.Container([
    
    
    # Header für Dashboard mit Logo, Titel und Dark/Light-Mode Button
    html.Div([
        # Logo
        html.Img(src='https://github.com/VillaCerveza/VIS-Modul/raw/main/Logo_Best_Selling_Books.png', 
                height='100px', 
                style={'vertical-align': 'middle', 'border': '3px solid gold'}),
        # Titel
        html.H1("Dashboard: Best Selling Books", id='header-title',
                style={'display': 'inline-block', 'vertical-align': 'middle', 'margin-left': '10px'}),
    ], id='header'),
    
    
    # Aufbau Diagramme und Interaktionen
    dbc.Row([
        
        # Diagramm 1 & 2 oben
        dbc.Col([
            dbc.Row([
                dbc.Col(dcc.Graph(id='diagramm1', figure=fig1, style={'height': '350px'}), width=4, id='content-diagram1'),
                dbc.Col(dcc.Graph(id='diagramm2', figure=fig2, style={'height': '350px'}), width=5, id='content-diagram2'),
                dbc.Col(dcc.Graph(id='diagramm4', figure=fig4, style={'height': '350px'}), width=3, id='content-diagram4')
            ]),
            
            
        # Diagramm 3 unten
            dbc.Row([
                dbc.Col(dcc.Graph(id='diagramm3', figure=fig3, style={'height': '470px'}), width=18, id='content-diagram3'),
            ]),
            
            # Rangeslider für Zeitverlauf bei Diagramm 3
                 dbc.Row([
                     dbc.Col(
                         dcc.RangeSlider(
                             id='rangeslider',
                             min=df['First published'].min(),
                             max=df['First published'].max(),
                             step=1,
                             marks={1800: '1800', 1850: '1850', 1900: '1900', 1950: '1950', 2000: '2000'},
                             value=[df['First published'].min(), df['First published'].max()],
                             tooltip={"placement": "bottom", "always_visible": True}), 
                             width=18, id='content-rangeslider'
                             )]),
            
            
        ], id='content'),
        
    ], style={'margin-bottom': '20px'}),
    
        

    # Footer
    #html.Div("designed by Bucher, Perrucci, Ratnam, Zeiter", id='footer'),
    html.Div(
    html.Div("designed by Bucher, Perrucci, Ratnam, Zeiter", id='footer'),
    style={'padding': '20px', 
        'text-align': 'center',
        'font-weight': 'bold'
    }
)

])

# Callback-Änderungen
@app.callback(
    Output('diagramm3', 'figure'),
    Input('rangeslider', 'value')
    )

def update_diagramm3(slider_range):
    low, high = slider_range
    filtered_df = df[(df['First published'] >= low) & (df['First published'] <= high)]
    df_sorted = filtered_df.sort_values(by=['Original language', 'First published'])
    
    color_map = {
        'Chinese': '#FD3216',
        'Czech': '#00FE35',
        'Dutch': '#6A76FC',
        'English': '#FED4C4',
        'French': '#FE00CE',
        'German': '#0DF9FF',
        'Hindi': '#F6F926',
        'Italian': '#FF9616',
        'Japanese': '#479B55',
        'Norwegian': '#EEA6FB',
        'Portuguese': '#DC587D',
        'Russian': '#D626FF',
        'Spanish': '#6E899C',
        'Swedish': '#00B5F7'
        }
    
    fig9 = px.line(
        df_sorted,
        x='First published',
        y='Approximate sales in millions',
        title='Verkaufszahlen nach Originalsprache im Zeitverlauf',
        color='Original language', 
        hover_data=['Book'], 
        markers=True, 
        color_discrete_map=color_map,
        template='plotly_dark')
    return fig9


# Dash-App starten
if __name__ == '__main__':
    app.run_server(debug=False, port=8117)