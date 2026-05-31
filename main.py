from fastapi import FastAPI, Query, HTTPException
import httpx
from datetime import datetime

app = FastAPI()
@app.get("/departures")
async def get_dep(q:str = Query(...)):
    if len(q) < 3:
      raise HTTPException(
        status_code=400,
        detail = "Query must be at least 3 characters long"
      )
    # return {"message": "working", "query": q}
    async with httpx.AsyncClient(timeout=10.0,follow_redirects=True) as client:
       response = await client.get("https://api.irail.be/stations/?format=json&lang=en",
                                   headers={"User-Agent": "lagovia-train-tracker/1.0"})
       all_data = response.json()
       stations = all_data["station"]

    #    return  {"status": response.status_code, "text": response.text[:500]}

    match_station = [
       s for s in stations
       if q.lower() in s["name"].lower()
    ]

    return {"query": q, "matched_station_found" : len(match_station), "stations" : match_station}






#Step 2 : Call iRail to fetch matching stations
#Step 3 : For each station, fetch departures and filter to 15 minutes
