User Agent Generator API
============

User Agent Generator is a simple tool for generating user agent strings. It returns a random user agent string.

![Build Status](https://img.shields.io/badge/build-passing-green)
![Code Climate](https://img.shields.io/badge/maintainability-B-purple)
![Prod Ready](https://img.shields.io/badge/production-ready-blue)

This is a Python API Wrapper for the [User Agent Generator API](https://apiverve.com/marketplace/api/useragentgenerator)

---

## Installation
	pip install apiverve-useragentgenerator

---

## Configuration

Before using the useragentgenerator API client, you have to setup your account and obtain your API Key.  
You can get it by signing up at [https://apiverve.com](https://apiverve.com)

---

## Usage

The User Agent Generator API documentation is found here: [https://docs.apiverve.com/api/useragentgenerator](https://docs.apiverve.com/api/useragentgenerator).  
You can find parameters, example responses, and status codes documented here.

### Setup

```
# Import the client module
from apiverve_useragentgenerator.apiClient import UseragentgeneratorAPIClient

# Initialize the client with your APIVerve API key
api = UseragentgeneratorAPIClient("[YOUR_API_KEY]")
```

---


### Perform Request
Using the API client, you can perform requests to the API.

###### Define Query

```
query = { "device": "" }
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
    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/604.1.28 (KHTML, like Gecko) Version/11.0.0 Safari/604.1.28",
    "browser": {
      "name": "Safari",
      "version": "11.0.0",
      "major": "11"
    },
    "engine": {
      "name": "WebKit",
      "version": "604.1.28"
    },
    "os": {
      "name": "Mac OS",
      "version": "10.12"
    },
    "device": {
      "vendor": "Apple",
      "model": "Macintosh"
    },
    "cpu": {}
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