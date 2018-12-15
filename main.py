#!/usr/bin/python
# -*- coding: utf-8 -*-

from googleroutes import CitiesRoutes

if __name__ == '__main__':
    route1 = CitiesRoutes()

    # print(route1.retrieve_cities(.1))

    route1.add_duration(.2)

    route1.add_duration(.05)

    folium_map = route1.folium_map
