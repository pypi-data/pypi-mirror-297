Worldwide Earthquakes API
============

Earthquake is a simple tool for getting earthquake data. It returns the earthquake data for the past hour.

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [Worldwide Earthquakes API](https://apiverve.com/marketplace/api/earthquake)

---

## Installation
	pip install apiverve-worldwideearthquakes

---

## Configuration

Before using the earthquake API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The Worldwide Earthquakes API documentation is found here: [https://docs.apiverve.com/api/earthquake](https://docs.apiverve.com/api/earthquake).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_worldwideearthquakes.apiClient import EarthquakeAPIClient

# Initialize the client with your APIVerve API key
api = EarthquakeAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
This API does not require a Query
```

###### Simple Request

```
# Make a request to the API
result = api.execute()

# Print the result
print(result)
```

###### Example Response

```
{
  "status": "ok",
  "error": null,
  "data": {
    "earthquakes_LastUpdated": 1725181203,
    "earthquakes_LastHour": 9,
    "earthquakes": [
      {
        "mag": 3.5,
        "place": "31 km NE of Seeley Lake, Montana",
        "time": 1725180427137,
        "status": "reviewed",
        "tsunami": 0,
        "sig": 188,
        "net": "us",
        "types": ",origin,phase-data,",
        "nst": 34,
        "dmin": 0.441,
        "rms": 0.43,
        "gap": 52,
        "magType": "ml",
        "type": "earthquake",
        "title": "M 3.5 - 31 km NE of Seeley Lake, Montana",
        "coordinates": [
          -113.1597,
          47.3504
        ]
      },
      {
        "mag": 1.7,
        "place": "35 km SSE of Denali National Park, Alaska",
        "time": 1725180060840,
        "status": "automatic",
        "tsunami": 0,
        "sig": 44,
        "net": "ak",
        "types": ",origin,phase-data,",
        "rms": 0.44,
        "magType": "ml",
        "type": "earthquake",
        "title": "M 1.7 - 35 km SSE of Denali National Park, Alaska",
        "coordinates": [
          -151.3884,
          63.2649
        ]
      },
      {
        "mag": 1.65,
        "place": "24 km E of Maricopa, CA",
        "time": 1725179864060,
        "status": "automatic",
        "tsunami": 0,
        "sig": 42,
        "net": "ci",
        "types": ",nearby-cities,origin,phase-data,scitech-link,",
        "nst": 44,
        "dmin": 0.0519,
        "rms": 0.25,
        "gap": 39,
        "magType": "ml",
        "type": "earthquake",
        "title": "M 1.7 - 24 km E of Maricopa, CA",
        "coordinates": [
          -119.1373333,
          35.0863333
        ]
      },
      {
        "mag": 1.7,
        "place": "55 km SW of Karluk, Alaska",
        "time": 1725178752780,
        "status": "automatic",
        "tsunami": 0,
        "sig": 44,
        "net": "ak",
        "types": ",origin,phase-data,",
        "rms": 0.1,
        "magType": "ml",
        "type": "earthquake",
        "title": "M 1.7 - 55 km SW of Karluk, Alaska",
        "coordinates": [
          -155.1242,
          57.2289
        ]
      },
      {
        "mag": 1.29,
        "place": "2 km ENE of The Geysers, CA",
        "time": 1725178615560,
        "status": "automatic",
        "tsunami": 0,
        "sig": 26,
        "net": "nc",
        "types": ",nearby-cities,origin,phase-data,scitech-link,",
        "nst": 16,
        "dmin": 0.004639,
        "rms": 0.02,
        "gap": 86,
        "magType": "md",
        "type": "earthquake",
        "title": "M 1.3 - 2 km ENE of The Geysers, CA",
        "coordinates": [
          -122.731666564941,
          38.7856674194336
        ]
      },
      {
        "mag": 0.6,
        "place": "10 km ENE of Goldfield, Nevada",
        "time": 1725178373409,
        "status": "automatic",
        "tsunami": 0,
        "sig": 6,
        "net": "nn",
        "types": ",origin,phase-data,",
        "nst": 8,
        "dmin": 0.566,
        "rms": 0.1218,
        "gap": 178.65000000000003,
        "magType": "ml",
        "type": "earthquake",
        "title": "M 0.6 - 10 km ENE of Goldfield, Nevada",
        "coordinates": [
          -117.1233,
          37.7492
        ]
      },
      {
        "mag": 0.46,
        "place": "9 km SW of Idyllwild, CA",
        "time": 1725177904710,
        "status": "automatic",
        "tsunami": 0,
        "sig": 3,
        "net": "ci",
        "types": ",nearby-cities,origin,phase-data,scitech-link,",
        "nst": 30,
        "dmin": 0.06759,
        "rms": 0.13,
        "gap": 74,
        "magType": "ml",
        "type": "earthquake",
        "title": "M 0.5 - 9 km SW of Idyllwild, CA",
        "coordinates": [
          -116.788,
          33.6831667
        ]
      },
      {
        "mag": 0.69,
        "place": "6 km ENE of Desert Hot Springs, CA",
        "time": 1725177853710,
        "status": "automatic",
        "tsunami": 0,
        "sig": 7,
        "net": "ci",
        "types": ",nearby-cities,origin,phase-data,scitech-link,",
        "nst": 35,
        "dmin": 0.04555,
        "rms": 0.14,
        "gap": 67,
        "magType": "ml",
        "type": "earthquake",
        "title": "M 0.7 - 6 km ENE of Desert Hot Springs, CA",
        "coordinates": [
          -116.4411667,
          33.9775
        ]
      },
      {
        "mag": 2.1,
        "place": "10 km NNW of Fritz Creek, Alaska",
        "time": 1725177706119,
        "status": "automatic",
        "tsunami": 0,
        "sig": 68,
        "net": "ak",
        "types": ",origin,phase-data,",
        "rms": 0.33,
        "magType": "ml",
        "type": "earthquake",
        "title": "M 2.1 - 10 km NNW of Fritz Creek, Alaska",
        "coordinates": [
          -151.3974,
          59.8151
        ]
      }
    ]
  },
  "code": 200
}
```

---

## Customer Support

Need any assistance? [Get in touch with Customer Support](https://apiverve.com/contact).

---

## Updates
Stay up to date by following [@apiverveHQ](https://twitter.com/apiverveHQ) on Twitter.

---

## Legal

All usage of the APIVerve website, API, and services is subject to the [APIVerve Terms of Service](https://apiverve.com/terms) and all legal documents and agreements.

---

## License
Licensed under the The MIT License (MIT)

Copyright (&copy;) 2024 APIVerve, and Evlar LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.