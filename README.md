# Lagovia Train Tracker

A lightweight HTTP API that returns live train departures for Belgian railway stations using the iRail API. Built with Python, FastAPI, and httpx.

## Features

* Searches Belgian railway stations using a partial station name
* Returns departures scheduled within the next 15 minutes
* Shows train number, destination, scheduled departure time, and delay
* Validates that the search query contains at least three characters
* Continues processing if a request for one station fails
* Provides interactive Swagger documentation through FastAPI

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/MaryamRani08/lagovia-train-tracker.git
cd lagovia-train-tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the development server

```bash
uvicorn main:app --reload
```

### 5. Open the API documentation

Visit:

```text
http://localhost:8000/docs
```

The interactive Swagger interface can be used to test the endpoint directly from the browser.

## API Endpoint

```http
GET /departures?q={query}
```

The endpoint returns departures scheduled within the next 15 minutes from all stations whose names contain the supplied query.

### Query Parameter

| Parameter | Type   | Required | Description                                           |
| --------- | ------ | -------: | ----------------------------------------------------- |
| `q`       | string |      Yes | Partial station name containing at least 3 characters |

### Example Request

```http
GET /departures?q=bru
```

### Example Response

```json
{
  "query": "bru",
  "stations_found": 16,
  "results": [
    {
      "station": "Brussels-Central",
      "departures": [
        {
          "train": "BE.NMBS.IC4510",
          "destination": "Antwerp-Central",
          "scheduled_time": "09:25",
          "delay_minutes": 0
        }
      ]
    }
  ]
}
```

## Error Responses

| Status Code | Explanation                                |
| ----------: | ------------------------------------------ |
|       `400` | The query contains fewer than 3 characters |
|       `503` | The iRail API could not be reached         |

## Technical Decisions

* **FastAPI:** Selected for its straightforward API development workflow, asynchronous support, automatic validation, and built-in Swagger documentation.

* **httpx.AsyncClient:** Used for asynchronous communication with the external iRail API.

* **UTC-based filtering:** Departure timestamps are compared using timezone-aware UTC values to avoid timezone inconsistencies.

* **Per-station error handling:** If the liveboard request for one station fails, the remaining stations are still processed.

## Known Limitations

* Every request retrieves fresh data from iRail, so high traffic could be affected by external API rate limits.
* Station liveboard requests are currently processed sequentially rather than concurrently.
* Search supports substring matching but does not support fuzzy matching or misspelled station names.

## Future Improvements

* Process liveboard requests concurrently using `asyncio.gather()`
* Add response caching
* Add automated tests
* Add fuzzy station-name matching
* Add a frontend interface for displaying departures visually



