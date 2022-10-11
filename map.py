import folium
import pandas as pd

dataframe = pd.read_excel('Tamanduá-bandeira_brasil_triado.xlsx')
latitude = list(dataframe['Latitude'])
longitude = list(dataframe['Longitude'])
year = list(dataframe['Ano'])

def color_producer(year):
    """
    Function responsible for changing popup color.
    This function will return a color string based on the year parameter.
    """
    color = ''
    if year <= 2010:
        color = 'red'
    elif year > 2010 and year <= 2013:
        color = 'blue'
    elif year > 2013 and year <= 2016:
        color = 'green'
    elif year > 2016 and year <= 2019:
        color = 'purple'
    else:
        color = 'orange'
    return color

html = """<h4>Giant Anteater information:</h4>
Year of registration: %s  
"""

map = folium.Map(location=[-16.60342859939122, -49.26652953937166], zoom_start=6, tiles='Stamen Terrain')

fga = folium.FeatureGroup(name='Giant Anteater')
for lat, lon, ye in zip(latitude, longitude, year):
    iframe = folium.IFrame(html=html % str(ye), width=200, height=100)
    fga.add_child(folium.CircleMarker(location=[lat,lon], radius=6, fill_opacity=0.7,
    popup=folium.Popup(iframe), fill_color=color_producer(ye), color='grey'))

fgp = folium.FeatureGroup(name='Population')

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgp)
map.add_child(fga)
map.add_child(folium.LayerControl())

map.save('map.html')