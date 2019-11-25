#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 15:40:21 2019

@author: aneesh
"""

import urllib
import requests

encoded_query = urllib.parse.quote('at the table')
params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3, 'format': 'tsv'}
params = '&'.join('{}={}'.format(name, value) for name, value in params.items())

response = requests.get('https://api.phrasefinder.io/search?' + params)

assert response.status_code == 200

print(response.text.split()[3])