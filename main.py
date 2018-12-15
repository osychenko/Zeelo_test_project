#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Oleg Osychenko"
__copyright__ = "Copyright 2018, Zurich test project"
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
    re
    pandas
    numpy
    folium
-----------------------
Description:
1)...
2)...
"""
from googleroutes import CitiesRoutes

if __name__ == '__main__':
    route1 = CitiesRoutes()

    # head() doesn't sort DF, this has been done in the query
    #print(route1.retrieve_cities())

    route1.add_duration()

    map = route1.map
