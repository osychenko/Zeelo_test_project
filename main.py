#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleroutes import CitiesRoutes

if __name__ == '__main__':
    route1 = CitiesRoutes()

    # head() doesn't sort DF, this has been done in the query
    # print(route1.retrieve_cities())

    route1.add_duration(.1)

    folium_map = route1.folium_map
