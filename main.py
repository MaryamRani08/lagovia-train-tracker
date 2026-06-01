from fastapi import FastAPI, Query, HTTPException
import httpx
from datetime import datetime, timezone, timedelta

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

    match_stations = [
       s for s in stations
       if q.lower() in s["name"].lower()
    ]

    # return {"query": q, "matched_station_found" : len(match_station), "stations" : match_station}
    
    results = []
    
    for station in match_stations:
       async with httpx.AsyncClient(timeout=10.0,follow_redirects=True) as client:
          lb_response = await client.get(
             "https://api.irail.be/liveboard/",
             params={"station": station["name"], "format": "json", "lang": "en"},
             headers= { "User-Agent": "lagovia-train-tracker/1.0"}
          )

          lb_data = lb_response.json()

          departures_all = lb_data.get("departures", {}).get("departure",[])

          now_time = datetime.now(timezone.utc)
          selected_time = now_time + timedelta(minutes=15) 

          filtered_dep = []

          for depar in departures_all:
             dep_time = datetime.fromtimestamp(int(depar["time"]), tz=timezone.utc)
             if now_time <=dep_time <= selected_time:
                filtered_dep.append({
                   "train" : depar["vehicle"],
                   "destination" : depar["station"],
                   "scheduled_time" : dep_time.strftime("%H:%M"),
                   "delay_minutes" : int(depar["delay"]) // 60 
                })

          results.append({
             "station" : station["name"],
             "departures" : filtered_dep
        })
          
    return {"query" : q, "stations_found": len(match_stations), "results": results}

          





#Step 2 : Call iRail to fetch matching stations
#Step 3 : For each station, fetch departures and filter to 15 minutes
