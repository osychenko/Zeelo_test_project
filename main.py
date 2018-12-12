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
-----------------------
Description:
1)...
2)...
"""
import pandas as pd
import numpy as np
from duration import Duration

if __name__ == '__main__':
    dur1 = Duration()

    # head() doesn't sort DF, this has been done in the query
    print(dur1.cities_table.head(int(len(dur1) * 0.05)))

    dur1.add_duration()

    print(dur1.cities_table_ratio, dur1.cities_table_short)