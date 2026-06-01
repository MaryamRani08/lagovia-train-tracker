# lagovia-train-tracker
HTTP API that returns live train departures for Belgian stations using the iRail API. Built with Python and FastAPI.

## How to run locally

1. Clone the repository 
     git clone https://github.com/MaryamRani08/lagovia-train-tracker.git
     cd lagovia-train-tracker

2. Create and activate a virtual environment (optional)
     python -m venv venv
     venv\Scripts\activate       # Windows
     source venv/bin/activate    # Mac/Linux

3. Install required dependencies
     pip install -r requirements.txt

4. Start the server using 
     uvicorn main:app --reload

5. Open http://localhost:8000/docs to test interactively

## Endpoint

GET /departures?q={query}

Returns upcoming departures scheduled within 15 minutes from all stations whose name contains the query string.

### Request

|parameter | Type   | Required | Description |
|----------|--------|----------|-----------------
|  q       | string |  yes     | Station name|
(atleast  3 chars)

### Response shape/results

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

### Error responses

|Status code  | Explanation |
-----------------------------------------------------
| 400         | Query is shorter than 3 characters |
| 503         | iRail API could not be reached |

## Decisions and trade-offs

-- **Python + FastAPI(Track A)** :

I have chosen this  because FastAPI is async-friendly which matters when making multiple HTTP calls to iRail (one per matching station). It also generates interactive docs automatically which made testing easy during development.

-- **One liveboard call per station** :

for each matching station I make a separate API call to iRail. This works fine for short queries but could be slow if many stations match. A future improvement would be to run these calls concurrently using asyncio.gather().

-- **follow_redirects=True** :

iRail returns a 303 redirect. Without this flag httpx stops at the redirect and returns an empty response. Took some debugging to discover.

-- **User-Agent header** :

iRail blocks requests with no User-Agent. Added a custom header to identify the app.

-- **15 minute window** :

calculated using UTC timestamps from iRail compared against datetime.now(timezone.utc). Both sides use UTC to avoid timezone issues.

-- **Error handling of stations** :

if one station's liveboard call fails, the app skips that station and continues instead of crashing the whole response.

## Known Limitations

- every request calls iRail fresh. So,high traffic would hit iRail's rate limits.
- Station liveboard calls are sequential, not concurrent.Could be faster with asyncio.gather().
- Fuzzy search not implemented — only exact substring matching supported

## Time spent

Approximately 5-8 hours over week.

## AI usage

I used Claude (claude.ai) and also chatgpt throughout this project as a learning tool.

**What I used it for:**
- Understanding the iRail API structure before writing any code
- learnign about API and how FastAPI works.
- Learning how async/await and httpx work in Python
- leanred about time conversion and different imports.

**What I did myself:**
- All code was typed by hand, not copy-pasted
- Variable names, structure, and logic decisions are my own
- I asked for explanations of each concept before implementing

**What I rejected or changed:**
- Claude initially suggested putting the liveboard calls   outside the try/except block. I moved them inside because if the call fails, I still want to handle it per station rather than crash everything.
- Claude suggested using "asyncio.gather()" for concurrent calls. I decided for now to keep the code readable and easy to explain but I noted it as a known limitation instead.  