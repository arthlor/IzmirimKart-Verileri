import pandas as pd
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import sys

# Attempt to read the Excel file
try:
    df = pd.read_excel('ulasim.xlsx')  # Update 'ulasim.xlsx' to your actual Excel file's path
    print("Excel file successfully read")

    # Convert 'Tarih' column to datetime
    df['Tarih'] = pd.to_datetime(df['Tarih'])

    # Get unique institutions
    kurumlar = df['Kurum'].unique()

    # Define the app with the viewport meta tag for mobile responsiveness
    app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

    # Define the layout of the app
    app.layout = html.Div([
        html.H1(id="graph-title", children="İzmirimKart Verileri",
                style={'textAlign': 'center', 'color': '#2b2b2b', 'fontFamily': 'Helvetica, sans-serif', 'fontSize': '21px'}),
        html.Div("Bu grafik, 1 Ocak 2021 ile 30 Ekim 2023 tarihleri arasında, çeşitli kurumlardaki İzmirimKart kullanım verilerini göstermektedir. En iyi deneyim için bilgisayardan incelenmesi önerilir.",
                 style={'textAlign': 'center', 'color': '#606060', 'fontFamily': 'Helvetica, sans-serif', 'marginTop': '10px', 'marginBottom': '20px'}),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': kurum, 'value': kurum} for kurum in kurumlar],
            value=kurumlar[0],
            style={'width': '100%', 'maxWidth': '500px', 'margin': '0 auto', 'color': '#2b2b2b', 'backgroundColor': '#fafafa', 'fontFamily': 'Helvetica, sans-serif'}
        ),
        dcc.Graph(
            id='grafik',
            style={'width': '100%', 'height': '100%', 'minHeight': '400px', 'margin': '20px auto'},
            config={'responsive': True}
        )
    ])

    # Callback to update the graph based on dropdown selection
    @app.callback(
        Output('grafik', 'figure'),
        [Input('dropdown', 'value')]
    )
    def grafik_güncelle(seçilen_değer):
        # Filter data for the selected institution
        filtrelenmiş_veri = df[df['Kurum'] == seçilen_değer]
        
        # Create traces for each passenger type
        izler = []
        renkler = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099', '#3b3eac', '#0099c6']
        for i, sütun in enumerate(filtrelenmiş_veri.columns[3:]):
            iz = go.Scatter(
                x=filtrelenmiş_veri['Tarih'],
                y=filtrelenmiş_veri[sütun],
                mode='lines+markers',
                name=sütun,
                hoverinfo='x+y+name',
                text=[f"{sütun}: {filtrelenmiş_veri.iloc[j][sütun]}" for j in range(len(filtrelenmiş_veri))],
                marker=dict(size=7, opacity=0.5),
                line=dict(color=renkler[i], width=2, dash='dot')
            )
            izler.append(iz)
        
        # Define the layout
        layout = go.Layout(
            xaxis=dict(title='Tarih', tickformat='%d %b %Y', gridcolor='#eaeaea', zeroline=False, titlefont=dict(family='Helvetica, sans-serif', size=18, color='#2b2b2b'), tickfont=dict(family='Helvetica, sans-serif', size=12, color='#2b2b2b')),
            yaxis=dict(title='Toplam Yolcu Sayısı', gridcolor='#eaeaea', zeroline=False, titlefont=dict(family='Helvetica, sans-serif', size=18, color='#2b2b2b'), tickfont=dict(family='Helvetica, sans-serif', size=12, color='#2b2b2b')),
            template='plotly_white',
            margin=dict(l=50, r=50, t=70, b=50),
            plot_bgcolor='#fafafa',
            paper_bgcolor='#fafafa',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(family='Helvetica, sans-serif', size=12, color='#2b2b2b')),
            hovermode='x unified',
            hoverlabel=dict(bgcolor='#ffffff', font=dict(family='Helvetica, sans-serif', color='#2b2b2b', size=14))
        )
        
        # Create the figure
        figür = go.Figure(data=izler, layout=layout)
        
        return figür

    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)

except FileNotFoundError:
    print("Excel file not found")
except Exception as e:
    print(f"Failed to read Excel file: {e}")

