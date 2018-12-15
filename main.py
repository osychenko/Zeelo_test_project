#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleroutes import CitiesRoutes

if __name__ == '__main__':
    route1 = CitiesRoutes()

    # print(route1.retrieve_cities(percentile=0.1))

    # route1.add_duration(percentile=0.2)

    # percentile=0.05 default
    # can be called several times, last value for percentile is saved as default
    route1.add_duration(.1)

    print(route1.retrieve_cities())

    route1.add_duration(.05)

    print(route1.retrieve_cities())

    folium_map = route1.folium_map
