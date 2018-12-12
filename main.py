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
    dur1 = CitiesRoutes()

    # head() doesn't sort DF, this has been done in the query
    #print(dur1.retrieve_cities(0.05))
    print(dur1.draw_map())

    dur1.add_duration()

