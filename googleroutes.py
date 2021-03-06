__author__ = "Oleg Osychenko"
__copyright__ = "Copyright 2018, Zeelo test project"
__credits__ = ["Zeelo developers"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Oleg Osychenko"
__email__ = "osychenko@gmail.com"
__status__ = "Development"

"""Module documentation
-----------------------
Requirements:
    python 3.6 or newer
Packages:
    urllib
    json
    pandas
    numpy
    folium
-----------------------
Description:
Class to generate driving/transit time ratio (or a similar combination of modes) for a given country. 
The list is loaded into pd.DataFrame, sorted by parameter (default population) in the query to API, 
no pandas-related sorting is used. 
"""

import urllib.request
import json
import pandas as pd
import numpy as np
import folium


class CitiesRoutes:
    """Class impementing a general interaction with Google Map API to compute travel times"""

    def __init__(self, country_code: str = 'gb', apikey: str = None):
        """ Lookup table for top (up to 1000) cities (ordeded by sort_param, default population),
        is generated here in the constructor.
ç       :param country_code: str code of a country, apikey: str Google Map API key
        """
        self.country_code: str = country_code.lower()
        self.apikey: str = 'AIzaSyASv326cA584q9e707cOiyB_7_guhWdv_4' if apikey is None else apikey
        self.destination: str or list = 'Victoria Station, London'

        # table generated
        self.cities_table: pd.DataFrame = self.cities_table_init()

        self.percentile: float = None

    def __len__(self):
        """ Returns number of rows in underlying DataFrame"""
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

        json_cities = json.load(request)
        results = json_cities.get('records')

        results_fields = [x['fields'] for x in results]
        drop_columns = []  # probably, better leave ["country"]

        return pd.DataFrame(results_fields).drop(drop_columns, axis=1).dropna(subset=['population'])

    def retrieve_cities(self, percentile: float = None, is_verbose: bool = True):
        """ Get a float fraction of top rows in DataFrame
        :param percentile: float between 0 and 1
        verbose - flush verbose data"""

        if percentile is None:
            self.percentile = self.percentile or 0.05
        else:
            self.percentile = percentile

        df_output = self.cities_table.head(int(len(self) * self.percentile))
        if is_verbose:
            print(f'Cities shown: {len(df_output)}')
        return df_output

    def get_duration(self, mode: str = 'driving', origins: list = None) -> list:
        """ Gets duration between self.destination and origins in chosen mode.
        List origins will be splitted in chunks (default 100), since this is the current
        limitation for request to Google Map API.
        ** Practical suggestion ** Use correctly defined string addresses whenever possible
        instead of coordinates, the probability to get ZERO_RESULTS are greatly reduced then.
        :param mode: str transport mode (default driving)
        :param origins: list (of str addresses or lists [lat, lon])
        :return: list of dicts [{'value'=duration_value, 'text'=duration_text}]
        """
        destinations_formatted = self.destination.replace(' ', '+')
        chunk_size = 100

        # get coordinates of the destination
        # might be needed to adjust the map, or for distancematrix
        url_dest = f'https://maps.googleapis.com/maps/api/geocode/json?' \
                   f'address={destinations_formatted}&key={self.apikey}'
        req = urllib.request.urlopen(url_dest)
        self.dest_coords = list(json.load(req)["results"][0]['geometry']['location'].values())

        def chunker(seq, size):
            """ Returns generator chunks of the given sequence"""
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        duration = []

        for chunk in chunker(origins, chunk_size):
            if isinstance(chunk[0], list):
                # if list of coordinate pairs [lat, lon]
                origins_chunk_formatted = '|'.join(f'{x[0]},{x[1]}' for x in chunk)
            else:
                # if list of names
                origins_chunk_formatted = '|'.join(f"{x.replace(' ', '+')},+{self.country_code}" for x in chunk)

            url = f'https://maps.googleapis.com/maps/api/distancematrix/json?' \
                  f'origins={origins_chunk_formatted}' \
                  f'&destinations={destinations_formatted}' \
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

    def add_duration(self, percentile=None):
        """ Cut self.cities_table to leave top percentile fraction, add columns for duration
        (as value in seconds and as text 'X hours Y minutes'), add column for ratio 'driving time / transit time'
        :param percentile: take the top percentile fraction or the whole, if provided.
        Otherwise, 0.05 or any value given priorly in retrive_cities.
        :return: None, updates cities_table to cities_table_duration
        """
        if percentile is None:
            self.percentile = self.percentile or 0.05
        else:
            self.percentile = percentile

        self.cities_table_duration = self.retrieve_cities(percentile=self.percentile, is_verbose=False).copy()
        print(f'Cities in the list: {len(self.cities_table_duration)}')

        # get coords or cities list
        self.coords = self.cities_table_duration['geopoint'].tolist()
        self.city = self.cities_table_duration['city'].tolist()

        dur_driving = self.get_duration(origins=self.city)
        dur_transit = self.get_duration(mode="transit", origins=self.city)

        self.cities_table_duration["dur_driving_val"] = pd.Series([x["value"] if x is not None else np.nan for x in dur_driving])
        self.cities_table_duration["dur_transit_val"] = pd.Series([x["value"] if x is not None else np.nan for x in dur_transit])
        self.cities_table_duration["dur_driving_txt"] = pd.Series([x["text"] if x is not None else None for x in dur_driving])
        self.cities_table_duration["dur_transit_txt"] = pd.Series([x["text"] if x is not None else None for x in dur_transit])

        self.cities_table_duration["dur_ratio"] = self.cities_table_duration.apply(
            lambda row: row["dur_driving_val"] / row["dur_transit_val"]
            if row.notnull().all() else None, axis=1)

    @property
    def folium_map(self):
        """ Generate Folium map with colors and icons of city labels coded,
        centered in the mean of the coordinates of cities given.
        Green for faster transit mode, the darker the faster (icon 'bus').
        Red for faster driving mode, the darker the faster (icon 'car').
        Ratio 'driving time / transit time' shown in labels.
        Gray for undefined ratio (icon 'question').
        :return: map.html, exposed as property
        """
        self.center_map = [self.cities_table_duration['latitude'].mean(),
                           self.cities_table_duration['longitude'].mean()]

        self.m = folium.Map(
            location=self.center_map,
            zoom_start=6
        )

        def color_code(ratio: float) -> str:
            if ratio is None:
                return 'lightgray'
            elif ratio > 1.35:
                return 'darkgreen'
            elif ratio > 1.15:
                return 'green'
            elif ratio > 1:
                return 'lightgreen'
            elif ratio > 0.85:
                return 'lightred'
            elif ratio > 0.65:
                return 'red'
            else:
                return 'darkred'

        def icon_code(ratio: float) -> str:
            if ratio is None:
                return 'question'
            elif ratio > 1:
                return 'bus'
            else:
                return 'car'

        def ratio_output(ratio: float) -> str:
            if ratio is None:
                return 'NO TRANSIT FOUND'
            else:
                return f'Ratio: {ratio:.2}'

        for index, row in self.cities_table_duration.iterrows():
            ratio = row['dur_ratio']

            # check for unavailable transit routes
            if ratio != ratio or np.isnan(ratio):
                ratio = None
            else:
                ratio = round(ratio, 3)

            # add labels to map
            folium.Marker(
                location=row['geopoint'],
                popup=f"City: {row['accentcity']}, {ratio_output(ratio)}",
                icon=folium.Icon(color=color_code(ratio), icon=icon_code(ratio), prefix='fa')
            ).add_to(self.m)

        self.m.save('folium_map.html')
        return self.m

    @property
    def cities_table_duration_dropna(self):
        """ Utility function removing NA (arise when Distance Matrix API returns ZERO_RESULT)"""
        return self.cities_table_duration.dropna(subset=["dur_ratio"])

    @property
    def cities_table_duration_short(self):
        """ Utility function reducing DataFrame to only used columns"""
        columns_short = ['accentcity', 'city', 'geopoint', 'dur_ratio']
        return self.cities_table_duration[columns_short]
