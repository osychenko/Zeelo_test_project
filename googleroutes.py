import urllib.request
import json
import pandas as pd
import numpy as np
import folium

class CitiesRoutes:
    'Class impementing a general interaction with Google Map API to compute routes'

    def __init__(self, country_code='gb'):
        self.country_code = country_code.lower()
        self.apikey = 'AIzaSyASv326cA584q9e707cOiyB_7_guhWdv_4'
        self.geoloc_apikey = 'AIzaSyAVwaIzBIVu3X1NYccY17rTpTiAqaaJsfQ'

        self.cities_table = self.cities_table_init()

    def __len__(self):
        return len(self.cities_table)

    def cities_table_init(self):
        nrows = 1000
        sort_param = 'population'
        url = f'https://public.opendatasoft.com/api/records/1.0/search/?dataset=worldcitiespop' \
              f'&sort={sort_param}' \
              f'&facet=country' \
              f'&refine.country={self.country_code}' \
              f'&rows={nrows}'

        request = urllib.request.urlopen(url)

        # dummy test
        # dummy_output = '{"nhits": 17708, "parameters": {"dataset": ["worldcitiespop"], "refine": {"country": "gb"}, "timezone": "UTC", "rows": 10, "sort": ["population"], "format": "json", "facet": ["country"]}, "records": [{"datasetid": "worldcitiespop", "recordid": "1a3a09c6d9e88e2750844a8155b7bd2f52fd18d4", "fields": {"city": "london", "country": "gb", "region": "H9", "geopoint": [51.514125, -0.093689], "longitude": -0.093689, "latitude": 51.514125, "accentcity": "London", "population": 7421228}, "geometry": {"type": "Point", "coordinates": [-0.093689, 51.514125]}, "record_timestamp": "2018-01-08T11:47:45+00:00"}, {"datasetid": "worldcitiespop", "recordid": "854dc62297a50ffd882d92fb217ac4d9a4cf4681", "fields": {"city": "birmingham", "country": "gb", "region": "A7", "geopoint": [52.466667, -1.916667], "longitude": -1.916667, "latitude": 52.466667, "accentcity": "Birmingham", "population": 984336}, "geometry": {"type": "Point", "coordinates": [-1.916667, 52.466667]}, "record_timestamp": "2018-01-08T11:47:45+00:00"}, {"datasetid": "worldcitiespop", "recordid": "f9a3795d645c9a29cfc5622c0a55bea7b439d003", "fields": {"city": "glasgow", "country": "gb", "region": "V2", "geopoint": [55.833333, -4.25], "longitude": -4.25, "latitude": 55.833333, "accentcity": "Glasgow", "population": 610271}, "geometry": {"type": "Point", "coordinates": [-4.25, 55.833333]}, "record_timestamp": "2018-01-08T11:47:45+00:00"}, {"datasetid": "worldcitiespop", "recordid": "cda05e49431e24c9c96e9d26e50717e2c713a9d7", "fields": {"city": "belfast", "country": "gb", "region": "R3", "geopoint": [54.583333, -5.933333], "longitude": -5.933333, "latitude": 54.583333, "accentcity": "Belfast", "population": 585994}, "geometry": {"type": "Point", "coordinates": [-5.933333, 54.583333]}, "record_timestamp": "2018-01-08T11:47:45+00:00"}, {"datasetid": "worldcitiespop", "recordid": "c80ec7a8f224c0fbb3aedd1d557b0a96435338df", "fields": {"city": "liverpool", "country": "gb", "region": "H8", "geopoint": [53.416667, -3.0], "longitude": -3.0, "latitude": 53.416667, "accentcity": "Liverpool", "population": 468946}, "geometry": {"type": "Point", "coordinates": [-3.0, 53.416667]}, "record_timestamp": "2018-01-08T11:47:45+00:00"}, {"datasetid": "worldcitiespop", "recordid": "ee99264d6f1cf1ce5899eff305f94a170a032a40", "fields": {"city": "leeds", "country": "gb", "region": "H3", "geopoint": [53.8, -1.583333], "longitude": -1.583333, "latitude": 53.8, "accentcity": "Leeds", "population": 455124}, "geometry": {"type": "Point", "coordinates": [-1.583333, 53.8]}, "record_timestamp": "2018-01-08T11:47:45+00:00"}, {"datasetid": "worldcitiespop", "recordid": "08a62eff5ed1a878161e1073263116687bf1eb06", "fields": {"city": "sheffield", "country": "gb", "region": "L9", "geopoint": [53.366667, -1.5], "longitude": -1.5, "latitude": 53.366667, "accentcity": "Sheffield", "population": 447048}, "geometry": {"type": "Point", "coordinates": [-1.5, 53.366667]}, "record_timestamp": "2018-01-08T11:47:45+00:00"}, {"datasetid": "worldcitiespop", "recordid": "ba9eba66e0fbfebf0b8bb7ffd33557ff77908289", "fields": {"city": "edinburgh", "country": "gb", "region": "U8", "geopoint": [55.95, -3.2], "longitude": -3.2, "latitude": 55.95, "accentcity": "Edinburgh", "population": 435794}, "geometry": {"type": "Point", "coordinates": [-3.2, 55.95]}, "record_timestamp": "2018-01-08T11:47:45+00:00"}, {"datasetid": "worldcitiespop", "recordid": "0eab24a1db6886503460c5dc0451978359c60894", "fields": {"city": "bristol", "country": "gb", "region": "B7", "geopoint": [51.45, -2.583333], "longitude": -2.583333, "latitude": 51.45, "accentcity": "Bristol", "population": 430714}, "geometry": {"type": "Point", "coordinates": [-2.583333, 51.45]}, "record_timestamp": "2018-01-08T11:47:45+00:00"}, {"datasetid": "worldcitiespop", "recordid": "223f64707d5fc855036cdf4da1867c381c2448b8", "fields": {"city": "manchester", "country": "gb", "region": "I2", "geopoint": [53.5, -2.216667], "longitude": -2.216667, "latitude": 53.5, "accentcity": "Manchester", "population": 395516}, "geometry": {"type": "Point", "coordinates": [-2.216667, 53.5]}, "record_timestamp": "2018-01-08T11:47:45+00:00"}], "facet_groups": [{"name": "country", "facets": [{"name": "gb", "path": "gb", "count": 17708, "state": "refined"}]}]}'
        # json_cities = json.loads(dummy_output)

        json_cities = json.load(request)
        results = json_cities.get('records')

        results_fields = [x['fields'] for x in results]
        drop_columns = []  # probably, better leave ["country"]

        return pd.DataFrame(results_fields).drop(drop_columns, axis=1).dropna(subset=['population'])

    def retrieve_cities(self, percentile=0.05):
        return self.cities_table.head(int(len(self)*percentile))

    def get_duration(self, mode='driving', origins=None, loc_dest_raw='Victoria Station, London'):
        destinations_formatted = loc_dest_raw.replace(' ', '+')
        chunk_size = 100

        url_dest = f'https://maps.googleapis.com/maps/api/geocode/json?' \
                   f'address={destinations_formatted}&key={self.apikey}'
        req = urllib.request.urlopen(url_dest)
        self.dest_coords = list(json.load(req)["results"][0]['geometry']['location'].values())


        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        duration = []

        for chunk in chunker(origins, chunk_size):
            origins_chunk_formatted = '|'.join(f'{x[0]},{x[1]}' for x in chunk)

            url = f'https://maps.googleapis.com/maps/api/distancematrix/json?' \
                  f'origins={origins_chunk_formatted}&destinations={destinations_formatted}' \
                  f'&key={self.apikey}&mode={mode}'
            request = urllib.request.urlopen(url)

            try:
                results = json.load(request).get('rows')

                if len(results) > 0:
                    duration.extend([x['elements'][0].get('duration', None) for x in results])
                else:
                    print('HTTP GET Request failed.')
            except ValueError as e:
                print(f'JSON decode failed: {request}')
                print(f'---\nError output:\n{e}\n---')

        return duration

    def add_duration(self, is_percentile=True):
        if is_percentile:
            self.cities_table = self.retrieve_cities(percentile=0.05)

        # get coords list
        self.coords = self.cities_table["geopoint"].tolist()

        dur_driving = self.get_duration(origins=self.coords)
        dur_transit = self.get_duration(mode="transit", origins=self.coords)

        self.cities_table["dur_driving_val"] = pd.Series([x["value"] if x is not None else np.nan for x in dur_driving])
        self.cities_table["dur_transit_val"] = pd.Series([x["value"] if x is not None else np.nan for x in dur_transit])
        self.cities_table["dur_driving_txt"] = pd.Series([x["text"] if x is not None else None for x in dur_driving])
        self.cities_table["dur_transit_txt"] = pd.Series([x["text"] if x is not None else None for x in dur_transit])

        self.cities_table["dur_ratio"] = self.cities_table.apply(
            lambda row: row["dur_driving_val"] / row["dur_transit_val"]
            if row.notnull().all() else None, axis=1)

    def draw_map(self):
        self.center_map = [self.cities_table['latitude'].mean(), self.cities_table['longitude'].mean()]

        self.m = folium.Map(
            location=[45.372, -121.6972],
            zoom_start=12,
            tiles='Stamen Terrain'
        )

        folium.Marker(
            location=[45.3288, -121.6625],
            popup='Mt. Hood Meadows',
            icon=folium.Icon(icon='cloud')
        ).add_to(self.m)

        folium.Marker(
            location=[45.3311, -121.7113],
            popup='Timberline Lodge',
            icon=folium.Icon(color='green')
        ).add_to(self.m)

        folium.Marker(
            location=[45.3300, -121.6823],
            popup='Some Other Location',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(self.m)
        self.m.save('map.html')

    @property
    def cities_table_ratio(self):
        return self.cities_table.dropna(subset=["dur_ratio"])

    @property
    def cities_table_short(self):
        columns_short = ['accentcity', 'geopoint', 'dur_ratio']
        return self.cities_table[columns_short]
