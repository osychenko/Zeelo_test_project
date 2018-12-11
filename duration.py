import urllib.request
import json
import pandas as pd
import numpy as np

class Duration:
    'Class impementing a general interaction with Google Map API to compute routes'

    def __init__(self, country_code):
        self.country_code = country_code