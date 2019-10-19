#!/bin/python

#this script takes parameters:
    # sourcetype
    # level
    # alert Threshold
# This script creates a detector
import sys
import requests
import json

token = 'xxx'   # Default token for SFDemo organization
debug = 1                          # 1 for HTTP logging, 0 for none


# Set up for API calls
detectorurl = '<redacted>'
headers = {'X-SF-TOKEN': <redacted>', 'Content-Type': 'application/json'}

if debug:
   try:
       import http.client as http_client
   except ImportError:
       # Python 2
       import httplib as http_client
   http_client.HTTPConnection.debuglevel = 1
   
# Create detector
# Build JSON for API call with SignalFlow program to create desired chart


# creates a historical detector by passing in 3 arguments


detectordata = {
'name': 'Anomaly - ' + sys.argv[1] +' ('+ sys.argv[2]+')' ,
'programText':"""A_ = data('event_count', filter=filter('sourcetype','""" + sys.argv[1]  +"""') and filter('level', '""" + sys.argv[2] +"""'), rollup='sum', extrapolation='zero').sum();
from signalfx.detectors.against_periods import streams;
def ha_scores(A):
    curr = A.mean(over=duration('30m'));
    baseline = streams.n_period_trimmed_threshold(A, duration('2h'), duration('1w'), 6, 0);
    s_d = streams.n_period_trimmed_threshold(A, duration('2h'), duration('1w'), 6, 1);
    return ((curr - baseline) / (s_d - baseline));
k = ha_scores(A_);
detect(when(k > """ + sys.argv[3] +""")).publish(label='ha_score')""",
'rules': [{'severity': 'Critical', 'detectLabel': 'ha_score', 'notifications':
                [{'type': 'Email', 'email': '<redacted>' }]
            }
            ]
        }

# Hit the SignalFx API endpoint to push the detector
r = requests.post(detectorurl, headers=headers, json=detectordata)

# If debug is turned on, print JSON response and HTTP status code
if debug:
   print(r.text)
   print(r.status_code)
