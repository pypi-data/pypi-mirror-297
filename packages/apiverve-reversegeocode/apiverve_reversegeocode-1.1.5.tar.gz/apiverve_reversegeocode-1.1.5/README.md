Reverse Geocode API
============

Reverse Geocode is a simple tool for getting the location of a set of coordinates. Only supports USA and Canada Coordinates. It returns the city, state, and more.

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [Reverse Geocode API](https://apiverve.com/marketplace/api/reversegeocode)

---

## Installation
	pip install apiverve-reversegeocode

---

## Configuration

Before using the reversegeocode API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The Reverse Geocode API documentation is found here: [https://docs.apiverve.com/api/reversegeocode](https://docs.apiverve.com/api/reversegeocode).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_reversegeocode.apiClient import ReversegeocodeAPIClient

# Initialize the client with your APIVerve API key
api = ReversegeocodeAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
query = { "lat": 40.714224,  "lon": -73.961452 }
```

###### Simple Request

```
# Make a request to the API
result = api.execute(query)

# Print the result
print(result)
```

###### Example Response

```
{
  "status": "ok",
  "error": null,
  "data": {
    "zipcode": "11211",
    "state_abbr": "NY",
    "city": "Brooklyn",
    "state": "New York",
    "distance": 0.65017573007586638,
    "latitudeClosest": "40.712090",
    "longitudeClosest": "-73.95427",
    "countryCode": "US",
    "latitudeClosestCity": null,
    "longitudeClosestCity": null,
    "latitude": 40.714224,
    "longitude": -73.961452,
    "estimatedCity": true,
    "nearestCities": [
      "Brooklyn",
      "Brooklyn Park",
      "East Brooklyn",
      "Brooklyn Center",
      "Brooklyn Heights"
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